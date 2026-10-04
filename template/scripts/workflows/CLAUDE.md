@./CONTEXT.md

# CLAUDE.md — scripts/workflows/

Read order: `.claude/CLAUDE.md` → `.claude/MEMORY.md` → `scripts/CONTEXT.md` →
`scripts/CLAUDE.md` → this folder's `CONTEXT.md` (imported above) → this file → the chosen
procedure's own four files.

## Purpose (one line)

Hold the scripts layer's ordered procedures, so every piece is briefed, written and boarded the
same way every time, whoever runs it.

## How to work here

- **Routing:** pick by what you want; `run-media-workflow` checks `local/<slug>/` before the
  template's folder of the same slug.

| You want to… | Procedure | Usually followed by |
|---|---|---|
| Open a new piece and agree its brief | `scripts/workflows/01-brief-a-piece/` | `scripts/workflows/02-write-a-script/`, or `production/workflows/08-bring-in-a-recording/` for a recorded piece |
| Write, time and approve a piece's script | `scripts/workflows/02-write-a-script/` | `scripts/workflows/03-storyboard-a-piece/`, or `production/workflows/02-make-a-voiceover/` for a piece with no picture |
| Board a script and give every shot a source | `scripts/workflows/03-storyboard-a-piece/` | `production/workflows/01-log-source-media/` and `production/workflows/02-make-a-voiceover/` |

- **Model:** the `_opus_` / `_sonnet_` tags in each `CHECKLIST.md` are authoritative: Opus for
  every judgement and every line a viewer or listener will hear or read; the mechanical tier only
  for file creation, table edits and ticks (`.claude/rules/syntek-media/05-model-allocation.md`).
- **Concrete steps (running one):** read the procedure's `CONTEXT.md` → `CLAUDE.md` →
  `STEPS.md`, then work `STEPS.md` in order with `CHECKLIST.md` open.
- **Concrete steps (changing one):** only on the author's instruction. Change all four files
  together; keep steps ordered, numbered and marked _Substantive._ or _Mechanical._; record a
  change that overturns an earlier decision in `.claude/MEMORY.md`.
- **Definition of done (running):** every checklist item ticked or waived with a reason; the
  output is where the procedure says it is; the brief's `status` moved only through the gate the
  checklist cites; nothing the author has not agreed was recorded as decided.

## Guardrails

- **Order is load-bearing.** Steps that read and question come before steps that write for a
  reason: reversing them produces a brief or a script that has to be redone.
- **Procedures cite rules; they never restate them.** If a `STEPS.md` explains why a rule
  exists, that explanation has drifted out of its rules file. Point at the rules file.
- **Gates are cited, never restated.** Each checklist names its gate from
  `scripts/docs/reference/the-piece-ladder.md` as 'M2 (briefed → scripted)'.
- **A waived step is recorded, not silent.** Say which step, and why, in the hand-back.
- **Never renumber or reuse a number.** Numbering is frozen and append-only; a template
  procedure you do not want is overridden in `local/`, not deleted.
- **Template folders are template-owned.** Never edit them in place; copy one to `local/` under
  the same slug and change the copy, with the author's instruction.

## Output & naming

- **Folders:** `NN-verb-first-kebab-name/`, four files each. Nothing here is generated.
- **Procedures produce nothing here.** Their output lands in `scripts/src/`.
