# CONTEXT.md — production/src/timing/

The accepted timing of a piece's joined voice, flat under the piece's `<piece>.` names: when each
word is said, the check the author signs that the voice said the words it was asked to say, and
which mouth shape shows when. Captions are timed from the words, and a scene's page types its
lines and moves its character's mouth from these files. Every file here is written by a toolkit
command, never by hand: the command writes a git-ignored working copy first, and reaches this
folder only through `-o`, once the author has accepted the run.

## Directory Tree

```text
production/src/timing/
├── CONTEXT.md                  ← this file
├── CLAUDE.md                   ← operating rules and the files' shapes
├── <piece>.words.json          ← every word of the joined voice: its start, end, score and segment
├── <piece>.words-check.md      ← the words check the author signs, written beside the words
└── <piece>.mouth.json          ← the joined voice's mouth shapes, A to H and X, as Rhubarb Lip Sync gives them
```

## What's here

- `<piece>.words.json` — written by `python3 toolkit/media.py transcribe <piece>`, which aligns
  each approved segment's known words to the piece's joined voice, so the aligner never guesses
  a word: each word's `word`, `start`, `end`, `score` and the `segment` it belongs to.
- `<piece>.words-check.md` — written beside the words by the same run, for the author to read:
  the segments that came back without words, the low scores, where a segment's `request` and
  `text` differ, and where the words a transcription heard differ from the script's.
- `<piece>.mouth.json` — written by `python3 toolkit/media.py lipsync <piece>` from the same
  joined voice: Rhubarb Lip Sync's mouth cues, its record of the sound file made relative to the
  repository, so no home folder reaches a tracked file.
- **Every time is in seconds from the start of the joined voice**,
  `production/src/renders/<piece>/<piece>.voice.wav`. A file here describes one joined voice: a
  new take means joining the voice again and timing it again.
- **The working copies** sit in the piece's git-ignored `production/src/renders/<piece>/timing/`,
  where a run can be repeated freely and nothing tracked changes unasked. A levels file is only
  ever a working copy there: no file in this folder holds one.
- This folder ships with every project, holding only its pair until a piece's voice is timed.

## Cross-references

- `production/docs/reference/voiceover.md` — segments, the register, and timing the joined voice.
- `production/src/voiceover/` — the segment registers whose approved takes the joined voice joins.
- `production/src/scenes/` — the cue index made from the words, and the scene that reads all three.
- `.claude/rules/syntek-media/04-toolkit-pipeline.md` Section 3 — the working copy, `-o`, and the
  named exception that lets a timing file be replaced.
- `production/workflows/CLAUDE.md` — the procedures, among them the one that times a scene
  piece's voice.
