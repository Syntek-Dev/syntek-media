@./CONTEXT.md

# CLAUDE.md — scripts/src/

Read order: `.claude/CLAUDE.md` → `.claude/MEMORY.md` → `scripts/CONTEXT.md` →
`scripts/CLAUDE.md` → this folder's `CONTEXT.md` (imported above) → this file → the target
piece's `CONTEXT.md` and `CLAUDE.md`.

## Purpose (one line)

Keep every piece's brief, words and picture plan current and consistent with each other, so each
production session starts from the same picture of the piece.

## How to work here

- **Routing:** each file has one writer and one procedure.

| File | Written by | Procedure |
|---|---|---|
| `piece-register.md`, a piece's folder, its pair and `brief.md` | the author, with the grill-with-docs skill (syntek-author), where present | `scripts/workflows/01-brief-a-piece/` |
| a scripted piece's `script.md` | `write-script` | `scripts/workflows/02-write-a-script/` |
| a recorded piece's `transcript.md` | `captions` | `production/workflows/08-bring-in-a-recording/` |
| `storyboard.md`, `shot-list.md` | `storyboard` | `scripts/workflows/03-storyboard-a-piece/` |

- **Model:** **Opus** for any brief, script line, board or judgement; the mechanical tier for a
  register row the author has dictated, renames and ticks
  (`.claude/rules/syntek-media/05-model-allocation.md`).
- **Concrete steps:** read the governing guide (`scripts/docs/reference/CONTEXT.md`); run the
  procedure in the table; after any change, check the brief, the script (or transcript) and the
  storyboard still agree with each other. A brief's `status` and `verified` move only as
  `scripts/docs/reference/the-piece-ladder.md` allows, through the procedure that serves the
  gate.
- **Definition of done:** no two files of a piece contradict each other, none contradicts a dated
  decision in `.claude/MEMORY.md`, and every brief's `status` is one its `verified` record earns.

## Guardrails

- **One sentence per line** in every artefact here, applied when a paragraph is edited, never by
  mass reflow (`.claude/rules/syntek-media/06-global-rules.md` Section 5). In a script or
  transcript that is one spoken sentence per line, by nature.
- **Report contradictions; never silently repair them.** When a brief, a script and a storyboard
  disagree, tell the author which is which. They decide which one is wrong.
- **Numbers are permanent.** A piece number, a board row (`B01`) and a shot (`S01`) keep their
  IDs for life; a retired piece keeps its register row, and its number is never reused.
- **No invented entries.** A row records something the author agreed or the work established.
  Never fill the register with plausible examples.
- **Never overwrite** an existing brief, script, transcript, storyboard or shot list without
  confirming with the author.

## Output & naming

- **Hand-written (with the author):** the register, and each piece's folder, pair and brief.
- **Written by skills:** `script.md`, `transcript.md`, `storyboard.md`, `shot-list.md`, in the
  piece's folder.
- **Kept current by procedures:** each brief's `status`, `verified` and `last_updated`.
- Piece folders `NNN-kebab-title`; dates DD/MM/YYYY in prose and DD-MM-YYYY in filenames.
