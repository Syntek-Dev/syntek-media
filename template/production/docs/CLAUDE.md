@./CONTEXT.md

# CLAUDE.md — production/docs/

Read order: `.claude/CLAUDE.md` → `.claude/MEMORY.md` → `production/CONTEXT.md` →
`production/CLAUDE.md` → this folder's `CONTEXT.md` (imported above) → this file.

## Purpose (one line)

Hold the guides that explain how this project's masters are made, split into the template's
reference guides and the author's own.

## How to work here

- **Routing:** a guide is read, not run. The workflow you are following names the guide it
  needs; read `production/docs/project/` first, because a same-named project guide overrides
  the reference one.
- **Model:** **Opus** for writing or revising a guide; the mechanical tier for renames and link
  fixes (`.claude/rules/syntek-media/05-model-allocation.md`).
- **Concrete steps (adding a project guide):**
  1. Confirm with the author that the guidance recurs; a one-off decision belongs in
     `.claude/MEMORY.md` or in the register it concerns.
  2. Write it in `production/docs/project/` in the guide format: routing frontmatter, a title
     with a gloss, the metadata header, **What it is.**, two to five topic sections,
     `## How we apply it here`, `## Who implements it`, `## Governing standard`.
  3. Name the file for the question it answers, in kebab-case.
- **Definition of done:** the guide is 54–82 lines, defers to the rules file it serves rather
  than restating it, and names the skill and workflow that apply it.

## Guardrails

- **Never edit `production/docs/reference/`.** It is template-owned and `copier update`
  replaces it. Override with a same-named file in `production/docs/project/`, or extend through
  that file's `## How we apply it here`.
- **Defer, do not restate.** A guide that repeats a rule drifts from it. Cite the rules file and
  section, and explain the everyday call.
- **No project facts in guides.** A guide says how to decide; the decision goes in a register
  under `production/src/`.
- **Never overwrite an existing project guide** without confirming with the author.

## Output & naming

- **Hand-written:** project guides, kebab-case, one question per file.
- **Generated:** nothing here.
