@./CONTEXT.md

# CLAUDE.md — production/workflows/local/

Read order: `.claude/CLAUDE.md` → `.claude/MEMORY.md` → `production/CONTEXT.md` →
`production/CLAUDE.md` → `production/workflows/CONTEXT.md` → `production/workflows/CLAUDE.md`
→ this folder's `CONTEXT.md` (imported above) → this file.

## Purpose (one line)

Hold the production procedures that belong to this project alone, and the overrides of template
procedures the author has chosen.

## How to work here

- **Routing:** `run-media-workflow` resolves local first: a folder here with the same slug as
  one in `production/workflows/` wins.
- **Model:** **Opus** for writing or changing a procedure; the checklist tags decide each item
  when it runs (`.claude/rules/syntek-media/05-model-allocation.md`).
- **Concrete steps (adding one):**
  1. Confirm with the author that the job recurs; a one-off needs no procedure.
  2. Number it in this folder's own sequence (`01-`, `02-` …), or reuse a template slug exactly
     to override that procedure.
  3. Write all four files in the template's shape: routing frontmatter (`workflow`, `phase`,
     `skills`, `model`) on `STEPS.md` and `CHECKLIST.md`, the metadata header, steps that name
     their skill and guide and end _Substantive._ or _Mechanical._, checklist items tagged with
     the model tier.
  4. Add a row to the table in this folder's `CONTEXT.md`.
- **Definition of done:** the four files exist, the index row is added, and the author has
  agreed the procedure.

## Guardrails

- **Author-owned.** Create or change a procedure here only on the author's instruction.
- **An override replaces the whole template procedure.** Carry across every step you still
  need; nothing from the template version runs.
- **An override never relaxes a gate.** A local procedure may add a check to a gate of
  `scripts/docs/reference/the-piece-ladder.md`, never remove or weaken one, and never spend a
  credit without stating the cost first.
- **Never overwrite an existing local procedure** without confirming with the author.

## Output & naming

- **Hand-written:** `<NN>-<verb-first-name>/` with `CONTEXT.md`, `CLAUDE.md`, `STEPS.md` and
  `CHECKLIST.md`.
- **Generated:** nothing here.
