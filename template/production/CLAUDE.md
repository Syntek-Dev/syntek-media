@./CONTEXT.md

# CLAUDE.md — production/

Read order: `.claude/CLAUDE.md` → `.claude/MEMORY.md` → this folder's `CONTEXT.md` (imported
above) → this file → the target folder's `CONTEXT.md` and `CLAUDE.md`.

## Purpose (one line)

Turn an approved script or recording into a master the author has watched or heard through,
made from sources that are logged, paid for once and cleared for use.

## How to work here

- **Routing:** start every job from the matching procedure in `production/workflows/` (the
  index is `production/workflows/CLAUDE.md`; `run-media-workflow` resolves
  `production/workflows/local/` first); each one names its skill and guide. Voiceover goes
  through `voiceover`; edit decision lists, cards and masters through `cut-for-platform`; a
  recording and its transcript through `captions`;
<: if 'audiobook' in MEDIA_KINDS :>  audiobook chapters through `narrate-audiobook`;
<: endif :>  logging source media and clearing rights are procedures with no skill.
- **Model:** **Opus** for every judgement (a voice, a cut, a take, a rights question); the
  mechanical tier for logging files, running the toolkit and ticking boxes
  (`.claude/rules/syntek-media/05-model-allocation.md`).
- **Concrete steps:**
  1. Read the piece's brief, with its `status` and `verified`, so the job starts at the right
     gate.
  2. Run the procedure; offer options and let the author choose every voice, take and cut.
  3. Write what it produces under `production/src/`, probe every output, and hand back the open
     questions as `AUTHOR TO CONFIRM` flags.
- **Definition of done:** the output exists where the procedure says; every source it uses is in
  the footage manifest and, where licensed or identifiable, in the rights register; every credit
  spent has its row in `production/src/credits-log.md`; and the brief records the gate it passed.

## Guardrails

- **Never spend unasked.** Every ElevenLabs call costs the author's credits: state the
  characters or minutes, the calls and the credits, and wait for a yes
  (`.claude/rules/syntek-media/03-production-ethics.md` Section 4).
- **Rights before publishing; consent before a likeness or a voice.** A licensed or identifiable
  item has its row in `production/src/rights-register.md` before it reaches a master, and no
  voice is cloned without the person's recorded consent.
- **Big binaries never sit in plain Git.** Footage lives in external storage and is listed in
  the manifest; renders and generated audio are git-ignored. Never force one in.
- **A take cannot be made again.** Approved generated audio is archived like source media before
  a master depends on it; for an audiobook, the approved mastered chapter.
- **Renders are generated.** Change the edit decision list, the cards or the sources and
  assemble again; never hand-edit a render.
- **Scaffolding is not progress.** A register full of planned rows brings no piece nearer; an
  approved master does.
- **Never overwrite** a master, a source file, a take or a register without confirming with the
  author.

## Output & naming

- **Written by skills and the toolkit:** segment registers in `production/src/voiceover/`, edit
  decision lists in `production/src/edits/`, cards in `production/src/cards/`;
<: if 'audiobook' in MEDIA_KINDS :>  chapter registers in `production/src/audiobook/`;
<: endif :>  rows in the footage manifest, the rights register and the credits log; a recorded
  piece's `transcript.md` in its piece folder.
- **Names:** a piece is `NNN-kebab-title`; a take `<piece>.sNN.tN.mp3`; a master
  `<piece>.master.mp4` (`.wav` for an audio master); footage and rights IDs (`F0001`, `RR0001`)
  are permanent. Dates are DD/MM/YYYY in prose and DD-MM-YYYY in filenames.
- **Generated (never hand-edit):** everything in `production/src/renders/` and in each folder
  named `generated`, which `production/src/.gitignore` ignores.
