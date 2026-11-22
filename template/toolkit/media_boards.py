#!/usr/bin/env python3
"""media_boards.py: the board sheet and the animatic, seen before M3 (DESIGN D92, D93).

Not run directly: python3 toolkit/media.py boards PIECE [--size WxH] [--no-animatic]
[--sound FILE] calls it, and media.py's self-test exercises it.

boards reads the piece's scripts/src/pieces/<piece>/storyboard.md (media_captions'
read_storyboard), its shot-list.md (media_repo's shot_rows) and its script.md, for the words
each board's Spoken references name. --size defaults to the edit decision list's [edit] size,
where production/src/edits/<piece>.toml exists, else 1920x1080. For every board Bnn it renders
one still at the size through card.py, from a scratch page built on templates/board.html, its
picture the board's first shot (the first shot-list row whose Board names it):

  card     an existing production/src/cards/<piece>.<card>.html, rendered as assemble renders
           it (its own render, in the piece's cards/ folder); its own words are the card's, so
           the On screen cues are not laid over it again;
  still    an image (a footage ID logged as an image, or an asset), framed to the size as
           assemble frames a still (fit, or the shot's Framing when it reads fit, crop or pad);
  frame    a logged footage ID of video (camera, screen, stock, or an edited shot once its
           export is logged, D93): one frame at its first tenth, labelled 'frame from Fnnnn —
           the edit chooses the moment';
  colour   a #RRGGBB source;
  placeholder  anything else (a shot to shoot, an edited shot to render, which names its
           editor where its Picture does, a scene board, a missing card's HTML, an unlogged ID,
           a mirror without the file, a text capture, a Source outside production/src/assets/
           and production/src/cards/, never opened): a labelled panel naming the board, why, and
           its Picture text, never an invented image. Each is a finding.

The board's On screen cues (each TEXT: cue, or the whole cell) are laid over the picture in
draft styling, so layout can be judged. A build-up board (Picture says build-up, or two or more
TEXT: cues) also gets one still per step, k1, k2 …, the first K cues shown. A board has motion
where its Picture names push-in, pan, zoom or fade.

Into the piece's ignored production/src/renders/<piece>/boards/, after taking out what an
earlier run of boards wrote there (its own names only): <piece>.bNN.board.<W>x<H>.png and
<piece>.bNN.board.kK.<W>x<H>.png; the contact sheet <piece>.boards.html, every still in board
order, each captioned beneath with its board, Time, the spoken words, Picture, On screen,
Sound, its motion and its Vertical framing, drawn as a box over the still (crop x=<px> as the
crop at 9:16, in the master's pixels; centre centred; pad and native named); and, where a board
has motion or a build-up, unless --no-animatic or the piece is a scene piece (a shot of Type
scene), the animatic: <piece>.animatic.toml, a working-copy edit decision list, and
<piece>.animatic.mp4, rendered by assemble with -o to that path. Every board is a still clip
lasting its Time (3 s, noted, where its Time cannot be read), a push-in board carrying
motion = "push-in", a fade board entering with transition = "fade" (its clip lengthened by the
fade, so each board still ends on its Time), a build-up board's step stills dividing its time;
pan and zoom are held still (assemble makes neither: an edited shot does, D93); loudness =
"none"; its sound --sound FILE, else the joined voice production/src/renders/<piece>/
<piece>.voice.wav where it exists, else silence. Nothing later reads any of it but the
animatic's own assemble: the master stays the edit decision list's.

The stills render in a scratch folder and move into boards/ together, so a run that cannot
finish leaves the last sheet as it was. Exit codes: 0 every board shown from its own picture;
1 findings (a board with no shot, a placeholder and why, a Time it could not read, a card's
HTML missing, a card.py or assemble finding), everything it could make still written; 2 could
not run (no storyboard, no uv or Chromium for card.py, no ffmpeg, a bad --size or --sound),
naming what is missing with its install hint.

Standard library only; Python 3.14+.
"""
from __future__ import annotations

import argparse
import html
import json
import re
import shutil
import tempfile
from dataclasses import dataclass, field
from pathlib import Path

import media_captions as K
import media_common as C
import media_repo as R
import media_video as V

DEFAULT_SIZE = (1920, 1080)
VERTICAL = (9, 16)          # the vertical deliverables' aspect the box is drawn at
FADE_SECONDS = 0.5          # an animatic fade, at most; never more than half of either board
HELD_SECONDS = 3.0          # an animatic board whose Time cannot be read
MOTION_RE = re.compile(r"\b(push[- ]in|pan|zoom|fade)\b", re.I)
BUILD_RE = re.compile(r"\bbuild[- ]up\b", re.I)
TIME_RE = re.compile(r"^\s*(\d+):(\d{2}(?:\.\d+)?)\s*[-–]\s*(\d+):(\d{2}(?:\.\d+)?)\s*$")
TEXT_RE = re.compile(r"\bTEXT:\s*")
FRAMING_RE = re.compile(r"^\s*(fit|crop|pad)\b(?:\s*x\s*=\s*(\d+))?", re.I)
CROP_RE = re.compile(r"^\s*crop\s*x\s*=\s*(\d+)", re.I)
EDITORS = ("DaVinci Resolve", "EffectCraft", "FilmCraft", "AniCraft", "Resolve")
EMPTY = ("", "—", "–", "-", "n/a")
SLOT = "<!--slot:frame-->"
TOKENS_LINK = 'href="../../brand/src/design-system/tokens.css"'


@dataclass
class Board:
    """One board as boards shows it: its storyboard row, its first shot, and what it is drawn from."""
    row: K.Board
    shot: dict | None
    picture: str = "placeholder"     # card, still, frame, colour or placeholder
    source: object = None            # the card's HTML, the image or video file, or the colour
    framing: tuple = ("fit", None)
    label: str = ""                  # the tag laid over a frame of video
    reason: str = ""                 # why a placeholder
    cues: list = field(default_factory=list)
    seconds: float | None = None
    motion: list = field(default_factory=list)
    build: bool = False
    spoken: str = ""
    stills: list = field(default_factory=list)   # the main still, then each step's

    @property
    def id(self) -> str:
        return self.row.id

    @property
    def stem(self) -> str:
        return self.row.id.lower()


def cell(row: K.Board, n: int) -> str:
    return str(row.cells[n]).strip()


def board_seconds(text: str):
    """A Time cell's length in seconds, MM:SS–MM:SS (seconds may carry a fraction), or None."""
    m = TIME_RE.match(text or "")
    if not m:
        return None
    a = int(m.group(1)) * 60 + float(m.group(2))
    b = int(m.group(3)) * 60 + float(m.group(4))
    return b - a if b > a else None


def board_cues(text: str) -> list:
    """The On screen cell's cues: each TEXT: cue, or the whole cell as one; none for a dash."""
    text = (text or "").strip()
    if text in EMPTY:
        return []
    if TEXT_RE.search(text):
        parts = [p.strip(" ;·,") for p in TEXT_RE.split(text)[1:]]
        return [re.sub(r"<br\s*/?>", " ", p).strip() for p in parts if p.strip(" ;·,")]
    return [re.sub(r"\s*<br\s*/?>\s*", " ", text)]


def editor_named(text: str) -> str:
    """The outside editor an edited shot's Picture names (D93), or ''."""
    low = (text or "").lower()
    return next((e for e in EDITORS if e.lower() in low), "")


def shots_of(piece: str) -> list | None:
    """The shot-list rows as dicts keyed by lower-case header, or None where there is no shot list."""
    shot = C.path(C.PIECES) / piece / "shot-list.md"
    if not shot.is_file():
        return None
    headers, rows = R.shot_rows(shot)
    names = [h.strip().lower() for h in headers]
    return [{k: v.strip().strip("`").strip() for k, v in zip(names, cells)} for _, cells in rows]


def first_shot(board_id: str, shots: list):
    number = int(board_id[1:])
    for s in shots or []:
        if any(int(n) == number for n in re.findall(r"[Bb](\d+)", s.get("board", ""))):
            return s
    return None


def spoken_words(script, refs: str, notes: list, board_id: str) -> str:
    """The words a board's Spoken references name, as 'SPEAKER: words', one line each."""
    if refs.strip() in EMPTY:
        return "—"
    if script is None:
        return refs
    try:
        lines = K.select_lines(script, refs)
    except C.Fatal as err:
        notes.append(f"{board_id}: its Spoken '{refs}' names no line of the script ({err}); the sheet shows "
                     "the reference")
        return refs
    return "\n".join(f"{line.speaker}: {line.text}" for line in lines)


def unreadable(source: str, entries: dict) -> str:
    """Why boards will not open a shot's Source (DESIGN Section 6.3, D50), or '': a footage ID's
    manifest path must stay inside the footage folder, and any other path must sit under
    production/src/assets/ or production/src/cards/, relative, never through '..' or a link out."""
    if re.fullmatch(r"F\d{4,}", source):
        rel = Path(str((entries.get(source) or {}).get("path", "")))
        if source in entries and (rel.is_absolute() or ".." in rel.parts):
            return f"{source}'s manifest path leaves {C.FOOTAGE}/"
        return ""
    rel, folders = Path(source), (C.ASSETS, C.CARDS)
    inside = [f for f in folders if rel.parts[:len(Path(f).parts)] == Path(f).parts]
    if rel.is_absolute() or ".." in rel.parts or not inside:
        return f"{source} is no Source a shot may name (a footage ID, or a file under {C.ASSETS}/ or {C.CARDS}/)"
    if not C.path(rel.as_posix()).resolve().is_relative_to(C.path(inside[0]).resolve()):
        return f"{source} points outside {inside[0]}/"
    return ""


def choose(b: Board, piece: str, entries: dict) -> None:
    """Set b's picture, source, label and reason from its first shot (D92, D93)."""
    s, picture = b.shot, cell(b.row, 3)
    if s is None:
        b.reason = "no shot in the shot list names this board"
        return
    kind, source = s.get("type", "").lower(), s.get("source", "")
    framing = FRAMING_RE.match(s.get("framing", ""))
    if framing:
        b.framing = (framing.group(1).lower(), int(framing.group(2)) if framing.group(2) else None)
    if kind == "scene" or source.endswith(".scene.py"):
        b.reason = "a scene board: scene.py draws it, seen at M4 (its stills and preview)"
        return
    if source.lower() == "to shoot":
        b.reason = "to shoot"
        return
    if source.lower() == "to render" or (kind == "edited" and not re.fullmatch(r"F\d{4,}", source)):
        editor = editor_named(picture)
        b.reason = f"edited in {editor}, to render" if editor else "edited in an outside editor, to render"
        return
    if re.fullmatch(r"#[0-9a-fA-F]{6}", source):
        b.picture, b.source = "colour", source
        return
    if not source:
        b.reason = "the shot has no Source"
        return
    refused = unreadable(source, entries)
    if refused:
        b.reason = refused
        return
    r = V.resolve_source(source, entries)
    if r["kind"] == "missing":
        b.reason = f"{source} is not in the footage manifest"
        return
    path = r["path"]
    if r["kind"] == "card":
        if C.path(C.ASSETS).resolve() in path.resolve().parents:
            b.reason = f"a text capture ({source}): the scene or the edit shows it"
        elif not path.is_file():
            b.reason = f"the card's HTML {source} is not made yet (cut-for-platform makes it)"
        else:
            b.picture, b.source = "card", path
        return
    if not path.is_file():
        b.reason = (f"{source}'s file is not in this machine's footage mirror"
                    if re.fullmatch(r"F\d{4,}", source) else f"{source} is not in this project")
        return
    if path.suffix.lower() in (".txt", ".ansi"):
        b.reason = f"a text capture ({source}): the scene or the edit shows it"
        return
    if r["kind"] == "still":
        b.picture, b.source = "still", path
        return
    if not C.streams(C.probe(path), "video"):
        b.reason = f"{source} is sound only"
        return
    b.picture, b.source = "frame", path
    editor = editor_named(picture) if kind == "edited" else ""
    b.label = f"frame from {source}{f' ({editor} export)' if editor else ''} — the edit chooses the moment"


def edited(b: Board) -> bool:
    """An edited shot (D93): its motion is the outside editor's, so the animatic holds its picture."""
    return (b.shot or {}).get("type", "").lower() == "edited"


def plan(piece: str) -> tuple:
    """(boards, findings, notes, scene piece) from the piece's storyboard, shot list and script."""
    folder = C.path(C.PIECES) / piece
    board_path = folder / "storyboard.md"
    if not board_path.is_file():
        raise C.Fatal(f"{C.shown(board_path)} is missing: boards draws a storyboard, so board the piece first "
                      "(scripts/workflows/03-storyboard-a-piece/)")
    _, rows = K.read_storyboard(board_path)
    shots = shots_of(piece)
    findings, notes = [], []
    if shots is None:
        notes.append(f"{C.shown(folder / 'shot-list.md')} is missing: every board is a placeholder")
    script = K.read_script(folder / "script.md") if (folder / "script.md").is_file() else None
    if script is None:
        notes.append(f"{C.shown(folder / 'script.md')} is missing: the sheet shows Spoken as references")
    entries = V.manifest_entries()
    boards = []
    for row in rows:
        b = Board(row, first_shot(row.id, shots))
        choose(b, piece, entries)
        b.cues = board_cues(cell(row, 5))
        b.seconds = board_seconds(cell(row, 2))
        b.motion = sorted({m.lower().replace(" ", "-") for m in MOTION_RE.findall(cell(row, 3))})
        b.build = bool(BUILD_RE.search(cell(row, 3))) or len(b.cues) >= 2
        b.spoken = spoken_words(script, cell(row, 4), notes, row.id)
        if b.shot is None:
            findings.append(f"{b.id}: no shot in the shot list names this board (a placeholder is shown)")
        elif b.picture == "placeholder":
            findings.append(f"{b.id}: a placeholder is shown: {b.reason}")
        if b.seconds is None:
            findings.append(f"{b.id}: its Time {cell(row, 2)!r} cannot be read as MM:SS–MM:SS")
        if b.build and len(b.cues) < 2:
            notes.append(f"{b.id}: its Picture says build-up, and it has {len(b.cues)} On screen cue(s): it is "
                         "shown as one still")
        if {"pan", "zoom"} & set(b.motion) and not edited(b):
            notes.append(f"{b.id}: {' and '.join(m for m in b.motion if m in ('pan', 'zoom'))} is held still in the "
                         "animatic: assemble makes neither, so it is an edited shot made outside "
                         "(production/docs/reference/complex-shots.md)")
        boards.append(b)
    scene = any((s.get("type", "").lower() == "scene") for s in shots or [])
    return boards, findings, notes, scene


# ── the pages and the stills ────────────────────────────────────────────────────────────

def layout() -> str:
    """templates/board.html, its tokens.css link pointing at the brand's own by its full path
    (the scratch page sits elsewhere), or dropped, with a note, where the brand has none yet."""
    text = C.read_text(C.TOOLKIT / "templates" / "board.html")
    tokens = C.path(C.TOKENS)
    if tokens.is_file():
        return text.replace(TOKENS_LINK, f'href="{html.escape(tokens.resolve().as_uri())}"')
    return re.sub(r'<link rel="stylesheet" [^>]*tokens\.css">\n?', "", text)


def page(template: str, b: Board, picture, cues: list) -> str:
    """One board's page: its framed picture (a PNG at the size) or its placeholder, its label
    and the cues it shows."""
    e = html.escape
    parts = []
    if picture is not None:
        parts.append(f'<img class="picture" src="{e(Path(picture).resolve().as_uri())}" alt="">')
    else:
        parts.append(f'<div class="placeholder"><p class="board-id">{e(b.id)}</p>'
                     f'<p class="why">placeholder: {e(b.reason)}</p>'
                     f'<p class="what">{e(lines(cell(b.row, 3)))}</p></div>')
    if b.label:
        parts.append(f'<p class="label">{e(b.label)}</p>')
    if cues:
        parts.append('<div class="cues">' + "".join(f'<p class="cue">{e(c)}</p>' for c in cues) + "</div>")
    return template.replace(SLOT, "".join(parts))


def picture_png(b: Board, w: int, h: int, tmp: Path, made: dict, findings: list):
    """The board's picture as one PNG of w x h, or None for a placeholder (whose reason is set)."""
    if b.picture == "card":
        try:
            return V.card_png(b.source, w, h, transparent=False)
        except C.Finding as err:
            findings.append(f"{b.id}: card.py found problems in its card: {err}")
            return None
    if b.picture == "colour":
        return V.framed_still({"kind": "colour", "colour": b.source, "id": b.id}, w, h, tmp, made)
    if b.picture in ("still", "frame"):
        image = b.source
        if b.picture == "frame":
            image = tmp / f"source-{b.stem}.png"
            at = C.duration(C.probe(b.source)) / 10
            V.render(["-y", "-ss", f"{at:.3f}", "-threads", "1", "-i", str(b.source), "-frames:v", "1", "-update",
                      "1", str(image)], image, what=f"a frame for {b.id}")
        clip = {"frame": b.framing[0], "x": b.framing[1]}
        return V.framed_still({"kind": "still", "path": image, "info": C.probe(image, frame=True), "clip": clip,
                               "id": b.id}, w, h, tmp, made)
    return None


def render_page(text: str, name: str, w: int, h: int, tmp: Path, findings: list, b: Board) -> Path:
    """One still through card.py (DESIGN D20's uv route): exit 1 is a finding, exit 2 stops."""
    src = tmp / f"{name}.html"
    src.write_text(text, encoding="utf-8")
    out = tmp / f"{name}.png"
    proc = C.uv_script(C.TOOLKIT / "card.py", ["render", src, "--size", f"{w}x{h}", "-o", out],
                       timeout=V.CARD_TIMEOUT, cwd=C.ROOT,
                       hint="a first run fetches Playwright, which a slow network can delay; run "
                            "'python3 toolkit/media.py check --setup', then boards again")
    if proc.returncode == 1:
        said = [line.strip()[5:] for line in proc.stdout.splitlines() if line.strip().startswith("FAIL ")]
        findings += [f"{b.id}: card.py: {line}" for line in said or [proc.stdout.strip()]]
    elif proc.returncode != 0 or not out.is_file():
        raise C.Fatal(f"card.py could not render the board {b.id} (exit {proc.returncode}):\n"
                      f"{(proc.stderr or proc.stdout).strip()[-800:]}")
    return out


# ── the contact sheet ───────────────────────────────────────────────────────────────────

def vertical(text: str, w: int, h: int) -> tuple:
    """(the box's left and width as fractions of the frame, or None; what the sheet says)."""
    text = (text or "").strip()
    crop = round(h * VERTICAL[0] / VERTICAL[1])
    if crop >= w:
        return None, f"{text or '—'} (the master is no wider than 9:16: nothing is cropped)"
    m = CROP_RE.match(text)
    if m:
        x = int(m.group(1))
        held = min(x, w - crop)
        said = f"{text}: the 9:16 crop from x = {held} of {w}" + (
            f" (x = {x} runs past the frame's right edge, so the crop is held at {held})" if held != x else "")
        return (held / w, crop / w), said
    low = text.lower()
    if low.startswith("centre") or low.startswith("center"):
        return ((w - crop) / 2 / w, crop / w), f"{text}: the centred 9:16 crop"
    if low.startswith("pad"):
        return None, f"{text}: the whole picture, over a blurred copy, at 9:16"
    if low.startswith("native"):
        return None, f"{text}: a scene renders its vertical aspect itself"
    return None, f"{text or '—'} (no framing to draw)"


SHEET_CSS = """
  body { margin: 0; padding: 24px; background: Canvas; color: CanvasText; font-family: sans-serif; }
  h1 { font-size: 1.4rem; margin: 0 0 4px; }
  .note { margin: 0 0 20px; color: GrayText; }
  .board { margin: 0 0 32px; max-width: 960px; }
  .still { position: relative; line-height: 0; }
  .still img { width: 100%; height: auto; border: 1px solid GrayText; }
  .vertical { position: absolute; top: 0; bottom: 0; box-sizing: border-box; border: 3px dashed Highlight; }
  .steps { display: flex; gap: 8px; margin-top: 8px; }
  .steps img { width: 24%; height: auto; border: 1px solid GrayText; }
  figcaption dl { display: grid; grid-template-columns: max-content 1fr; gap: 2px 16px; margin: 8px 0 0; }
  figcaption dt { font-weight: bold; }
  figcaption dd { margin: 0; white-space: pre-line; }
  .placeholder { color: Mark; }
"""


def lines(text: str) -> str:
    """A table cell as the sheet shows it: a Markdown table's <br> as a line break (escaped later)."""
    return re.sub(r"\s*<br\s*/?>\s*", "\n", text)


def sheet(piece: str, boards: list, w: int, h: int, animatic) -> str:
    """The contact sheet: every still in board order, each captioned beneath, never over it."""
    e = html.escape
    out = ["<!doctype html>", '<html lang="en-GB">', "<head>", '<meta charset="utf-8">',
           f"<title>{e(piece)} — boards</title>", f"<style>{SHEET_CSS}</style>", "</head>", "<body>",
           f"<h1>{e(piece)} — boards at {w}x{h}</h1>",
           '<p class="note">Made by python3 toolkit/media.py boards before M3; never tracked. The dashed box is '
           "each board's Vertical framing at 9:16."
           + (f" The animatic: <a href=\"{e(animatic.name)}\">{e(animatic.name)}</a>." if animatic else "")
           + "</p>"]
    for b in boards:
        box, framed = vertical(cell(b.row, 7), w, h)
        motion = ", ".join(b.motion) + (" · build-up" if b.build else "") if b.motion or b.build else "—"
        main = b.stills[0].name if b.stills else ""
        out.append(f'<figure class="board" id="{e(b.stem)}">')
        out.append(f'<div class="still"><img src="{e(main)}" alt="{e(b.id)}">'
                   + (f'<div class="vertical" style="left: {box[0] * 100:.2f}%; width: {box[1] * 100:.2f}%">'
                      "</div>" if box else "") + "</div>")
        if len(b.stills) > 1:
            out.append('<div class="steps">' + "".join(f'<img src="{e(s.name)}" alt="{e(b.id)} step {k}">'
                                                       for k, s in enumerate(b.stills[1:], start=1)) + "</div>")
        shown = {"card": "the card's own render (its words are the card's)", "still": "the image, framed",
                 "frame": b.label, "colour": f"the colour {b.source}"}.get(b.picture, "")
        rows = [("Board", f"{b.id} · beat {b.row.beat}"), ("Time", cell(b.row, 2)), ("Spoken", b.spoken),
                ("Picture", lines(cell(b.row, 3))), ("On screen", lines(cell(b.row, 5))),
                ("Sound", lines(cell(b.row, 6))),
                ("Motion", motion), ("Vertical framing", framed),
                ("Shown", shown if b.picture != "placeholder" else f"placeholder: {b.reason}")]
        out.append("<figcaption><dl>" + "".join(
            f"<dt>{e(k)}</dt><dd{' class=\"placeholder\"' if k == 'Shown' and b.picture == 'placeholder' else ''}>"
            f"{e(v)}</dd>" for k, v in rows) + "</dl></figcaption>")
        out.append("</figure>")
    out += ["</body>", "</html>", ""]
    return "\n".join(out)


# ── the animatic ────────────────────────────────────────────────────────────────────────

def rel(p: Path) -> str:
    p = Path(p).resolve()
    root = C.ROOT.resolve()
    return p.relative_to(root).as_posix() if p.is_relative_to(root) else str(p)


def animatic_toml(piece: str, boards: list, w: int, h: int, sound, notes: list) -> str:
    """The animatic's working-copy edit decision list: every board a still clip lasting its Time."""
    q = json.dumps
    lines = ["# The animatic of python3 toolkit/media.py boards: a working copy, never tracked and never",
             "# the master's edit decision list (that is production/src/edits/<piece>.toml).",
             "[edit]", f"piece = {q(piece)}", f'size = "{w}x{h}"', 'loudness = "none"', ""]
    before = None
    for b in boards:
        moves = [] if edited(b) else b.motion
        seconds = b.seconds
        if seconds is None:
            seconds = HELD_SECONDS
            notes.append(f"{b.id}: held {HELD_SECONDS:g} s in the animatic, its Time unread")
        steps = b.stills[1:] if len(b.stills) > 1 else b.stills[:1]
        each = seconds / len(steps)
        for k, still in enumerate(steps):
            length = each
            clip = ["[[clip]]", f'id = "{b.stem}{f"k{k + 1}" if len(steps) > 1 else ""}"',
                    f"source = {q(rel(still))}"]
            if k == 0 and "fade" in moves and before is not None:
                fade = round(min(FADE_SECONDS, before / 2, each / 2), 3)
                length += fade
                clip += ['transition = "fade"', f"transition_seconds = {fade:g}"]
            if "push-in" in moves and len(steps) == 1:
                clip.append('motion = "push-in"')
            clip.append(f"seconds = {round(length, 6):g}")
            lines += clip + [""]
            before = each
        if "push-in" in moves and len(steps) > 1:
            notes.append(f"{b.id}: a push-in over a build-up is shown as its steps, without the push-in")
    if sound is not None:
        lines += ["[[audio]]", f"source = {q(rel(sound))}", 'role = "voice"', ""]
    return "\n".join(lines)


# ── the command ─────────────────────────────────────────────────────────────────────────

def animatic_sound(piece: str, sound):
    """The animatic's sound: --sound, else the joined voice where it already exists, else None."""
    if sound is not None:
        return sound
    voice = C.piece_folder(C.PROD_RENDERS, piece) / f"{piece}.voice.wav"
    return voice if voice.is_file() else None


def board_size(piece: str, given):
    """(w, h, where it came from): --size, else the edit decision list's [edit] size, else 1920x1080."""
    if given:
        size = V.parse_size(given)
        return size[0], size[1], "--size"
    edl = C.path(C.EDITS) / f"{piece}.toml"
    if edl.is_file():
        size = V.parse_size(str((C.load_toml(edl).get("edit") or {}).get("size", "") or ""))
        if size:
            return size[0], size[1], C.shown(edl)
    return DEFAULT_SIZE[0], DEFAULT_SIZE[1], "the default"


def cmd_boards(args) -> int:
    piece = R.piece_name(args.piece, "PIECE")
    boards, findings, notes, scene = plan(piece)
    w, h, said = board_size(piece, args.size)
    sound = Path(args.sound) if args.sound else None
    if sound is not None and not sound.is_file():
        raise C.Fatal(f"--sound {C.shown(sound)} is not found")
    for tool in ("ffmpeg", "ffprobe", "uv"):
        C.need(tool)
    moving = [b for b in boards if b.motion or b.build]
    animate = bool(moving) and not args.no_animatic and not scene
    print(f"boards {piece}: {len(boards)} board(s) at {w}x{h} ({said})"
          + ("; a scene piece, so no animatic (its motion is seen at M4)" if scene and moving else ""))
    folder = C.piece_folder(C.PROD_RENDERS, piece, "boards")
    template = layout()
    if not C.path(C.TOKENS).is_file():
        notes.append(f"{C.TOKENS} is missing: the boards use the browser's own colours and faces")
    with tempfile.TemporaryDirectory(prefix="media-boards-") as tmp:
        tmp, made = Path(tmp), {}
        for b in boards:
            picture = picture_png(b, w, h, tmp, made, findings)
            if picture is None and b.picture != "placeholder":
                b.picture, b.reason = "placeholder", b.reason or "its card did not render"
            cues = [] if b.picture == "card" else b.cues
            name = f"{piece}.{b.stem}.board.{w}x{h}"
            b.stills = [render_page(page(template, b, picture, cues), name, w, h, tmp, findings, b)]
            if b.build and len(b.cues) >= 2 and b.picture != "card":
                for k in range(1, len(b.cues) + 1):
                    step = f"{piece}.{b.stem}.board.k{k}.{w}x{h}"
                    b.stills.append(render_page(page(template, b, picture, b.cues[:k]), step, w, h, tmp,
                                                findings, b))
        folder.mkdir(parents=True, exist_ok=True)
        for old in [*folder.glob(f"{piece}.b*.board.*png"), *(folder / f"{piece}.{n}" for n in
                    ("boards.html", "animatic.toml", "animatic.mp4"))]:
            if old.is_file():
                old.unlink()
        for b in boards:
            b.stills = [Path(shutil.move(str(s), folder / s.name)) for s in b.stills]
    for b in boards:
        for s in b.stills:
            print(f"wrote {C.shown(s)}")
    animatic = None
    contact = folder / f"{piece}.boards.html"
    contact.write_text(sheet(piece, boards, w, h, None), encoding="utf-8")   # kept should assemble stop
    if animate:
        heard = animatic_sound(piece, sound)
        edl = folder / f"{piece}.animatic.toml"
        edl.write_text(animatic_toml(piece, boards, w, h, heard, notes), encoding="utf-8")
        print(f"wrote {C.shown(edl)} (the animatic's working edit list; sound: "
              f"{C.shown(heard) if heard else 'none, so it is silent'})")
        animatic = folder / f"{piece}.animatic.mp4"
        try:
            code = V.cmd_assemble(argparse.Namespace(edl=str(edl), o=str(animatic), memory_max=None))
        except C.Finding as err:
            print(f"  FAIL {err}")
            code = 1
        if code != 0:
            findings.append(f"the animatic's assemble exited {code} (its findings are above)")
        if not animatic.is_file():
            animatic = None
    elif moving and args.no_animatic:
        notes.append("--no-animatic: the boards that move or build up are seen as stills only")
    contact.write_text(sheet(piece, boards, w, h, animatic), encoding="utf-8")
    print(f"wrote {C.shown(contact)} (the contact sheet: the author opens it in a browser)")
    if animatic:
        print(f"wrote {C.shown(animatic)} (the animatic: the author plays it)")
    for note in notes:
        print(f"  note: {note}")
    for finding in findings:
        print(f"  FAIL {finding}")
    stills = sum(len(b.stills) for b in boards)
    print(f"boards {piece}: {stills} still(s), {len(findings)} finding(s); open each still by the path printed")
    return 1 if findings else 0
