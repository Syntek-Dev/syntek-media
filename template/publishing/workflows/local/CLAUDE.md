@./CONTEXT.md

# CLAUDE.md — publishing/workflows/local/

Read order: `.claude/CLAUDE.md` → `.claude/MEMORY.md` → `publishing/CONTEXT.md` →
`publishing/CLAUDE.md` → `publishing/workflows/CONTEXT.md` → `publishing/workflows/CLAUDE.md` →
this folder's `CONTEXT.md` (imported above) → this file.

## Purpose (one line)

Hold the author's own publishing procedures, which run in place of a template procedure with the
same slug.

## How to work here

- **Routing:** write a procedure here only on the author's instruction, and only for publishing
  work that genuinely recurs. To change a template procedure, copy its folder here under the
  same slug and edit the copy.
- **Model:** **Opus** for writing a procedure; its checklist tags then govern each run
  (`.claude/rules/syntek-media/05-model-allocation.md`).
- **Concrete steps:**
  1. Agree with the author what the procedure is for and when it runs.
  2. Write all four files in the template's shape: routing frontmatter (`workflow`, `phase`,
     `skills`, `model`) on `STEPS.md` and `CHECKLIST.md`, the metadata header, numbered steps
     ending _Substantive._ or _Mechanical._, and checklist items tagged with their tier.
  3. Number a new procedure next in this folder's sequence; keep the template's slug for an
     override.
  4. Add a row to the table in this folder's `CONTEXT.md`.
- **Definition of done:** the author has approved all four files, and the router would pick the
  procedure for the request it is meant for.

## Guardrails

- **Author-owned.** `copier update` never touches files here, this seeded pair included, and
  never improves them; an override stops receiving the template's changes to the procedure it
  replaces.
- **Four files or none.** A procedure missing one of its files is incomplete.
- **Never post.** A local procedure may change how a deliverable is made or packaged; it never
  lets anything reach a platform without the author posting it.
- **Never overwrite** an existing procedure without confirming with the author.

## Output & naming

- **Hand-written:** `NN-verb-first-name/`, kebab-case, four files each.
