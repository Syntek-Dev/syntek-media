# CONTEXT.md — scripts/workflows/03-storyboard-a-piece/

The procedure for turning an approved script into a storyboard and a shot list the author has
approved: a picture for every spoken line, framing for every vertical deliverable, the words and
sounds over each board, and a source for every shot, stills, cards and colour clips included.
Every licensed or identifiable thing it shows or plays opens a rights row as it is boarded. It
ends with the piece at `status: storyboarded` and M3 (scripted → storyboarded) recorded. It
shoots, renders and clears nothing.

## Directory Tree

```text
scripts/workflows/03-storyboard-a-piece/
├── CONTEXT.md          ← this file (when to use, what it produces)
├── CLAUDE.md           ← operating rules for this workflow
├── STEPS.md            ← ordered steps to execute
└── CHECKLIST.md        ← verification checklist before marking complete
```

## When to use this

- A piece with pictures has an approved script, and the author asks to board it, plan its shots
  or work out what it needs filmed, found or made.
- An approved script changed, or a shot fell through, and the boards no longer match: this
  procedure revises them in place.

Reach for a **different** procedure when: the script is not yet approved
(`scripts/workflows/02-write-a-script/`); the piece has no picture or is a recording, so M3 is
`n/a` and the next job is its voice or its master; the shots exist and the next job is logging
them (`production/workflows/01-log-source-media/`); or the job is clearing a right already
boarded (`production/workflows/07-clear-the-rights/`).

## What it produces, and where

- `scripts/src/pieces/<piece>/storyboard.md` — one row per board, approved and dated.
- `scripts/src/pieces/<piece>/shot-list.md` — one row per shot, each with its source, status and
  rights ID.
- A `needed` row in `production/src/rights-register.md` for every licensed or identifiable item,
  and its ID in the brief's `rights:` list.
- The brief's `status: storyboarded`, with `M3` dated in `verified`.

## The failure this procedure exists to prevent

A master assembled from whatever footage was to hand. Lines go out over a face that is not
speaking them, a vertical cut crops the one detail the line was about, and a stock clip, a song
or a stranger's face is found uncleared only when the post is ready. A board for every line and
a source for every shot let the edit decision list be written without guessing, and a rights row
opened at the first sketch means nothing reaches M7 unasked about.

## Cross-references

- `scripts/docs/reference/storyboards-and-shot-lists.md` — both formats, framing and rights.
- `scripts/docs/reference/the-piece-ladder.md` — M3, and when it is `n/a`.
- `.claude/skills/storyboard/SKILL.md` — this procedure in skill form, with its mode file.
- `production/docs/reference/rights-and-consent.md` — what needs a rights row, and consent.
