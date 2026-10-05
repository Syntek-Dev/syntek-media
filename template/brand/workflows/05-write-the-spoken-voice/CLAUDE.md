@./CONTEXT.md

# CLAUDE.md — brand/workflows/05-write-the-spoken-voice/

Read order: `.claude/CLAUDE.md` → `.claude/MEMORY.md` → `brand/CONTEXT.md` → `brand/CLAUDE.md`
→ `brand/workflows/CONTEXT.md` → `brand/workflows/CLAUDE.md` → this folder's `CONTEXT.md`
(imported above) → this file → `STEPS.md` (with `CHECKLIST.md` open).

## Purpose (one line)

Decide once, with the author, how the brand sounds aloud and who says it for each use, so every
voiceover uses the same narrator, settings and pronunciations.

## How to work here

- **Routing:** no media skill runs this procedure; it opens with the grill-with-docs skill
  (syntek-author), where present, or the same questions in rounds. Guide
  `brand/docs/reference/the-spoken-voice.md`; free tools `mcp__elevenlabs__list_models`,
  `mcp__elevenlabs__search_voices` and `mcp__elevenlabs__search_voice_library` from the
  user-scope server `elevenlabs`; any trial through `production/workflows/02-make-a-voiceover/`
  and the `voiceover` skill.
- **Model:** **Opus** for the spoken style, choosing a narrator with the author and settling a
  pronunciation; the mechanical tier for listing models and voices and writing rows the author
  has decided (`.claude/rules/syntek-media/05-model-allocation.md`). The checklist tags are
  authoritative.
- **Concrete steps:** follow `STEPS.md` in order and tick `CHECKLIST.md` as you go: grill the
  spoken voice → write the spoken style → check the server → find the model and list voices →
  consent before any clone → trials only on the author's word → record each narrator →
  pronunciations → clear the flags and record → hand back.
- **Definition of done:** the spoken style is written; every use the project needs has one
  narrator row with its model, settings and date, and a cleared consent ID for any clone; the
  pronunciations known so far are recorded; no flag is left in a section `voiceover` reads.

## Guardrails

- **Never generate here.** Listing models and voices is free; hearing one costs credits, and a
  trial runs only on the author's word, through the voiceover procedure, which states the cost
  and waits for a yes (`.claude/rules/syntek-media/03-production-ethics.md` Section 4). Its
  audio goes to `production/src/voiceover/generated/voice-trials/<name>/`, made by
  `python3 toolkit/media.py speak plan --trial <name>`, never by `mkdir`.
- **No clone without recorded consent.** A cloned voice, the owner's own included, needs a
  cleared `voice-consent` row before it is made or used
  (`.claude/rules/syntek-media/03-production-ethics.md` Section 6).
- **One narrator per use.** A second voice for the same use makes the brand sound like two.
- **The model is found, never assumed.** Record the model ID `mcp__elevenlabs__list_models`
  returns when the narrator is chosen.
- **Voice IDs stay in `voice.md`.** Never copy one into a guide, a procedure, a post or
  `.claude/MEMORY.md`.
- **Never overwrite** a narrator row or a pronunciation without confirming with the author.

## Output & naming

- **Produces:** `brand/src/voice/voice.md`, its sections filled.
- **Also writes:** `voice-consent` rows in `production/src/rights-register.md`; dated decisions
  in `.claude/MEMORY.md`.
- **Does not touch:** any script, any piece's segment register, or the written voice files of
  syntek-author.
