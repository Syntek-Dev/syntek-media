@./CONTEXT.md

# CLAUDE.md — scripts/

Read order: `.claude/CLAUDE.md` → `.claude/MEMORY.md` → this folder's `CONTEXT.md`
(imported above) → this file.

## Purpose (one line)

Hold the plan and the words of every piece, so production always starts from an agreed brief,
an approved script and a storyboard, and never from memory.

## How to work here

- **Routing:** pick a procedure from `scripts/workflows/CLAUDE.md` (the `run-media-workflow`
  skill resolves `workflows/local/` first). A new piece → `scripts/workflows/01-brief-a-piece/`;
  its words → `scripts/workflows/02-write-a-script/`; its pictures →
  `scripts/workflows/03-storyboard-a-piece/`. A recorded talk or interview, once briefed, goes to
  `production/workflows/08-bring-in-a-recording/`, whose approved transcript stands in for a
  script. Guides: `scripts/docs/reference/`, overridden by same-named files in
  `scripts/docs/project/`.
- **Model:** **Opus** for every line a viewer or listener will hear or read, and for every
  judgement; the mechanical tier for renames, ticks and register rows the author has dictated
  (`.claude/rules/syntek-media/05-model-allocation.md`).
- **Concrete steps:**
  1. Identify the piece and read its brief, then the sublayer's `CONTEXT.md` and `CLAUDE.md`.
  2. For anything in `src/`, read the guide that governs it first (indexed in
     `scripts/docs/reference/CONTEXT.md`).
  3. Change the file, then check that the brief, the script (or transcript) and the storyboard
     still agree.
- **Definition of done:** every piece about to go into production has an approved brief, an
  approved script or transcript, and a storyboard or an `n/a` recorded against M3; each brief's
  `status` and `verified` say so honestly; nothing here contradicts `.claude/MEMORY.md`
  Decisions (under the heading syntek-author's project settings file, 00-project.md, maps it to,
  where present).

## Guardrails

- **Plans and words, not renders.** Nothing in this layer is cut, voiced or posted. A take, a
  render or a caption file belongs to the production or publishing layer.
- **Scaffolding is not progress.** Brief the next piece to be made, not every idea at once. A
  shelf of briefs with no approved script behind them reads as progress and is not.
- **The author approves; the AI proposes.** A brief, a script and a storyboard take effect only
  when the author has read them and said yes (`.claude/rules/syntek-media/03-production-ethics.md`
  Section 1).
- **Route, do not restate.** Project state lives in MEMORY and in each brief's frontmatter; a
  status copied anywhere else drifts from its owner within weeks.
- **Never overwrite** an existing brief, script, transcript, storyboard or shot list without
  confirming with the author.

## Output & naming

- **Hand-written (with the author):** each piece's `brief.md` and its folder's pair, and the
  piece register.
- **Written by skills:** `script.md` (`write-script`), `storyboard.md` and `shot-list.md`
  (`storyboard`), `transcript.md` (`captions`, through the production layer).
- **Generated (never hand-edit):** nothing; renders and generated audio live in the production
  and publishing layers.
- Piece folders `NNN-kebab-title`; other files kebab-case; dates DD/MM/YYYY in prose and
  DD-MM-YYYY in filenames.
