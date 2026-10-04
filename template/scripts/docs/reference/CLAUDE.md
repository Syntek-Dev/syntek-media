@./CONTEXT.md

# CLAUDE.md — scripts/docs/reference/

Read order: `.claude/CLAUDE.md` → `.claude/MEMORY.md` → `scripts/CONTEXT.md` →
`scripts/CLAUDE.md` → `scripts/docs/CONTEXT.md` → `scripts/docs/CLAUDE.md` → this folder's
`CONTEXT.md` (imported above) → this file.

## Purpose (one line)

Serve the template's guides for planning and writing a piece read-only, so every project carries
a piece the same way until its author decides otherwise in `scripts/docs/project/`.

## How to work here

- **Routing:** check `scripts/docs/project/` for a same-named override first; if none exists,
  the guide here applies. The skill and workflow each guide names are the ones to run. For a
  piece, read the ladder guide, the guide for the file you are changing, and the guide for the
  piece's kind where the project makes that kind (all listed in `CONTEXT.md`).
- **Model:** **Opus** for reading a guide into a judgement; nothing here is written
  (`.claude/rules/syntek-media/05-model-allocation.md`).
- **Concrete steps:**
  1. Find the guide for the question in `CONTEXT.md`.
  2. Check `scripts/docs/project/` for an override of the same name.
  3. Apply the guide through the workflow it names; follow the rules file it cites where they
     differ.
- **Definition of done:** the piece you worked on follows the guide (or its override), and any
  point where the guide did not fit has been reported to the author rather than improvised
  around.

## Guardrails

- **Read-only.** These files are template-owned and updated by `copier update`. To change one
  for this project, copy it to `scripts/docs/project/` under the same name and edit the copy,
  with the author's instruction.
- **Never self-edit.** No skill rewrites a guide without the author's explicit instruction
  (`.claude/rules/syntek-media/06-global-rules.md` Section 3).
- **The ladder binds every piece.** An override of the ladder guide may add a check to a gate,
  never remove or weaken one (`.claude/rules/syntek-media/03-production-ethics.md` Section 3).
- **A guide never outranks the rules.** Where a guide and the rules file it cites disagree, the
  rules file wins; report the disagreement.

## Output & naming

- **Template-owned:** every guide here. Nothing in this folder is generated or written by a
  skill.
- A guide for a kind of piece ships only while that kind is among the project's media kinds;
  removing the kind through Copier deletes its guide.
