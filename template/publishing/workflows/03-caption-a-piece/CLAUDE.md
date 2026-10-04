@./CONTEXT.md

# CLAUDE.md — publishing/workflows/03-caption-a-piece/

Read order: `.claude/CLAUDE.md` → `.claude/MEMORY.md` → `publishing/CONTEXT.md` →
`publishing/CLAUDE.md` → `publishing/workflows/CONTEXT.md` → `publishing/workflows/CLAUDE.md` →
this folder's `CONTEXT.md` (imported above) → this file → `STEPS.md` (with `CHECKLIST.md` open).

## Purpose (one line)

Give every deliverable with speech and picture captions that are timed to it, readable at its
size and true word for word to what was scripted or said.

## How to work here

**Follow `STEPS.md` in order and tick `CHECKLIST.md` as you go.** The model tags in the checklist
are authoritative: `opus` items are judgement; `sonnet` items belong to the mechanical tier.

- **Routing:** skill `captions`. Guides: `publishing/docs/reference/captions.md`,
  `production/docs/reference/recorded-pieces.md` for a recorded piece, and the guide for each
  platform a deliverable goes to. Tools: `python3 toolkit/media.py captions …` and
  `extract-audio`.
- **Model:** **Opus** for line breaks, speaker changes, resolving a word that differs from the
  script and judging a burned preview; the mechanical tier for running the toolkit, rewrapping,
  converting and recording the gate (`.claude/rules/syntek-media/05-model-allocation.md`).
- **Concrete steps:** list what needs captions → choose the route → make the master's captions →
  make each cut's → rewrap where a width differs → check every file → burn or attach → watch a
  burned preview → record the gate → hand back.
- **Definition of done:** every deliverable that needs captions has a file that passes
  `captions check --script`, burned where its platform takes no sidecar; a burned preview has
  been checked by eye; M6 is recorded, or `n/a` with its reason.

## Guardrails

- **The words come from the script or the approved transcript.** No caption is retyped from
  memory or made from speech-to-text here; a piece with neither goes back to
  `production/workflows/08-bring-in-a-recording/`.
- **Speech-to-text spends credits.** It runs only when the author asks, its cost stated first, and
  its call is logged in `production/src/credits-log.md`.
- **Fix the source, not the caption.** A mis-transcription is corrected in the transcript first,
  with the author; a caption never improves on what was said.
- **No braced direction or audio tag** reaches a caption.
- **A font fallback is a failure.** `captions burn` fails when the caption font is missing; fix
  the font, never accept the fallback.
- **Never overwrite** a checked caption file without confirming with the author.

## Output & naming

- **Produces:** `publishing/src/captions/<piece>[--cNN|.<FID>][.<platform>-<format>].en-GB.srt`,
  with `.vtt` beside it where a platform takes one; published transcripts
  `publishing/src/captions/<piece>[--cNN].transcript.en-GB.md`.
- **Also writes:** burned renders in `publishing/src/renders/`; the brief's `status` and
  `verified`.
- **Does not touch:** the script, the transcript's words without the author's agreement, or any
  other render.
