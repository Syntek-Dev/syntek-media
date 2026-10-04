#!/usr/bin/env python3
"""media_captions.py: captions and script timing for media.py.

Not run directly: python3 toolkit/media.py captions … and media.py script time call it, and
media.py's self-test exercises it. It reads the script and transcript format of
scripts/src/pieces/<piece>/ (one H2 per beat, '## N. Name (target MM:SS)' or, in a transcript,
'(at HH:MM:SS.mmm)'; a spoken line opens with an upper-case speaker tag and a colon; TEXT, SFX,
MUSIC and NOTE are cues, never spoken; directions sit in braces and {pause S} adds seconds), and
writes SRT (the master format), WebVTT and the ASS file that burn-in uses.

House caption limits (DESIGN Section 6.9): at most 42 characters a line (32 for a 9:16
deliverable), at most two lines a cue, at most 17 characters a second, a cue of 1.0 to 7.0
seconds, at least 0.08 seconds between cues, no braces and no audio tags.

Timing routes (DESIGN D22): from-segments spreads each approved voiceover segment's probed
duration over its cues by character share, so a cue starts exactly where its segment starts;
align spreads a script's or transcript's cues over the speech ffmpeg's silencedetect finds (a
heuristic: the author checks it by eye in a burned preview), beat by beat with --anchors; retime
carries timing through an edit decision list (each cue into the clip holding at least half of it,
never doubled across an edit; a cue the edit leaves less than half of is dropped and named), or
from a master to one cut (a cue clipped at the cut's edge by more than 0.25 s is named).

check compares the captions with the script or transcript; for a recorded piece whose edit
leaves stretches of the recording out (production/src/edits/<piece>.toml), transcript words
missing from the captions are a note, not a finding, where every beat they belong to reaches
into a removed stretch (by the beats' anchors). An SRT with no cue, an empty cue or overlapping
cues is refused by burn, cut --captions and vtt.

Where the output goes: from-segments writes to publishing/src/renders/ unless -o names a path;
align, retime, rewrap and vtt write to the path -o names, or else to stdout, with every report
line on stderr, because their files belong in the tracked publishing/src/captions/, where the
toolkit never chooses a path itself. burn writes its render to publishing/src/renders/.

script time reads each beat heading's '(target MM:SS)' as that beat's own duration, never a
running time: it compares every beat with its own target, sums the beat targets for the piece,
and judges the total against the brief's target_seconds (within 10%) and every deliverable's
max_seconds. The pace is --wpm, else the brief's words_per_minute, else 150.

Standard library only; Python 3.11+.
"""
from __future__ import annotations

import difflib
import math
import re
import sys
import tempfile
from dataclasses import dataclass, field
from pathlib import Path

import media_common as C

CUE_TAGS = {"TEXT", "SFX", "MUSIC", "NOTE"}
SPEAKER_RE = re.compile(r"^([A-Z](?:[A-Z0-9 .'’-]*[A-Z0-9])?)\s*:\s*(.*)$")
BEAT_RE = re.compile(r"^##\s+(\d+)\.\s+(.*?)\s*(?:\((target|at)\s+([0-9:.,]+)\))?\s*$")
BRACE_RE = re.compile(r"\{[^{}]*\}")
PAUSE_RE = re.compile(r"\{\s*pause\s+(\d*\.?\d+)\s*\}", re.I)
WORD_RE = re.compile(r"[^\W_]+(?:['’][^\W_]+)*")
COUNT_RE = re.compile(r"[^\W_]+(?:['’-][^\W_]+)*")
TIMING_RE = re.compile(r"^\s*(\d+:\d{1,2}:\d{1,2}[,.]\d{1,3})\s*-->\s*(\d+:\d{1,2}:\d{1,2}[,.]\d{1,3})")
CUT_NAME_RE = re.compile(r"--c\d+")
LIMITS = {"lines": 2, "cps": 17.0, "min": 1.0, "max": 7.0, "gap": C.MIN_GAP}


@dataclass
class Cue:
    start: float
    end: float
    lines: list = field(default_factory=list)

    @property
    def text(self) -> str:
        return " ".join(line.strip() for line in self.lines)


@dataclass
class Line:
    beat: int
    n: int
    speaker: str
    text: str          # as spoken: directions removed
    pause: float       # seconds of {pause S} on the line


@dataclass
class Script:
    path: Path
    meta: dict
    beats: list        # (number, name, kind 'target'|'at'|None, value)
    lines: list


# ── Reading scripts and transcripts ─────────────────────────────────────────────────────

def read_script(p) -> Script:
    p = Path(p)
    meta, body, _ = C.split_frontmatter(C.read_text(p))
    beats, lines, beat, n = [], [], 0, 0
    for raw in body.splitlines():
        stripped = raw.strip()
        m = BEAT_RE.match(stripped)
        if m:
            beat, n = int(m.group(1)), 0
            beats.append((beat, m.group(2), m.group(3), m.group(4)))
            continue
        if stripped.startswith("## "):
            beat, n = 0, 0
            continue
        s = SPEAKER_RE.match(stripped)
        if not s or s.group(1) in CUE_TAGS:
            continue
        pause = sum(float(x) for x in PAUSE_RE.findall(s.group(2)))
        text = re.sub(r"\s+", " ", BRACE_RE.sub(" ", s.group(2))).strip()
        if not text and not pause:
            continue
        n += 1
        lines.append(Line(beat, n, s.group(1), text, pause))
    return Script(p, meta, beats, lines)


def count_words(text: str) -> int:
    return len(COUNT_RE.findall(text))


def words_of(text: str) -> list:
    """Words for comparing captions with a script: lower case, non-speech [sounds] and '- ' left out."""
    text = re.sub(r"\[[^\]]*\]", " ", text.replace("’", "'").replace("‘", "'"))
    text = re.sub(r"(^|\n)\s*-\s+", " ", text)
    return [w.lower() for w in WORD_RE.findall(text)]


def select_lines(script: Script, spec: str | None) -> list:
    """The spoken lines of a 'B.L-B.L' range (or one 'B.L'); every line when spec is empty."""
    if not spec:
        return list(script.lines)
    m = re.fullmatch(r"\s*(\d+)\.(\d+)\s*(?:[-–]\s*(\d+)\.(\d+)\s*)?", spec)
    if not m:
        raise C.Fatal(f"--lines {spec!r} is not B.L or B.L-B.L (beat.line, spoken lines only)")
    a = (int(m.group(1)), int(m.group(2)))
    b = (int(m.group(3)), int(m.group(4))) if m.group(3) else a
    chosen = [ln for ln in script.lines if a <= (ln.beat, ln.n) <= b]
    if not chosen:
        raise C.Fatal(f"--lines {spec} names no spoken line of {C.shown(script.path)}")
    return chosen


# ── SRT, VTT and ASS ────────────────────────────────────────────────────────────────────

def parse_srt(text: str, where: str = "SRT") -> list:
    text = text.replace("\r\n", "\n").replace("\r", "\n").lstrip("\ufeff")
    cues = []
    for block in re.split(r"\n\s*\n", text.strip()):
        rows = [r for r in block.split("\n") if r.strip() != ""]
        if not rows:
            continue
        if not TIMING_RE.match(rows[0]) and len(rows) > 1 and TIMING_RE.match(rows[1]):
            rows = rows[1:]
        m = TIMING_RE.match(rows[0])
        if not m:
            raise C.Fatal(f"{where}: unreadable cue: {block.splitlines()[0]!r}")
        cues.append(Cue(C.parse_tc(m.group(1)), C.parse_tc(m.group(2)), rows[1:]))
    return cues


def read_srt(p) -> list:
    return parse_srt(C.read_text(p), C.shown(p))


def srt_text(cues: list) -> str:
    out = []
    for i, c in enumerate(cues, start=1):
        out.append(f"{i}\n{C.fmt_tc(c.start, ',')} --> {C.fmt_tc(c.end, ',')}\n" + "\n".join(c.lines))
    return "\n\n".join(out) + "\n"


def vtt_text(cues: list) -> str:
    out = ["WEBVTT", ""]
    for c in cues:
        out.append(f"{C.fmt_tc(c.start)} --> {C.fmt_tc(c.end)}\n" + "\n".join(c.lines) + "\n")
    return "\n".join(out)


def ass_colour(hex6: str) -> str:
    h = hex6.lstrip("#")
    return f"&H00{h[4:6]}{h[2:4]}{h[0:2]}".upper()


def ass_time(t: float) -> str:
    cs = int(round(max(0.0, t) * 100))
    h, cs = divmod(cs, 360_000)
    m, cs = divmod(cs, 6000)
    s, cs = divmod(cs, 100)
    return f"{h}:{m:02d}:{s:02d}.{cs:02d}"


def ass_text(cues: list, width: int, height: int, style: dict, table: dict | None,
             shift: float = 0.0) -> str:
    """An ASS file whose PlayResX and PlayResY are the output size, so sizes are pixel-true."""
    zone = (table or {}).get("safe_zone") or {}
    tw, th = (table or {}).get("width") or width, (table or {}).get("height") or height
    bottom = round(zone.get("bottom", 0) * height / th) if zone.get("bottom") else round(0.08 * height)
    left = round(zone.get("left", 0) * width / tw) if zone.get("left") else round(0.05 * width)
    right = round(zone.get("right", 0) * width / tw) if zone.get("right") else round(0.05 * width)
    weight = style["weight"]
    bold = 0 if weight < 550 else (-1 if weight == 700 else weight)
    size = max(1, round(style["size_vh"] * height / 100))
    outline = round(style["outline_vh"] * height / 100, 1)
    family = style["family"].replace(",", " ")
    head = [
        "[Script Info]", "ScriptType: v4.00+", f"PlayResX: {width}", f"PlayResY: {height}",
        "ScaledBorderAndShadow: yes", "WrapStyle: 0", "YCbCr Matrix: None", "",
        "[V4+ Styles]",
        "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, "
        "BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, "
        "BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
        f"Style: Default,{family},{size},{ass_colour(style['text'])},&H000000FF,"
        f"{ass_colour(style['outline'])},&H00000000,{bold},0,0,0,100,100,0,0,1,{outline},0,2,"
        f"{left},{right},{bottom},1",
        "", "[Events]",
        "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text",
    ]
    for c in cues:
        text = "\\N".join(BRACE_RE.sub("", line).replace("{", "").replace("}", "") for line in c.lines)
        head.append(f"Dialogue: 0,{ass_time(c.start + shift)},{ass_time(c.end + shift)},"
                    f"Default,,0,0,0,,{text}")
    return "\n".join(head) + "\n"


def font_fell_back(log: str, family: str):
    """(fell_back, chosen) from libass's 'fontselect:' lines; fell_back is None when unknown."""
    chosen = [m.group(1).strip() for m in re.finditer(r"fontselect:\s*\([^)]*\)\s*->\s*(.+)", log)]
    if family.lower() in C.GENERIC_FAMILIES:
        return None, ", ".join(chosen)
    if not chosen:
        return None, ""
    want = re.sub(r"[^a-z0-9]", "", family.lower())
    bad = [c for c in chosen if want not in re.sub(r"[^a-z0-9]", "", c.lower())]
    return bool(bad), ", ".join(chosen)


# ── Limits, line breaking and chunking ──────────────────────────────────────────────────

def width_for(table: dict | None) -> int:
    return 32 if table and C.portrait(table) else 42


def check_cues(cues: list, width: int) -> list:
    """Every breach of the house limits, one string per finding."""
    if not cues:
        return ["the file holds no cues"]
    found = []
    for i, c in enumerate(cues, start=1):
        at = f"cue {i} ({C.fmt_tc(c.start)})"
        dur = c.end - c.start
        if dur <= 0:
            found.append(f"{at}: ends before it starts")
            continue
        if not c.text.strip():
            found.append(f"{at}: has no text")
            continue
        if len(c.lines) > LIMITS["lines"]:
            found.append(f"{at}: {len(c.lines)} lines (limit {LIMITS['lines']})")
        for k, line in enumerate(c.lines, start=1):
            if len(line) > width:
                found.append(f"{at}: line {k} has {len(line)} characters (limit {width})")
        chars = sum(len(line) for line in c.lines)
        if chars / dur > LIMITS["cps"] + 1e-9:
            found.append(f"{at}: {chars / dur:.1f} characters a second (limit {LIMITS['cps']:g})")
        if dur < LIMITS["min"] - 1e-6:
            found.append(f"{at}: lasts {dur:.3f} s (at least {LIMITS['min']:g})")
        if dur > LIMITS["max"] + 1e-6:
            found.append(f"{at}: lasts {dur:.3f} s (at most {LIMITS['max']:g})")
        if "{" in c.text or "}" in c.text:
            found.append(f"{at}: carries a braced direction, which never reaches captions")
        if i < len(cues):
            gap = cues[i].start - c.end
            if gap < -1e-6:
                found.append(f"{at}: overlaps the next cue by {-gap:.3f} s")
            elif gap < LIMITS["gap"] - 1e-6:
                found.append(f"{at}: {gap:.3f} s before the next cue (at least {LIMITS['gap']:g})")
    return found


STRUCTURAL = ("holds no cues", "ends before it starts", "has no text", "overlaps the next cue")


def structural(findings: list) -> list:
    """The findings no render or conversion may carry: no cues, a cue with no text or no length,
    and overlapping cues. The rest (line length, reading speed, length, gaps) are limits."""
    return [f for f in findings if any(k in f for k in STRUCTURAL)]


def burn_check(cues: list, width: int, label: str) -> None:
    """Before a burn: refuse captions that are empty, negative or overlapping (exit 1, nothing
    rendered); print every other breach of the house limits as a warning."""
    found = check_cues(cues, width)
    hard = structural(found)
    if hard:
        raise C.Finding(f"{label} cannot be burned in: " + "; ".join(hard)
                        + ". Fix the captions (captions check names each), then burn again; nothing rendered")
    for f in found:
        print(f"  warning: {f} (captions check fails it: rewrap or retime before publishing)")


def _name_join(a: str, b: str) -> bool:
    return bool(a[:1].isupper() and b[:1].isupper() and not re.search(r"[.!?:;,]$", a))


def break_lines(text: str, width: int, max_lines: int = 2):
    """The text as one or two balanced lines within width, or None when it cannot fit."""
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) <= width:
        return [text]
    if max_lines < 2:
        return None
    words = text.split(" ")
    best = None
    for i in range(1, len(words)):
        a, b = " ".join(words[:i]), " ".join(words[i:])
        if len(a) > width or len(b) > width:
            continue
        score = max(len(a), len(b))
        score += 0 if re.search(r"[,.;:!?—–]$", words[i - 1]) else 7
        score += 8 if _name_join(words[i - 1], words[i]) else 0
        if best is None or score < best[0]:
            best = (score, [a, b])
    return best[1] if best else None


def _split_words(text: str, width: int, max_lines: int) -> list:
    words = text.split()
    total = len(text)
    n = max(1, math.ceil(total / (width * max_lines * 0.9)))
    while n <= len(words):
        target, pieces, cur = total / n, [], []
        for w in words:
            if cur and len(" ".join(cur + [w])) > target * 1.15 and len(pieces) < n - 1:
                pieces.append(" ".join(cur))
                cur = []
            cur.append(w)
        pieces.append(" ".join(cur))
        if all(break_lines(p, width, max_lines) for p in pieces):
            return pieces
        n += 1
    return [" ".join(words)]


def chunk_text(text: str, width: int, max_lines: int = 2) -> list:
    """Cue texts: sentence and clause boundaries first; a short sentence joins its neighbour."""
    text = re.sub(r"\s+", " ", BRACE_RE.sub(" ", text)).strip()
    if not text:
        return []
    pieces = []
    for sentence in re.split(r"(?<=[.!?…])\s+", text):
        if break_lines(sentence, width, max_lines):
            pieces.append(sentence)
            continue
        cur = ""
        for clause in re.split(r"(?<=[,;:—–])\s+", sentence):
            trial = f"{cur} {clause}".strip()
            if break_lines(trial, width, max_lines):
                cur = trial
                continue
            if cur:
                pieces.append(cur)
            if break_lines(clause, width, max_lines):
                cur = clause
            else:
                pieces.extend(_split_words(clause, width, max_lines))
                cur = ""
        if cur:
            pieces.append(cur)
    merged = []
    for p in pieces:
        if merged and len(merged[-1]) < 20 and break_lines(merged[-1] + " " + p, width, max_lines):
            merged[-1] = merged[-1] + " " + p
        else:
            merged.append(p)
    return merged


def as_cue_lines(text: str, width: int) -> list:
    return break_lines(text, width) or [text]


def spread(texts: list, start: float, end: float, width: int) -> list:
    """Cues over [start, end] by character share; starts exact, ends leave the house gap."""
    total = sum(len(t) for t in texts) or 1
    cues, acc = [], 0
    for t in texts:
        a = start + (end - start) * acc / total
        acc += len(t)
        b = start + (end - start) * acc / total
        cues.append(Cue(a, b, as_cue_lines(t, width)))
    for i in range(len(cues) - 1):
        cues[i].end = min(cues[i].end, cues[i + 1].start - C.MIN_GAP)
    return cues


def keep_gaps(cues: list) -> list:
    """Cues in time order with the house gap between them. A cue the gap would leave with no
    length (it starts at or after the next cue's start, less the gap) is merged into the next,
    its words first, so no cue ends before it starts and no word is lost; captions check then
    judges the merged cue's lines and reading speed."""
    cues.sort(key=lambda c: c.start)
    i = 0
    while i < len(cues) - 1:
        a, b = cues[i], cues[i + 1]
        if b.start - a.end < C.MIN_GAP:
            if b.start - C.MIN_GAP <= a.start + 0.05:
                cues[i + 1] = Cue(a.start, max(a.end, b.end), list(a.lines) + list(b.lines))
                del cues[i]
                continue
            a.end = b.start - C.MIN_GAP
        i += 1
    return cues


def report(findings: list, label: str, stream=None) -> int:
    for f in findings:
        print(f"  FAIL {f}", file=stream)
    if findings:
        print(f"{label}: {len(findings)} finding(s)", file=stream)
        return 1
    print(f"{label}: clean", file=stream)
    return 0


def note(text: str) -> None:
    """A report line for a command whose product may go to stdout: it goes to stderr."""
    print(text, file=sys.stderr)


def default_srt(name: str) -> Path:
    return C.path(C.PUB_RENDERS) / name


def write_out(out: Path, text: str) -> None:
    out.write_text(text, encoding="utf-8")
    print(f"wrote {C.shown(out)}")


def emit(text: str, given, inputs=()) -> None:
    """align, retime, rewrap and vtt: write to the path -o names, or else print to stdout.

    Their output belongs in publishing/src/captions/, which is tracked, so the toolkit never
    picks a path there itself (DESIGN Section 4.2): without -o the captions go to stdout and every
    report line to stderr. An existing file outside a renders/ or generated/ folder is never
    overwritten, so a caption file is made again only after the author has moved the old one.
    """
    if given:
        out = C.output_path(Path(given), None, inputs=inputs)
        out.write_text(text, encoding="utf-8")
        note(f"wrote {C.shown(out)}")
    else:
        sys.stdout.write(text)
        sys.stdout.flush()


# ── Commands ────────────────────────────────────────────────────────────────────────────

def cmd_check(args) -> int:
    cues = read_srt(args.srt)
    table = C.preset(args.deliverable) if args.deliverable else None
    width = width_for(table)
    found = check_cues(cues, width)
    if args.script:
        compared = compare_with_script(cues, args.script, CUT_NAME_RE.search(Path(args.srt).name), args.srt)
        found += compared[0]
        for n in compared[1]:
            print(f"  note: {n}")
    return report(found, f"captions check {C.shown(args.srt)} ({width} characters a line)")


def edited_out(script: Script, srt_path) -> tuple:
    """(source ID, the stretches of a recorded piece's recording its master leaves out).

    Only for a transcript (a 'source' footage ID and beats anchored 'at' the recording) checked
    against captions timed to the master or a cut, never to the recording itself: the piece's
    edit decision list, production/src/edits/<piece>.toml, gives the stretches of that source
    its clips keep, and the rest is what the edit removed. ('', []) when there is nothing cut."""
    src = str(script.meta.get("source", "") or "").strip()
    if not re.fullmatch(r"F\d{4,}", src) or not any(kind == "at" for _, _, kind, _ in script.beats):
        return "", []
    if srt_path is None or re.search(r"\.F\d{4,}\.", Path(srt_path).name):
        return src, []
    edl = C.path(C.EDITS) / f"{C.piece_of(srt_path)}.toml"
    if not edl.is_file():
        return src, []
    import media_video as V
    try:
        items = V.timeline(V.load_edl(edl))
    except C.Fatal:
        return src, []
    spans = sorted((c["in"], c["in"] + c["dur"]) for c in items if c["source"] == src and c["kind"] == "media")
    if not spans:
        return src, []
    entry = V.manifest_entries().get(src, {})
    length = float(entry.get("duration") or 0)
    p = C.path(C.FOOTAGE) / str(entry.get("path", "")) if entry.get("path") else None
    if p is not None and p.is_file():
        length = C.duration(C.probe(p)) or length
    gaps, cur = [], 0.0
    for a, b in spans:
        if a > cur + 0.05:
            gaps.append((cur, a))
        cur = max(cur, b)
    if length and cur < length - 0.05:
        gaps.append((cur, length))
    return src, gaps


def compare_with_script(cues: list, script_path, is_cut, srt_path=None) -> tuple:
    """(findings, notes): the caption words against the spoken words; a cut may start and end
    inside the script. For a recorded piece whose edit leaves stretches of the recording out,
    script words missing from the captions are a note, not a finding, when every beat they
    belong to reaches into a stretch the edit removed (by the transcript's beat anchors)."""
    script = read_script(script_path)
    want, beat_of = [], []
    for ln in script.lines:
        w = words_of(ln.text)
        want += w
        beat_of += [ln.beat] * len(w)
    got = words_of("\n".join("\n".join(c.lines) for c in cues))
    if not got:
        return ["the captions carry no words"], []
    src, gaps = edited_out(script, srt_path)
    anchors = sorted((C.parse_tc(v, "beat anchor"), num) for num, _, kind, v in script.beats if kind == "at" and v)
    reach = {}
    for k, (t, num) in enumerate(anchors):
        end = anchors[k + 1][0] if k + 1 < len(anchors) else float("inf")
        reach[num] = any(a < end and b > t for a, b in gaps)

    def cut_away(i1, i2) -> bool:
        return bool(gaps) and all(reach.get(b, False) for b in beat_of[i1:i2])
    found, notes = [], []
    sm = difflib.SequenceMatcher(None, want, got, autojunk=False)
    ops = sm.get_opcodes()
    removed = ", ".join(f"{C.fmt_tc(a)}–{C.fmt_tc(b)}" for a, b in gaps)
    for tag, i1, i2, j1, j2 in ops:
        if tag == "equal":
            continue
        edge = (i1 == 0 and j1 == j2 == 0) or (i2 == len(want) and j1 == j2 == len(got))
        if tag == "delete" and cut_away(i1, i2):
            notes.append(f"words of the transcript the edit leaves out of {src} ({removed}): "
                         f"'{' '.join(want[i1:i2][:24])}'")
            continue
        if tag == "delete" and edge:
            if not is_cut:
                where = "opening" if i1 == 0 else "closing"
                found.append(f"the {where} words of the script are not captioned: "
                             f"'{' '.join(want[i1:i2][:12])}'")
            continue
        if tag == "delete":
            found.append(f"words of the script missing from the captions: '{' '.join(want[i1:i2])}'")
        elif tag == "insert":
            found.append(f"words in the captions that the script does not have: '{' '.join(got[j1:j2])}'")
        else:
            found.append(f"captions say '{' '.join(got[j1:j2])}' where the script says "
                         f"'{' '.join(want[i1:i2])}'")
    return found, notes


def segment_duration(p: Path) -> float:
    info = C.probe(p)
    audio = C.streams(info, "audio")
    if not audio:
        raise C.Fatal(f"{C.shown(p)} has no audio stream")
    try:
        return float(audio[0].get("duration") or C.duration(info))
    except (TypeError, ValueError):
        return C.duration(info)


def approved_segments(register: Path) -> tuple:
    data = C.load_toml(register)
    head = data.get("voiceover", {})
    segs = [s for s in data.get("segment", []) if str(s.get("status", "")).strip() == "approved"]
    if not segs:
        raise C.Fatal(f"{C.shown(register)} has no approved segment")
    for s in segs:
        if not s.get("file"):
            raise C.Fatal(f"segment {s.get('id', '?')} of {C.shown(register)} is approved but names no file")
        f = C.path(C.VOICEOVER) / s["file"]
        if not f.is_file():
            raise C.Fatal(f"segment {s.get('id', '?')}: its take {C.shown(f)} is missing")
    return head, segs


def cmd_from_segments(args) -> int:
    register = Path(args.register)
    head, segs = approved_segments(register)
    table = C.preset(args.deliverable)
    width = width_for(table)
    per_cue = bool(head.get("per_cue", False))
    t = C.parse_tc(args.offset) if args.offset else 0.0
    cues = []
    for s in segs:
        f = C.path(C.VOICEOVER) / s["file"]
        dur = segment_duration(f)
        text = str(s.get("text", "")).strip()
        texts = [re.sub(r"\s+", " ", BRACE_RE.sub(" ", text)).strip()] if per_cue else chunk_text(text, width)
        if cues and texts:
            cues[-1].end = min(cues[-1].end, t - C.MIN_GAP)
        cues.extend(spread(texts, t, t + dur, width))
        t += dur + float(s.get("pause_after", 0.0) or 0.0)
    piece = head.get("piece") or C.piece_of(register)
    out = C.output_path(default_srt(f"{piece}.{C.file_form(args.deliverable)}.en-GB.srt"), args.o)
    write_out(out, srt_text(cues))
    print(f"{len(cues)} cue(s) from {len(segs)} approved segment(s); every segment's first cue "
          f"starts on its segment")
    return report(check_cues(cues, width), "captions from-segments")


def speech_intervals(audio: Path, noise_db: float, min_silence: float) -> tuple:
    """(speech intervals, duration) from ffmpeg's silencedetect."""
    info = C.probe(audio)
    total = C.duration(info)
    proc = C.ffmpeg(C.input_args(audio) + ["-map", "0:a:0", "-af",
                                           f"silencedetect=noise={noise_db}dB:d={min_silence}",
                                           "-f", "null", "-"], what="silencedetect")
    silences, start = [], None
    for line in proc.stderr.splitlines():
        m = re.search(r"silence_start:\s*(-?[\d.]+)", line)
        if m:
            start = max(0.0, float(m.group(1)))
        m = re.search(r"silence_end:\s*([\d.]+)", line)
        if m and start is not None:
            silences.append((start, float(m.group(1))))
            start = None
    if start is not None:
        silences.append((start, total))
    speech, cur = [], 0.0
    for a, b in silences:
        if a - cur > 0.02:
            speech.append((cur, a))
        cur = max(cur, b)
    if total - cur > 0.02:
        speech.append((cur, total))
    return speech, total


class Timeline:
    """Speech time (seconds of speech) against real time, inside one block."""

    def __init__(self, intervals: list):
        self.iv = intervals
        self.total = sum(b - a for a, b in intervals)

    def real(self, x: float, start: bool = False) -> float:
        """Real time at speech time x; at a gap, a start leans to the next stretch of speech."""
        acc = 0.0
        for a, b in self.iv:
            if (x < acc + (b - a) - 1e-9) if start else (x <= acc + (b - a) + 1e-9):
                return a + max(0.0, x - acc)
            acc += b - a
        return self.iv[-1][1]

    def speech(self, t: float) -> float:
        acc = 0.0
        for a, b in self.iv:
            if t <= a:
                return acc
            if t <= b:
                return acc + (t - a)
            acc += b - a
        return acc

    def gaps(self) -> list:
        out, acc = [], 0.0
        for k in range(len(self.iv) - 1):
            acc += self.iv[k][1] - self.iv[k][0]
            out.append((acc, self.iv[k][1], self.iv[k + 1][0]))
        return out


def place_block(lines: list, intervals: list, b0: float, b1: float, width: int):
    """(cues, warnings, unplaced) for the spoken lines of one block of audio."""
    iv = [(max(a, b0), min(b, b1)) for a, b in intervals if b > b0 and a < b1 and min(b, b1) - max(a, b0) > 0.05]
    texts = [chunk_text(ln.text, width) for ln in lines]
    flat = [t for group in texts for t in group]
    if not iv:
        return [], [], flat
    tl = Timeline(iv)
    sizes = [sum(len(t) for t in group) for group in texts]
    total = sum(sizes) or 1
    bounds, acc = [], 0
    for s in sizes[:-1]:
        acc += s
        bounds.append(tl.total * acc / total)
    starts, ends = [iv[0][0]], []
    gaps, used = tl.gaps(), -1.0
    avg = tl.total / max(1, len(lines))
    for x in bounds:
        tol = max(0.5, 0.35 * avg)
        options = [g for g in gaps if g[0] > used + 1e-6 and abs(g[0] - x) <= tol]
        if options:
            g = min(options, key=lambda g: abs(g[0] - x))
            used = g[0]
            ends.append(g[1])
            starts.append(g[2])
        else:
            ends.append(tl.real(x))
            starts.append(tl.real(x, start=True))
    ends.append(iv[-1][1])
    cues, warnings, unplaced = [], [], []
    for group, a, b in zip(texts, starts, ends):
        xa, xb = tl.speech(a), tl.speech(b)
        g_total = sum(len(t) for t in group) or 1
        acc = 0
        for t in group:
            s = tl.real(xa + (xb - xa) * acc / g_total, start=True)
            acc += len(t)
            e = tl.real(xa + (xb - xa) * acc / g_total)
            cues.append(Cue(s, e, as_cue_lines(t, width)))
    keep_gaps(cues)
    for c in cues:
        dur = c.end - c.start
        if dur < 0.3:
            unplaced.append(c.text)
            continue
        silent = dur - (tl.speech(c.end) - tl.speech(c.start))
        if dur > LIMITS["max"] or len(c.text) / dur < 4 or silent > 1.0:
            warnings.append(f"cue at {C.fmt_tc(c.start)} is stretched over {dur:.2f} s "
                            f"({silent:.2f} s of it silence): '{c.text[:40]}'")
    return [c for c in cues if c.end - c.start >= 0.3], warnings, unplaced


def cmd_align(args) -> int:
    script = read_script(args.text)
    audio = Path(args.audio)
    if args.anchors and args.lines:
        raise C.Fatal("--anchors works on the whole recording, --lines on one cut's audio: use one")
    chosen = select_lines(script, args.lines)
    intervals, total = speech_intervals(audio, args.noise, args.min_silence)
    width = 42
    cues, warnings, unplaced = [], [], []
    if args.anchors:
        anchors = {num: C.parse_tc(value, "beat anchor") for num, _, kind, value in script.beats
                   if kind == "at" and value}
        beats = sorted({ln.beat for ln in chosen})
        missing = [b for b in beats if b not in anchors]
        if missing:
            raise C.Fatal(f"--anchors: beat(s) {', '.join(map(str, missing))} of "
                          f"{C.shown(script.path)} carry no '(at HH:MM:SS.mmm)' anchor")
        order = sorted(anchors.items())
        for b in beats:
            start = anchors[b]
            later = [t for num, t in order if t > start]
            end = min(later) if later else total
            block = [ln for ln in chosen if ln.beat == b]
            got, warn, lost = place_block(block, intervals, start, end, width)
            cues += got
            warnings += warn
            unplaced += lost
    else:
        got, warn, lost = place_block(chosen, intervals, 0.0, total, width)
        cues, warnings, unplaced = got, warn, lost
    cues.sort(key=lambda c: c.start)
    keep_gaps(cues)
    emit(srt_text(cues), args.o, inputs=[args.text, audio])
    for w in warnings:
        note(f"  warning: {w}")
    note(f"{len(cues)} cue(s) placed over {len(intervals)} stretch(es) of speech "
         f"(silence below {args.noise:g} dB for {args.min_silence:g} s or more); check them by "
         "eye in a burned preview")
    if unplaced:
        for u in unplaced:
            note(f"  FAIL could not place: '{u[:60]}'")
        note(f"captions align: {len(unplaced)} cue(s) could not be placed")
        return 1
    return 0


def place_in_spans(cues: list, spans: list) -> tuple:
    """(cues on the master, report) for recording-timed cues and the clip spans (in, out, start on
    the master) of one source. A cue goes into each span holding at least half of it, clipped to
    that span: never into two spans that split it at an edit (the larger part is kept), and never
    a fragment under half (dropped, and named), so no cue is doubled across an edit or a fade."""
    out, clipped, dropped, outside = [], [], [], 0
    for n, c in enumerate(cues, start=1):
        dur = max(c.end - c.start, 1e-6)
        parts = sorted(((min(c.end, b) - max(c.start, a), a, b, at) for a, b, at in spans
                        if min(c.end, b) - max(c.start, a) > 0), key=lambda p: -p[0])
        if not parts:
            outside += 1
            continue
        held = [p for p in parts if p[0] >= 0.5 * dur - 1e-6]
        if not held:
            dropped.append((n, c))
            continue
        best = held[0]
        keep = [best]
        for p in held[1:]:   # the same stretch used twice in the edit is captioned twice
            shared = min(c.end, best[2], p[2]) - max(c.start, best[1], p[1])
            if shared >= 0.5 * dur - 1e-6:
                keep.append(p)
        for ov, a, b, at in keep:
            s, e = max(c.start, a), min(c.end, b)
            out.append(Cue(at + s - a, at + e - a, list(c.lines)))
        if best[0] < dur - 0.25:
            clipped.append((n, c, dur - best[0]))
    return out, clipped, dropped, outside


def cmd_retime(args) -> int:
    cues = read_srt(args.srt)
    out_cues, clipped, dropped, outside = [], [], [], 0
    if args.edl:
        if not args.source:
            raise C.Fatal("--edl needs --source FID (the recording the captions are timed to)")
        if args.cut_in is not None or args.cut_out is not None:
            raise C.Fatal("captions retime takes --in and --out, or --edl and --source, not both")
        import media_video as V
        edl = V.load_edl(Path(args.edl))
        spans = [(c["in"], c["in"] + c["dur"], c["start"]) for c in V.timeline(edl)
                 if c["source"] == args.source and c["kind"] == "media"]
        if not spans:
            raise C.Fatal(f"{C.shown(args.edl)} has no [[clip]] of {args.source}")
        out_cues, clipped, dropped, outside = place_in_spans(cues, spans)
        where = "an edit"
    else:
        if args.cut_in is None or args.cut_out is None:
            raise C.Fatal("captions retime needs --in and --out, or --edl and --source")
        if args.source:
            raise C.Fatal("--source goes with --edl; --in and --out retime master timing to a cut")
        a, b = C.parse_tc(args.cut_in), C.parse_tc(args.cut_out)
        if b <= a:
            raise C.Fatal("--out must come after --in")
        for n, c in enumerate(cues, start=1):
            s, e = max(c.start, a), min(c.end, b)
            if e - s > 0.2:
                out_cues.append(Cue(s - a, e - a, list(c.lines)))
                if (c.end - c.start) - (e - s) > 0.25:
                    clipped.append((n, c, (c.end - c.start) - (e - s)))
            elif e > s:
                dropped.append((n, c))
            else:
                outside += 1
        where = "the cut's edge"
    out_cues = keep_gaps(out_cues)
    emit(srt_text(out_cues), args.o, inputs=[args.srt])
    for n, c, lost in clipped:
        note(f"  warning: cue {n} ({C.fmt_tc(c.start)}) is clipped by {lost:.3f} s at {where} but keeps all "
             f"its words ('{c.text[:40]}'): check it with captions check, and re-time that stretch with "
             "'captions align --lines' where it reads too fast")
    for n, c in dropped:
        note(f"  warning: cue {n} ({C.fmt_tc(c.start)}) is dropped: less than half of it survives {where} "
             f"('{c.text[:40]}'); caption that stretch again with 'captions align --lines'")
    note(f"{len(out_cues)} cue(s) written from {len(cues)}; {len(clipped)} clipped, {len(dropped)} dropped, "
         f"{outside} outside {'every clip of ' + args.source if args.edl else 'the cut'}")
    return 0


def cmd_rewrap(args) -> int:
    cues = read_srt(args.srt)
    table = C.preset(args.deliverable)
    width = width_for(table)
    out_cues = []
    for c in cues:
        texts = chunk_text(c.text, width)
        if len(texts) <= 1:
            out_cues.append(Cue(c.start, c.end, as_cue_lines(c.text, width)))
        else:
            out_cues.extend(spread(texts, c.start, c.end, width))
    emit(srt_text(keep_gaps(out_cues)), args.o, inputs=[args.srt])
    return report(check_cues(out_cues, width), f"captions rewrap ({width} characters a line)",
                  stream=sys.stderr)


def cmd_vtt(args) -> int:
    cues = read_srt(args.srt)
    hard = structural(check_cues(cues, 42)) + [
        f"cue {i} ({C.fmt_tc(c.start)}): carries a brace (a direction or an ASS override such as "
        "{\\an8}), which WebVTT shows as text" for i, c in enumerate(cues, start=1) if "{" in c.text or "}" in c.text]
    if hard:
        for f in hard:
            note(f"  FAIL {f}")
        note(f"captions vtt: {len(hard)} finding(s) in {C.shown(args.srt)}; nothing written (fix the SRT first)")
        return 1
    emit(vtt_text(cues), args.o, inputs=[args.srt])
    return 0


def caption_ass(cues, width, height, table, shift=0.0) -> tuple:
    """(ass text, family) from the caption tokens."""
    style = C.caption_style(C.read_tokens())
    return ass_text(cues, width, height, style, table, shift), style["family"]


def stage_fonts(tmp: Path) -> str | None:
    """The brand fonts folder, reachable from tmp as 'fonts' (no quoting in the filtergraph)."""
    fonts = C.path(C.FONTS)
    if not fonts.is_dir():
        return None
    link = tmp / "fonts"
    try:
        link.symlink_to(fonts.resolve(), target_is_directory=True)
    except OSError:
        import shutil
        shutil.copytree(fonts, link)
    return "fonts"


def subtitles_filter(tmp: Path, ass: str) -> str:
    (tmp / "captions.ass").write_text(ass, encoding="utf-8")
    fonts = stage_fonts(tmp)
    return "subtitles=filename=captions.ass" + (f":fontsdir={fonts}" if fonts else "")


def cmd_burn(args) -> int:
    import media_video as V
    src = Path(args.src)
    table = C.preset(args.deliverable)
    info = C.probe(src)
    video = C.streams(info, "video")
    if not video:
        raise C.Fatal(f"{C.shown(src)} has no picture to burn captions into")
    w, h = int(video[0]["width"]), int(video[0]["height"])
    cues = read_srt(args.srt)
    burn_check(cues, width_for(table), C.shown(args.srt))
    stem = src.name.rsplit(".", 1)[0]
    out = C.output_path(C.path(C.PUB_RENDERS) / f"{stem}.burned.mp4", args.o, inputs=[src])
    with tempfile.TemporaryDirectory(prefix="media-burn-") as tmp:
        tmp = Path(tmp)
        ass, family = caption_ass(cues, w, h, table)
        vf = subtitles_filter(tmp, ass) + ",format=yuv420p"
        cmd = ["-y", "-loglevel", "info", "-i", str(src.resolve()), "-map", "0:v:0", "-map", "0:a:0?",
               "-vf", vf] + V.video_codec_args(table, C.rate(video[0].get("r_frame_rate"))) + \
              ["-c:a", "copy", "-movflags", "+faststart", str(out.resolve())]
        proc = V.render(cmd, out, cwd=tmp, what="caption burn-in")
    found = V.verify(out, table, expect=C.duration(info))
    fell, chosen = font_fell_back(proc.stderr, family)
    if fell:
        found.append(f"the caption font '{family}' was not found; libass fell back to {chosen} "
                     "(add the font to brand/src/design-system/fonts/ or install it)")
    elif fell is None and family.lower() not in C.GENERIC_FAMILIES:
        print(f"  note: libass did not say which font it chose for '{family}'")
    V.print_summary(out)
    return report(found, f"captions burn {C.shown(out)}")


# ── script time ─────────────────────────────────────────────────────────────────────────

def mmss(seconds: float) -> str:
    m, s = divmod(max(0.0, seconds), 60)
    if s >= 59.95:
        m, s = m + 1, 0.0
    return f"{int(m):02d}:{s:04.1f}"


def beat_target(kind, value):
    """A beat heading's '(target MM:SS)' in seconds: the beat's own duration, never a running time."""
    if kind != "target" or not value:
        return None
    return C.parse_tc(value, "beat target")


def beat_verdict(estimate: float, target) -> str:
    """How one beat's estimate sits against its own target (a report, not a gate)."""
    if target is None:
        return ""
    if target <= 0:
        return f"target {mmss(target)}"
    diff = estimate - target
    if abs(diff) <= max(0.5, target * 0.1):
        return f"target {mmss(target)}: on time"
    return f"target {mmss(target)}: {'long' if diff > 0 else 'short'} by {abs(diff):.1f} s"


def cmd_script_time(args) -> int:
    script = read_script(args.path)
    brief_path = script.path.parent / "brief.md"
    brief = C.split_frontmatter(C.read_text(brief_path))[0] if brief_path.is_file() else {}
    if args.wpm is not None:
        wpm, said = args.wpm, "--wpm"
    elif isinstance(brief.get("words_per_minute"), (int, float)) and brief["words_per_minute"]:
        wpm, said = brief["words_per_minute"], "the brief's words_per_minute"
    else:
        wpm, said = 150, "the house default"
    wpm = float(wpm)
    if wpm <= 0:
        raise C.Fatal("words a minute must be above 0")
    rows, words_total, pause_total, targets = [], 0, 0.0, []
    for num, name, kind, value in script.beats or [(0, "(no beats)", None, None)]:
        lines = [ln for ln in script.lines if ln.beat == num]
        w = sum(count_words(ln.text) for ln in lines)
        p = sum(ln.pause for ln in lines)
        words_total += w
        pause_total += p
        est = w / wpm * 60 + p
        target = beat_target(kind, value)
        if target is not None:
            targets.append(target)
        note = beat_verdict(est, target) if kind != "at" else f"at {value} on the recording"
        rows.append((f"{num}. {name}" if num else name, w, p, est, note))
    stray = [ln for ln in script.lines if ln.beat == 0 and script.beats]
    if stray:
        w = sum(count_words(ln.text) for ln in stray)
        p = sum(ln.pause for ln in stray)
        words_total += w
        pause_total += p
        rows.append(("(outside a numbered beat)", w, p, w / wpm * 60 + p, ""))
    estimate = words_total / wpm * 60 + pause_total
    beat_sum = sum(targets) if targets else None
    print(f"script time {C.shown(script.path)} ({wpm:g} words a minute, from {said})")
    print(f"  {'Beat':<40} {'Words':>6} {'Pauses':>7} {'Estimate':>9}  Against the beat's own target")
    for label, w, p, est, note in rows:
        print(f"  {label[:40]:<40} {w:>6} {p:>7.1f} {mmss(est):>9}  {note}")
    print(f"  {'Total':<40} {words_total:>6} {pause_total:>7.1f} {mmss(estimate):>9}  "
          + (f"beat targets sum to {mmss(beat_sum)}" if beat_sum is not None else ""))
    found = []
    target = brief.get("target_seconds")
    if isinstance(target, (int, float)) and target > 0:
        lo, hi = target * 0.9, target * 1.1
        verdict = "within" if lo <= estimate <= hi else "OUTSIDE"
        print(f"brief target_seconds {target:g}: {estimate:.1f} s is {verdict} 10% ({lo:.1f}–{hi:.1f})")
        if verdict == "OUTSIDE":
            found.append(f"the estimate {estimate:.1f} s is outside 10% of target_seconds {target:g}")
        if beat_sum is not None and abs(beat_sum - target) > max(0.5, target * 0.1):
            print(f"  note: the beat targets sum to {beat_sum:g} s, not the brief's {target:g} s: "
                  "a beat's target is its own duration, so they should add up to the piece")
    elif beat_sum:
        lo, hi = beat_sum * 0.9, beat_sum * 1.1
        verdict = "within" if lo <= estimate <= hi else "OUTSIDE"
        print(f"{'no brief.md beside the script' if not brief else 'the brief sets no target_seconds'}: "
              f"against the beat targets' sum {beat_sum:g} s, {estimate:.1f} s is {verdict} 10% "
              f"({lo:.1f}–{hi:.1f})")
        if verdict == "OUTSIDE":
            found.append(f"the estimate {estimate:.1f} s is outside 10% of the beat targets' sum {beat_sum:g}")
    elif not brief:
        print("no brief.md beside the script: no target to compare")
    deliverables = brief.get("deliverables") or []
    if deliverables:
        data = C.load_presets(quiet=True)[0]
        for key in deliverables:
            try:
                limit = C.preset(key, data).get("max_seconds")
            except C.Fatal as err:
                found.append(str(err))
                continue
            if limit:
                ok = estimate <= limit
                print(f"{key} max_seconds {limit:g}: {'ok' if ok else 'OVER'}")
                if not ok:
                    found.append(f"the estimate {estimate:.1f} s is over {key} max_seconds {limit:g}")
    if args.write:
        text = C.set_frontmatter(C.read_text(script.path),
                                 {"words": words_total, "estimated_seconds": round(estimate, 1)})
        script.path.write_text(text, encoding="utf-8")
        print(f"wrote words and estimated_seconds into {C.shown(script.path)}")
    return report(found, "script time")
