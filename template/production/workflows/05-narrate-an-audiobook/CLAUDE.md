@./CONTEXT.md

# CLAUDE.md — production/workflows/05-narrate-an-audiobook/

Read order: `.claude/CLAUDE.md` → `.claude/MEMORY.md` → `production/CONTEXT.md` →
`production/CLAUDE.md` → `production/workflows/CONTEXT.md` → `production/workflows/CLAUDE.md`
→ this folder's `CONTEXT.md` (imported above) → this file → `STEPS.md` (with `CHECKLIST.md`
open).

## Purpose (one line)

Plan the book, then voice or record each chapter by the route its channels accept, at a cost the
author has agreed, with every take and recording logged.

## How to work here

- **Routing:** skill `narrate-audiobook`; guides `production/docs/reference/audiobook-narration.md`
  and `production/docs/reference/elevenlabs.md`; tools `mcp__elevenlabs__list_models`,
  `mcp__elevenlabs__search_voices`, `mcp__elevenlabs__check_subscription` and
  `mcp__elevenlabs__text_to_speech` from the user-scope server `elevenlabs`, loaded with
  ToolSearch; commands `python3 toolkit/media.py check --setup`, `audiobook text`, `take add` and
  `footage add`.
- **Model:** **Opus** for choosing a route and a narrator, and for judging a take with the author;
  the mechanical tier for making chunks, counting characters, generating and logging
  (`.claude/rules/syntek-media/05-model-allocation.md`). The checklist tags are authoritative.
- **Concrete steps:** follow `STEPS.md` in order and tick `CHECKLIST.md` as you go: confirm the
  request → choose the route per channel → write the register and the credits, and record M2 →
  check the setup and the narrator → make the chapter text → state the cost and wait → generate,
  one call at a time → log a human recording → listen and approve → hand back.
- **Definition of done:** the plan is approved (M2), every chapter asked for has approved takes or
  a logged recording (or its external export recorded), every call has its credits-log row, and no
  chapter text sits in a tracked file.

## Guardrails

- **The route is chosen per channel, with the author, before anything is spent.** Say plainly
  that ACX and Audible need a human narrator unless the author is authorised otherwise, and that
  INaudio takes synthetic narration only as ElevenLabs' own package, made outside this template.
- **Never generate unasked**, and never for a channel on the `external` route.
- **State the characters, calls and credits before any batch, and wait for a yes.** One call at a
  time; `take add` straight after each; stop at the first error.
- **An absolute `output_directory`, always,** inside `production/src/audiobook/generated/` and
  built from `git rev-parse --show-toplevel`.
- **Chapter text stays out of Git.** It is read from its source by `audiobook text`; never copy
  it into the register, a script or any tracked file.
- **Disclosure always.** A synthetic narrator is recorded in the brief and named on every channel.

## Output & naming

- **Produces:** `production/src/audiobook/<piece>.md` and the credits' `<piece>.ch00.md` and
  `<piece>.ch99.md`; chunks `<piece>.chNN.pNN.txt`, their sidecar `<piece>.chNN.chunks.toml` and
  takes `<piece>.chNN.pNN.tN.mp3` in `production/src/audiobook/generated/`.
- **Also writes:** the brief's `status` and `verified` (M2, and M3 `n/a — no picture`),
  credits-log rows (through `take add`), footage-manifest rows for recordings and any archived
  take, and the narration record in `brand/src/voice/voice.md` the first time.
- **Does not touch:** the source text, or any master.
