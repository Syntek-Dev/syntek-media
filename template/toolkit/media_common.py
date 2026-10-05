#!/usr/bin/env python3
"""media_common.py: what every media_*.py module and card.py share.

Not run directly: python3 toolkit/media.py is the one command, and its self-test exercises
this module. It holds the one copy of each rule the toolkit must agree on: where the project's
folders are; how a timecode is read and written (HH:MM:SS.mmm; SRT's comma form only in .srt
files); how toolkit/data/platforms.toml is read and the brand's [[override]] tables in
brand/src/platforms/overrides.toml applied and printed; how a deliverable key such as
youtube.short or audiobook.acx names its table; which custom properties tokens.css must define;
where an output may be written (a renders/ or generated/ folder, or a path -o names, and nothing
outside those folders is ever overwritten, with named exceptions: a podcast show's tracked
feed, publishing/src/podcast/<show>.feed.xml, which only 'feed write -o' replaces, through a
temporary file renamed over it), and D66's timing and scene files, replaced only by their owning
command while committed and unchanged in Git, through the same temporary-file rule; how ffmpeg
and ffprobe are run (argument lists, never a shell
string, so a path with spaces or quotes is safe under zsh); how a raw ElevenLabs PCM take
(.pcm) is read; which image formats an image deliverable takes and which ffmpeg encoder writes
each; the project's timezone, for the dates a podcast feed carries; and how the files git
ignores are left unread.

A piece's output sits in a folder named for it (DESIGN D64, Section 6.16): piece_folder puts a
file whose name begins with a piece key (NNN-kebab-title) in <output folder>/<piece>/, or in a
named subfolder of it (cards/, timing/, takes/), and keeps a name with no piece key (a footage
file's extract, a show's cover) at the output folder's top. Tracked files never sit in a
per-piece folder: timing/ and scenes/ stay flat under their <piece>. names.

uv_script is the one way the toolkit starts a PEP 723 script (DESIGN D20): 'uv run --python'
with the interpreter UV_PYTHON names, or else the one 'uv python find --system' returns for the
script's requires-python, so an active virtual environment, its bin on PATH or a .venv in the
working folder never mislinks the script's environment; within a timeout, after which the run
and everything it started are stopped; and under a first-run lock at user scope, never in the
project, so no run starts while another run of the same script is building its environment.
The lock is fcntl's flock (msvcrt's byte lock on Windows), held on every run so a deleted uv
environment is rebuilt safely too. Where the lock cannot be taken, the command exits 2 with
the fix rather than start an environment build unlocked.

Standard library only; Python 3.11+ (tomllib).
"""
from __future__ import annotations

import contextlib
import copy
import datetime
import errno
import hashlib
import json
import os
import re
import shutil
import signal
import subprocess
import sys
import time
from pathlib import Path

if sys.version_info < (3, 11):
    sys.exit("error: the media toolkit needs Python 3.11 or later (it reads TOML with tomllib)")
import tomllib  # noqa: E402

TOOLKIT = Path(__file__).resolve().parent
PLATFORMS_TOML = TOOLKIT / "data" / "platforms.toml"
BRAND_NAME = "<%BRAND_NAME%>"
TIMEZONE = "<%TIMEZONE%>"   # the project's IANA timezone: a podcast feed's dates are written in it


def _find_root() -> Path:
    """The project root: the toolkit's parent, because toolkit/ always sits at the project's root
    (DESIGN Section 4.2). Git's top level is not used: a project nested inside another repository
    (a monorepo, a dotfiles repository) would otherwise resolve every path against the parent.
    git_toplevel() gives git's view, which 'check' compares with this."""
    return TOOLKIT.parent


def git_toplevel(where: Path):
    """Git's top level for a folder, or None outside a work tree (or without git)."""
    git = shutil.which("git")
    if not git:
        return None
    proc = subprocess.run([git, "rev-parse", "--show-toplevel"], cwd=where, capture_output=True, text=True)
    return Path(proc.stdout.strip()).resolve() if proc.returncode == 0 and proc.stdout.strip() else None


ROOT = _find_root()

# Project paths, relative to ROOT (DESIGN Sections 4.3 and 6). Functions join them at call time,
# so the self-test can point ROOT at a scratch project.
OVERRIDES = "brand/src/platforms/overrides.toml"
TOKENS = "brand/src/design-system/tokens.css"
FONTS = "brand/src/design-system/fonts"
VOICE_MD = "brand/src/voice/voice.md"
PIECES = "scripts/src/pieces"
FOOTAGE = "production/src/footage"
MANIFEST = "production/src/footage/manifest.toml"
RAW = "production/src/footage/raw"
ASSETS = "production/src/assets"
EDITS = "production/src/edits"
CARDS = "production/src/cards"
VOICEOVER = "production/src/voiceover"
VO_GENERATED = "production/src/voiceover/generated"
AUDIOBOOK = "production/src/audiobook"
AB_GENERATED = "production/src/audiobook/generated"
AB_RENDERS = "production/src/audiobook/renders"
PROD_RENDERS = "production/src/renders"
PUB_RENDERS = "publishing/src/renders"
TIMING = "production/src/timing"     # a piece's tracked word and mouth timings and its words check (D64, D66)
SCENES = "production/src/scenes"     # a piece's tracked cue index, real-source index and scene code (D64, D69, D70)
CAPTIONS = "publishing/src/captions"
PODCAST = "publishing/src/podcast"   # show registers and tracked feeds, where the project self-hosts a podcast
CREDITS_LOG = "production/src/credits-log.md"
SETTINGS = ".claude/settings.json"
OUTPUT_FOLDERS = ("renders", "generated")

REQUIRED_TOKENS = (
    "--color-bg", "--color-surface", "--color-text", "--color-text-muted", "--color-accent",
    "--color-on-accent", "--font-display", "--font-body", "--weight-display", "--weight-body",
    "--space-unit", "--radius", "--caption-font", "--caption-weight", "--caption-size",
    "--caption-text", "--caption-outline", "--caption-outline-width",
)
GENERIC_FAMILIES = {"serif", "sans-serif", "monospace", "cursive", "fantasy", "system-ui",
                    "ui-serif", "ui-sans-serif", "ui-monospace", "ui-rounded", "math", "emoji"}

INSTALL = {
    "ffmpeg": "install ffmpeg built with libass, libx264 and libmp3lame (Debian/Ubuntu: sudo apt "
              "install ffmpeg; Fedora: sudo dnf install ffmpeg; macOS: brew install ffmpeg; "
              "NixOS: pkgs.ffmpeg-full)",
    "ffprobe": "ffprobe ships with ffmpeg: install ffmpeg (Debian/Ubuntu: sudo apt install ffmpeg; "
               "macOS: brew install ffmpeg)",
    "uv": "install uv (pipx install uv, or brew install uv); card.py runs as "
          "'uv run toolkit/card.py'",
    "git": "install git",
    "git-lfs": "install git-lfs, then run 'git lfs install' once (Debian/Ubuntu: sudo apt install "
               "git-lfs; macOS: brew install git-lfs)",
    "pandoc": "optional: install pandoc for a cleaner plain-text conversion",
    "espeak-ng": "optional: install espeak-ng for a scratch timing track (sudo apt install espeak-ng)",
}

X264_PRESET = "medium"   # the self-test lowers it to "ultrafast" for speed
MIN_GAP = 0.08


class Fatal(Exception):
    """Could not run: bad arguments, a missing input or tool, or the tool itself failed (exit 2)."""


class Finding(Exception):
    """A check failed, or an output failed its verification (exit 1)."""


# ── Paths and display ───────────────────────────────────────────────────────────────────

def path(rel: str) -> Path:
    """A project path from its root-relative form."""
    return ROOT / rel


def shown(p) -> str:
    """A path as a reader should see it: relative to the repository or the working folder."""
    p = Path(p)
    for base in (ROOT, Path.cwd()):
        try:
            return str(p.resolve().relative_to(base.resolve()))
        except ValueError:
            continue
    return str(p)


def in_output_folder(p: Path) -> bool:
    """True when a path lies inside a renders/ or generated/ folder."""
    return any(part in OUTPUT_FOLDERS for part in Path(p).resolve().parent.parts)


TIMING_OUTPUTS = {"words.json": TIMING, "words-check.md": TIMING, "mouth.json": TIMING,
                  "cues.json": SCENES, "real.json": SCENES}


def clean_tracked_output(out: Path) -> None:
    """D66: HEAD holds this file, and neither the index nor the working copy changes it."""
    git = shutil.which("git")
    top = git_toplevel(ROOT)
    if not git or top is None:
        raise Fatal(f"{shown(out)} cannot be replaced outside a Git work tree (D66)")
    if out.is_symlink():
        raise Fatal(f"{shown(out)} is a symbolic link; the tracked timing file cannot be replaced")
    try:
        rel = str(out.resolve().relative_to(top))
    except ValueError:
        raise Fatal(f"{shown(out)} is outside this Git work tree") from None
    held = subprocess.run([git, "cat-file", "-e", f"HEAD:{rel}"], cwd=top, capture_output=True)
    status = subprocess.run([git, "status", "--porcelain", "--untracked-files=all", "--", rel],
                            cwd=top, capture_output=True, text=True)
    if held.returncode or status.returncode or status.stdout.strip():
        raise Fatal(f"{shown(out)} is not committed and unchanged in Git: commit or preserve the "
                    "author's changes before replacing it (D66); nothing written")


def output_path(default: Path, given=None, inputs=(), tracked_feed=None, tracked_timing=None) -> Path:
    """Where to write: -o when given, else the default; never over a file outside the output folders.

    The feed exception (DESIGN Section 4.2, D59): tracked_feed names a show's tracked feed,
    publishing/src/podcast/<show>.feed.xml, which only 'feed write -o' passes; that one file may
    exist and be replaced, and the caller replaces it with replace_file (a temporary file renamed
    over it), never by writing into it. tracked_timing is (piece, suffix), passed only by the
    command that owns that D66 output; an existing named copy must be committed and unchanged.
    Both exceptions require an explicit -o, and the caller writes through replace_file."""
    out = Path(given) if given else Path(default)
    for src in inputs:
        if src is not None and out.resolve() == Path(src).resolve():
            raise Fatal(f"the output {shown(out)} is also an input; name another with -o")
    allowed = given is not None and tracked_feed is not None and out.resolve() == Path(tracked_feed).resolve()
    if tracked_timing is not None:
        piece, suffix = tracked_timing
        if suffix not in TIMING_OUTPUTS or piece_key(piece) != piece:
            raise Fatal("unknown tracked timing or scene output")
        named = path(TIMING_OUTPUTS[suffix]) / f"{piece}.{suffix}"
        if given is not None and out.resolve() == named.resolve():
            if out.exists():
                clean_tracked_output(out)
            allowed = True
    if out.exists() and not in_output_folder(out) and not allowed:
        raise Fatal(f"{shown(out)} exists outside a renders/ or generated/ folder, and the toolkit "
                    "never overwrites it: move it aside first (with the author's say-so), or name "
                    "another path with -o")
    out.parent.mkdir(parents=True, exist_ok=True)
    return out


def replace_file(out: Path, data: bytes) -> None:
    """Write data to out through a temporary file in the same folder, renamed over it, so a
    reader never sees half a file and a failed write leaves the old one whole."""
    out = Path(out)
    tmp = out.with_name(f".{out.name}.partial")
    try:
        tmp.write_bytes(data)
        os.replace(tmp, out)
    finally:
        if tmp.exists():
            tmp.unlink()


PIECE_KEY_RE = re.compile(r"^(\d{3}-[a-z0-9][a-z0-9-]*)")


def piece_key(p) -> str | None:
    """The piece key a file's name begins with (NNN-kebab-title, before any --cNN), or None."""
    m = PIECE_KEY_RE.match(Path(p).name)
    return m.group(1).split("--")[0] if m else None


def piece_of(p) -> str:
    """The piece a file belongs to: the leading NNN-kebab-title of its name, else its stem."""
    return piece_key(p) or Path(p).name.split(".")[0]


def piece_folder(top, name, sub: str = "") -> Path:
    """The folder an output named name lands in, inside the output folder top (a root-relative
    path such as PROD_RENDERS, or a Path): top/<piece>/, or top/<piece>/<sub>/ (cards, timing,
    takes), for a name that begins with a piece key, and top itself for a name with none, which
    takes no sub (DESIGN D64, Section 6.16). It only names the folder; the writer makes it."""
    base = path(top) if isinstance(top, str) else Path(top)
    key = piece_key(name)
    if key is None:
        return base
    return base / key / sub if sub else base / key


def file_form(key: str) -> str:
    """A deliverable key as it appears in a file name: youtube.short -> youtube-short."""
    return key.replace(".", "-").replace("_", "-")


def today() -> str:
    return datetime.date.today().strftime("%d/%m/%Y")


def parse_date(text: str) -> datetime.date:
    try:
        return datetime.datetime.strptime(text.strip(), "%d/%m/%Y").date()
    except ValueError:
        raise Fatal(f"{text!r} is not a date in the form DD/MM/YYYY") from None


def zone():
    """The project's timezone (the TIMEZONE answer), as a tzinfo."""
    from zoneinfo import ZoneInfo, ZoneInfoNotFoundError
    if TIMEZONE.startswith("<"):
        raise Fatal("this toolkit was never rendered: TIMEZONE in toolkit/media_common.py holds no "
                    "timezone (run it from a project generated by syntek-media)")
    try:
        return ZoneInfo(TIMEZONE)
    except (ZoneInfoNotFoundError, ValueError):
        raise Fatal(f"the project's timezone {TIMEZONE!r} is not known to this machine: install the "
                    "system tz database (tzdata), or answer TIMEZONE with an IANA name") from None


def parse_datetime(text: str, what: str = "date and time") -> datetime.datetime:
    """'DD/MM/YYYY HH:MM' in the project's timezone, as an aware datetime."""
    try:
        naive = datetime.datetime.strptime(str(text).strip(), "%d/%m/%Y %H:%M")
    except ValueError:
        raise Fatal(f"{what} {text!r} is not DD/MM/YYYY HH:MM") from None
    return naive.replace(tzinfo=zone())


# ── Timecodes ───────────────────────────────────────────────────────────────────────────

def parse_tc(text, what="timecode") -> float:
    """HH:MM:SS.mmm (or MM:SS.mmm, or plain seconds) -> seconds."""
    if isinstance(text, (int, float)):
        return float(text)
    s = str(text).strip().replace(",", ".")
    parts = s.split(":")
    try:
        if not 1 <= len(parts) <= 3 or any(p == "" for p in parts):
            raise ValueError
        secs = float(parts[-1])
        mins = int(parts[-2]) if len(parts) >= 2 else 0
        hours = int(parts[-3]) if len(parts) == 3 else 0
        if secs < 0 or mins < 0 or hours < 0 or (len(parts) > 1 and (secs >= 60 or mins >= 60)):
            raise ValueError
    except ValueError:
        raise Fatal(f"{what} {text!r} is not HH:MM:SS.mmm") from None
    return hours * 3600 + mins * 60 + secs


def fmt_tc(seconds: float, sep: str = ".") -> str:
    """Seconds -> HH:MM:SS.mmm (sep ',' gives SRT's form)."""
    ms = int(round(max(0.0, seconds) * 1000))
    h, ms = divmod(ms, 3_600_000)
    m, ms = divmod(ms, 60_000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d}{sep}{ms:03d}"


def tc_name(seconds: float) -> str:
    """A timecode fit for a file name: 00-01-02-500."""
    return fmt_tc(seconds).replace(":", "-").replace(".", "-")


# ── TOML, frontmatter and Markdown tables ───────────────────────────────────────────────

def load_toml(p) -> dict:
    p = Path(p)
    try:
        with open(p, "rb") as fh:
            return tomllib.load(fh)
    except FileNotFoundError:
        raise Fatal(f"not found: {shown(p)}") from None
    except tomllib.TOMLDecodeError as err:
        raise Fatal(f"{shown(p)} is not valid TOML: {err}") from None


def read_text(p) -> str:
    try:
        return Path(p).read_text(encoding="utf-8")
    except FileNotFoundError:
        raise Fatal(f"not found: {shown(p)}") from None
    except UnicodeDecodeError:
        raise Fatal(f"{shown(p)} is not UTF-8 text") from None


def strip_value(raw: str) -> str:
    """A frontmatter value without its trailing comment or its quotes."""
    raw = raw.strip()
    if raw[:1] in ("'", '"'):
        end = raw.find(raw[0], 1)
        return raw[1:end] if end > 0 else raw[1:]
    return re.split(r"(?:^|\s+)#", raw, maxsplit=1)[0].strip()


def parse_scalar(raw: str):
    """A frontmatter value as Python: a list, a number, an empty map, or a string."""
    raw = raw.strip()
    head = re.split(r"(?:^|\s+)#", raw, maxsplit=1)[0].strip() if raw[:1] not in "'\"" else raw
    if head.startswith("[") and head.endswith("]"):
        inner = head[1:-1].strip()
        return [strip_value(x) for x in inner.split(",")] if inner else []
    if head == "{}":
        return {}
    value = strip_value(raw)
    if re.fullmatch(r"-?\d+", value):
        return int(value)
    if re.fullmatch(r"-?\d+\.\d*", value):
        return float(value)
    return value


def split_frontmatter(text: str):
    """(meta, body, end_line): meta maps each top-level key to its value; block lists are read."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, text, None
    end = next((i for i in range(1, len(lines)) if lines[i].strip() == "---"), None)
    if end is None:
        return {}, text, None
    meta, current = {}, None
    for line in lines[1:end]:
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        m = re.match(r"^([A-Za-z_][A-Za-z0-9_-]*)\s*:\s*(.*)$", line)
        if m and not line.startswith((" ", "\t", "-")):
            current = m.group(1)
            meta[current] = parse_scalar(m.group(2)) if m.group(2).strip() else []
            continue
        item = re.match(r"^\s*-\s+(.*)$", line)
        if item and current is not None and isinstance(meta.get(current), list):
            meta[current].append(strip_value(item.group(1)))
    return meta, "\n".join(lines[end + 1:]), end


def set_frontmatter(text: str, updates: dict) -> str:
    """Write each key's value into the frontmatter, replacing its line or adding it at the end."""
    lines = text.split("\n")
    if not lines or lines[0].strip() != "---":
        raise Fatal("the file has no frontmatter to write into")
    end = next((i for i in range(1, len(lines)) if lines[i].strip() == "---"), None)
    if end is None:
        raise Fatal("the frontmatter is not closed with a '---' line")
    for key, value in updates.items():
        new = f"{key}: {value}"
        for i in range(1, end):
            if re.match(rf"^{re.escape(key)}\s*:", lines[i]):
                comment = re.search(r"\s+#.*$", lines[i])
                lines[i] = new + (comment.group(0) if comment else "")
                break
        else:
            lines.insert(end, new)
            end += 1
    return "\n".join(lines)


def split_row(line: str) -> list:
    """A Markdown table row's cells; a pipe written \\| is text."""
    body = line.strip()
    if body.startswith("|"):
        body = body[1:]
    if body.endswith("|") and not body.endswith("\\|"):
        body = body[:-1]
    return [c.strip().replace("\\|", "|") for c in re.split(r"(?<!\\)\|", body)]


def find_table(lines: list, first_cells: tuple):
    """(header_index, last_row_index) of the table whose header opens with first_cells."""
    want = [c.lower() for c in first_cells]
    for i, line in enumerate(lines):
        if line.lstrip().startswith("|"):
            cells = [c.lower() for c in split_row(line)]
            if cells[:len(want)] == want and i + 1 < len(lines) and re.match(r"^\s*\|[\s:|-]+\|?\s*$",
                                                                                lines[i + 1]):
                last = i + 1
                while last + 1 < len(lines) and lines[last + 1].lstrip().startswith("|"):
                    last += 1
                return i, last
    return None, None


def cell(text) -> str:
    return str(text).replace("|", "\\|").replace("\n", " ")


def append_table_row(p: Path, first_cells: tuple, cells: list) -> None:
    """Add one row at the end of the named table; add the table when the file lacks it."""
    text = read_text(p)
    lines = text.split("\n")
    head, last = find_table(lines, first_cells)
    row = "| " + " | ".join(cell(c) for c in cells) + " |"
    if head is None:
        raise Fatal(f"{shown(p)} has no table headed '| {' | '.join(first_cells)} |'")
    lines.insert(last + 1, row)
    Path(p).write_text("\n".join(lines), encoding="utf-8")


# ── Platform data and the brand's overrides ─────────────────────────────────────────────

def _is_deliverable(table) -> bool:
    return isinstance(table, dict) and "kind" in table


def _resolve_key(data: dict, key: str):
    """(table, field_path, label) for an override or deliverable key; None when it names nothing."""
    parts = key.split(".")
    if parts[0] == "platform":
        parts = parts[1:]
    if len(parts) < 2:
        return None
    if parts[0] == "house":
        return data.get("house"), parts[1:], "house"
    if parts[0] == "audiobook":
        table = data.get("audiobook", {}).get(parts[1])
        return (table, parts[2:], f"audiobook.{parts[1]}") if isinstance(table, dict) else None
    ptable = data.get("platform", {}).get(parts[0])
    if not isinstance(ptable, dict):
        return None
    if len(parts) >= 3 and _is_deliverable(ptable.get(parts[1])):
        return ptable[parts[1]], parts[2:], f"{parts[0]}.{parts[1]}"
    return ptable, parts[1:], f"platform.{parts[0]}"


def load_presets(quiet: bool = False):
    """(data, applied, problems): platforms.toml with every valid brand override applied."""
    data = copy.deepcopy(load_toml(PLATFORMS_TOML))
    applied, problems = [], []
    ov_path = path(OVERRIDES)
    if ov_path.is_file():
        ov = load_toml(ov_path)
        for n, row in enumerate(ov.get("override", []), start=1):
            key, value = row.get("key"), row.get("value")
            where = f"{shown(ov_path)} [[override]] {n}"
            if not key or value is None:
                problems.append(f"{where}: needs both key and value")
                continue
            found = _resolve_key(data, str(key))
            if not found or found[0] is None or not found[1]:
                problems.append(f"{where}: key {key!r} names no table or field of platforms.toml")
                continue
            table, fields, label = found
            target = table
            for f in fields[:-1]:
                target = target.setdefault(f, {})
                if not isinstance(target, dict):
                    break
            if not isinstance(target, dict):
                problems.append(f"{where}: key {key!r} does not name a field")
                continue
            old = target.get(fields[-1])
            numeric = (int, float)
            if old is not None and not (isinstance(old, numeric) and isinstance(value, numeric)
                                        and not isinstance(old, bool)) and type(old) is not type(value):
                problems.append(f"{where}: {key} is a {type(old).__name__} in platforms.toml; "
                                f"the override gives a {type(value).__name__}")
                continue
            target[fields[-1]] = value
            verify = table.get("verify")
            if isinstance(verify, list) and fields[0] in verify:
                table["verify"] = [v for v in verify if v != fields[0]]
            applied.append({"key": key, "value": value, "was": old, "why": row.get("why", ""),
                            "source": row.get("source", ""), "checked": row.get("checked", ""),
                            "table": label})
    if not quiet:   # on stderr, so a command whose product goes to stdout keeps it clean
        for a in applied:
            print(f"note: brand override {a['key']} = {a['value']!r} (platforms.toml: "
                  f"{a['was']!r}){'; checked ' + a['checked'] if a['checked'] else ''}", file=sys.stderr)
        for p in problems:
            print(f"warning: {p}; ignored", file=sys.stderr)
    return data, applied, problems


def deliverable_keys(data: dict) -> list:
    keys = []
    for name, ptable in data.get("platform", {}).items():
        for fmt, table in ptable.items():
            if _is_deliverable(table):
                keys.append(f"{name}.{fmt}")
    for store in data.get("audiobook", {}):
        keys.append(f"audiobook.{store}")
    return keys


def preset(key: str, data=None, quiet: bool = False) -> dict:
    """The deliverable table for a key (youtube.short, podcast.apple_rss_audio, audiobook.acx)."""
    if data is None:
        data = load_presets(quiet=quiet)[0]
    found = _resolve_key(data, key + ".x")
    if not found or not _is_deliverable(found[0]) or found[1] != ["x"]:
        raise Fatal(f"{key!r} is not a deliverable key of toolkit/data/platforms.toml "
                    f"(for example {', '.join(deliverable_keys(data)[:4])}; run 'media.py presets')")
    table = copy.deepcopy(found[0])
    table["key"] = key
    table["platform"] = key.split(".")[0]
    return table


def loudness_target(name: str, data=None) -> tuple:
    """(integrated LUFS, true peak dBTP) for social, podcast or acx (DESIGN D23, D24)."""
    if data is None:
        data = load_presets(quiet=True)[0]
    if name == "social":
        h = data.get("house", {})
        return float(h["social_loudness_lufs"]), float(h["social_true_peak_db"])
    if name == "podcast":
        t = data["platform"]["podcast"]["apple_rss_audio"]
        return float(t["loudness_lufs"]), float(t["true_peak_db"])
    if name == "acx":
        # ACX is measured in RMS, peak and noise floor, not LUFS: master to about -20 LUFS and
        # -3.5 dBTP, which lands inside [audiobook.acx]'s window, then run the ACX check.
        return -20.0, -3.5
    raise Fatal(f"unknown loudness target {name!r}: use social, podcast or acx")


def target_for(table: dict) -> str:
    """Which loudness target a deliverable takes."""
    if table["key"].startswith("audiobook."):
        return "acx"
    if table.get("kind") == "audio" and table["platform"] == "podcast":
        return "podcast"
    return "social"


def portrait(table: dict) -> bool:
    w, h = table.get("width"), table.get("height")
    if w and h:
        return h / w >= 1.7
    return table.get("aspect") == "9:16"


def size_of(table: dict):
    w, h = table.get("width"), table.get("height")
    if not (w and h):
        return None
    return int(w), int(h)


def max_bytes(text: str):
    m = re.fullmatch(r"\s*([\d.]+)\s*(KB|MB|GB|TB)\s*", str(text or ""), re.I)
    if not m:
        return None
    return float(m.group(1)) * {"KB": 1e3, "MB": 1e6, "GB": 1e9, "TB": 1e12}[m.group(2).upper()]


# ── Image deliverables and silent video (DESIGN D57) ────────────────────────────────────

IMAGE_FORMATS = {"jpg": ".jpg", "png": ".png", "webp": ".webp", "avif": ".avif", "gif": ".gif"}
IMAGE_CODECS = {"jpg": "mjpeg", "png": "png", "webp": "webp", "avif": "av1", "gif": "gif"}   # ffprobe's codec_name
IMAGE_ENCODERS = {"jpg": ("mjpeg",), "png": ("png",), "webp": ("libwebp",),
                  "avif": ("libaom-av1", "libsvtav1"), "gif": ("gif",)}
ALPHA_PIX_FMTS = ("rgba", "bgra", "argb", "abgr", "ya8", "ya16", "yuva", "gbrap", "rgba64", "bgra64")


def formats_of(table: dict) -> list:
    """An image deliverable's file formats, the first being what 'image' writes by default."""
    return [str(f).lower().replace("jpeg", "jpg") for f in (table.get("formats") or [])]


def is_gif(table: dict) -> bool:
    """A kind = "image" table whose only format is gif: an animated GIF, which 'cut' makes."""
    return table.get("kind") == "image" and formats_of(table) == ["gif"]


def silent(table: dict) -> bool:
    """A video deliverable with audio_tracks = 0: no sound track at all (a hero loop)."""
    value = table.get("audio_tracks")
    return value is not None and not isinstance(value, bool) and int(value) == 0


def has_alpha(pix_fmt) -> bool:
    """True for a pixel format that carries an alpha channel."""
    return str(pix_fmt or "").startswith(ALPHA_PIX_FMTS)


_TOOL_LISTS: dict = {}


def ffmpeg_list(kind: str) -> set:
    """The names in 'ffmpeg -encoders' (kind 'encoders') or 'ffmpeg -muxers' ('muxers')."""
    if kind not in _TOOL_LISTS:
        proc = run([need("ffmpeg"), "-hide_banner", f"-{kind}"], what=f"ffmpeg -{kind}")
        names = set()
        for line in proc.stdout.splitlines():
            parts = line.split()
            if len(parts) >= 2 and re.fullmatch(r"[A-Z.]{1,7}", parts[0]) and parts[0] != "------":
                names.add(parts[1])
        _TOOL_LISTS[kind] = names
    return _TOOL_LISTS[kind]


def image_encoder(fmt: str):
    """The ffmpeg encoder this build has for an image format, or None (AVIF also needs the muxer)."""
    encoders = ffmpeg_list("encoders")
    found = next((e for e in IMAGE_ENCODERS.get(fmt, ()) if e in encoders), None)
    if fmt == "avif" and "avif" not in ffmpeg_list("muxers"):
        return None
    return found


# ── tokens.css ──────────────────────────────────────────────────────────────────────────

def read_tokens(p=None) -> dict:
    """Every custom property declared in tokens.css (comments removed; the last one wins)."""
    css = re.sub(r"/\*.*?\*/", " ", read_text(p or path(TOKENS)), flags=re.S)
    return {m.group(1): m.group(2).strip() for m in
            re.finditer(r"(--[A-Za-z0-9_-]+)\s*:\s*([^;{}]+?)\s*(?:;|(?=}))", css)}


def resolve_token(tokens: dict, name: str, depth: int = 0):
    value = tokens.get(name)
    if value is None or depth > 8:
        return None
    m = re.fullmatch(r"var\(\s*(--[A-Za-z0-9_-]+)\s*(?:,\s*(.+))?\)", value)
    if m:
        return resolve_token(tokens, m.group(1), depth + 1) or (m.group(2) or None)
    return value


def font_faces(p=None) -> list:
    """(family, url) for every @font-face src url in tokens.css."""
    css = re.sub(r"/\*.*?\*/", " ", read_text(p or path(TOKENS)), flags=re.S)
    out = []
    for block in re.findall(r"@font-face\s*{([^}]*)}", css):
        fam = re.search(r"font-family\s*:\s*([^;]+)", block)
        family = fam.group(1).strip().strip("'\"") if fam else ""
        for url in re.findall(r"url\(\s*['\"]?([^'\")]+)['\"]?\s*\)", block):
            out.append((family, url))
    return out


COLOUR_RE = re.compile(r"#(?:[0-9a-fA-F]{3,4}|[0-9a-fA-F]{6}|[0-9a-fA-F]{8})|"
                       r"(?:rgb|rgba|hsl|hsla|hwb|lab|lch|oklab|oklch|color)\(.+\)|[a-zA-Z]+")
LENGTH_RE = re.compile(r"0|-?\d*\.?\d+(?:px|rem|em|vh|vw|vmin|vmax|%|pt)")


def token_problems(tokens: dict) -> list:
    """What is missing or unreadable among the required tokens (DESIGN Section 6.11)."""
    problems = []
    for name in REQUIRED_TOKENS:
        value = resolve_token(tokens, name)
        if value is None:
            problems.append(f"{name} is missing" if name not in tokens
                            else f"{name} refers to a property that is not defined")
            continue
        if name in ("--caption-text", "--caption-outline"):
            ok = re.fullmatch(r"#[0-9a-fA-F]{6}", value)
            want = "a #RRGGBB colour"
        elif name.startswith("--color-"):
            ok, want = COLOUR_RE.fullmatch(value), "a colour"
        elif name in ("--caption-size", "--caption-outline-width"):
            ok, want = re.fullmatch(r"\d*\.?\d+vh", value), "a length in vh"
        elif name in ("--weight-display", "--weight-body", "--caption-weight"):
            ok = re.fullmatch(r"\d{3}|normal|bold", value)
            want = "a weight (100 to 900, normal or bold)"
        elif name in ("--space-unit", "--radius"):
            ok, want = LENGTH_RE.fullmatch(value), "a length"
        else:
            ok, want = first_family(value), "a font family"
        if not ok:
            problems.append(f"{name} is {value!r}; it must be {want}")
    return problems


def first_family(value: str) -> str:
    return (value or "").split(",")[0].strip().strip("'\"")


def caption_style(tokens: dict) -> dict:
    """The caption tokens as numbers: family, weight, size and outline in vh, two #RRGGBB colours."""
    problems = token_problems(tokens)
    caption = [p for p in problems if p.startswith("--caption")]
    if caption:
        raise Fatal("the caption tokens in tokens.css are not usable: " + "; ".join(caption))
    weight = resolve_token(tokens, "--caption-weight")
    weight = {"normal": 400, "bold": 700}.get(weight, None) or int(weight)
    return {
        "family": first_family(resolve_token(tokens, "--caption-font")),
        "weight": weight,
        "size_vh": float(resolve_token(tokens, "--caption-size")[:-2]),
        "text": resolve_token(tokens, "--caption-text"),
        "outline": resolve_token(tokens, "--caption-outline"),
        "outline_vh": float(resolve_token(tokens, "--caption-outline-width")[:-2]),
    }


# ── Tools ───────────────────────────────────────────────────────────────────────────────

def need(tool: str) -> str:
    found = shutil.which(tool)
    if not found:
        raise Fatal(f"{tool} is not installed: {INSTALL.get(tool, 'install it')}")
    return found


def run(cmd: list, cwd=None, what: str = "", input_text=None) -> subprocess.CompletedProcess:
    """Run a tool from an argument list; raise Fatal with the end of its log when it fails."""
    cmd = [str(c) for c in cmd]
    try:
        proc = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, input=input_text,
                              encoding="utf-8", errors="replace")
    except FileNotFoundError:
        raise Fatal(f"{cmd[0]} is not installed: {INSTALL.get(Path(cmd[0]).name, 'install it')}") from None
    if proc.returncode != 0:
        tail = "\n".join(line for line in proc.stderr.strip().splitlines()[-8:])
        raise Fatal(f"{what or Path(cmd[0]).name} failed (exit {proc.returncode}):\n{tail}")
    return proc


def threads() -> int:
    """The house thread cap for ffmpeg: MEDIA_THREADS when it is a whole number of 1 or more,
    else every CPU but two (at least one), so a render never takes the whole machine."""
    raw = os.environ.get("MEDIA_THREADS", "").strip()
    if raw:
        if raw.isdigit() and int(raw) >= 1:
            return int(raw)
        raise Fatal(f"MEDIA_THREADS={raw!r} is not a whole number of threads, 1 or more")
    return max(1, (os.cpu_count() or 1) - 2)


def ffmpeg(args: list, cwd=None, what: str = "ffmpeg") -> subprocess.CompletedProcess:
    """Run ffmpeg under the thread cap: the filter graphs' threads as global options, and the
    encoder's as an output option just before the output, which every call names last."""
    n = str(threads())
    args = [str(a) for a in args]
    capped = args[:-1] + ["-threads", n] + args[-1:] if args else args
    return run([need("ffmpeg"), "-hide_banner", "-nostdin", "-nostats", "-filter_threads", n,
                "-filter_complex_threads", n] + capped, cwd=cwd, what=what)


# ── uv scripts: D20's interpreter, a timeout and the first-run lock ─────────────────────

UV_LOCKS = None   # the first-run locks' folder; None is the user's cache (the self-test names a scratch one)
PEP723_RE = re.compile(r"(?m)^# /// (?P<type>[a-zA-Z0-9-]+)$\s(?P<content>(^#(| .*)$\s)+)^# ///$")
UV_FIND_ENV = {"UV_PYTHON_DOWNLOADS": "never", "UV_OFFLINE": "1"}   # 'uv python find' fetches nothing


def _script_match(script):
    return next((m for m in PEP723_RE.finditer(read_text(script)) if m.group("type") == "script"), None)


def script_block(script) -> str:
    """The text of a PEP 723 script's '# /// script' block, or '' where it has none."""
    m = _script_match(script)
    return m.group(0) if m else ""


def script_metadata(script) -> dict:
    """A PEP 723 script's inline metadata as TOML (requires-python, dependencies); {} with none."""
    m = _script_match(script)
    if not m:
        return {}
    body = "".join(line[2:] if line.startswith("# ") else line[1:]
                   for line in m.group("content").splitlines(keepends=True))
    try:
        return tomllib.loads(body)
    except tomllib.TOMLDecodeError as err:
        raise Fatal(f"the '# /// script' block of {shown(script)} is not valid TOML: {err}") from None


def uv_find(uv: str, request: str = "", system: bool = False, cwd=None) -> str:
    """The interpreter 'uv python find' reports for a request, or '' where none meets it. It never
    downloads a Python or reaches the network, and builds nothing. system skips every virtual
    environment: an active one, its bin on PATH and a .venv in the working folder alike."""
    cmd = [uv, "python", "find"] + (["--system"] if system else []) + ([request] if request else [])
    try:
        proc = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=60,
                              env=dict(os.environ, **UV_FIND_ENV))
    except (OSError, subprocess.TimeoutExpired):
        return ""
    lines = proc.stdout.strip().splitlines()
    return lines[-1].strip() if proc.returncode == 0 and lines else ""


def uv_python(uv: str, script) -> tuple:
    """(interpreter, how it was chosen) for a uv script (DESIGN D20): the one UV_PYTHON names where
    it is set, else the one 'uv python find --system' returns for the script's requires-python.
    A virtual environment's interpreter is never taken unasked: one made with --copies reports
    another Python as its base, and uv then records one version and links the other, so the
    script's packages do not import. Nothing meeting the range is exit 2, naming the fix."""
    named = os.environ.get("UV_PYTHON", "").strip()
    if named:
        return named, "UV_PYTHON"
    want = str(script_metadata(script).get("requires-python", "") or "").strip()
    found = uv_find(uv, want, system=True)
    if not found:
        raise Fatal(f"no Python outside a virtual environment meets {Path(script).name}'s requires-python "
                    f"{want or '(any)'}, so uv cannot build its environment: install one in that range (for "
                    "example 'uv python install 3.12', or your system's package), or set UV_PYTHON at user "
                    "scope to an interpreter in that range")
    return found, "uv python find --system"


def lock_folder() -> Path:
    """Where the per-script locks live: the user's cache, never the project."""
    if UV_LOCKS:
        return Path(UV_LOCKS)
    home = Path.home()
    if sys.platform == "darwin":
        base = home / "Library" / "Caches"
    elif os.name == "nt":
        base = Path(os.environ.get("LOCALAPPDATA") or home / "AppData" / "Local")
    else:
        base = Path(os.environ.get("XDG_CACHE_HOME") or home / ".cache")
    return base / "media-toolkit" / "uv-first-run"


def _try_lock(fh):
    """True when the lock on fh was taken, False while another process holds it, None where this
    platform or file system has no lock to take."""
    try:
        import fcntl
    except ImportError:
        fcntl = None
    if fcntl is not None:
        try:
            fcntl.flock(fh.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
            return True
        except OSError as err:
            return False if err.errno in (errno.EAGAIN, errno.EACCES, errno.EWOULDBLOCK) else None
    try:
        import msvcrt
    except ImportError:
        return None
    try:
        fh.seek(0)
        msvcrt.locking(fh.fileno(), msvcrt.LK_NBLCK, 1)
        return True
    except OSError:
        return False


def _unlock(fh) -> None:
    try:
        import fcntl
        fcntl.flock(fh.fileno(), fcntl.LOCK_UN)
    except ImportError:
        import msvcrt
        fh.seek(0)
        msvcrt.locking(fh.fileno(), msvcrt.LK_UNLCK, 1)
    except OSError:
        pass


@contextlib.contextmanager
def _exclusive(lock: Path, deadline: float, label: str, timeout: float):
    """Hold the lock file, waiting for another holder until the deadline (exit 2 after it). It
    exits 2 where no lock can be taken, so an environment is never built unlocked.
    A lock dies with its process, so a run that was killed never leaves one behind."""
    why = ""
    try:
        lock.parent.mkdir(parents=True, exist_ok=True)
        fh = open(lock, "a+b")
    except OSError as err:
        fh, why = None, f"{shown(lock.parent)} cannot be written: {err.strerror or err}"
    if fh is None:
        raise Fatal(f'{label} cannot take its first-run lock: {why}; use a writable user-cache '
                    'directory on a file system that supports locks')
    with fh:
        waited = False
        while (got := _try_lock(fh)) is False:
            if not waited:
                print(f"  note: waiting for another run of {label} to finish building its environment",
                      file=sys.stderr)
                waited = True
            if time.monotonic() >= deadline:
                raise Fatal(f"another run of {label} was still building its environment after {timeout:g} s "
                            f"(its lock is {shown(lock)}): let it finish, then run this again")
            time.sleep(0.2)
        if got is None:
            raise Fatal(f'{label} cannot take its first-run lock on {shown(lock)}: '
                        'use a user-cache directory on a file system that supports locks')
        try:
            yield bool(got)
        finally:
            if got:
                _unlock(fh)


def _stop(proc) -> None:
    """Stop a run and every process it started (its own process group, on POSIX)."""
    try:
        if os.name == "posix":
            os.killpg(proc.pid, signal.SIGKILL)
        else:
            proc.kill()
    except OSError:
        pass
    try:
        proc.communicate(timeout=10)
    except (subprocess.TimeoutExpired, ValueError, OSError):
        pass


def _run_until(cmd: list, cwd, capture: bool, deadline: float, label: str, timeout: float, hint: str):
    left = deadline - time.monotonic()
    pipe = subprocess.PIPE if capture else None
    try:
        proc = subprocess.Popen(cmd, cwd=cwd, stdout=pipe, stderr=pipe, text=True, encoding="utf-8",
                                errors="replace", start_new_session=os.name == "posix")
    except FileNotFoundError:
        raise Fatal(f"uv is not installed: {INSTALL['uv']}") from None
    try:
        out, err = proc.communicate(timeout=max(left, 0.01))
    except subprocess.TimeoutExpired:
        _stop(proc)
        raise Fatal(f"{label} did not finish within {timeout:g} s, so it was stopped, with every process it "
                    f"started{': ' + hint if hint else ''}") from None
    except BaseException:
        _stop(proc)
        raise
    return subprocess.CompletedProcess(cmd, proc.returncode, out or "", err or "")


def uv_script(script, args: list, timeout: float, cwd=None, offline: bool = False, capture: bool = True,
              hint: str = "") -> subprocess.CompletedProcess:
    """Run a PEP 723 script through uv as DESIGN D20 says, and hand back its exit and output for the
    caller to read: 'uv run --quiet --python <uv_python's interpreter> [--offline] SCRIPT ARGS';
    under the per-script lock on every run, including rebuilds after cache removal; and within
    timeout seconds, a wait on the lock included, after which it is stopped (exit 2, with hint).
    capture=False lets the script's output through to the terminal. Exit 2 where uv is absent."""
    uv = need("uv")
    script = Path(script).resolve()
    python, _how = uv_python(uv, script)
    cmd = [uv, "run", "--quiet", "--python", python] + (["--offline"] if offline else []) \
        + [str(script)] + [str(a) for a in args]
    deadline = time.monotonic() + timeout
    name = f"{script.stem}-{hashlib.sha256(str(script).encode('utf-8')).hexdigest()[:16]}"
    with _exclusive(lock_folder() / f'{name}.lock', deadline, script.name, timeout):
        return _run_until(cmd, cwd, capture, deadline, script.name, timeout, hint)


FORMAT_RE = re.compile(r"(?:mp3|pcm)_\d+(?:_\d+)?")


def voice_row(use: str) -> dict:
    """The Narrators row of brand/src/voice/voice.md whose Use is use (lower-case column names)."""
    p = path(VOICE_MD)
    if not use or not p.is_file():
        return {}
    lines = read_text(p).split("\n")
    head, last = find_table(lines, ("Use", "Service"))
    if head is None:
        return {}
    names = [c.lower() for c in split_row(lines[head])]
    for i in range(head + 2, last + 1):
        cells = dict(zip(names, split_row(lines[i])))
        if cells.get("use") == use:
            return cells
    return {}


def chapter_format(piece: str) -> tuple:
    """(output_format, where it was read) for an audiobook's takes: the chapter register's
    output_format, else the Output format of its voice_use row in voice.md, else mp3_44100_128."""
    reg = path(AUDIOBOOK) / f"{piece}.md"
    meta = split_frontmatter(read_text(reg))[0] if reg.is_file() else {}
    fmt = str(meta.get("output_format", "") or "").strip()
    if FORMAT_RE.fullmatch(fmt):
        return fmt, f"output_format in {shown(reg)}"
    use = str(meta.get("voice_use", "") or "narration").strip()
    fmt = str(voice_row(use).get("output format", "") or "").strip()
    if FORMAT_RE.fullmatch(fmt):
        return fmt, f"the Output format of the {use} row of {VOICE_MD}"
    return "mp3_44100_128", ("the default (neither the chapter register nor the "
                             f"{use} row of {VOICE_MD} records an output format)")


def pcm_format_for(p) -> str | None:
    """The ElevenLabs output_format of a .pcm take, read from the register its name points to."""
    p = Path(p)
    if p.suffix.lower() != ".pcm":
        return None
    m = re.match(r"^(.+?)\.s\d+\.t\d+\.pcm$", p.name)
    if m:
        reg = path(VOICEOVER) / f"{m.group(1)}.toml"
        if reg.is_file():
            fmt = load_toml(reg).get("voiceover", {}).get("output_format", "")
            if str(fmt).startswith("pcm_"):
                return fmt
    m = re.match(r"^(.+?)\.ch\d+\.p\d+\.t\d+\.pcm$", p.name)
    if m:
        fmt = chapter_format(m.group(1))[0]
        if fmt.startswith("pcm_"):
            return fmt
    raise Fatal(f"{shown(p)} is raw PCM, and its register gives no pcm_* output_format: record "
                "output_format in the register (or pass --output-format to probe)")


def pcm_rate(fmt: str) -> int:
    m = re.fullmatch(r"pcm_(\d+)", str(fmt))
    if not m:
        raise Fatal(f"{fmt!r} is not a pcm_<rate> output format")
    return int(m.group(1))


def input_args(p, pcm_format=None) -> list:
    """ffmpeg input arguments; a .pcm take is headerless 16-bit little-endian mono (VERIFY)."""
    p = Path(p)
    fmt = pcm_format or pcm_format_for(p)
    if fmt:
        return ["-f", "s16le", "-ar", str(pcm_rate(fmt)), "-ac", "1", "-i", str(p)]
    return ["-i", str(p)]


def probe(p, pcm_format=None, frame: bool = False) -> dict:
    """ffprobe's format and streams as a dict (JSON). frame adds the first decoded frame under
    "frames": what a filter graph is handed, which the stream's header does not always say (an
    image's EXIF orientation arrives as the frame's display matrix)."""
    p = Path(p)
    if not p.is_file():
        raise Fatal(f"not found: {shown(p)}")
    cmd = [need("ffprobe"), "-v", "error", "-print_format", "json", "-show_format", "-show_streams"]
    if frame:
        cmd += ["-show_frames", "-read_intervals", "%+#1"]
    fmt = pcm_format or pcm_format_for(p)
    if fmt:
        cmd += ["-f", "s16le", "-sample_rate", str(pcm_rate(fmt)), "-ch_layout", "mono"]
    proc = run(cmd + [str(p)], what=f"ffprobe on {shown(p)}")
    try:
        return json.loads(proc.stdout)
    except json.JSONDecodeError:
        raise Fatal(f"ffprobe gave no readable answer for {shown(p)}") from None


def streams(info: dict, kind: str) -> list:
    return [s for s in info.get("streams", []) if s.get("codec_type") == kind
            and not s.get("disposition", {}).get("attached_pic")]


def duration(info: dict) -> float:
    for value in [info.get("format", {}).get("duration")] + \
                 [s.get("duration") for s in info.get("streams", [])]:
        try:
            if value not in (None, "N/A"):
                return float(value)
        except (TypeError, ValueError):
            continue
    return 0.0


def rate(text) -> float:
    try:
        num, _, den = str(text).partition("/")
        return float(num) / float(den or 1)
    except (ValueError, ZeroDivisionError):
        return 0.0


def moov_first(p) -> bool | None:
    """True when an MP4's moov box precedes its mdat (faststart); None when it is not an MP4."""
    try:
        with open(p, "rb") as fh:
            while True:
                head = fh.read(8)
                if len(head) < 8:
                    return None
                size, kind = int.from_bytes(head[:4], "big"), head[4:8]
                if kind == b"moov":
                    return True
                if kind == b"mdat":
                    return False
                if size == 1:
                    size = int.from_bytes(fh.read(8), "big")
                    fh.seek(size - 16, 1)
                elif size == 0:
                    return None
                else:
                    fh.seek(size - 8, 1)
    except OSError:
        return None


# ── Images: a still, or a moving image (an animated GIF or WebP) ────────────────────────

IMAGE_EXT = {".png", ".jpg", ".jpeg", ".webp", ".bmp", ".gif", ".tif", ".tiff"}
ANIMATED_EXT = {".gif", ".webp"}   # image formats that may hold more than one frame


def webp_animated(p) -> bool:
    """True when a WebP's VP8X header sets the animation flag."""
    try:
        with open(p, "rb") as fh:
            head = fh.read(21)
    except OSError:
        return False
    return (len(head) == 21 and head[:4] == b"RIFF" and head[8:12] == b"WEBP"
            and head[12:16] == b"VP8X" and bool(head[20] & 0x02))


def image_frames(p, info=None) -> int:
    """How many frames an image file holds: 1 for a still, more for an animated GIF or WebP
    (a screen recording saved as a GIF, VHS's default output). Read from ffprobe's nb_frames,
    or by counting packets where the demuxer gives none; never decoded."""
    p = Path(p)
    if p.suffix.lower() not in ANIMATED_EXT:
        return 1
    info = info or probe(p)
    v = streams(info, "video")
    if p.suffix.lower() == ".webp" and webp_animated(p) and (not v or not int(v[0].get("width") or 0)):
        raise Fatal(f"{shown(p)} is an animated WebP, and this ffmpeg cannot decode it (ffprobe "
                    "finds no picture size; ffmpeg 6.1 has no animated WebP decoder): record to MP4, "
                    "WebM or GIF instead, or convert it with a tool that reads animated WebP")
    if not v:
        return 1
    try:
        return max(1, int(v[0].get("nb_frames")))
    except (TypeError, ValueError):
        pass
    proc = run([need("ffprobe"), "-v", "error", "-select_streams", "v:0", "-count_packets",
                "-show_entries", "stream=nb_read_packets", "-of", "csv=p=0", str(p)],
               what=f"ffprobe on {shown(p)}")
    try:
        return max(1, int(proc.stdout.strip().split(",")[0]))
    except ValueError:
        return 1


def is_still(p, info=None) -> bool:
    """True for an image ffmpeg holds as one frame: PNG, JPEG, BMP, TIFF, and a GIF or WebP with
    a single frame. A GIF or WebP with more frames is a moving source, cut by in and out."""
    p = Path(p)
    return p.suffix.lower() in IMAGE_EXT and image_frames(p, info) <= 1


def still_input(p, fps_text: str, seconds=None) -> list:
    """ffmpeg input arguments that hold one image as a stream of frames at fps_text. The gif
    demuxer has no loop option ('Option loop not found'), so a GIF is read by the image2 demuxer
    with the gif decoder named, which also holds the first frame of a moving GIF. The decoder
    runs one thread: with one frame thread per CPU, each looped 1920x1080 image held about 180 MB
    for the whole render, and with one about 37 MB (ffmpeg 6.1.1, 16 CPUs)."""
    p = Path(p)
    head = ["-f", "image2", "-c:v", "gif"] if p.suffix.lower() == ".gif" else []
    tail = ["-t", f"{seconds:.6f}"] if seconds is not None else []
    return head + ["-loop", "1", "-framerate", str(fps_text)] + tail + ["-threads", "1", "-i", str(p)]


# ── Git: never read what it ignores (DESIGN D50) ────────────────────────────────────────

def in_work_tree(where: Path) -> bool:
    git = shutil.which("git")
    if not git:
        return False
    proc = subprocess.run([git, "rev-parse", "--is-inside-work-tree"], cwd=where,
                          capture_output=True, text=True)
    return proc.stdout.strip() == "true"


def not_ignored(paths: list, where: Path) -> list:
    """The paths git does not ignore (or a negation re-includes); all of them outside a work tree."""
    git = shutil.which("git")
    if not paths or not git or not in_work_tree(where):
        return list(paths)
    names = {str(Path(p).resolve()): p for p in paths}
    proc = subprocess.run([git, "check-ignore", "-z", "--stdin", "--verbose", "--non-matching"],
                          cwd=where, input="".join(n + "\0" for n in names),
                          capture_output=True, text=True, encoding="utf-8")
    if proc.returncode not in (0, 1):
        raise Fatal(f"git check-ignore failed in {shown(where)}: {proc.stderr.strip()}")
    fields = proc.stdout.split("\0")
    keep = set()
    for k in range(0, len(fields) - 3, 4):  # source, line, pattern, path
        source, pattern, name = fields[k], fields[k + 2], fields[k + 3]
        if not source or pattern.startswith("!"):
            keep.add(name)
    return [p for n, p in names.items() if n in keep]


def git_lines(args: list, cwd: Path, z: bool = True) -> list:
    proc = run([need("git")] + args, cwd=cwd, what="git " + args[0])
    sep = "\0" if z else "\n"
    return [x for x in proc.stdout.split(sep) if x]


def walk_files(base: Path) -> list:
    """Every file under base, .git and __pycache__ left out."""
    out = []
    for dirpath, dirnames, filenames in os.walk(base):
        dirnames[:] = [d for d in dirnames if d not in (".git", "__pycache__")]
        out.extend(Path(dirpath) / f for f in filenames)
    return sorted(out)
