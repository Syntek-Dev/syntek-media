@./CONTEXT.md

# CLAUDE.md — brand/docs/reference/

Read order: `.claude/CLAUDE.md` → `.claude/MEMORY.md` → `brand/CONTEXT.md` → `brand/CLAUDE.md`
→ `brand/docs/CONTEXT.md` → `brand/docs/CLAUDE.md` → this folder's `CONTEXT.md` (imported
above) → this file.

## Purpose (one line)

Serve the template's brand guides read-only, so every project keeps its brand the same way until
its author decides otherwise in `brand/docs/project/`.

## How to work here

- **Routing:** check `brand/docs/project/` for a same-named override first; if none exists, the
  guide here applies. The skill and workflow each guide names are the ones to run.
- **Model:** **Opus** for reading a guide into a judgement; nothing here is written
  (`.claude/rules/syntek-media/05-model-allocation.md`).
- **Concrete steps:**
  1. Find the guide for the question in `CONTEXT.md`.
  2. Check `brand/docs/project/` for an override of the same name.
  3. Apply the guide through the workflow it names; follow its rules file where they differ.
- **Definition of done:** the brand file you changed follows the guide (or its override), and any
  point where the guide did not fit has been reported to the author rather than improvised
  around.

## Guardrails

- **Read-only.** These files are template-owned and updated by `copier update`. To change one
  for this project, copy it to `brand/docs/project/` under the same name and edit the copy, with
  the author's instruction.
- **Never self-edit.** No skill rewrites a guide without the author's explicit instruction
  (`.claude/rules/syntek-media/06-global-rules.md` Section 3).
- **A guide never outranks the rules.** Where a guide and its rules file disagree, the rules
  win; report the disagreement.

## Output & naming

- **Template-owned:** every guide here. Nothing in this folder is generated or written by a
  skill.
