# CONTEXT.md — production/workflows/06-master-an-audiobook/

The procedure for mastering an audiobook's chapters and making them ready for each channel. Each
chapter's approved takes, or its logged recording, are mastered by
`python3 toolkit/media.py audiobook master` with room tone at head and tail, measured by
`audiobook check` against the ACX targets, heard through by the author, archived, and packaged
per channel with its credits and its disclosure. The audiobook passes M4 when every mastered
chapter is approved and archived (its chunk takes need not be), and M5 when every file passes its
check. It voices nothing
(`production/workflows/05-narrate-an-audiobook/`) and makes nothing for a channel on the
`external` route.

## Directory Tree

```text
production/workflows/06-master-an-audiobook/
├── CHECKLIST.md        ← model-tagged checklist; tick it as you go
├── CLAUDE.md           ← operating rules for this procedure
├── CONTEXT.md          ← this file: when to use it, what it produces
└── STEPS.md            ← the ordered steps, each naming its skill and guide
```

## When to use this

- Every part of a chapter is approved (AI route) or its recording logged (human route).
- A chapter failed its check, and the author wants it mastered again.
- A channel is added, and the approved masters need packaging for it.

Reach for a **different** procedure when a chapter still needs voicing or recording
(`production/workflows/05-narrate-an-audiobook/`), or when the job is the audiobook's post
package and disclosure (`publishing/workflows/05-prepare-a-post/`).

## What it produces, and where

- **Mastered chapters** `production/src/audiobook/renders/<piece>.chNN.mp3`, git-ignored, each
  passing `audiobook check`.
- **Register rows** updated with each chapter's Master, Duration, Check and Status.
- **Footage rows** for each approved master, archived as source media.
- **The brief's** `verified` entries for M4, M5 and M6 (not applicable to an audiobook).

## The failure this procedure exists to prevent

A chapter rejected by a store, or one nobody has heard. A file a few decibels off a store's
targets is sent back after the whole book has gone in; a master checked only by the toolkit can
still carry a mispronounced name or a dropped line; and a master that was never archived is lost
with the disk it sat on.

## Cross-references

- `production/docs/reference/audiobook-narration.md` — the ACX targets and the channels.
- `production/docs/reference/sound-and-loudness.md` — why an audiobook is measured in RMS.
- `production/src/audiobook/` — the register, and the git-ignored masters.
- `.claude/skills/narrate-audiobook/SKILL.md` — the skill that runs this procedure.
