# CONTEXT.md — scripts/workflows/02-write-a-script/

The procedure for turning an agreed brief into a script the author has approved: written for the
ear, one spoken sentence per line, every claim checked, timed against the brief and every
deliverable, reported on by the companion skills where they are present, and revised on the
author's notes. It ends with the script approved and the piece at `status: scripted` with M2
(briefed → scripted) recorded. It generates no audio and boards no pictures.

## Directory Tree

```text
scripts/workflows/02-write-a-script/
├── CONTEXT.md          ← this file (when to use, what it produces)
├── CLAUDE.md           ← operating rules for this workflow
├── STEPS.md            ← ordered steps to execute
└── CHECKLIST.md        ← verification checklist before marking complete
```

## When to use this

- A scripted piece is briefed and the author asks to write, draft or start its script.
- An existing script needs revising on the author's notes, or has to be cut to fit a
  deliverable: this procedure revises it in place.
- A short, a trailer, an episode or a standalone read is to be written from the author's own
  written work, which is read here and never edited.

Reach for a **different** procedure when: the piece has no agreed brief
(`scripts/workflows/01-brief-a-piece/`); the piece is a recording, whose words come from its
transcript (`production/workflows/08-bring-in-a-recording/`); it is an audiobook, which has no
script: its plan and M2 go through the audiobook procedures, where the project makes audiobooks; the
script is approved and the next job is its pictures (`scripts/workflows/03-storyboard-a-piece/`);
or the job is a text-only post (the social-media-documents skill (syntek-author), where
present).

## What it produces, and where

- `scripts/src/pieces/<piece>/script.md` — the script, with `approved:` dated, and `words` and
  `estimated_seconds` written by `python3 toolkit/media.py script time --write`.
- The brief's `status: scripted`, with `M2` dated in `verified`; for a piece with no picture,
  `M3` recorded `n/a — no picture` as well.
- A hand-back in chat: how long the script runs, which companion reports ran, and what was
  decided or waived.

## The failure this procedure exists to prevent

A script written for the page and discovered at the voiceover. Long sentences, unsaid numbers and
a hook in the third line sound fine read silently and fail the moment they are spoken; a script
that runs long is cut in the edit, where every cut costs a re-take or a re-render; and a claim
nobody checked becomes a caption nobody can take back. That is why the claims are checked before
the writing (step 4), the timing runs before anyone hears it (step 6), and nothing is approved
while a flag is open.

## Cross-references

- `scripts/docs/reference/writing-for-the-ear.md` — the script format, timing and the companions.
- `scripts/docs/reference/the-piece-ladder.md` — M2 for a scripted piece.
- `.claude/skills/write-script/SKILL.md` — this procedure in skill form, with its mode file.
- `.claude/rules/syntek-media/03-production-ethics.md` — who approves, and never fabricate.
