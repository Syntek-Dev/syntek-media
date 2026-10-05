@./CONTEXT.md

# CLAUDE.md — production/workflows/02-make-a-voiceover/

Read order: `.claude/CLAUDE.md` → `.claude/MEMORY.md` → `production/CONTEXT.md` →
`production/CLAUDE.md` → `production/workflows/CONTEXT.md` → `production/workflows/CLAUDE.md`
→ this folder's `CONTEXT.md` (imported above) → this file → `STEPS.md` (with `CHECKLIST.md`
open).

## Purpose (one line)

Give a scripted piece the voice the author approved, a sentence at a time, at a cost the author
has agreed, with every take named, logged and kept.

## How to work here

- **Routing:** skill `voiceover`; guides `production/docs/reference/voiceover.md` and
  `production/docs/reference/elevenlabs.md`; tools `mcp__elevenlabs__list_models`,
  `mcp__elevenlabs__search_voices`, `mcp__elevenlabs__check_subscription` and
  `mcp__elevenlabs__text_to_speech` from the user-scope server `elevenlabs`, loaded with
  ToolSearch; `python3 toolkit/media.py check --setup`, `speak plan`, `take add` and `voice join`;
  fallback `espeak-ng`.
- **Model:** **Opus** for choosing a voice, splitting the script and judging a take with the
  author; the mechanical tier for building request text, counting characters, generating and
  logging (`.claude/rules/syntek-media/05-model-allocation.md`). The checklist tags are
  authoritative.
- **Concrete steps:** follow `STEPS.md` in order and tick `CHECKLIST.md` as you go: confirm the
  request → check the setup → check or choose the narrator → split the script into segments →
  build the request text → state the cost and wait → generate, one call at a time → fall back if
  needed → listen, approve and archive → hand back.
- **Definition of done:** every segment the author asked for has a take in the register, made
  with the recorded narrator and model; the cost was stated before it was spent; every call has
  its credits-log row; every approved take is archived; the script is unchanged.

## Guardrails

- **Never generate unasked.** Not as a demonstration, not to check a setting, not as a helpful
  extra after another job. Every call spends credits.
- **State the offline plan's characters and calls before any batch, and wait for a yes.** Never
  invent a credit rate; copy the requests to the register without changing the script or `text`.
- **One call at a time, renamed at once.** Run `take add` straight after each call, before the
  next; stop at the first error.
- **An absolute `output_directory`, always,** built from `git rev-parse --show-toplevel`, so no
  file ever lands outside the project: the piece's
  `production/src/voiceover/generated/<piece>/takes/`, which
  `python3 toolkit/media.py speak plan <piece>` makes before the first call, or a voice trial's
  `production/src/voiceover/generated/voice-trials/<name>/`, which `speak plan --trial <name>`
  makes. Never make either with `mkdir`.
- **One narrator per use.** Use the voice and model recorded for the voiceover use in
  `brand/src/voice/voice.md`; changing either is the author's decision, recorded with the date.
  A cloned voice speaks only with a `cleared` voice-consent row.
- **The script is never changed to suit a voice.** If a take is wrong, regenerate it on the
  author's word, or note the fault.
- **Audio is git-ignored** (`production/src/.gitignore`). Never commit it or force it past that
  rule.

## Output & naming

- **Produces:** `production/src/voiceover/<piece>.toml` and its takes in
  `production/src/voiceover/generated/<piece>/takes/`, named `<piece>.sNN.tN.mp3` (or `.pcm`).
- **Also writes:** credits-log rows (through `take add`), the narrator record the first time, and
  a footage-manifest row for each archived take; a scratch track in `generated/<piece>/`, beside
  its takes folder. A voice trial is never a take: it keeps the server's name in
  `voice-trials/<name>/`, enters no register, and its credits-log row has `—` for the piece.
- **Also writes:** the joined mono 16-bit voice in the piece's production renders folder, and
  `M4.takes` in a scene piece's brief after the used takes are approved and archived.
- **Does not touch:** the script or the brief's other gates.
