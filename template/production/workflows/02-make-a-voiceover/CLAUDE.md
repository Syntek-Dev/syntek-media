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
  ToolSearch; `python3 toolkit/media.py check --setup` and `take add`; fallback `espeak-ng`.
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
- **State the characters, calls and credits before any batch, and wait for a yes.** Count the
  request text exactly as it will be sent.
- **One call at a time, renamed at once.** Run `take add` straight after each call, before the
  next; stop at the first error.
- **An absolute `output_directory`, always,** inside `production/src/voiceover/generated/` and
  built from `git rev-parse --show-toplevel`, so no file ever lands outside the project.
- **One narrator per use.** Use the voice and model recorded for the voiceover use in
  `brand/src/voice/voice.md`; changing either is the author's decision, recorded with the date.
  A cloned voice speaks only with a `cleared` voice-consent row.
- **The script is never changed to suit a voice.** If a take is wrong, regenerate it on the
  author's word, or note the fault.
- **Audio is git-ignored** (`production/src/.gitignore`). Never commit it or force it past that
  rule.

## Output & naming

- **Produces:** `production/src/voiceover/<piece>.toml` and its takes in
  `production/src/voiceover/generated/`, named `<piece>.sNN.tN.mp3` (or `.pcm`).
- **Also writes:** credits-log rows (through `take add`), the narrator record the first time, and
  a footage-manifest row for each archived take.
- **Does not touch:** the script, the brief's gates, or any render.
