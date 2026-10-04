# CONTEXT.md — scripts/src/

The pieces themselves. The register assigns every piece its number, and each piece has one
folder holding its brief, its words and its plan for the picture. Nothing here is rendered,
recorded or posted, and no audio, footage or caption file lives here: those belong to the
production and publishing layers, named for the piece. A project generated with examples starts
with one worked example piece, which `copier update` never brings back once it is deleted.

## Directory Tree

```text
scripts/src/
├── CONTEXT.md                ← this file
├── CLAUDE.md                 ← operating rules
├── piece-register.md         ← seed: every piece number opened, with kind, origin and parent
└── pieces/                   ← one folder per piece, each with its own pair
    └── NNN-kebab-title/      ← brief.md · script.md or transcript.md · storyboard.md · shot-list.md
```

## What's here

- `piece-register.md` — **the one place a piece number is assigned.** One row per piece, in
  number order, kept for life; a retired piece keeps its row. It holds no status: a piece's
  status lives in its brief.
- `pieces/` — **one folder per piece**, `NNN-kebab-title` (three digits, frozen once assigned,
  never reused). Each folder carries its own `CONTEXT.md` and `CLAUDE.md`, written when the piece
  is opened, then:
  - `brief.md` — the plan, and the record of where the piece stands: `status` and `verified`.
  - `script.md` — a scripted piece's words, one spoken sentence per line; or `transcript.md` —
    a recorded piece's words, as said, with every beat anchored on the recording. An audiobook
    has neither: its plan is its chapter register, in the production layer.
  - `storyboard.md` and `shot-list.md` — a picture for every spoken line, and a source for every
    shot; absent where the piece has no picture or was recorded.

The register ships with headings and writing rules but no entries. `copier update` recreates it
if you delete it and never touches it once you have edited it.

## Cross-references

- `scripts/docs/reference/the-piece-ladder.md` — the brief's `status` and `verified`, and the
  gates M1 to M7.
- `scripts/docs/reference/writing-for-the-ear.md` — the script and transcript formats.
- `scripts/docs/reference/storyboards-and-shot-lists.md` — the storyboard and shot-list formats.
- `scripts/workflows/CLAUDE.md` — the procedure that writes each file.
- `production/src/CONTEXT.md` and `publishing/src/CONTEXT.md` — where a piece's footage,
  voice, edit, cut-downs, captions, thumbnails and posts are kept.
