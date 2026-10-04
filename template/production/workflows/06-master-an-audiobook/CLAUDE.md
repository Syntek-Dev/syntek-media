@./CONTEXT.md

# CLAUDE.md — production/workflows/06-master-an-audiobook/

Read order: `.claude/CLAUDE.md` → `.claude/MEMORY.md` → `production/CONTEXT.md` →
`production/CLAUDE.md` → `production/workflows/CONTEXT.md` → `production/workflows/CLAUDE.md`
→ this folder's `CONTEXT.md` (imported above) → this file → `STEPS.md` (with `CHECKLIST.md`
open).

## Purpose (one line)

Turn approved chapters into files every chosen channel will accept, checked by the toolkit, heard
by the author and kept safe.

## How to work here

- **Routing:** skill `narrate-audiobook`; guides `production/docs/reference/audiobook-narration.md`
  and `production/docs/reference/sound-and-loudness.md`; commands
  `python3 toolkit/media.py audiobook master`, `audiobook check`, `probe`, `cut` (a retail
  sample) and `footage add`.
- **Model:** **Opus** for judging a chapter with the author and for every packaging decision; the
  mechanical tier for mastering, checking, archiving and recording the gates
  (`.claude/rules/syntek-media/05-model-allocation.md`). The checklist tags are authoritative.
- **Concrete steps:** follow `STEPS.md` in order and tick `CHECKLIST.md` as you go: confirm the
  chapters are ready → master each chapter → check each file → listen through and approve →
  archive the masters and record M4 → package per channel → record M5 → hand back.
- **Definition of done:** every chapter not on the `external` route is mastered, passes
  `audiobook check`, has been heard and approved by the author and is archived; each channel's
  package is complete; M4 and M5 are dated in the brief.

## Guardrails

- **Fix a failure at its source.** A chapter that fails its check is mastered again, or its part
  regenerated or re-recorded on the author's word; the check is never loosened to pass it.
- **Never master for a channel on the `external` route.** Its package comes from ElevenLabs' own
  product, unmodified, and the register only records it.
- **A re-encoded take is not a better one.** A 128 kbps take raised to 192 kbps meets the letter
  of the bitrate rule, not its intent; say so, and ask for the higher format next time.
- **Disclosure always.** A synthetic narrator is disclosed on every channel, in the form that
  channel asks for.
- **Never overwrite** an approved master without confirming with the author.

## Output & naming

- **Produces:** `production/src/audiobook/renders/<piece>.chNN.mp3`, git-ignored.
- **Also writes:** the register's Master, Duration, Check and Status; footage-manifest rows for the
  archived masters; the brief's `verified` entries for M4, M5 and M6, and its `status`.
- **Does not touch:** the source text, the takes, the recordings, or any external package.
