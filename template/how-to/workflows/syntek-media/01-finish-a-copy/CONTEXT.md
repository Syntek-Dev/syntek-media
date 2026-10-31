# CONTEXT.md — how-to/workflows/syntek-media/01-finish-a-copy/

The procedure for finishing a fresh copy of syntek-media, from the lines Copier printed to the
project's first commit with the template. It reads what the copy reported with the author,
adds by hand only what no copy offers, carries the asks and denies to the other coding agents'
files, sets up the ElevenLabs server and Git LFS where the project needs them, checks the set-up
before anything spends a credit, and commits the copy with its answers file.

## Directory Tree

```text
how-to/workflows/syntek-media/01-finish-a-copy/
├── CONTEXT.md          ← this file (when to use, what it produces)
├── CLAUDE.md           ← operating rules for this procedure
├── STEPS.md            ← ordered steps to execute, with every command
└── CHECKLIST.md        ← verification checklist before marking complete
```

## When to use this

- syntek-media has just been copied into this project, over a syntek-author project or into an
  empty folder, and nothing has been committed since.
- The message after the copy has scrolled away, or a session started before anyone read it.
- A first session is about to make audio or video, and nobody has checked the set-up.

Reach for a **different** procedure when: the project already holds a committed copy and the
template has moved on (`how-to/workflows/syntek-media/04-update-the-template/`); an answer given
at the copy must change (`how-to/workflows/syntek-media/02-change-the-answers/`); or the copy
stopped on a collision, which is a fault in the template
(`how-to/workflows/syntek-media/03-report-a-template-problem/`).

## What it produces, and where

- The settings entries the copy left to the author, added to `.claude/settings.json` on their
  word, and the asks and denies carried to the other coding agents' files that exist.
- The ElevenLabs server registered once at user scope, outside the project, and Git LFS set up
  for this repository where large design exports will be kept.
- A clean report from `python3 toolkit/media.py check --setup`, or each open finding accepted by
  the author, and one commit holding the copy and `.copier-answers.syntek-media.yml`.

## The failure this procedure exists to prevent

A first session that spends credits before the project is ready. A settings file kept from
before the copy lacks the ask rules that make Claude Code stop before a paid call, and an
ElevenLabs server whose base path does not contain the project refuses every file it is given.
A copy left uncommitted also leaves the first update with no answers file to work from.

## Cross-references

- `how-to/docs/syntek-media/finishing-a-copy.md`: why each step is there.
- `how-to/src/TEMPLATE-GUIDE/syntek-media/03-applying-over-syntek-author.md` and
  `how-to/src/TEMPLATE-GUIDE/syntek-media/04-a-standalone-project.md`: what the copy itself does.
- `production/docs/reference/elevenlabs.md`: the server, its base path and its commands.
- `brand/workflows/06-check-the-setup/`: the set-up check this procedure runs at step 7.
