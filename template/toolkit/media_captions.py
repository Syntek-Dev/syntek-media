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

Timing routes (DESIGN D22): from-words uses each cue's first and last aligned word and reports
short gaps without trimming a spoken word; from-segments spreads each approved segment's probed
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

transcript writes the published transcript of a piece, or with --lines of one cut's lines (the
same lines align --lines takes), for <piece>[--cNN].transcript.en-GB.md (DESIGN D60): the
spoken words as the script or transcript spells them, one sentence per line, a paragraph per
beat; speaker names, bold, only where two or more people speak (VO, ON and NARRATOR are the
piece's one voice); a TEXT cue as [On screen: …], an SFX or MUSIC cue as a bracketed sound in
lower case; NOTE cues and braced directions dropped; and 'As recorded on DD/MM/YYYY' from
--date or, for a recorded piece's transcript.md, its recording's recorded date in the
manifest. What the picture shows and the words leave out is added by hand.

Where the output goes: from-words and from-segments write to publishing/src/renders/<piece>/ unless
-o names a path; align, retime, rewrap, vtt and transcript write to the path -o names, or else to
stdout, with every report line on stderr, because their files belong in the tracked
publishing/src/captions/, where the toolkit never chooses a path itself. burn writes its render
to the piece's publishing/src/renders/<piece>/ too. The piece is the leading NNN-kebab-title of
the output's name; a name with none stays at the top of publishing/src/renders/ (DESIGN D64).

script time reads each beat heading's '(target MM:SS)' as that beat's own duration, never a
running time: it compares every beat with its own target, sums the beat targets for the piece,
and judges the total against the brief's target_seconds (within 10%) and every deliverable's
max_seconds. The pace is --wpm, else the brief's words_per_minute, else 150.

Standard library only; Python 3.11+.
"""
from __future__ import annotations

import difflib
import json
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


@dataclass
class Board:
    id: str
    beat: int
    cells: list       # the storyboard's nine cells, a missing Timing notes cell filled with a dash


def read_storyboard(p: Path) -> tuple:
    """Read either storyboard table shape without changing its text (DESIGN Section 6.3)."""
    lines = C.read_text(p).splitlines()
    first, last = C.find_table(lines, ('#', 'Beat'))
    if first is None:
        raise C.Fatal(f'{C.shown(p)} needs a storyboard table beginning with # and Beat')
    headers = C.split_row(lines[first])
    expected = ['#', 'Beat', 'Time', 'Picture', 'Spoken', 'On screen', 'Sound', 'Vertical framing']
    if [h.lower() for h in headers] not in ([h.lower() for h in expected],
                                         [h.lower() for h in expected + ['Timing notes']]):
        raise C.Fatal('storyboard needs its eight columns, with an optional ninth Timing notes column')
    boards, seen = [], set()
    for number in range(first + 2, last + 1):
        cells = C.split_row(lines[number])
        if len(cells) != len(headers):
            raise C.Fatal(f'{C.shown(p)}:{number + 1}: storyboard row has the wrong number of cells')
        if not re.fullmatch(r'B[0-9]{2,}', cells[0]) or int(cells[0][1:]) < 1:
            raise C.Fatal(f'{C.shown(p)}:{number + 1}: board ID must be B01 or later')
        if cells[0] in seen:
            raise C.Fatal(f'{C.shown(p)}:{number + 1}: duplicate board {cells[0]}')
        if not re.fullmatch(r'[0-9]+', cells[1]) or int(cells[1]) < 1:
            raise C.Fatal(f'{C.shown(p)}:{number + 1}: board Beat must be a positive script beat number')
        seen.add(cells[0])
        boards.append(Board(cells[0], int(cells[1]), cells + (['—'] if len(cells) == 8 else [])))
    if not boards:
        raise C.Fatal('the storyboard table holds no boards')
    return expected + ['Timing notes'], boards


def match_script_words(script: Script, rows: list) -> tuple:
    """Map aligned word indices to spoken script lines; report every sequence disagreement.

    Normalisation is the caption checker's: punctuation and case do not change a word,
    hyphen parts retain their one original word index, and repeated words stay in order.
    This computes associations only; the owning command decides how to print/store them.
    """
    if not isinstance(rows, list):
        raise C.Fatal('the words file must hold an array of word rows')
    expected, line_of, heard, index_of = [], [], [], []
    indices = {f'{line.beat}.{line.n}': [] for line in script.lines}
    findings = []
    for line in script.lines:
        tokens = words_of(line.text)
        expected.extend(tokens)
        line_of.extend([f'{line.beat}.{line.n}'] * len(tokens))
    for index, row in enumerate(rows):
        if not isinstance(row, dict) or not isinstance(row.get('word'), str) \
                or len(row['word'].split()) != 1:
            raise C.Fatal('every words row needs one spoken word as text')
        if any(char in row['word'] for char in '{}[]'):
            raise C.Finding('a direction or audio tag cannot be a timed word')
        tokens = words_of(row['word'])
        if not tokens:
            findings.append(f'word {index}: {row["word"]!r} has no spoken letters')
        heard.extend(tokens)
        index_of.extend([index] * len(tokens))
    matching = difflib.SequenceMatcher(None, expected, heard, autojunk=False)
    for operation, a0, a1, b0, b1 in matching.get_opcodes():
        if operation == 'equal':
            for a, b in zip(range(a0, a1), range(b0, b1)):
                line = line_of[a]
                if index_of[b] not in indices[line]:
                    indices[line].append(index_of[b])
        else:
            if a0 != a1:
                affected = ', '.join(dict.fromkeys(line_of[a0:a1]))
                findings.append(f'script lines {affected}: words not matched: ' + ' '.join(expected[a0:a1]))
            if b0 != b1:
                findings.append('aligned words not in the script at this position: ' + ' '.join(heard[b0:b1]))
    return indices, findings


def cue_words(source: Path) -> tuple:
    """Read alignment rows without inventing timings for missing or untimed words."""
    def reject_constant(value):
        raise ValueError(f'non-finite JSON number {value}')

    try:
        rows = json.loads(C.read_text(source), parse_constant=reject_constant)
    except ValueError:
        raise C.Fatal(f'{C.shown(source)} is not a words JSON file') from None
    if not isinstance(rows, list) or not rows:
        raise C.Finding('the words file holds no words')
    findings, previous = [], None
    for index, row in enumerate(rows):
        if not isinstance(row, dict) or not all(key in row for key in ('word', 'start', 'end', 'score', 'segment')):
            raise C.Fatal('every words row needs word, start, end, score and segment')
        if not isinstance(row['word'], str) or len(row['word'].split()) != 1 or not row['segment']:
            raise C.Fatal('every words row needs one spoken word and its segment')
        score = row['score']
        if score is not None and (isinstance(score, bool) or not isinstance(score, (int, float))
                                  or not math.isfinite(score) or not 0 <= score <= 1):
            raise C.Fatal('word scores must be null or finite numbers between zero and one')
        a, b = row['start'], row['end']
        for value in (a, b):
            if value is not None and (isinstance(value, bool) or not isinstance(value, (int, float))
                                      or not math.isfinite(value) or value < 0):
                raise C.Fatal('word times must be null or finite nonnegative seconds')
        if a is None or b is None:
            findings.append(f'word {index} {row["word"]!r} is untimed')
        elif b <= a:
            raise C.Fatal('every timed word must end after it starts')
        else:
            if previous is not None and a < previous:
                findings.append(f'word {index} overlaps or runs backwards')
            previous = b
    return rows, findings


def cue_span(indices: list, words: list) -> tuple:
    if not indices or any(words[i]['start'] is None or words[i]['end'] is None for i in indices):
        return None, None
    return min(words[i]['start'] for i in indices), max(words[i]['end'] for i in indices)


def build_cues(piece: str, script: Script, boards: list, rows: list) -> tuple:
    """The approved separate lists; each original aligned word appears exactly once."""
    indices, findings = match_script_words(script, rows)
    words = [dict(row, line=None) for row in rows]
    lines, by_line = [], {}
    for line in script.lines:
        key = f'{line.beat}.{line.n}'
        chosen = indices[key]
        complete = (words_of(line.text) == [token for i in chosen for token in words_of(rows[i]['word'])])
        start, end = cue_span(chosen, rows) if complete else (None, None)
        item = dict(id=key, beat=line.beat, word_indices=chosen, start=start, end=end)
        lines.append(item)
        by_line[key] = item
        for i in chosen:
            if words[i]['line'] is not None:
                findings.append(f'word {i} belongs to more than one script line')
            else:
                words[i]['line'] = key
        if start is None:
            findings.append(f'line {key} cannot be fully timed')
    for i, word in enumerate(words):
        if word['line'] is None:
            findings.append(f'word {i} has no script line')
    beats = []
    for number, title, _kind, _target in script.beats:
        selected = [line for line in lines if line['beat'] == number]
        complete = bool(selected) and all(line['start'] is not None for line in selected)
        beats.append(dict(id=number, title=title, lines=[line['id'] for line in selected],
                          start=min(line['start'] for line in selected) if complete else None,
                          end=max(line['end'] for line in selected) if complete else None))
    timed_boards = []
    for board in boards:
        references, complete = [], True
        try:
            selected = select_lines(script, board.cells[4])
            if not board.cells[4].strip():
                raise C.Fatal('Spoken references are empty')
            limits = re.fullmatch(r'\s*(\d+)\.(\d+)\s*(?:[-–]\s*(\d+)\.(\d+)\s*)?', board.cells[4])
            first = f'{int(limits[1])}.{int(limits[2])}'
            last = f'{int(limits[3])}.{int(limits[4])}' if limits[3] else first
            references = [f'{line.beat}.{line.n}' for line in selected]
            complete = (references[0] == first and references[-1] == last
                        and any(line.beat == board.beat for line in selected)
                        and all(by_line[key]['start'] is not None for key in references))
        except C.Fatal as exc:
            findings.append(f'board {board.id}: {exc}')
            complete = False
        timed_boards.append(dict(id=board.id, beat=board.beat, spoken=board.cells[4],
                                timing_notes=board.cells[8], lines=references,
                                start=min(by_line[key]['start'] for key in references) if complete else None,
                                end=max(by_line[key]['end'] for key in references) if complete else None))
        if not complete:
            findings.append(f'board {board.id} cannot be matched to fully timed script lines')
    return dict(piece=piece, beats=beats, boards=timed_boards, lines=lines, words=words, events=[]), findings


def retimed_table(headers: list, boards: list, timed: list) -> str:
    """MM:SS contains the spoken interval; JSON retains the exact seconds."""
    def mmss(seconds):
        return f'{seconds // 60:02d}:{seconds % 60:02d}'

    def row(cells):
        return '| ' + ' | '.join(str(cell).replace('|', '\\|') for cell in cells) + ' |'

    lines = [row(headers), row(['---'] * len(headers))]
    for board, timing in zip(boards, timed):
        cells = list(board.cells)
        a, b = timing['start'], timing['end']
        cells[2] = f'{mmss(math.floor(a))}–{mmss(math.ceil(b))}' if a is not None else '—'
        lines.append(row(cells))
    return '\n'.join(lines)


def script_events(script: Script, data: dict) -> tuple:
    """Preserve instructions at their source positions, without aligning them as spoken words."""
    _, body, _ = C.split_frontmatter(C.read_text(script.path))
    line_map = {line['id']: line for line in data['lines']}
    events, findings, beat, number = [], [], 0, 0
    for source_line, raw in enumerate(body.splitlines(), start=1):
        text = raw.strip()
        heading = BEAT_RE.match(text)
        if heading:
            beat, number = int(heading[1]), 0
            continue
        if text.startswith('## '):
            beat, number = 0, 0
            continue
        tagged = SPEAKER_RE.match(text)
        if not tagged:
            continue
        tag, content = tagged[1], tagged[2]
        if tag in ('SFX', 'MUSIC'):
            events.append(dict(id=f'e{len(events) + 1:02d}', kind='sfx' if tag == 'SFX' else 'music',
                               instruction=content, beat=beat, source_line=source_line,
                               script_line=None, anchor=None, start=None, end=None, source=None, mix=None))
        elif tag not in CUE_TAGS:
            spoken = re.sub(r'\s+', ' ', BRACE_RE.sub(' ', content)).strip()
            if not spoken and not PAUSE_RE.findall(content):
                continue
            number += 1
            key = f'{beat}.{number}'
            timed = line_map.get(key)
            flattened = [i for i in (timed['word_indices'] if timed else [])
                         for _token in words_of(data['words'][i]['word'])]
            for direction in BRACE_RE.finditer(content):
                before = len(words_of(BRACE_RE.sub(' ', content[:direction.start()])))
                anchor = None
                if flattened and timed['start'] is not None:
                    index = flattened[min(before, len(flattened) - 1)]
                    edge = 'start' if before < len(flattened) else 'end'
                    anchor = dict(kind='word', word=index, edge=edge, time=data['words'][index][edge])
                event = dict(id=f'e{len(events) + 1:02d}', kind='delivery',
                             instruction=direction[0][1:-1].strip(), beat=beat,
                             source_line=source_line, script_line=key, anchor=anchor)
                events.append(event)
                if anchor is None:
                    findings.append(f'event {event["id"]} has no timed word anchor in line {key}')
    return events, findings


def bind_audio_events(piece: str, events: list, edl: dict, entries: dict) -> list:
    """Resolve approved cue links from tracked audio rows and manifest metadata only."""
    findings, links = [], {}
    by_id = {event['id']: event for event in events}
    tracks = edl.get('audio', [])
    if not isinstance(tracks, list) or any(not isinstance(track, dict) for track in tracks):
        raise C.Fatal('the edit needs [[audio]] rows')
    for index, track in enumerate(tracks):
        cue = str(track.get('cue', '')).strip()
        if not cue:
            continue
        if cue not in by_id or by_id[cue]['kind'] == 'delivery':
            findings.append(f'audio row {index + 1}: cue {cue!r} is not a sound or music event')
        links.setdefault(cue, []).append((index, track))
    sounds = [event for event in events if event['kind'] != 'delivery']
    if not sounds:
        return findings
    voices = [track for track in tracks if track.get('source') == f'vo:{piece}']
    if len(voices) != 1:
        return findings + ['sound/music cues need exactly one vo:<piece> audio row to locate the joined voice']

    def seconds(value, label):
        result = C.parse_tc(value, label)
        if not math.isfinite(result) or result < 0:
            raise C.Fatal(f'{label} must be finite nonnegative seconds')
        return result

    offset = seconds(voices[0].get('at') or 0, 'voice at')
    for event in sounds:
        linked = links.get(event['id'], [])
        if len(linked) != 1:
            findings.append(f'event {event["id"]}: needs exactly one audio row with cue = {event["id"]!r}')
            continue
        index, track = linked[0]
        role = 'effect' if event['kind'] == 'sfx' else 'music'
        source = str(track.get('source', ''))
        entry = entries.get(source)
        if track.get('role') != role or entry is None or entry.get('kind') == 'image':
            findings.append(f'event {event["id"]}: needs role = {role!r} and a logged sound footage ID')
            continue
        duration = entry.get('duration')
        if isinstance(duration, bool) or not isinstance(duration, (int, float)) \
                or not math.isfinite(duration) or duration <= 0:
            findings.append(f'event {event["id"]}: source {source} has no finite sound duration')
            continue
        at = seconds(track.get('at') or 0, f'{event["id"]} at')
        a = seconds(track.get('in') or 0, f'{event["id"]} in')
        b = seconds(track['out'], f'{event["id"]} out') if track.get('out') else duration
        if b <= a or b > duration:
            findings.append(f'event {event["id"]}: its source range is outside {source}')
            continue
        mix = dict(role=role, gain_db=track.get('gain_db', 0), fade_in=track.get('fade_in', 0),
                   fade_out=track.get('fade_out', 0), duck=track.get('duck', False),
                   source_in=a, source_out=b, master_at=at)
        for field in ('gain_db', 'fade_in', 'fade_out'):
            value = mix[field]
            if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) \
                    or (field != 'gain_db' and value < 0):
                raise C.Fatal(f'event {event["id"]}: {field} must be a finite number, fades nonnegative')
        if not isinstance(mix['duck'], bool) or (mix['duck'] and role != 'music'):
            raise C.Fatal(f'event {event["id"]}: duck must be boolean and only ducks music')
        start, end = at - offset, at - offset + b - a
        if not math.isfinite(start) or not math.isfinite(end):
            raise C.Fatal(f'event {event["id"]}: the derived interval must be finite')
        event.update(source=source, anchor=dict(kind='audio', row=index, voice_offset=offset),
                     start=start, end=end, mix=mix)
    return findings


def cmd_cues(args) -> int:
    piece = str(args.piece)
    if not piece or C.piece_key(piece) != piece:
        raise C.Fatal('cues needs PIECE (NNN-kebab-title)')
    folder = C.path(C.PIECES) / piece
    script_path, board_path = folder / 'script.md', folder / 'storyboard.md'
    words_path = C.path(C.TIMING) / f'{piece}.words.json'
    edl_path = C.path(C.EDITS) / f'{piece}.toml'
    manifest_path = C.path(C.MANIFEST)
    inputs = [script_path, board_path, words_path, edl_path, manifest_path]
    default = C.piece_folder(C.PROD_RENDERS, piece, 'timing') / f'{piece}.cues.json'
    out = C.output_path(default, args.o, inputs=inputs, tracked_timing=(piece, 'cues.json'))
    script = read_script(script_path)
    headers, boards = read_storyboard(board_path)
    words, findings = cue_words(words_path)
    data, matching = build_cues(piece, script, boards, words)
    findings.extend(matching)
    data['events'], event_findings = script_events(script, data)
    findings.extend(event_findings)
    edl = C.load_toml(edl_path) if edl_path.is_file() else {}
    if edl and edl.get('edit', {}).get('piece') != piece:
        raise C.Fatal('the cue audio list belongs to another piece')
    entries = {str(row.get('id')): row for row in C.load_toml(manifest_path).get('file', [])} \
        if manifest_path.is_file() else {}
    findings.extend(bind_audio_events(piece, data['events'], edl, entries))
    print(retimed_table(headers, boards, data['boards']))
    for board in data['boards']:
        if board['start'] is not None:
            print(f'{board["id"]}: exact start={board["start"]} end={board["end"]}; '
                  f'Seconds={board["end"] - board["start"]}')
    for event in data['events']:
        print(f'{event["id"]} {event["kind"]}: {event["instruction"]}; '
              f'anchor={event["anchor"]}; source={event.get("source")}')
    out = C.output_path(default, args.o, inputs=inputs, tracked_timing=(piece, 'cues.json'))
    C.replace_file(out, (json.dumps(data, indent=2, ensure_ascii=False, allow_nan=False) + '\n').encode('utf-8'))
    print(f'wrote {C.shown(out)}')
    return report(findings, 'cues')


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


def keep_gaps(cues: list, preserve_words: bool = False) -> list:
    """Cues in time order with the house gap between them. A cue the gap would leave with no
    length (it starts at or after the next cue's start, less the gap) is merged into the next,
    its words first, so no cue ends before it starts and no word is lost; captions check then
    judges the merged cue's lines and reading speed."""
    cues.sort(key=lambda c: c.start)
    if preserve_words:
        # D22's word boundaries take priority: check_cues reports any short gap.
        return cues
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
    """Where a caption file named name goes without -o: its piece's publishing/src/renders/<piece>/,
    or the folder's top for a name with no piece key (DESIGN D64, Section 6.16)."""
    return C.piece_folder(C.PUB_RENDERS, name) / name


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


def cmd_from_words(args) -> int:
    source = Path(args.words)
    try:
        rows = json.loads(C.read_text(source))
    except ValueError:
        raise C.Fatal(f'{C.shown(source)} is not a words JSON file') from None
    if not isinstance(rows, list) or not rows:
        raise C.Finding('the words file holds no words')
    width = width_for(C.preset(args.deliverable))
    offset = C.parse_tc(args.offset) if args.offset else 0.0
    groups, previous = [], None
    for row in rows:
        if not isinstance(row, dict) or not str(row.get('word', '')).strip() or not row.get('segment') \
                or 'score' not in row:
            raise C.Fatal('every words row needs word, start, end, score and segment')
        if any(char in str(row['word']) for char in '{}[]'):
            raise C.Finding('a direction or audio tag cannot reach captions from words')
        a, b = row.get('start'), row.get('end')
        if a is None or b is None:
            raise C.Finding(f"untimed word {row['word']!r}; fix the words check before making captions")
        score = row['score']
        if not isinstance(score, (int, float)) or isinstance(score, bool) or not math.isfinite(score) \
                or not 0 <= score <= 1:
            raise C.Fatal('every timed word needs a finite score between zero and one')
        if any(not isinstance(v, (int, float)) or isinstance(v, bool) or not math.isfinite(v)
               for v in (a, b)) or a < 0 or b <= a:
            raise C.Fatal('every word needs finite, increasing start/end times')
        if previous is not None and a < previous:
            raise C.Finding('word times overlap or run backwards')
        previous = b
        if not groups or groups[-1][0]['segment'] != row['segment']:
            groups.append([])
        groups[-1].append(row)
    cues = []
    for group in groups:
        chunks = chunk_text(' '.join(row['word'] for row in group), width)
        cursor = 0
        for chunk in chunks:
            # Original words preserve punctuation; chunk_text may only split between them.
            chosen = []
            while cursor + len(chosen) < len(group):
                chosen.append(group[cursor + len(chosen)])
                if ' '.join(row['word'] for row in chosen) == chunk:
                    break
            if not chosen or ' '.join(row['word'] for row in chosen) != chunk:
                raise C.Fatal('caption chunking changed the word sequence; nothing written')
            cue = Cue(chosen[0]['start'] + offset, chosen[-1]['end'] + offset, as_cue_lines(chunk, width))
            cues.append(cue)
            cursor += len(chosen)
        if cursor != len(group):
            raise C.Fatal('caption chunking left words out; nothing written')
    piece = C.piece_of(source)
    out = C.output_path(default_srt(f'{piece}.{C.file_form(args.deliverable)}.en-GB.srt'), args.o,
                        inputs=[source])
    keep_gaps(cues, preserve_words=True)
    write_out(out, srt_text(cues))
    print(f'{len(cues)} cue(s) from word boundaries; alignment times are estimates')
    return report(check_cues(cues, width), 'captions from-words')


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


# ── The published transcript (DESIGN D60, Section 6.9) ──────────────────────────────────

ONE_VOICE = {"VO", "ON", "NARRATOR"}   # delivery tags of the piece's own voice: one speaker, not three


@dataclass
class Element:
    beat: int
    kind: str          # 'line' (spoken, numbered as read_script numbers it) or 'cue'
    tag: str
    text: str
    n: int = 0


def script_elements(p) -> tuple:
    """(H1 title, beats, elements) of a script or transcript, in reading order: spoken lines
    numbered exactly as read_script numbers them (so --lines names the same lines as captions
    align --lines), and the TEXT, SFX and MUSIC cues between them; NOTE cues and braced
    directions dropped."""
    _, body, _ = C.split_frontmatter(C.read_text(p))
    title, beats, out, beat, n = "", [], [], 0, 0
    for raw in body.splitlines():
        stripped = raw.strip()
        if not title and stripped.startswith("# "):
            title = re.sub(r"\s+—\s+(script|transcript)\s*$", "", stripped[2:]).strip()
            continue
        m = BEAT_RE.match(stripped)
        if m:
            beat, n = int(m.group(1)), 0
            beats.append(beat)
            continue
        if stripped.startswith("## "):
            beat, n = 0, 0
            continue
        s = SPEAKER_RE.match(stripped)
        if not s:
            continue
        tag = s.group(1)
        if tag == "NOTE":
            continue
        text = re.sub(r"\s+", " ", BRACE_RE.sub(" ", s.group(2))).strip()
        if tag in CUE_TAGS:
            if text:
                out.append(Element(beat, "cue", tag, text))
            continue
        pause = PAUSE_RE.findall(s.group(2))
        if not text and not pause:
            continue
        n += 1
        out.append(Element(beat, "line", tag, text, n))
    return title, beats, out


def speaker_name(tag: str) -> str:
    return "Narrator" if tag in ONE_VOICE else " ".join(w.capitalize() for w in tag.split())


def recorded_date(p: Path, meta: dict) -> str:
    """For a recorded piece's transcript.md: its recording's recorded date in the manifest."""
    fid = str(meta.get("source", "") or "").strip()
    manifest = C.path(C.MANIFEST)
    if not fid or not manifest.is_file():
        return ""
    for row in C.load_toml(manifest).get("file", []):
        if str(row.get("id", "")) == fid:
            return str(row.get("recorded", "") or "").strip()
    return ""


def cmd_transcript(args) -> int:
    src = Path(args.text)
    script = read_script(src)
    chosen = {(ln.beat, ln.n) for ln in select_lines(script, args.lines)}
    title, _, elements = script_elements(src)
    spoken = [i for i, e in enumerate(elements) if e.kind == "line" and (e.beat, e.n) in chosen]
    if not spoken:
        raise C.Fatal(f"{C.shown(src)} has no spoken line to transcribe")
    # The whole piece keeps every cue; one cut's lines keep the cues between its first and last line.
    first, last = (spoken[0], spoken[-1]) if args.lines else (0, len(elements) - 1)
    keep = [e for i, e in enumerate(elements) if first <= i <= last
            and (e.kind == "cue" or (e.beat, e.n) in chosen) and (e.kind == "cue" or e.text)]
    voices = {speaker_name(e.tag) for e in keep if e.kind == "line"}
    labelled = len(voices) > 1
    meta = script.meta
    date = ""
    if args.date:
        date = C.parse_date(args.date).strftime("%d/%m/%Y")
    elif meta.get("source"):
        date = recorded_date(src, meta)
        try:
            date = C.parse_date(date).strftime("%d/%m/%Y") if date else ""
        except C.Fatal:
            date = ""
        if not date:
            note(f"  note: the manifest gives no recorded date for {meta.get('source')}: pass --date DD/MM/YYYY "
                 "for the 'As recorded on' line")
    head = f"# {title or script.meta.get('piece', src.stem)} — transcript"
    if args.lines:
        head += f" (lines {args.lines.strip()})"
    out = [head, ""]
    if date:
        out += [f"As recorded on {date}.", ""]
    para, beat, speaker = [], None, None
    for e in keep:
        if e.beat != beat and para:
            out += para + [""]
            para, speaker = [], None
        beat = e.beat
        if e.kind == "cue":
            para.append(f"[On screen: {e.text}]" if e.tag == "TEXT" else f"[{e.text.lower()}]")
            continue
        who = speaker_name(e.tag)
        if labelled and who != speaker:
            if para:
                out += para + [""]
                para = []
            para.append(f"**{who}:** {e.text}")
        else:
            para.append(e.text)
        speaker = who
    if para:
        out += para
    text = "\n".join(out).rstrip("\n") + "\n"
    emit(text, args.o, inputs=[src])
    words = sum(count_words(e.text) for e in keep if e.kind == "line")
    note(f"captions transcript {C.shown(src)}: {sum(1 for e in keep if e.kind == 'line')} spoken line(s), {words} "
         f"words{', ' + str(len(voices)) + ' speakers named' if labelled else ''}; describe by hand what the "
         "picture shows that the words leave out")
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
    name = f"{src.name.rsplit('.', 1)[0]}.burned.mp4"
    out = C.output_path(C.piece_folder(C.PUB_RENDERS, name) / name, args.o, inputs=[src])
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
