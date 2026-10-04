@./CONTEXT.md

# CLAUDE.md — brand/src/voice/

Read order: `.claude/CLAUDE.md` → `.claude/MEMORY.md` → `brand/CONTEXT.md` → `brand/CLAUDE.md`
→ `brand/src/CONTEXT.md` → `brand/src/CLAUDE.md` → this folder's `CONTEXT.md` (imported above)
→ this file.

## Purpose (one line)

Keep one record of how the brand sounds aloud and who says it, so every voiceover uses the same
narrator, settings and pronunciations without asking again.

## How to work here

- **Routing:** workflow `brand/workflows/05-write-the-spoken-voice/`; guide
  `brand/docs/reference/the-spoken-voice.md`; skill `voiceover`, which records a narrator here
  the first time it needs one and reads this file before every call.
- **Model:** **Opus** for the spoken style, choosing a narrator with the author and settling a
  pronunciation; the mechanical tier for writing a row the author has decided
  (`.claude/rules/syntek-media/05-model-allocation.md`).
- **Concrete steps:** read the written voice, where present → settle the spoken style with the
  author → choose a narrator per use (model found with `mcp__elevenlabs__list_models`, voices
  listed free; any trial costed and agreed first) → record each with its date → add
  pronunciations as words come up.
- **Definition of done:** every use the project needs has one narrator row, with its consent ID
  where the voice is a clone; the spoken style is written; no flag is left in a section a
  voiceover reads.

## Guardrails

- **One narrator per use.** A second voice for the same use makes the brand sound like two.
  Changing a narrator is the author's decision, recorded in `.claude/MEMORY.md` with its date
  before the row changes.
- **No clone without recorded consent.** A cloned voice, the owner's own included, needs a
  cleared `voice-consent` row in `production/src/rights-register.md`, and its ID in the
  Consent column, before the first call.
- **Voice IDs stay here.** Never copy one into a guide, a procedure, a post or `.claude/MEMORY.md`
  (`.claude/rules/syntek-media/06-global-rules.md` Section 10).
- **The script holds no IPA.** Pronunciations live here and are substituted into the request
  text only, never written back into a script.
- **Never generate to choose a voice unasked.** Listening to a trial costs credits; state the
  cost and wait for a yes (`.claude/rules/syntek-media/03-production-ethics.md` Section 4).
- **Never overwrite** a narrator row or a pronunciation without confirming with the author.

## Output & naming

- **Hand-written (with the author):** `voice.md`, one sentence per line outside its tables.
- **Written by skills:** a narrator row, the first time, by `voiceover`.
- **Generated (never hand-edit):** nothing here; trial audio lands in the git-ignored
  `production/src/voiceover/generated/`.
