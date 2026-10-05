# CONTEXT.md — production/workflows/03-assemble-the-master/

The procedure for building a piece's master. The edit decision list is written with the author
from the storyboard and shot list (or, for a recorded piece, from its transcript), the brand's
card component is copied for each card, and `python3 toolkit/media.py assemble` builds the master
from logged footage, the cards and the approved voiceover. The master is probed and measured, a
recorded piece's captions are carried through to it, and the author watches or hears it through
before M4 is recorded. It does not cut deliverables (`publishing/workflows/02-cut-for-a-platform/`)
and does not make the voiceover (`production/workflows/02-make-a-voiceover/`).

## Directory Tree

```text
production/workflows/03-assemble-the-master/
├── CHECKLIST.md        ← model-tagged checklist; tick it as you go
├── CLAUDE.md           ← operating rules for this procedure
├── CONTEXT.md          ← this file: when to use it, what it produces
└── STEPS.md            ← the ordered steps, each naming its skill and guide
```

## When to use this

- A piece is storyboarded, its footage logged and its voiceover approved and archived.
- A recorded piece's transcript is approved and its recording logged: its master is cut from the
  recording.
- A trailer or explainer is made of stills, cards, fades and push-ins under a music bed.
- The author wants a change to a master: a new version of the same list.

Reach for a **different** procedure when the master is an episode's audio and the project makes
podcasts (its own procedure, cut the same way), or when the job is an audiobook's chapters (the
narrate-audiobook skill, where the project makes audiobooks).

## What it produces, and where

- **The edit decision list** `production/src/edits/<piece>.toml`, with the author.
- **Cards** `production/src/cards/<piece>.<card>.html`, copied from the brand's component.
- **The master** `production/src/renders/<piece>/<piece>.master.mp4` (`.wav` for an audio
  master), in the piece's own folder, and each card's PNG in
  `production/src/renders/<piece>/cards/`, git-ignored and regenerable.
- **Master-timed captions** `publishing/src/captions/<piece>.en-GB.srt`, for a recorded piece.
- **The brief's** `verified` entry for M4 and its `status`, on the author's word.

## The failure this procedure exists to prevent

A master nobody can rebuild, or one the author never saw. A cut made by hand starts from scratch
at the next change; a master assembled from an unverified file or an unapproved take is not the
piece that was agreed; and a master called done before the author watched it through passes its
mistake on to every cut-down made from it.

## Cross-references

- `production/docs/reference/edit-decision-lists.md` — the list, field by field.
- `production/docs/reference/sound-and-loudness.md` — beds, ducking, fades and the targets.
- `production/docs/reference/recorded-pieces.md` — cutting from a recording, and its captions.
- `.claude/skills/cut-for-platform/SKILL.md` — the skill that writes the list and renders.
