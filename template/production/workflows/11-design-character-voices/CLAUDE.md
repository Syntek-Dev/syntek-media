@./CONTEXT.md

# CLAUDE.md — production/workflows/11-design-character-voices/

Read order: `.claude/CLAUDE.md` → `.claude/MEMORY.md` → `production/CONTEXT.md` →
`production/CLAUDE.md` → `production/workflows/CONTEXT.md` → `production/workflows/CLAUDE.md`
→ this folder's `CONTEXT.md` (imported above) → this file → `STEPS.md` (with `CHECKLIST.md`
open).

## Purpose (one line)

Give a character a voice of its own, remixed from the author's cleared clone, heard and chosen by
the author, saved once and recorded where every later call will find it.

## How to work here

- **Routing:** skill `voiceover`; guides `production/docs/reference/character-voices.md` and
  `production/docs/reference/elevenlabs.md`; tools `mcp__elevenlabs__search_voices`,
  `mcp__elevenlabs__list_models`, `mcp__elevenlabs__check_subscription`,
  `mcp__elevenlabs__create_voice_from_preview` and, for a trial only,
  `mcp__elevenlabs__text_to_speech`, from the user-scope server `elevenlabs`, loaded with
  ToolSearch; `python3 toolkit/media.py check --setup`, `voice remix plan`, `voice remix run`
  and `speak plan --trial`.
- **Model:** **Opus** for drafting a description, judging previews with the author and choosing;
  the mechanical tier for running the toolkit, saving the chosen voice and writing the agreed row
  (`.claude/rules/syntek-media/05-model-allocation.md`). The checklist tags are authoritative.
- **Concrete steps:** follow `STEPS.md` in order and tick `CHECKLIST.md` as you go: confirm the
  request → check the setup → confirm the source clone and its consent → draft the descriptions →
  plan the remix and wait → run it → listen and choose, or plan again → save the chosen voice →
  record the character's row → try it on a few lines, if asked → hand back.
- **Definition of done:** every character the author asked for has a saved voice and a
  `character:<name>` row whose consent is the source clone's, or the author has stopped; every
  call was stated and agreed before it was made, and has its credits-log row.

## Guardrails

- **Never generate unasked.** A remix, a save and a trial each spend from the author's account.
- **Remix only the author's own clone, with its `voice-consent` row `cleared`.** Never a Voice
  Library voice, never another person's voice, and never a description that imitates a real
  actor, reader or public figure (`.claude/rules/syntek-media/03-production-ethics.md` Section 6).
- **Plan, state, wait, then run.** `voice remix plan` first; `voice remix run --approve-call` only
  after the author's yes, with exactly the planned arguments; the project's ask rule prompts for
  it. Stop at the first error; never retry.
- **The key stays in the shell.** `voice remix run` reads the user-scope `ELEVENLABS_API_KEY`;
  never type it on a command line, print it or write it to a file
  (`.claude/rules/syntek-media/06-global-rules.md` Section 10).
- **A new remix takes a new trial name.** The toolkit refuses a name already used; never delete a
  trial to reuse its name.
- **This procedure never clones a voice and never makes a take.** A preview or a trial enters no
  register and is never approved for a piece.

## Output & naming

- **Produces:** remix previews `<name>.pNN.mp3` and `<name>.remix.json` in
  `production/src/voiceover/generated/voice-trials/<name>/`, a saved voice in the author's
  account, and the `character:<name>` row in `brand/src/voice/voice.md`.
- **Also writes:** the remix run's credits-log row (by `voice remix run`), and the save's and any
  trial's rows (by the skill), each with `—` for the piece. A trial of the saved voice keeps the
  server's name in its own `voice-trials/<name>/`.
- **Does not touch:** any script, segment register, take or brief.
