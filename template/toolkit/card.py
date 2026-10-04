#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["playwright==1.62.0"]
# ///
"""card.py: render a thumbnail or card layout (HTML and CSS) to PNG, and check a layout.

Usage (run through uv, which fetches Playwright for this script alone; nothing is installed):
    uv run toolkit/card.py render HTML (--deliverable KEY | --size WxH) [--transparent] [-o OUT]
    uv run toolkit/card.py check HTML
    uv run toolkit/card.py --self-test

render  Opens HTML in headless Chromium through Playwright 1.62.0 (pinned: an unpinned version
        asks for a browser build that may not be installed), with the viewport at the output
        size and a device scale of 1. It sets --safe-top, --safe-right, --safe-bottom and
        --safe-left (pixels, from the deliverable's safe_zone in toolkit/data/platforms.toml,
        brand overrides applied; 0 for --size) and --frame-width and --frame-height on :root,
        aborts every http(s) request (a layout loads nothing over the network, so any request
        is a finding), waits for document.fonts.ready, checks that every image loaded (an <img>,
        a CSS background such as --picture, any local file the page asked for: a missing still
        is a finding), then takes the screenshot. --transparent
        keeps the page's transparent background as alpha (an overlay card) and marks :root
        with data-transparent, so one layout can drop its own backdrop. The PNG is read back
        and must be exactly the size asked for, and within the deliverable's max_size (over its
        max_size_mobile is a warning). Default output: production/src/renders/ for a
        card under production/src/cards/, publishing/src/renders/ otherwise, named
        <html-stem>.<platform>-<format>.png (--deliverable) or <html-stem>.<W>x<H>.png (--size).
check   The layout contract of DESIGN Section 6.11: <!doctype html> and <html lang="en-GB">;
        a stylesheet link to tokens.css by relative path that resolves; every required token
        resolves on :root; every @font-face loads (a brand font in fonts/ beside tokens.css);
        every image loads; nothing is fetched over the network; and, for a file under a previews/ folder, line 1
        is <!-- @dsCard group="Colors|Type|Spacing|Brand|Components" -->.

A missing browser is exit 2 with the command that installs it:
    uv run --with playwright==1.62.0 playwright install chromium

Exit codes: 0 = done (or clean); 1 = a finding (a request over the network, a missing token,
font or image, a PNG of the wrong size or over max_size, a contract breach); 2 = could not run (bad arguments, a missing
file, Playwright or its browser missing).
"""
from __future__ import annotations

import argparse
import re
import struct
import sys
import tempfile
import zlib
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import media_common as C  # noqa: E402

INSTALL_BROWSER = "uv run --with playwright==1.62.0 playwright install chromium"
DSCARD_RE = re.compile(r'^<!--\s*@dsCard\s+group="(Colors|Type|Spacing|Brand|Components)"\s*-->')
SET_VARS = """(vars) => {
  const root = document.documentElement;
  for (const [name, value] of Object.entries(vars)) {
    if (name === 'data-transparent') { root.setAttribute('data-transparent', ''); continue; }
    root.style.setProperty(name, value);
  }
  const style = getComputedStyle(root);
  return Object.fromEntries(Object.keys(vars).map(n => [n, style.getPropertyValue(n).trim()]));
}"""
LOAD_FONTS = """() => Promise.all(Array.from(document.fonts).map(f =>
  f.load().then(() => [f.family, 'loaded'], () => [f.family, 'error'])))"""
IMAGES = """async () => {
  const bad = [], seen = new Set();
  for (const img of Array.from(document.images)) {
    if (!img.complete) await new Promise(r => { img.addEventListener('load', r, {once: true});
                                                img.addEventListener('error', r, {once: true}); });
    const url = img.currentSrc || img.src || img.getAttribute('src') || '';
    if (!img.naturalWidth && !seen.has(url)) { seen.add(url); bad.push(url); }
  }
  const urls = [];
  for (const el of [document.documentElement, ...document.querySelectorAll('*')]) {
    for (const pseudo of [null, '::before', '::after']) {
      const bg = getComputedStyle(el, pseudo).backgroundImage;
      if (!bg || bg === 'none') continue;
      for (const m of bg.matchAll(/url\\(\\s*(['"]?)(.*?)\\1\\s*\\)/g)) urls.push(m[2]);
    }
  }
  for (const url of urls) {
    if (seen.has(url)) continue;
    seen.add(url);
    const ok = await new Promise(r => { const i = new Image(); i.onload = () => r(i.naturalWidth > 0);
                                        i.onerror = () => r(false); i.src = url; });
    if (!ok) bad.push(url);
  }
  return bad;
}"""
READ_TOKENS = """(names) => {
  const style = getComputedStyle(document.documentElement);
  return Object.fromEntries(names.map(n => [n, style.getPropertyValue(n).trim()]));
}"""


def png_info(p: Path) -> dict:
    """Width, height, colour type and the first pixel's alpha (None without alpha) of a PNG."""
    data = Path(p).read_bytes()
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        raise C.Fatal(f"{C.shown(p)} is not a PNG")
    pos, ihdr, idat = 8, None, b""
    while pos + 8 <= len(data):
        length, kind = struct.unpack(">I4s", data[pos:pos + 8])
        body = data[pos + 8:pos + 8 + length]
        if kind == b"IHDR":
            ihdr = struct.unpack(">IIBBBBB", body)
        elif kind == b"IDAT":
            idat += body
        elif kind == b"IEND":
            break
        pos += 12 + length
    if not ihdr:
        raise C.Fatal(f"{C.shown(p)} has no IHDR")
    width, height, depth, colour = ihdr[0], ihdr[1], ihdr[2], ihdr[3]
    alpha = None
    if colour == 6 and depth == 8 and idat:
        raw = zlib.decompressobj().decompress(idat, 8)
        alpha = raw[4] if len(raw) >= 5 else None
    return {"width": width, "height": height, "colour": colour, "alpha0": alpha}


def safe_vars(table: dict | None, w: int, h: int) -> dict:
    zone = (table or {}).get("safe_zone") or {}
    tw, th = (table or {}).get("width") or w, (table or {}).get("height") or h
    out = {"--frame-width": f"{w}px", "--frame-height": f"{h}px"}
    for edge, total, size in (("top", h, th), ("bottom", h, th), ("left", w, tw), ("right", w, tw)):
        out[f"--safe-{edge}"] = f"{round(zone.get(edge, 0) * total / size)}px"
    return out


def playwright():
    try:
        from playwright.sync_api import sync_playwright, Error
    except ImportError:
        raise C.Fatal("Playwright is not available: run this script with "
                      "'uv run toolkit/card.py …', which supplies it from the script's own metadata") from None
    return sync_playwright, Error


class Browser:
    """One headless Chromium whose pages abort every http(s) request and record it."""

    def __enter__(self):
        sync_playwright, self.Error = playwright()
        self.pw = sync_playwright().start()
        try:
            self.browser = self.pw.chromium.launch()
        except self.Error as err:
            self.pw.stop()
            if "Executable doesn't exist" in str(err) or "playwright install" in str(err):
                raise C.Fatal(f"Chromium for Playwright 1.62.0 is not installed: {INSTALL_BROWSER}") from None
            raise C.Fatal(f"Chromium would not start: {str(err).splitlines()[0]}") from None
        return self

    def __exit__(self, *exc):
        self.browser.close()
        self.pw.stop()

    def page(self, html: Path, w: int, h: int):
        """(page, blocked, failed): every http(s) request aborted and listed in blocked; every
        local file that did not load (a missing still, font or stylesheet) listed in failed."""
        page = self.browser.new_page(viewport={"width": w, "height": h}, device_scale_factor=1)
        blocked, failed = [], []

        def route(r):
            if r.request.url.startswith(("http://", "https://")):
                blocked.append(r.request.url)
                r.abort()
            else:
                r.continue_()

        def fail(request):
            if request.url.startswith("file:") and request.url not in failed:
                failed.append(request.url)
        page.on("requestfailed", fail)
        page.route("**/*", route)
        page.goto(html.resolve().as_uri(), wait_until="load")
        return page, blocked, failed


def local_name(url: str) -> str:
    """A file: URL as a path the reader knows; any other URL as it is."""
    if url.startswith("file:"):
        from urllib.parse import unquote, urlparse
        return C.shown(Path(unquote(urlparse(url).path)))
    return url


def image_findings(page, failed: list) -> list:
    """Every image the layout names that did not load: an <img>, a CSS background (the frame's
    --picture among them) or any local file the page asked for. A layout whose still is missing
    renders as bare surface colour, so this is a finding, never a warning (build ruling C3)."""
    found, seen = [], set()
    for url in page.evaluate(IMAGES):
        if url.startswith(("http://", "https://")):
            continue   # aborted, and reported as a request over the network
        name = local_name(url) if url else "an <img> with no src"
        if name not in seen:
            seen.add(name)
            found.append(f"the image {name} did not load: commit it to production/src/assets/ "
                         "(or fix the path) and render again")
    for url in failed:
        name = local_name(url)
        if name not in seen:
            seen.add(name)
            found.append(f"{name} did not load (a file the layout names is missing)")
    return found


def parse_size(text: str) -> tuple:
    m = re.fullmatch(r"(\d+)\s*[xX×]\s*(\d+)", text or "")
    if not m or not 16 <= int(m.group(1)) <= 8192 or not 16 <= int(m.group(2)) <= 8192:
        raise C.Fatal(f"--size {text!r} is not WIDTHxHEIGHT (16 to 8192 pixels)")
    return int(m.group(1)), int(m.group(2))


def default_png(html: Path, suffix: str) -> Path:
    cards = C.path(C.CARDS).resolve()
    folder = C.PROD_RENDERS if cards == html.resolve().parent else C.PUB_RENDERS
    return C.path(folder) / f"{html.stem}.{suffix}.png"


def render(html: Path, w: int, h: int, table, transparent: bool, out: Path) -> tuple:
    """(findings, the variables as the page read them back)."""
    found = []
    variables = safe_vars(table, w, h)
    if transparent:
        variables["data-transparent"] = ""
    with Browser() as b:
        page, blocked, failed = b.page(html, w, h)
        got = page.evaluate(SET_VARS, variables)
        page.evaluate("document.fonts.ready.then(() => true)")
        fonts = page.evaluate(LOAD_FONTS)
        found += image_findings(page, failed)
        page.screenshot(path=str(out), omit_background=transparent, full_page=False)
        page.close()
    for url in blocked:
        found.append(f"requested {url} over the network (aborted): a layout loads only local files")
    for family, status in fonts:
        if status != "loaded":
            found.append(f"the font {family!r} did not load")
    info = png_info(out)
    if (info["width"], info["height"]) != (w, h):
        found.append(f"the PNG is {info['width']}x{info['height']}, not {w}x{h}")
    if transparent and info["colour"] != 6:
        found.append("--transparent gave a PNG with no alpha channel")
    return found, got


def cmd_render(args) -> int:
    html = Path(args.html)
    if not html.is_file():
        raise C.Fatal(f"not found: {C.shown(html)}")
    if bool(args.deliverable) == bool(args.size):
        raise C.Fatal("render takes --deliverable KEY or --size WxH (one of them)")
    table = None
    if args.deliverable:
        table = C.preset(args.deliverable)
        size = C.size_of(table)
        if not size:
            raise C.Fatal(f"{args.deliverable} has no width and height: pass --size WxH (and say so)")
        if table.get("kind") == "audio":
            raise C.Fatal(f"{args.deliverable} is an audio deliverable")
        suffix = C.file_form(args.deliverable)
    else:
        size = parse_size(args.size)
        suffix = f"{size[0]}x{size[1]}"
    out = C.output_path(default_png(html, suffix), args.o, inputs=[html])
    found, _ = render(html, size[0], size[1], table, args.transparent, out)
    weight = out.stat().st_size
    print(f"wrote {C.shown(out)}: {size[0]}x{size[1]}{' with alpha' if args.transparent else ''}, "
          + (f"{weight / 1e6:.1f} MB" if weight >= 1e5 else f"{weight / 1e3:.0f} kB"))
    found += size_findings(weight, table)
    for f in found:
        print(f"  FAIL {f}")
    return 1 if found else 0


def size_findings(weight: int, table) -> list:
    """The file's size against the deliverable's max_size (a finding) and max_size_mobile (a
    warning, printed: an upload from a phone takes only that much)."""
    if not table:
        return []
    found = []
    limit = C.max_bytes(table.get("max_size"))
    if limit and weight > limit:
        found.append(f"{weight / 1e6:.1f} MB is over {table['key']} max_size {table['max_size']}")
    mobile = C.max_bytes(table.get("max_size_mobile"))
    if mobile and weight > mobile and not (limit and weight > limit):
        print(f"  warning: {weight / 1e6:.1f} MB is over {table['key']} max_size_mobile "
              f"{table['max_size_mobile']}: upload it from a computer, or make the image simpler")
    return found


def static_findings(html: Path, text: str) -> list:
    found = []
    first = text.split("\n", 1)[0]
    body = text.split("\n", 1)[1] if DSCARD_RE.match(first) else text
    if "previews" in html.resolve().parent.parts and not DSCARD_RE.match(first):
        found.append('line 1 is not <!-- @dsCard group="Colors|Type|Spacing|Brand|Components" -->')
    if not re.match(r"\s*<!doctype html>", body, re.I):
        found.append("it does not open with <!doctype html>")
    if not re.search(r"<html[^>]*\blang=\"en-GB\"", text):
        found.append('<html> does not carry lang="en-GB"')
    links = re.findall(r"<link\b[^>]*>", text, re.I)
    sheets = [re.search(r'href="([^"]+)"', ln).group(1) for ln in links
              if re.search(r'rel="stylesheet"', ln) and re.search(r'href="([^"]+)"', ln)]
    tokens = [s for s in sheets if s.endswith("tokens.css")]
    if not tokens:
        found.append("no <link rel=\"stylesheet\"> to tokens.css")
    for s in tokens:
        if re.match(r"^[a-z]+:", s) or s.startswith("/"):
            found.append(f"tokens.css is linked as {s}, not by a relative path")
        elif not (html.parent / s).is_file():
            found.append(f"the linked {s} does not exist")
    for url in re.findall(r"(?:src|href)=\"(https?://[^\"]+)\"|url\(['\"]?(https?://[^'\")]+)", text):
        found.append(f"names {url[0] or url[1]} over the network")
    return found


def cmd_check(args) -> int:
    html = Path(args.html)
    if not html.is_file():
        raise C.Fatal(f"not found: {C.shown(html)}")
    found = static_findings(html, C.read_text(html))
    with Browser() as b:
        page, blocked, failed = b.page(html, 1280, 720)
        page.evaluate(SET_VARS, safe_vars(None, 1280, 720))
        page.evaluate("document.fonts.ready.then(() => true)")
        values = page.evaluate(READ_TOKENS, list(C.REQUIRED_TOKENS))
        fonts = page.evaluate(LOAD_FONTS)
        found += image_findings(page, failed)
        page.close()
    for name, value in values.items():
        if not value:
            found.append(f"{name} does not resolve")
    for family, status in fonts:
        if status != "loaded":
            found.append(f"the font {family!r} did not load")
    for url in blocked:
        found.append(f"requested {url} over the network")
    for f in found:
        print(f"  FAIL {f}")
    print(f"check {C.shown(html)}: {'clean' if not found else f'{len(found)} finding(s)'}")
    return 1 if found else 0


# ── Self-test ───────────────────────────────────────────────────────────────────────────

FIXTURE_TOKENS = """:root {
  --color-bg: #101418; --color-surface: #1c232b; --color-text: #f4f1ea;
  --color-text-muted: #b9b4aa; --color-accent: #d4a24c; --color-on-accent: #101418;
  --font-display: FONT, sans-serif; --font-body: sans-serif; --weight-display: 700;
  --weight-body: 400; --space-unit: 8px; --radius: 6px; --caption-font: sans-serif;
  --caption-weight: 700; --caption-size: 4.5vh; --caption-text: #FFFFFF;
  --caption-outline: #000000; --caption-outline-width: 0.4vh;
}
"""
FIXTURE_CARD = """<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<link rel="stylesheet" href="../design-system/tokens.css">
<style>
html, body { margin: 0; width: 100vw; height: 100vh; overflow: hidden; }
:root:not([data-transparent]) body { background: var(--color-bg); }
.title { position: absolute; left: var(--safe-left); bottom: var(--safe-bottom);
         font-family: var(--font-display); color: var(--color-text); }
</style>
</head>
<body><div class="title">Fixture</div>EXTRA</body>
</html>
"""


def self_test() -> int:
    """Prove the PNG reader, the safe zone, rendering and the layout check on runtime fixtures."""
    import contextlib
    import io
    import shutil
    import subprocess
    failures = []

    def verdict(label, passed, detail=""):
        print(f"  {'ok  ' if passed else 'FAIL'} {label}")
        if not passed:
            failures.append(label)
            print(f"         {str(detail)[-1200:]}")

    def cli(*argv):
        out = io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(out):
            code = main([str(a) for a in argv])
        return code, out.getvalue()

    print("card.py --self-test")
    saved_root = C.ROOT
    with tempfile.TemporaryDirectory(prefix="card-self-test-") as tmp:
        root = Path(tmp)
        C.ROOT = root
        try:
            png = root / "tiny.png"
            row = b"\x00" + bytes([10, 20, 30, 0]) * 3
            png.write_bytes(b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", 3, 2, 8, 6, 0, 0, 0))
                            + chunk(b"IDAT", zlib.compress(row * 2)) + chunk(b"IEND", b""))
            info = png_info(png)
            verdict("the PNG reader gives size, colour type and the first pixel's alpha",
                    info == {"width": 3, "height": 2, "colour": 6, "alpha0": 0}, info)
            table = {"width": 1080, "height": 1920, "safe_zone": {"top": 288, "bottom": 672, "left": 48, "right": 192}}
            got = safe_vars(table, 540, 960)
            verdict("the safe zone scales to the render size", got["--safe-bottom"] == "336px"
                    and got["--safe-right"] == "96px" and got["--frame-height"] == "960px", got)
            ds = root / "brand/src/design-system"
            ds.mkdir(parents=True)
            font = system_font()
            if font:
                (ds / "fonts").mkdir()
                shutil.copy2(font, ds / "fonts" / ("fixture" + font.suffix))
                faces = (f'@font-face {{ font-family: "Fixture Face"; src: url("fonts/fixture{font.suffix}"); }}\n')
                family = '"Fixture Face"'
            else:
                faces, family = "", "serif"
            (ds / "tokens.css").write_text(faces + FIXTURE_TOKENS.replace("FONT", family), encoding="utf-8")
            cards = root / "brand/src/cards"
            cards.mkdir(parents=True)
            card = cards / "001-fixture.title.html"
            card.write_text(FIXTURE_CARD.replace("EXTRA", ""), encoding="utf-8")
            try:
                with Browser():
                    pass
                have_browser, why = True, ""
            except C.Fatal as err:
                have_browser, why = False, str(err)
            if not have_browser:
                print(f"  skip render, transparency, the network guard and check: {why}")
            else:
                out = root / "renders" / "card.png"
                code, text = cli("render", card, "--size", "320x180", "-o", out)
                info = png_info(out) if out.is_file() else {}
                verdict("render writes a PNG of exactly the size asked", code == 0 and info.get("width") == 320
                        and info.get("height") == 180 and info.get("colour") == 2, text + str(info))
                code, text = cli("render", card, "--size", "320x180", "--transparent", "-o", root / "renders" / "alpha.png")
                info = png_info(root / "renders" / "alpha.png")
                verdict("--transparent keeps alpha where the layout drops its backdrop",
                        code == 0 and info["colour"] == 6 and info["alpha0"] == 0, text + str(info))
                found, got = render(card, 540, 960, table, False, root / "renders" / "safe.png")
                verdict("render sets the safe-zone variables on :root from the deliverable",
                        not found and got.get("--safe-bottom") == "336px" and got.get("--safe-left") == "24px",
                        str(found) + str(got))
                code, text = cli("render", card, "--deliverable", "youtube.thumbnail", "-o", root / "renders" / "yt.png")
                info = png_info(root / "renders" / "yt.png") if (root / "renders" / "yt.png").is_file() else {}
                verdict("render --deliverable takes the table's size", code == 0 and info.get("width") == 3840, text)
                net = cards / "001-fixture.net.html"
                net.write_text(FIXTURE_CARD.replace("EXTRA", '<img src="https://example.com/x.png">'), encoding="utf-8")
                code, text = cli("render", net, "--size", "320x180", "-o", root / "renders" / "net.png")
                verdict("a request over the network is aborted and reported", code == 1 and "example.com" in text, text)
                missing = cards / "001-fixture.missing.html"
                missing.write_text(FIXTURE_CARD.replace("EXTRA", '<img src="../assets/missing-still.png" alt="">'
                                                        '<div style="--picture: url(../assets/also-missing.jpg); '
                                                        'background-image: var(--picture); width: 10px; '
                                                        'height: 10px"></div>'), encoding="utf-8")
                code, text = cli("check", missing)
                verdict("check fails a layout whose still (an <img>) and --picture background are missing",
                        code == 1 and "missing-still.png did not load" in text and "also-missing.jpg did not load"
                        in text, text)
                code, text = cli("render", missing, "--size", "320x180", "-o", root / "renders" / "missing.png")
                verdict("render fails a layout whose images did not load (never bare surface colour)",
                        code == 1 and "missing-still.png" in text, text)
                (root / "brand/src/assets").mkdir(parents=True, exist_ok=True)
                shutil.copy2(root / "renders" / "card.png", root / "brand/src/assets/missing-still.png")
                shutil.copy2(root / "renders" / "card.png", root / "brand/src/assets/also-missing.jpg")
                code, text = cli("check", missing)
                verdict("check passes the same layout once its images are there", code == 0, text)
                for p in ("missing-still.png", "also-missing.jpg"):
                    (root / "brand/src/assets" / p).unlink()
                code, text = cli("render", card, "--deliverable", "youtube.thumbnail", "-o", root / "renders" / "yt.png")
                verdict("render prints the PNG's size against max_size", code == 0 and (" MB" in text or " kB" in text), text)
                thumb, said = C.preset("youtube.thumbnail", quiet=True), io.StringIO()
                with contextlib.redirect_stdout(said):
                    mobile, over = size_findings(3_000_000, thumb), size_findings(60_000_000, thumb)
                verdict("a PNG over max_size_mobile is a warning, over max_size a finding",
                        not mobile and "max_size_mobile" in said.getvalue() and over, f"{mobile} {over} {said.getvalue()}")
                code, text = cli("check", card)
                verdict("check passes a layout that meets the contract" + (" (brand font loaded)" if font else ""),
                        code == 0, text)
                templates = Path(__file__).resolve().parent / "templates"
                for name in ("thumbnail.html", "card.html"):
                    copy = root / "toolkit/templates" / name
                    copy.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(templates / name, copy)
                    code, text = cli("check", copy)
                    verdict(f"check passes the toolkit's {name}", code == 0, text)
                    code, text = cli("render", copy, "--deliverable", "youtube.short", "-o",
                                     root / "renders" / f"{name}.png")
                    verdict(f"the toolkit's {name} renders at 1080x1920 with nothing fetched", code == 0, text)
                (ds / "tokens.css").write_text(faces.replace("fixture", "missing") +
                                               FIXTURE_TOKENS.replace("FONT", family).replace("--radius: 6px;", ""),
                                               encoding="utf-8")
                code, text = cli("check", card)
                verdict("check fails a missing token" + (" and a font that does not load" if font else ""),
                        code == 1 and "--radius does not resolve" in text and (not font or "did not load" in text), text)
                preview = ds / "previews" / "colors.html"
                preview.parent.mkdir()
                preview.write_text(FIXTURE_CARD.replace("../design-system/tokens.css", "../tokens.css")
                                   .replace("EXTRA", ""), encoding="utf-8")
                code, text = cli("check", preview)
                verdict("check fails a preview without its @dsCard line", code == 1 and "@dsCard" in text, text)
        finally:
            C.ROOT = saved_root
    if shutil.which("fc-match") is None:
        print("  skip the brand-font probe: fc-match is not installed to find a font file")
    if failures:
        print(f"self-test FAILED: {len(failures)} case(s)")
        return 1
    print("self-test passed")
    return 0


def chunk(kind: bytes, body: bytes) -> bytes:
    return struct.pack(">I", len(body)) + kind + body + struct.pack(">I", zlib.crc32(kind + body) & 0xFFFFFFFF)


def system_font():
    """A TrueType font file on this machine, to stand in for a brand font (never shipped)."""
    import shutil
    import subprocess
    if not shutil.which("fc-match"):
        return None
    proc = subprocess.run(["fc-match", "-f", "%{file}", "sans-serif:fontformat=TrueType"],
                          capture_output=True, text=True)
    p = Path(proc.stdout.strip())
    return p if proc.returncode == 0 and p.is_file() and p.suffix.lower() in (".ttf", ".otf") else None


def main(argv=None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    argv = sys.argv[1:] if argv is None else list(argv)
    if argv[:1] == ["--self-test"]:
        return self_test()
    ap = argparse.ArgumentParser(prog="card.py", description=__doc__.split("\n\n")[0],
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", metavar="command")
    r = sub.add_parser("render", help="HTML and CSS to PNG at a deliverable's size")
    r.add_argument("html")
    r.add_argument("--deliverable", metavar="KEY")
    r.add_argument("--size", metavar="WxH")
    r.add_argument("--transparent", action="store_true", help="keep the background's alpha (an overlay)")
    r.add_argument("-o", metavar="OUT")
    r.set_defaults(func=cmd_render)
    c = sub.add_parser("check", help="the layout contract: tokens, fonts, network, @dsCard")
    c.add_argument("html")
    c.set_defaults(func=cmd_check)
    args = ap.parse_args(argv)
    if not getattr(args, "func", None):
        ap.print_help()
        return 2
    try:
        return args.func(args)
    except C.Fatal as err:
        print(f"error: {err}", file=sys.stderr)
        return 2
    except OSError as err:
        print(f"error: {err}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
