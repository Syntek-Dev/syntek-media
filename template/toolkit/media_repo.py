#!/usr/bin/env python3
"""media_repo.py: source media, tokens, flags, where and the repository guard for media.py.

Not run directly: python3 toolkit/media.py footage …, tokens, flags, where and check call it,
and media.py's self-test exercises it.

Source media (DESIGN D19, D46, D52): every recorded or licensed source file, music beds and
archived generated takes included, is a row of production/src/footage/manifest.toml (ID,
path, kind, sha256, bytes, duration, location label) with a git-ignored local mirror in
production/src/footage/raw/. 'footage add' copies a file into the mirror (never moves it),
hashes it and appends the next F ID; it refuses a file whose hash is already listed; a voiceover
take archived with --kind generated has its F ID written into its segment's archived. 'footage
verify' proves the mirror against the manifest: a changed file or an unlisted file fails, an
entry not mirrored here is listed.

The guard (DESIGN D19): Git LFS is used only for brand/src/exports/large/. 'check' finds an
LFS-marked file stored as a plain blob, an LFS-marked file present while no LFS filter is
configured, a file over 10 MB outside the ignored and LFS folders, and a missing nested ignore
rule. 'check --setup' adds the readiness report of DESIGN D49: ffmpeg and ffprobe with libass,
x264 and mp3lame, the optional encoders 'image' needs (libwebp for WebP; an AV1 encoder and the
avif muxer for AVIF), each named with the formats its absence blocks and never a finding,
Python, uv and whether the interpreter a plain 'uv run' of card.py or scene.py would choose here
is a virtual environment's whose base is another Python version (DESIGN D20's mislink, found
with 'uv python find' and the interpreter's own -c answer, so no environment is built and the
network is never reached), the pinned Playwright's Chromium, git-lfs where large exports exist,
the optional espeak-ng, pandoc and fontconfig's fc-match (card.py --self-test's brand-font
probe), the allow, ask and deny entries of .claude/settings.json (D13's two deny entries keep
hand edits out of renders/ and generated/), and whether the user-scope ElevenLabs server's base path contains this
repository. It reads only that one key of ~/.claude.json and prints no other value from it.

'flags' lists both flags (DESIGN D37) across the media layers or the paths given; --piece keeps
one piece's files: its folder under scripts/src/pieces/ and every file in scripts/, production/
and publishing/ (or under the paths given) named <piece>.… or <piece>--cNN.… (DESIGN Section
6.16), its tracked timing and scene files in production/src/timing/ and production/src/scenes/
among them (D64), which M7 needs clear.

'where PIECE' (DESIGN D64) prints the piece's files gathered as flags --piece gathers them, then
names its three ignored per-piece folders, production/src/renders/<piece>/,
production/src/voiceover/generated/<piece>/ and publishing/src/renders/<piece>/, each said to
exist or not and never listed; no file inside an output folder or the footage mirror is ever
named, even outside a Git work tree, where the list is otherwise the plain one.

Nothing here reads a file git ignores (DESIGN D50): flags, where and the large-file scan list
only what git tracks or would track; footage verify opens a mirrored file only by the path the
manifest names, and prints names and hashes, never content.

Standard library only; Python 3.11+.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

import media_common as C

KINDS = ("video", "audio", "music", "stock", "image", "generated")
LARGE = 10 * 1024 * 1024
FLAG_RE = re.compile(r"(?:^|[^`])(?:<!--\s*|/\*\s*|#\s*)(AUTHOR TO CONFIRM|VERIFY):\s*(.*)")
MEDIA_LAYERS = ("brand", "scripts", "production", "publishing")
PLAYWRIGHT_REVISION = "1234"   # the Chromium build Playwright 1.62.0 installs (VERIFY on a pin change)
SETTINGS_ALLOW = ("Bash(python3 toolkit/*.py *)", "Bash(uv run toolkit/*.py *)", "Bash(ffmpeg *)",
                  "Bash(ffprobe *)", "WebSearch", "WebFetch")
SETTINGS_DENY = ("Edit(**/generated/**)", "Edit(**/renders/**)")   # D13; required, like the allows (D49)
SETTINGS_ASK = tuple(f"mcp__elevenlabs__{t}" for t in (
    "text_to_speech", "speech_to_text", "compose_music", "text_to_sound_effects", "speech_to_speech",
    "voice_clone", "isolate_audio", "text_to_voice", "create_voice_from_preview"))
IGNORE_RULES = {
    "production/src/.gitignore": ["/renders/*", "!/renders/README.md", "/footage/raw/*",
                                  "!/footage/raw/README.md", "/voiceover/generated/*",
                                  "!/voiceover/generated/README.md", "/audiobook/generated/*",
                                  "!/audiobook/generated/README.md", "/audiobook/renders/*",
                                  "!/audiobook/renders/README.md"],
    "publishing/src/.gitignore": ["/renders/*", "!/renders/README.md"],
    "toolkit/.gitignore": ["/__pycache__/"],
    "brand/src/exports/large/.gitattributes": ["* filter=lfs diff=lfs merge=lfs -text",
                                               ".gitattributes !filter !diff !merge text",
                                               "CONTEXT.md !filter !diff !merge text",
                                               "CLAUDE.md !filter !diff !merge text"],
}
IGNORED_FOLDERS = ("production/src/renders", "production/src/footage/raw",
                   "production/src/voiceover/generated", "production/src/audiobook/generated",
                   "production/src/audiobook/renders", "publishing/src/renders")


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for block in iter(lambda: fh.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


# ── footage ─────────────────────────────────────────────────────────────────────────────

def manifest_rows(p: Path) -> list:
    return C.load_toml(p).get("file", [])


def toml_line(key: str, value) -> str:
    if isinstance(value, str):
        return f'{key} = "' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'
    if isinstance(value, float):
        return f"{key} = {value:.3f}"
    return f"{key} = {value}"


def cmd_footage_add(args) -> int:
    src = Path(args.file)
    if not src.is_file():
        raise C.Fatal(f"not found: {C.shown(src)}")
    if args.kind not in KINDS:
        raise C.Fatal(f"--kind must be one of {', '.join(KINDS)}")
    if args.rights and not re.fullmatch(r"RR\d{4,}", args.rights):
        raise C.Fatal(f"--rights {args.rights!r} is not a rights-register ID (RR0001)")
    if not args.location.strip():
        raise C.Fatal("--location needs a label for where the master copy lives")
    if "://" in args.location:
        print("  note: --location is a label (a drive or service name), never a link that grants access")
    manifest = C.path(C.MANIFEST)
    if not manifest.is_file():
        raise C.Fatal(f"not found: {C.shown(manifest)} (the footage manifest seed)")
    rows = manifest_rows(manifest)
    digest = sha256(src)
    for r in rows:
        if str(r.get("sha256", "")).lower() == digest:
            raise C.Fatal(f"{C.shown(src)} is already logged as {r.get('id')} ({r.get('path')}): "
                          "nothing added")
    duration = 0.0   # measured before the copy, so a file ffmpeg cannot read is never mirrored
    if src.suffix.lower() in C.IMAGE_EXT:
        # An image's duration is 0.0 (Section 6.5) when it holds one frame, whatever the kind;
        # a GIF or WebP holding more is moving media (a screen recording) and keeps its length.
        if C.is_still(src):
            if args.kind not in ("image", "stock"):
                print(f"  note: {src.name} is a still image (one frame): logged with duration 0.0; "
                      "an edit decision list holds it for seconds")
        else:
            duration = round(C.duration(C.probe(src)), 3)
            print(f"  note: {src.name} moves ({C.image_frames(src)} frames): an edit decision list cuts "
                  "it by in and out, like a video")
    elif args.kind != "image":
        try:
            duration = round(C.duration(C.probe(src)), 3)
        except C.Fatal as err:
            if args.kind in ("video", "audio", "music", "generated"):
                raise
            print(f"  note: no duration read ({err})")
    raw = C.path(C.RAW)
    raw.mkdir(parents=True, exist_ok=True)
    if raw.resolve() in src.resolve().parents:
        dest = src
    else:
        dest = raw / src.name
        if dest.exists():
            if sha256(dest) != digest:
                raise C.Fatal(f"{C.shown(dest)} already holds a different file: rename one first")
        else:
            shutil.copy2(src, dest)
            print(f"copied {C.shown(src)} → {C.shown(dest)} (the original is left where it was)")
    numbers = [int(m.group(1)) for r in rows if (m := re.fullmatch(r"F(\d+)", str(r.get("id", ""))))]
    fid = f"F{max(numbers, default=0) + 1:04d}"
    rel = dest.resolve().relative_to(C.path(C.FOOTAGE).resolve()).as_posix()
    block = ["", "[[file]]"] + [toml_line(k, v) for k, v in (
        ("id", fid), ("path", rel), ("kind", args.kind), ("sha256", digest), ("bytes", dest.stat().st_size),
        ("duration", float(duration)), ("location", args.location.strip()), ("recorded", ""),
        ("rights", args.rights or ""), ("notes", f"archives {src.name}" if args.kind == "generated" else ""))]
    text = C.read_text(manifest).rstrip("\n") + "\n" + "\n".join(block) + "\n"
    manifest.write_text(text, encoding="utf-8")
    print(f"logged {fid}: {rel} · {args.kind} · {dest.stat().st_size:,} bytes · {duration:.3f} s · "
          f"sha256 {digest[:16]}… · {args.location.strip()}")
    if args.kind == "generated":
        record_archive(src, fid)
    return 0


TAKE_NAME_RE = re.compile(r"^(\d{3}-[a-z0-9][a-z0-9-]*)\.(s\d+)\.t(\d+)\.(?:mp3|pcm)$")


def record_archive(src: Path, fid: str) -> None:
    """A voiceover take archived with --kind generated: its footage ID goes into the segment's
    archived in production/src/voiceover/<piece>.toml (DESIGN Section 6.6, D52), when that
    segment's file is this take and archived is empty. Any other file is left to the skill."""
    import media_audio as A
    m = TAKE_NAME_RE.match(src.name)
    if not m:
        return
    reg = C.path(C.VOICEOVER) / f"{m.group(1)}.toml"
    if not reg.is_file():
        return
    seg = next((x for x in C.load_toml(reg).get("segment", []) if str(x.get("id")) == m.group(2)), None)
    if seg is None or Path(str(seg.get("file", ""))).name != src.name:
        print(f"  note: {src.name} is not the current take of {m.group(2)} in {C.shown(reg)}: its archived "
              "is left as it is")
        return
    held = str(seg.get("archived", "") or "").strip()
    if held and held != fid:
        print(f"  note: {m.group(2)} in {C.shown(reg)} already records archived = \"{held}\": left as it is")
        return
    reg.write_text(A.set_toml_fields(C.read_text(reg), "segment", ("id", m.group(2)),
                                     {"archived": A.toml_str(fid)}), encoding="utf-8")
    print(f"wrote archived = \"{fid}\" for {m.group(2)} in {C.shown(reg)}")


def cmd_footage_verify(args) -> int:
    manifest = Path(args.manifest) if args.manifest else C.path(C.MANIFEST)
    if not manifest.is_file():
        raise C.Fatal(f"not found: {C.shown(manifest)}")
    base = manifest.parent
    rows = manifest_rows(manifest)
    bad, absent, listed = [], [], set()
    for r in rows:
        rel = str(r.get("path", ""))
        p = (base / rel).resolve()
        listed.add(p)
        if not p.is_file():
            absent.append(f"{r.get('id')} {rel}")
            continue
        size, digest = p.stat().st_size, sha256(p)
        if size != int(r.get("bytes", -1)) or digest != str(r.get("sha256", "")).lower():
            bad.append(f"{r.get('id')} {rel}: the mirror's bytes or sha256 differ from the manifest "
                       f"({size:,} bytes, sha256 {digest[:16]}…)")
        else:
            print(f"  ok    {r.get('id')} {rel}")
    raw = base / "raw"
    unlisted = [f for f in C.walk_files(raw) if f.name != "README.md" and f.resolve() not in listed] \
        if raw.is_dir() else []
    for b in bad:
        print(f"  FAIL  {b}")
    for u in unlisted:
        print(f"  FAIL  {C.shown(u)} is in the mirror but not in the manifest: log it with 'footage add'")
    for a in absent:
        print(f"  --    {a}: not mirrored here")
    found = len(bad) + len(unlisted)
    print(f"footage verify {C.shown(manifest)}: {len(rows)} entr{'y' if len(rows) == 1 else 'ies'}, "
          f"{len(absent)} not mirrored, {'clean' if not found else f'{found} finding(s)'}")
    return 1 if found else 0


# ── tokens ──────────────────────────────────────────────────────────────────────────────

def cmd_tokens(args) -> int:
    p = Path(args.tokens) if args.tokens else C.path(C.TOKENS)
    tokens = C.read_tokens(p)
    problems = C.token_problems(tokens)
    for name in C.REQUIRED_TOKENS:
        mine = [x for x in problems if x.startswith(name + " ")]
        if mine:
            print(f"  FAIL  {mine[0]}")
        else:
            print(f"  ok    {name}: {C.resolve_token(tokens, name)}")
    for family, url in C.font_faces(p):
        if re.match(r"^[a-z]+://", url):
            problems.append(f"@font-face {family!r} loads {url} over the network")
            print(f"  FAIL  @font-face {family!r} loads {url} over the network")
        elif not (p.parent / url).is_file():
            problems.append(f"@font-face {family!r}: {url} is missing")
            print(f"  FAIL  @font-face {family!r}: {url} is missing beside tokens.css")
        else:
            print(f"  ok    @font-face {family!r}: {url}")
    print(f"tokens {C.shown(p)}: {'clean' if not problems else f'{len(problems)} finding(s)'}")
    return 1 if problems else 0


# ── flags ───────────────────────────────────────────────────────────────────────────────

def tracked_or_trackable(targets: list) -> list:
    """Files under targets that git tracks or would track; every file outside a work tree."""
    root = C.ROOT
    if C.in_work_tree(root):
        rels = C.git_lines(["ls-files", "-z", "--cached", "--others", "--exclude-standard", "--"]
                           + [str(t) for t in targets], cwd=root)
        files = sorted({(root / r) for r in rels if (root / r).is_file()})
        return C.not_ignored(files, root) if files else []
    out = []
    for t in targets:
        t = Path(t) if Path(t).is_absolute() else root / t
        out += [t] if t.is_file() else C.walk_files(t)
    return out


def is_text(p: Path) -> bool:
    try:
        with open(p, "rb") as fh:
            return b"\0" not in fh.read(8192)
    except OSError:
        return False


PIECE_LAYERS = ("scripts", "production", "publishing")
PIECE_RE = re.compile(r"\d{3}-[a-z0-9][a-z0-9-]*")   # NNN-kebab-title (DESIGN D17, Section 6.16)
PIECE_OUTPUTS = (C.PROD_RENDERS, C.VO_GENERATED, C.PUB_RENDERS)   # where a piece's own ignored folder sits (D64)


def piece_name(piece: str, what: str = "--piece") -> str:
    """piece, once it is a piece name with its folder under scripts/src/pieces/ (exit 2 otherwise)."""
    if not PIECE_RE.fullmatch(piece or ""):
        raise C.Fatal(f"{what} {piece!r} is not a piece name (NNN-kebab-title)")
    if not (C.path(C.PIECES) / piece).is_dir():
        raise C.Fatal(f"no piece folder {C.PIECES}/{piece}/")
    return piece


def piece_files(files: list, piece: str) -> list:
    """The files of one piece by the names of DESIGN Section 6.16: its folder under
    scripts/src/pieces/, and every file in the three layers named <piece>.… or <piece>--cNN.…,
    its tracked timing and scene files in production/src/timing/ and production/src/scenes/
    among them (D64); they stay flat there, so the name finds them as it finds edits/ and cards/."""
    folder = C.path(C.PIECES).resolve() / piece
    out = []
    for f in files:
        f = Path(f).resolve()
        if folder == f.parent or folder in f.parents or f.name.startswith((piece + ".", piece + "--")):
            out.append(f)
    return out


def cmd_flags(args) -> int:
    if args.piece and not PIECE_RE.fullmatch(args.piece):
        raise C.Fatal(f"--piece {args.piece!r} is not a piece name (NNN-kebab-title)")
    layers = PIECE_LAYERS if args.piece else MEDIA_LAYERS
    targets = [C.path(d).resolve() for d in layers if C.path(d).exists()]
    if args.paths:
        targets = []
        for given in args.paths:
            p = Path(given)
            p = p if p.is_absolute() else (Path.cwd() / p if (Path.cwd() / p).exists() else C.path(given))
            if not p.exists():
                raise C.Fatal(f"not found: {given}")
            targets.append(p.resolve())
    hits = {"AUTHOR TO CONFIRM": [], "VERIFY": []}
    files = tracked_or_trackable(targets)
    if args.piece:
        files = piece_files(files, piece_name(args.piece))
    for f in files:
        if not is_text(f):
            continue
        for n, line in enumerate(f.read_text(encoding="utf-8", errors="replace").splitlines(), start=1):
            m = FLAG_RE.search(line)
            if m:
                text = re.split(r"-->|\*/", m.group(2))[0].strip()
                hits[m.group(1)].append(f"{C.shown(f)}:{n}: {text}")
    total = 0
    for kind, rows in hits.items():
        print(f"{kind}: {len(rows)}")
        for r in rows:
            print(f"  {r}")
        total += len(rows)
    scope = f" of {args.piece}" if args.piece else ""
    print(f"flags: {total} open across {len(files)} file(s){scope} git tracks or would track")
    return 1 if args.strict and total else 0


# ── where ───────────────────────────────────────────────────────────────────────────────

def in_ignored_folder(f: Path) -> bool:
    """True for a file inside an output folder (renders/, generated/, at any depth) or the footage
    mirror, judged from the project root, so where never names one even outside a work tree."""
    try:
        rel = Path(f).resolve().relative_to(C.ROOT.resolve())
    except ValueError:
        return False
    raw = Path(C.RAW).parts
    return any(part in C.OUTPUT_FOLDERS for part in rel.parts[:-1]) or rel.parts[:len(raw)] == raw


def cmd_where(args) -> int:
    """A piece's files across the three layers, gathered as flags --piece gathers them, then its
    ignored per-piece folders by name, each said to exist or not, never listed (DESIGN D50, D64)."""
    piece = piece_name(args.piece, "PIECE")
    root = C.ROOT
    targets = [C.path(d).resolve() for d in PIECE_LAYERS if C.path(d).exists()]
    files = [f for f in piece_files(tracked_or_trackable(targets), piece) if not in_ignored_folder(f)]
    order = {layer: k for k, layer in enumerate(PIECE_LAYERS)}
    files.sort(key=lambda f: (order.get(Path(C.shown(f)).parts[0], len(order)), C.shown(f)))
    print(f"where {piece}: {len(files)} file(s) git tracks or would track, across "
          f"{', '.join(d + '/' for d in PIECE_LAYERS)}")
    if not C.in_work_tree(root):
        print("  note: not inside a Git work tree, so every file under the layers is listed; no file inside "
              "an output folder or the footage mirror ever is")
    for f in files:
        print(f"  {C.shown(f)}")
    print("ignored per-piece folders, named and never listed (D50, D64):")
    width = max(len(f"{top}/{piece}/") for top in PIECE_OUTPUTS)
    for top in PIECE_OUTPUTS:
        folder = C.piece_folder(top, piece)
        print(f"  {f'{top}/{piece}/':<{width}}  {'exists' if folder.is_dir() else 'absent'}")
    return 0


# ── check ───────────────────────────────────────────────────────────────────────────────

def lfs_marked(paths: list, root: Path) -> set:
    if not paths:
        return set()
    proc = C.run([C.need("git"), "check-attr", "-z", "--stdin", "filter"], cwd=root,
                 input_text="".join(p + "\0" for p in paths), what="git check-attr")
    fields = proc.stdout.split("\0")
    return {fields[k] for k in range(0, len(fields) - 2, 3) if fields[k + 2] == "lfs"}


def git_config(key: str, root: Path) -> str:
    proc = subprocess.run([C.need("git"), "config", "--get", key], cwd=root, capture_output=True, text=True)
    return proc.stdout.strip() if proc.returncode == 0 else ""


def repository_guard(root: Path) -> tuple:
    findings, warnings = [], []
    top = C.git_toplevel(root)
    if top is not None and top != root.resolve():
        warnings.append(f"git's top level is {top}, not this project's root {root.resolve()} (the folder "
                        "holding toolkit/): every toolkit path is read from the project's root, and the "
                        "checks below cover only the files under it")
    if C.in_work_tree(root):
        tracked = set(C.git_lines(["ls-files", "-z", "--cached"], cwd=root))
        present = sorted(set(C.git_lines(["ls-files", "-z", "--cached", "--others", "--exclude-standard"],
                                         cwd=root)))
        present = [p for p in present if (root / p).is_file()]
        marked = lfs_marked(present, root)
        for p in sorted(marked & tracked):
            # ':./path' is relative to the working folder, so a project nested inside a larger
            # repository reads its own index entry (':path' alone is relative to git's top level).
            blob = subprocess.run([C.need("git"), "cat-file", "-p", f":./{p}"], cwd=root, capture_output=True)
            if not blob.stdout[:64].startswith(b"version https://git-lfs.github.com/spec/v1"):
                findings.append(f"{p} is marked for Git LFS but stored as a plain blob: remove it from "
                                "the index (git rm --cached), run 'git lfs install', then add it again")
        if marked and not (git_config("filter.lfs.process", root) or git_config("filter.lfs.clean", root)):
            for p in sorted(marked):
                findings.append(f"{p} is marked for Git LFS but no LFS filter is configured: "
                                f"{C.INSTALL['git-lfs']}")
        for p in present:
            if p not in marked and (root / p).stat().st_size > LARGE:
                findings.append(f"{p} is {(root / p).stat().st_size / 1e6:.1f} MB outside the ignored and "
                                "LFS folders: log source media with 'footage add' (it lives in external "
                                "storage), or move a large design export to brand/src/exports/large/")
        probes = [f"{d}/probe.mp4" for d in IGNORED_FOLDERS if (root / d).is_dir()]
        readmes = [f"{d}/README.md" for d in IGNORED_FOLDERS if (root / d / "README.md").is_file()]
        ignored = set()
        if probes or readmes:
            proc = subprocess.run([C.need("git"), "check-ignore", "-z", "--no-index", "--stdin"], cwd=root,
                                  input="".join(p + "\0" for p in probes + readmes), capture_output=True,
                                  text=True)
            ignored = set(x for x in proc.stdout.split("\0") if x)
        for p in probes:
            if p not in ignored:
                findings.append(f"{p.rsplit('/', 1)[0]}/ is not git-ignored: renders and generated "
                                "audio must never reach plain Git")
        for p in readmes:
            if p in ignored:
                findings.append(f"{p} is git-ignored: the folder's README must stay tracked")
    else:
        warnings.append("not inside a git work tree: the LFS checks need git, and the large-file scan "
                        "read every file")
        for f in C.walk_files(root):
            if f.stat().st_size > LARGE and not any(part in C.OUTPUT_FOLDERS or part == "raw"
                                                    for part in f.relative_to(root).parts):
                findings.append(f"{C.shown(f)} is {f.stat().st_size / 1e6:.1f} MB outside the ignored folders")
    for rel, rules in IGNORE_RULES.items():
        p = root / rel
        if not p.is_file():
            findings.append(f"{rel} is missing: it carries the template's ignore rules")
            continue
        lines = {ln.strip() for ln in C.read_text(p).splitlines()}
        for rule in rules:
            if rule not in lines:
                findings.append(f"{rel} lacks the rule '{rule}'")
    return findings, warnings


def playwright_cache() -> Path:
    env = os.environ.get("PLAYWRIGHT_BROWSERS_PATH")
    if env and env != "0":
        return Path(env)
    home = Path.home()
    if sys.platform == "darwin":
        return home / "Library" / "Caches" / "ms-playwright"
    if sys.platform.startswith("win"):
        return home / "AppData" / "Local" / "ms-playwright"
    return Path(os.environ.get("XDG_CACHE_HOME") or home / ".cache") / "ms-playwright"


def suggested_base(root: Path) -> str:
    home = Path.home().resolve()
    if home == root or home in root.parents:
        return "$HOME"
    p = root
    while p.parent != p and not os.path.ismount(p):
        p = p.parent
    return str(p if p.parent != p else root.parent)


UV_SCRIPTS = ("card.py", "scene.py")   # the scripts an author or a skill may start with a plain 'uv run' (D20)
PYTHON_PROBE = ("import json, sys; print(json.dumps({'version': list(sys.version_info[:3]), "
                "'base': getattr(sys, '_base_executable', '') or '', 'venv': sys.prefix != sys.base_prefix}))")


def python_info(python: str):
    """{version, base, venv} from an interpreter's own answer to -c (its base being the interpreter
    uv would link a new environment to), or None where it cannot be run. Nothing is installed."""
    try:
        proc = subprocess.run([python, "-I", "-c", PYTHON_PROBE], capture_output=True, text=True, timeout=30)
        said = proc.stdout.strip().splitlines() if proc.returncode == 0 else []
        info = json.loads(said[-1]) if said else None
    except (OSError, subprocess.TimeoutExpired, json.JSONDecodeError):
        return None
    ok = isinstance(info, dict) and isinstance(info.get("version"), list) and len(info["version"]) >= 2
    return info if ok else None


def same_file(a: str, b: str) -> bool:
    try:
        return Path(a).resolve().samefile(Path(b).resolve())
    except OSError:
        return a == b


def uv_interpreter_rows(root: Path) -> list:
    """(ok, label, fix) for each requires-python range among the uv scripts here (DESIGN D20, D49):
    whether the interpreter a plain 'uv run' would choose from the project root (UV_PYTHON where it
    is set, else 'uv python find' for the range, an active virtual environment, its bin on PATH and
    a .venv here all counted) is a virtual environment's whose base is another Python version. uv
    would record one version and link the other, and the script's packages would not import. The
    check asks 'uv python find' with downloads and the network off and runs each interpreter with
    -c only, so it builds no environment and fetches nothing. A FAIL names the interpreter media.py
    itself takes ('uv python find --system'), which never mislinks."""
    uv = shutil.which("uv")
    if not uv:
        return [(None, "uv's interpreter: not checked, because uv is not installed", "")]
    ranges: dict = {}
    for name in UV_SCRIPTS:
        script = C.TOOLKIT / name
        if script.is_file():
            try:
                want = str(C.script_metadata(script).get("requires-python", "") or "").strip()
            except C.Fatal:
                want = ""
            ranges.setdefault(want, []).append(name)
    named = os.environ.get("UV_PYTHON", "").strip()
    install = ("install a Python in that range (for example 'uv python install 3.12', or your system's package), "
               "or set UV_PYTHON at user scope to one")
    rows = []
    for want, names in ranges.items():
        head = f"uv's interpreter for {' and '.join(names)}{f' ({want})' if want else ''}: "
        chosen = C.uv_find(uv, named or want, cwd=root)
        system = "" if named else C.uv_find(uv, want, system=True, cwd=root)
        who = f"UV_PYTHON names {named}, and a plain 'uv run' takes " if named else "a plain 'uv run' here takes "
        if named:
            fix = ("point UV_PYTHON at an interpreter outside any virtual environment "
                   "('uv python find --system' lists one), which media.py then takes too")
        else:
            to = f" to {system}, the interpreter media.py itself takes" if system else ""
            fix = (f"set UV_PYTHON at user scope (in your shell profile){to}, or run with no virtual "
                   "environment active, its bin off PATH and no .venv in the project root")
        if not chosen:
            rows.append((False, head + (f"UV_PYTHON names {named}, which uv cannot find" if named
                                        else "no Python here meets the range"), install))
            continue
        info = python_info(chosen)
        if info is None:
            rows.append((False, head + who + f"{chosen}, which could not be run", fix))
            continue
        version = ".".join(str(n) for n in info["version"][:3])
        base = str(info.get("base") or "")
        if info.get("venv") and base and not same_file(base, chosen):
            known = python_info(base)
            if known is None or known["version"][:2] != info["version"][:2]:
                was = f"Python {'.'.join(str(n) for n in known['version'][:3])}" if known else "missing or broken"
                rows.append((False, head + who + f"{chosen}, a virtual environment's Python {version} whose base, "
                             f"{base}, is {was}: uv would record one version and link the other, and the "
                             "script's packages would not import", fix))
                continue
            label = f"{chosen}, a virtual environment's Python {version} on a base of the same version"
        else:
            label = f"{chosen} (Python {version}{', a virtual environment' if info.get('venv') else ''})"
        if not named and not system:
            rows.append((False, head + who + label + "; but no Python outside a virtual environment meets the "
                         "range, so media.py cannot start the script", install))
            continue
        rows.append((True, head + who + label, ""))
    return rows


def setup_report(root: Path) -> tuple:
    """(rows, findings): one row per readiness item, each finding with its fix."""
    rows, findings = [], []

    def item(ok, label, fix=""):
        rows.append(("ok  " if ok is True else "FAIL" if ok is False else "--  ") + f"  {label}")
        if ok is False:
            findings.append(label)
            if fix:
                rows.append(f"        fix: {fix}")
    ff = shutil.which("ffmpeg")
    if ff:
        conf = subprocess.run([ff, "-hide_banner", "-version"], capture_output=True, text=True).stdout
        version = conf.split("\n", 1)[0].replace("ffmpeg version ", "").split(" ")[0]
        lacks = [lib for lib in ("libass", "libx264", "libmp3lame") if f"--enable-{lib}" not in conf]
        item(not lacks, f"ffmpeg {version}" + (f" lacks {', '.join(lacks)}" if lacks else
                                              " with libass, libx264 and libmp3lame"), C.INSTALL["ffmpeg"])
    else:
        item(False, "ffmpeg is not installed", C.INSTALL["ffmpeg"])
    item(bool(shutil.which("ffprobe")), "ffprobe" + ("" if shutil.which("ffprobe") else " is not installed"),
         C.INSTALL["ffprobe"])
    item(sys.version_info >= (3, 11), f"Python {sys.version.split()[0]} (3.11 or later)")
    uv = shutil.which("uv")
    item(bool(uv), "uv" if uv else "uv is not installed (card.py runs through it)", C.INSTALL["uv"])
    for ok, label, fix in uv_interpreter_rows(root):
        item(ok, label, fix)
    import media_audio as A
    import transcribe as T
    python = A.transcribe_python()
    if not python:
        item(None, 'WhisperX interpreter absent: transcribe needs the author-run transcribe fetch, '
                   'or MEDIA_TRANSCRIBE_PYTHON at user scope')
    else:
        try:
            proc = subprocess.run([python, str(A.transcribe_script()), 'status'], capture_output=True,
                                  text=True, timeout=30)
            status = json.loads(proc.stdout) if proc.returncode == 0 else {}
        except (OSError, subprocess.TimeoutExpired, ValueError):
            status = {}
        version = status.get('version', '')
        item(version == T.VERSION and status.get('supported_python') is True,
             f'WhisperX interpreter: {python}; version {version or "missing or broken"}'
             f' (requires {T.VERSION})', C.INSTALL['whisperx'])
    missing = T.missing_cache(T.cache_paths())
    for label in ('English wav2vec2 weights', "nltk's English punkt_tab",
                  'faster-whisper large-v3-turbo in the default Hugging Face cache'):
        item(None if label in missing else True, f'transcribe cache: {label}'
             + (' absent; run transcribe fetch once yourself' if label in missing else ' ready'))
    rhubarb = shutil.which('rhubarb')
    if not rhubarb:
        item(None, 'rhubarb absent: lipsync needs the release with its resources', C.INSTALL['rhubarb'])
    else:
        try:
            version = subprocess.run([rhubarb, '--version'], capture_output=True, text=True, timeout=10)
            works = version.returncode == 0 and C.rhubarb_dictionary(rhubarb).is_file()
        except (OSError, subprocess.TimeoutExpired):
            works = False
        item(works, 'rhubarb for lipsync: ' + ('dictionary ready beside its real path' if works else
                   'broken executable or missing res/sphinx/cmudict-en-us.dict'), C.INSTALL['rhubarb'])
    cache = playwright_cache()
    found = [d.name for d in cache.glob(f"chromium*-{PLAYWRIGHT_REVISION}")] if cache.is_dir() else []
    item(bool(found), f"Chromium for Playwright 1.62.0 ({', '.join(found) or 'not installed'})",
         "uv run --with playwright==1.62.0 playwright install chromium")
    large = root / "brand/src/exports/large"
    exports = [f for f in C.walk_files(large) if f.name not in (".gitattributes", "CONTEXT.md", "CLAUDE.md")] \
        if large.is_dir() else []
    if exports:
        lfs = subprocess.run(["git", "lfs", "version"], capture_output=True, text=True) if shutil.which("git") \
            else None
        configured = git_config("filter.lfs.process", root) or git_config("filter.lfs.clean", root)
        item(bool(lfs and lfs.returncode == 0 and configured),
             f"git-lfs for {len(exports)} large export(s)" + ("" if configured else ": no LFS filter configured"),
             C.INSTALL["git-lfs"])
    else:
        item(None, "git-lfs: not needed until brand/src/exports/large/ holds a file")
    item(None, "espeak-ng (optional scratch track): " + ("present" if shutil.which("espeak-ng") else "absent"))
    item(None, "pandoc (optional, for audiobook text): " + ("present" if shutil.which("pandoc") else "absent"))
    item(None, "fc-match (optional, fontconfig: card.py --self-test's brand-font probe, which without it is "
               "skipped and the self-test incomplete, exit 2): "
               + ("present" if shutil.which("fc-match") else "absent"))
    if ff:
        import media_image as I
        for ok, label in I.optional_encoders():   # a note, never a finding (DESIGN D57)
            item(ok, label)
    settings = root / C.SETTINGS
    try:
        perms = json.loads(settings.read_text(encoding="utf-8")).get("permissions", {}) if settings.is_file() else None
    except (json.JSONDecodeError, OSError):
        perms = None
        item(False, f"{C.SETTINGS} is not valid JSON", "fix the file by hand")
    if perms is None and not settings.is_file():
        item(False, f"{C.SETTINGS} is missing", "create it with the allow, ask and deny entries the README lists")
    perms = perms or {}
    allow, ask, deny = (set(perms.get(k, []) or []) for k in ("allow", "ask", "deny"))
    for entry in SETTINGS_ALLOW:
        item(entry in allow, f"allow {entry}" + ("" if entry in allow else f" is not in {C.SETTINGS}"),
             f"add \"{entry}\" to permissions.allow by hand")
    for entry in SETTINGS_ASK:
        if entry in ask:
            item(True, f"ask {entry}")
        elif entry in allow:
            item(False, f"{entry} is allowed without a prompt", f"move it from permissions.allow to "
                 "permissions.ask: every credit-spending call must prompt")
        elif entry in deny:
            item(None, f"{entry} is denied (the tool cannot run at all)")
        else:
            item(False, f"ask {entry} is not in {C.SETTINGS}", f"add \"{entry}\" to permissions.ask by hand")
    for entry in SETTINGS_DENY:
        item(entry in deny, f"deny {entry}" + ("" if entry in deny else f" is not in {C.SETTINGS}, so a "
             "file in a renders/ or generated/ folder can be edited by hand"),
             f"add \"{entry}\" to permissions.deny by hand")
    rows.append("      (an entry kept in .claude/settings.local.json or a user settings file is "
                "reported absent: media never reads a file git ignores)")
    claude_json = Path.home() / ".claude.json"
    server, base = None, None
    try:
        data = json.loads(claude_json.read_text(encoding="utf-8")) if claude_json.is_file() else {}
        servers = data.get("mcpServers") if isinstance(data, dict) else None
        server = servers.get("elevenlabs") if isinstance(servers, dict) else None
        if isinstance(server, dict):
            env = server.get("env") if isinstance(server.get("env"), dict) else {}
            base = env.get("ELEVENLABS_MCP_BASE_PATH")
    except (json.JSONDecodeError, OSError, AttributeError):
        server = None
    fix_base = suggested_base(root.resolve())
    readd = ("claude mcp remove elevenlabs --scope user; then "
             f"claude mcp add --env ELEVENLABS_API_KEY=\"$ELEVENLABS_API_KEY\" --env ELEVENLABS_MCP_BASE_PATH=\"{fix_base}\" "  # scrub: allow — the setup command; it names a variable, never a key
             "--transport stdio --scope user elevenlabs -- uvx elevenlabs-mcp")
    if not isinstance(server, dict):
        item(False, "no user-scope MCP server named elevenlabs in ~/.claude.json", readd.split("; then ", 1)[1])
    else:
        shown_base = base if base else "not set (the server's default is ~/Desktop)"
        path = Path(str(base) if base else "~/Desktop").expanduser()
        try:
            path = path.resolve()
        except OSError:
            pass
        inside = path == root.resolve() or path in root.resolve().parents
        item(inside, f"ElevenLabs base path: {shown_base}; it "
             + ("contains this repository" if inside else "does not contain this repository, so speech-to-text "
                "will refuse every project file ('outside of allowed directory')"), readd)
    return rows, findings


def cmd_check(args) -> int:
    root = C.ROOT
    findings, warnings = repository_guard(root)
    print(f"check {root.name}: the repository guard")
    for f in findings:
        print(f"  FAIL  {f}")
    for w in warnings:
        print(f"  warn  {w}")
    if not findings:
        print("  ok    no plain-blob LFS file, no unfiltered LFS file, nothing over 10 MB outside the "
              "ignored and LFS folders, every nested ignore rule present")
    setup = []
    if args.setup:
        rows, setup = setup_report(root)
        print("check --setup: readiness (nothing is changed)")
        for r in rows:
            print(f"  {r}")
    total = len(findings) + len(setup) + (len(warnings) if args.strict else 0)
    print(f"check: {'clean' if not total else f'{total} finding(s)'}")
    return 1 if total else 0
