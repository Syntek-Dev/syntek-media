#!/usr/bin/env python3
"""media_image.py: image deliverables, and the GIF pass of cut, for media.py.

Not run directly: python3 toolkit/media.py image calls it, media.py cut hands it a GIF table,
and media.py's self-test exercises it (DESIGN D57).

image encodes one image deliverable of toolkit/data/platforms.toml (brand overrides applied):
a poster, a share, featured or preview image, a show's cover or its ID3 copy. Its source is a
PNG or other still (a card.py render, a frame, an asset, a design export) or a video, whose
frame --at names (a poster is the deliverable's own render at --at, with no layout). The
picture is scaled to the table's width and height; a source of another shape needs --frame
crop (fills the frame, losing the edges) or --frame pad (keeps it all, over a blurred copy),
because nothing is ever cropped unasked. It is written in the table's first format, or in
--format where that is another of the table's formats: jpg (mjpeg), png, webp (libwebp) or avif
(libaom-av1, else libsvtav1, through the avif muxer, set for speed: a still picture and a fast
preset). A GIF is never image's: an animated GIF is cut's. Where the table sets alpha = false,
and always for jpg and avif, transparency is flattened onto the brand's --color-bg (black where
tokens.css gives no #RRGGBB). The output is then probed: size, codec, alpha, min_width and
max_size are findings, a weight over max_size_mobile a warning. A PNG already at the table's
size, asked for as png with no -o, is verified where it stands and nothing is written. A table
with no width and height (a size no platform publishes) is refused: render it with card.py
--size. A missing encoder is exit 2, named, as check --setup reports it. Default output:
publishing/src/renders/<stem>.<platform>-<format>.<ext>, <stem> being the source's name up to
its first '.' (DESIGN Section 6.16).

The GIF pass (a kind = "image" table whose only format is gif: newsletter.preview_gif) is run
by thumbnail-brief towards M7, never at M5, because its overlay comes from the piece's
thumbnail layout. cut trims the master by --in and --out (seeking before the input),
reframes, lays the --overlay PNG (card.py render --transparent at the deliverable's own size;
any other size is exit 2) over every frame, the first included, burns --captions only where
given, and writes the GIF through palettegen (stats_mode=diff, at most colours_max colours) and
paletteuse. Frame delays in a GIF are whole hundredths of a second, so the rate is 100 / delay
for the smallest whole delay at or under min(the source's rate, fps_max), and the frame count is
the whole number of frames the range holds, so the GIF never lasts longer than its range. It
plays floor(max_seconds / its own seconds) times, written as the gif muxer's -loop of plays - 1,
or -1 (no loop extension) for one play, so the motion stops within max_seconds; a range longer
than max_seconds renders nothing (exit 1). Over max_size it is made again with every second
frame kept (the delay doubled, the duration unchanged), then every fourth, and otherwise fails,
naming its size. A GIF has no sound. gif_facts reads a GIF's size, frames, delays and loop count
from its own blocks, which is how its play time is verified.

Standard library only; Python 3.11+.
"""
from __future__ import annotations

import math
import sys
import tempfile
from pathlib import Path

import media_common as C
import media_audio as A
import media_video as V


# ── Helpers ─────────────────────────────────────────────────────────────────────────────

def weight(n: int) -> str:
    return f"{n / 1e6:.1f} MB" if n >= 1e5 else f"{n / 1e3:.0f} kB"


def background() -> str:
    """The colour transparency is flattened onto: the brand's --color-bg as #RRGGBB, else black."""
    p = C.path(C.TOKENS)
    if p.is_file():
        value = C.resolve_token(C.read_tokens(p), "--color-bg") or ""
        if len(value) == 7 and value.startswith("#"):
            try:
                int(value[1:], 16)
                return value
            except ValueError:
                pass
        if len(value) == 4 and value.startswith("#"):
            return "#" + "".join(ch * 2 for ch in value[1:])
    return "#000000"


def need_encoder(fmt: str, key: str) -> str:
    encoder = C.image_encoder(fmt)
    if encoder:
        return encoder
    wanted = {"webp": "the libwebp encoder", "avif": "an AV1 encoder (libaom-av1 or libsvtav1) and the avif muxer"}
    raise C.Fatal(f"this ffmpeg cannot write {fmt} for {key}: it lacks {wanted.get(fmt, fmt)} "
                  f"('media.py check --setup' lists the optional encoders); {C.INSTALL['ffmpeg']}")


def encoder_args(fmt: str, encoder: str, keep_alpha: bool) -> list:
    """Codec, quality and pixel format for one still in fmt."""
    if fmt == "jpg":
        return ["-c:v", "mjpeg", "-q:v", "3", "-pix_fmt", "yuvj420p", "-frames:v", "1", "-update", "1"]
    if fmt == "png":
        return ["-c:v", "png", "-pix_fmt", "rgba" if keep_alpha else "rgb24", "-frames:v", "1", "-update", "1"]
    if fmt == "webp":
        return ["-c:v", "libwebp", "-quality", "82", "-compression_level", "4",
                "-pix_fmt", "yuva420p" if keep_alpha else "yuv420p", "-frames:v", "1"]
    if fmt == "avif":
        if encoder == "libaom-av1":
            return ["-c:v", "libaom-av1", "-still-picture", "1", "-usage", "allintra", "-cpu-used", "8",
                    "-crf", "30", "-b:v", "0", "-pix_fmt", "yuv420p", "-frames:v", "1", "-f", "avif"]
        return ["-c:v", "libsvtav1", "-preset", "10", "-crf", "35", "-svtav1-params", f"lp={C.threads()}",
                "-pix_fmt", "yuv420p", "-frames:v", "1", "-f", "avif"]
    raise C.Fatal(f"image writes jpg, png, webp or avif, not {fmt}")


def verify_image(out: Path, table: dict, fmt: str) -> list:
    """Findings for an encoded image against its table; a weight over max_size_mobile is printed."""
    key = table["key"]
    info = C.probe(out)
    v = C.streams(info, "video") or [s for s in info.get("streams", []) if s.get("codec_type") == "video"]
    if not v:
        return ["it holds no picture"]
    found = []
    got = (int(v[0].get("width") or 0), int(v[0].get("height") or 0))
    size = C.size_of(table)
    if size and got != size:
        found.append(f"picture is {got[0]}x{got[1]}; {key} wants {size[0]}x{size[1]}")
    if table.get("min_width") and got[0] < int(table["min_width"]):
        found.append(f"{got[0]} px wide is under {key} min_width {table['min_width']}")
    want = C.IMAGE_CODECS.get(fmt)
    if want and v[0].get("codec_name") != want:
        found.append(f"it holds {v[0].get('codec_name')}; a {fmt} file holds {want}")
    if fmt not in (C.formats_of(table) or [fmt]):
        found.append(f"{fmt} is not one of {key}'s formats ({', '.join(C.formats_of(table))})")
    if table.get("alpha") is False and C.has_alpha(v[0].get("pix_fmt")):
        found.append(f"it keeps an alpha channel ({v[0].get('pix_fmt')}); {key} sets alpha = false")
    n = out.stat().st_size
    limit = C.max_bytes(table.get("max_size"))
    if limit and n > limit:
        found.append(f"{weight(n)} is over {key} max_size {table['max_size']}")
    mobile = C.max_bytes(table.get("max_size_mobile"))
    if mobile and n > mobile and not (limit and n > limit):
        print(f"  warning: {weight(n)} is over {key} max_size_mobile {table['max_size_mobile']}: upload "
              "it from a computer, or make the image simpler")
    for k in table.get("verify", []) or []:
        if k in ("width", "height", "max_size", "safe_zone", "formats", "fps_max"):
            print(f"  note: {key} {k} is unconfirmed (verify): re-check it before publishing")
    return found


def describe(p: Path) -> str:
    info = C.probe(p)
    v = [s for s in info.get("streams", []) if s.get("codec_type") == "video"]
    parts = [f"{s.get('width')}x{s.get('height')} {s.get('codec_name')} {s.get('pix_fmt')}" for s in v[:1]]
    parts.append(weight(p.stat().st_size))
    return " · ".join(parts)


def finish(out: Path, found: list, label: str) -> int:
    print(f"  probe: {describe(out)}")
    for f in found:
        print(f"  FAIL {f}")
    print(f"{label} {C.shown(out)}: {'verified' if not found else f'{len(found)} finding(s)'}")
    return 1 if found else 0


# ── image ───────────────────────────────────────────────────────────────────────────────

def cmd_image(args) -> int:
    src = Path(args.src)
    table = C.preset(args.deliverable)
    key = table["key"]
    if table.get("kind") != "image":
        raise C.Fatal(f"{key} is a {table.get('kind')} deliverable: image makes image deliverables "
                      "(use cut or encode)")
    if C.is_gif(table):
        raise C.Fatal(f"{key} is an animated GIF, which cut makes from its thumbnail brief: media.py cut "
                      f"<master> --deliverable {key} --in TC --out TC --overlay <png>")
    formats = C.formats_of(table) or ["png"]
    fmt = str(args.format or formats[0]).lower().replace("jpeg", "jpg")
    if fmt == "gif":
        raise C.Fatal("image never writes a GIF: an animated GIF is cut's")
    if fmt not in C.IMAGE_FORMATS:
        raise C.Fatal(f"--format {fmt} is not jpg, png, webp or avif")
    if fmt not in formats:
        raise C.Fatal(f"--format {fmt} is not one of {key}'s formats ({', '.join(formats)})")
    size = C.size_of(table)
    if not size:
        raise C.Fatal(f"{key} has no width and height (no size is published): render it at a size you "
                      "choose and say so, with 'uv run toolkit/card.py render HTML --size WxH'")
    w, h = size
    info = C.probe(src)
    v = C.streams(info, "video")
    if not v:
        raise C.Fatal(f"{C.shown(src)} holds no picture")
    still = C.is_still(src, info)
    at = None
    if args.at is not None:
        if still:
            raise C.Fatal(f"--at names a frame of a video, and {C.shown(src)} is a still image")
        at = C.parse_tc(args.at, "--at")
        if at >= C.duration(info):
            raise C.Fatal(f"--at {C.fmt_tc(at)} is past the end of {C.shown(src)} ({C.fmt_tc(C.duration(info))})")
    elif not still:
        raise C.Fatal(f"{C.shown(src)} moves: name the frame with --at TC (a poster records it in the "
                      "thumbnail brief's ## Image)")
    sw, sh = int(v[0]["width"]), int(v[0]["height"])
    if abs((sw / sh) / (w / h) - 1) > 0.005 and not args.frame:
        raise C.Fatal(f"{C.shown(src)} is {sw}x{sh} and {key} is {w}x{h}: their shapes differ, so say how "
                      "the picture fills the frame: --frame crop (fills it, losing the edges) or --frame "
                      "pad (keeps it all, over a blurred copy)")
    encoder = need_encoder(fmt, key)
    alpha_src = C.has_alpha(v[0].get("pix_fmt"))
    keep_alpha = alpha_src and table.get("alpha") is not False and fmt in ("png", "webp")
    flatten = alpha_src and not keep_alpha
    if (src.suffix.lower() == ".png" and fmt == "png" and (sw, sh) == (w, h) and not args.o
            and not flatten and at is None):
        print(f"image {C.shown(src)}: already a {w}x{h} PNG; verified where it stands, nothing written")
        return finish(src, verify_image(src, table, "png"), "image")
    stem = src.name.split(".")[0]
    out = C.output_path(C.path(C.PUB_RENDERS) / f"{stem}.{C.file_form(key)}{C.IMAGE_FORMATS[fmt]}",
                        args.o, inputs=[src])
    graph = V.reframe("0:v", "rf", sw, sh, w, h, args.frame or "crop", None, "0")
    last = "rf"
    if flatten:
        colour = background()
        graph.append(f"color=c=0x{colour[1:]}:s={w}x{h}[bg]")
        graph.append(f"[bg][{last}]overlay=0:0:format=auto:shortest=1[flat]")
        last = "flat"
        why = "alpha = false" if table.get("alpha") is False else f"{fmt} keeps no transparency"
        print(f"  note: the source is transparent and {key} takes none ({why}): flattened onto {colour}")
    graph.append(f"[{last}]null[v]")
    head = ["-y"] + (["-ss", C.fmt_tc(at)] if at is not None else []) + C.input_args(src)
    cmd = head + ["-filter_complex", ";".join(graph), "-map", "[v]", "-an", "-map_metadata", "-1"] \
        + encoder_args(fmt, encoder, keep_alpha) + [str(out)]
    A.render(cmd, out, what=f"image ({fmt})")
    print(f"image {C.shown(src)}{f' at {C.fmt_tc(at)}' if at is not None else ''} → {C.shown(out)} "
          f"({key}, {fmt}, {encoder})")
    return finish(out, verify_image(out, table, fmt), "image")


# ── The GIF pass of cut ─────────────────────────────────────────────────────────────────

def overlay_size(png, size: tuple) -> Path:
    """The --overlay PNG, refused (exit 2) unless it is exactly the deliverable's size."""
    p = Path(png)
    v = C.streams(C.probe(p), "video")
    if not v:
        raise C.Fatal(f"--overlay {C.shown(p)} holds no picture")
    got = (int(v[0]["width"]), int(v[0]["height"]))
    if got != tuple(size):
        raise C.Fatal(f"--overlay {C.shown(p)} is {got[0]}x{got[1]}; the deliverable is {size[0]}x{size[1]}: "
                      "render the overlay at the deliverable's own size (uv run toolkit/card.py render "
                      "<layout> --deliverable KEY --transparent)")
    if not C.has_alpha(v[0].get("pix_fmt")):
        print(f"  note: --overlay {C.shown(p)} has no alpha channel, so it covers the whole picture "
              "(render it with --transparent)")
    return p


def gif_facts(p) -> dict:
    """A GIF's own blocks read: width, height, frames, the delays (hundredths of a second), the
    loop count (None with no NETSCAPE2.0 extension: one play; 0: endless) and the play time."""
    data = Path(p).read_bytes()
    if data[:6] not in (b"GIF87a", b"GIF89a"):
        raise C.Fatal(f"{C.shown(p)} is not a GIF")
    width = int.from_bytes(data[6:8], "little")
    height = int.from_bytes(data[8:10], "little")
    packed = data[10]
    pos = 13 + (3 * 2 ** ((packed & 7) + 1) if packed & 0x80 else 0)
    delays, loop, frames, pending = [], None, 0, 0

    def sub_blocks(i):
        chunks = []
        while i < len(data):
            n = data[i]
            i += 1
            if n == 0:
                break
            chunks.append(data[i:i + n])
            i += n
        return chunks, i
    while pos < len(data):
        b = data[pos]
        if b == 0x3B:   # trailer
            break
        if b == 0x21:   # extension
            label = data[pos + 1]
            chunks, pos = sub_blocks(pos + 2)
            if label == 0xF9 and chunks and len(chunks[0]) >= 3:
                pending = chunks[0][1] | (chunks[0][2] << 8)
            elif label == 0xFF and chunks and chunks[0][:11] == b"NETSCAPE2.0" and len(chunks) > 1 \
                    and len(chunks[1]) >= 3 and chunks[1][0] == 1:
                loop = chunks[1][1] | (chunks[1][2] << 8)
            continue
        if b == 0x2C:   # an image
            flags = data[pos + 9]
            pos += 10 + (3 * 2 ** ((flags & 7) + 1) if flags & 0x80 else 0)
            pos += 1   # LZW minimum code size
            _, pos = sub_blocks(pos)
            frames += 1
            delays.append(pending)
            pending = 0
            continue
        raise C.Fatal(f"{C.shown(p)}: an unknown GIF block at byte {pos}")
    once = sum(delays) / 100
    plays = 1 if loop is None else (math.inf if loop == 0 else loop + 1)
    return {"width": width, "height": height, "frames": frames, "delays": delays, "loop": loop,
            "seconds": once, "plays": plays, "play_seconds": once * plays}


def verify_gif(out: Path, table: dict) -> list:
    key = table["key"]
    facts = gif_facts(out)
    found = []
    size = C.size_of(table)
    if size and (facts["width"], facts["height"]) != size:
        found.append(f"picture is {facts['width']}x{facts['height']}; {key} wants {size[0]}x{size[1]}")
    if facts["frames"] and facts["seconds"] > 0:
        fps = facts["frames"] / facts["seconds"]
        if table.get("fps_max") and fps > float(table["fps_max"]) + 0.01:
            found.append(f"{fps:.2f} frames a second is above {key} fps_max {table['fps_max']}")
    limit = table.get("max_seconds")
    if limit and facts["play_seconds"] > float(limit) + 0.005:
        plays = "endlessly" if facts["plays"] == math.inf else f"{facts['plays']} time(s)"
        found.append(f"it plays {plays} for {facts['play_seconds']:.2f} s; {key} max_seconds is {limit:g}")
    n = out.stat().st_size
    cap = C.max_bytes(table.get("max_size"))
    if cap and n > cap:
        found.append(f"{weight(n)} is over {key} max_size {table['max_size']}")
    for k in table.get("verify", []) or []:
        print(f"  note: {key} {k} is unconfirmed (verify): re-check it before publishing")
    return found


def cut_gif(args, table: dict, src: Path, info: dict, a: float, b: float) -> int:
    """cut to a GIF table (DESIGN D57): see this module's docstring."""
    key = table["key"]
    size = C.size_of(table)
    if not size:
        raise C.Fatal(f"{key} has no width and height to cut a GIF to")
    length = b - a
    limit = float(table.get("max_seconds") or 0)
    if limit and length > limit + 1e-6:
        print(f"  FAIL the range lasts {length:.3f} s; {key} max_seconds is {limit:g}: a GIF in an email has "
              "no pause control (nothing rendered)")
        return 1
    if args.overlay:
        overlay = overlay_size(args.overlay, size)
    else:
        overlay = None
        print(f"  note: no --overlay: the GIF carries no play button or words of its own (render them "
              f"with card.py render <layout> --deliverable {key} --transparent)")
    need_encoder("gif", key)
    v = C.streams(info, "video")
    src_fps = C.rate(v[0].get("avg_frame_rate") or v[0].get("r_frame_rate"))
    cap = float(table.get("fps_max") or 0) or (src_fps if src_fps > 0 else 10.0)
    target = min(src_fps, cap) if src_fps > 0 else cap
    base = max(2, math.ceil(100 / target - 1e-9))   # hundredths of a second a frame (2 is the shortest browsers keep)
    colours = max(2, min(256, int(table.get("colours_max") or 256)))
    burned = bool(args.captions)
    out = C.output_path(C.path(C.PUB_RENDERS) / V.deliverable_name(src, key, args.cut, burned, ".gif"),
                        args.o, inputs=[src] + ([overlay] if overlay else []))
    budget = C.max_bytes(table.get("max_size"))
    found = []
    for divisor, label in ((1, "every frame"), (2, "every second frame"), (4, "every fourth frame")):
        delay = base * divisor
        frames = max(1, math.floor(length * 100 / delay + 1e-6))
        seconds = frames * delay / 100
        plays = max(1, math.floor(limit / seconds + 1e-9)) if limit else 0
        loop = -1 if plays == 1 else (plays - 1 if plays > 1 else 0)
        with tempfile.TemporaryDirectory(prefix="media-gif-") as tmp:
            tmp = Path(tmp)
            graph, tail, _ = V.picture_filters(info, dict(table, fps_max=None, fps_allowed=None),
                                               args.frame, args.x)
            seek, extra, family, _ = V.caption_pass(args, table, a, b, tmp) if burned else (
                ["-ss", C.fmt_tc(a), "-to", C.fmt_tc(b)], "", None, [])
            inputs = seek + ["-i", str(src.resolve())]
            if overlay:
                inputs += ["-i", str(Path(overlay).resolve())]
                graph.append("[rf][1:v]overlay=0:0:format=auto[rfo]")
                tail = "[rfo]" + tail[len("[rf]"):]
            graph.append(tail + extra + f"fps=100/{delay},split[g1][g2]")
            graph.append(f"[g1]palettegen=max_colors={colours}:stats_mode=diff[pal]")
            graph.append("[g2][pal]paletteuse=dither=bayer:bayer_scale=5:diff_mode=rectangle[v]")
            cmd = ["-y", "-loglevel", "info"] + inputs + ["-filter_complex", ";".join(graph), "-map", "[v]",
                                                          "-an", "-frames:v", str(frames), "-loop", str(loop),
                                                          "-f", "gif", str(out.resolve())]
            proc = A.render(cmd, out, cwd=tmp, what="cut (GIF)")
        n = out.stat().st_size
        plays_text = "endlessly" if loop == 0 else f"{plays} time{'s' if plays != 1 else ''}"
        print(f"  {label}: {frames} frames at {100 / delay:.2f} a second ({delay / 100:.2f} s each), "
              f"{seconds:.2f} s, plays {plays_text}, {weight(n)}")
        if not budget or n <= budget or divisor == 4:
            break
        print(f"  note: {weight(n)} is over {key} max_size {table['max_size']}: made again keeping "
              f"{'every second' if divisor == 1 else 'every fourth'} frame, the duration unchanged")
    if burned:
        import media_captions as K
        fell, chosen = K.font_fell_back(proc.stderr, family)
        if fell:
            found.append(f"the caption font '{family}' was not found; libass fell back to {chosen}")
    found = verify_gif(out, table) + found
    facts = gif_facts(out)
    loops = "no loop extension" if facts["loop"] is None else f"loop count {facts['loop']}"
    print(f"  probe: {facts['width']}x{facts['height']} gif · {facts['frames']} frames · "
          f"{facts['seconds']:.2f} s × {facts['plays']} = {facts['play_seconds']:.2f} s ({loops}) · {weight(out.stat().st_size)}")
    for f in found:
        print(f"  FAIL {f}")
    print(f"cut {C.shown(out)}: {'verified' if not found else f'{len(found)} finding(s)'}")
    return 1 if found else 0


def optional_encoders() -> list:
    """(ok, label) rows for check --setup: the encoders image needs beyond ffmpeg's own."""
    rows = []
    try:
        webp, avif = C.image_encoder("webp"), C.image_encoder("avif")
    except C.Fatal:
        return [(None, "optional image encoders: ffmpeg is not installed")]
    users = {"webp": "website.poster, website.poster_720, blog.featured_image and blog.poster",
             "avif": "blog.featured_image"}
    rows.append((None, "libwebp (optional, for media.py image --format webp): "
                       + (f"present ({webp})" if webp else f"absent, so image cannot write WebP for {users['webp']}")))
    rows.append((None, "an AV1 encoder and the avif muxer (optional, for media.py image --format avif): "
                       + (f"present ({avif})" if avif else f"absent, so image cannot write AVIF for {users['avif']}")))
    return rows


if __name__ == "__main__":
    sys.exit("media_image.py has no command of its own: run python3 toolkit/media.py image --help")
