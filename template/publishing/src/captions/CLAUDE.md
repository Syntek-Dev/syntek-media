@./CONTEXT.md

# CLAUDE.md — publishing/src/captions/

Read order: `.claude/CLAUDE.md` → `.claude/MEMORY.md` → `publishing/CONTEXT.md` →
`publishing/CLAUDE.md` → `publishing/src/CONTEXT.md` → `publishing/src/CLAUDE.md` → this folder's
`CONTEXT.md` (imported above) → this file.

## Purpose (one line)

Hold every caption file, each timed to one thing and true word for word to the script or the
approved transcript.

## How to work here

- **Routing:** skill `captions`, through `publishing/workflows/03-caption-a-piece/` (or
  `production/workflows/08-bring-in-a-recording/` for a recording's own file); guide
  `publishing/docs/reference/captions.md`.
- **Model:** **Opus** for line breaks, speaker changes and anything a viewer reads; the mechanical
  tier for running `media.py captions` and renaming
  (`.claude/rules/syntek-media/05-model-allocation.md`).
- **Concrete steps:** pick the timing route → make the SRT with the toolkit → rewrap where a
  deliverable needs its own width → `captions check --script` → generate the VTT where needed →
  burn or upload, per the platform's guide.
- **Definition of done:** every file passes `captions check` against its script or transcript;
  its name says what it is timed to; a burned preview has been checked by eye.

## Guardrails

- **The words are not edited here.** A caption carries what was scripted or said; only a
  mis-transcription is fixed, and the fix goes into the transcript first.
- **No braced direction or audio tag** ever reaches a caption.
- **Speech-to-text only when the author asks:** it spends credits, and the call is logged in
  `production/src/credits-log.md`.
- **Never overwrite** a checked caption file without confirming with the author; a retimed
  version is a new file with its own name.

## Output & naming

- **Written by `captions`:** `<piece>[--cNN|.<FID>][.<platform>-<format>].en-GB.srt`, with a
  `.vtt` of the same stem where a platform needs one; `en-GB` always; timecodes in SRT's comma
  form inside the file only.
- **Written by `captions`, with the author:** `<piece>[--cNN].transcript.en-GB.md`, a published
  transcript of exactly what a page plays (the whole piece, or one cut placed on a site of the
  website or blog profile), or of a feed episode: one sentence per line, a paragraph per beat,
  speaker names only where two or more people speak, and a recorded piece's 'As recorded on
  DD/MM/YYYY' line; what the picture carries and the words leave out is described by hand.
- **Generated:** burned deliverables go to `publishing/src/renders/`, never here.
- **Not here:** the script or transcript the words come from (`scripts/src/pieces/`).
