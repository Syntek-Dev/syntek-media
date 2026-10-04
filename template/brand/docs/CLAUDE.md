@./CONTEXT.md

# CLAUDE.md — brand/docs/

Read order: `.claude/CLAUDE.md` → `.claude/MEMORY.md` → `brand/CONTEXT.md` → `brand/CLAUDE.md`
→ this folder's `CONTEXT.md` (imported above) → this file.

## Purpose (one line)

Keep the brand layer's guides in two places — template-owned reference, author-owned project —
with one precedence rule between them.

## How to work here

- **Routing:** to read a guide, look in `project/` first, then `reference/`; the first match by
  filename wins. To change how the brand is kept in this project, write or extend a guide in
  `project/`.
- **Model:** **Opus** for writing or revising a guide; the mechanical tier for renames
  (`.claude/rules/syntek-media/05-model-allocation.md`).
- **Concrete steps:**
  1. Read the reference guide you intend to override or extend.
  2. Write the project guide in the same shape: routing frontmatter, `# Title — gloss`, metadata
     header, `**What it is.**`, two to five topic sections, `## How we apply it here`,
     `## Who implements it`, `## Governing standard`.
  3. Name it for the question it answers, in kebab-case.
- **Definition of done:** a reader looking for how part of the brand is kept finds exactly one
  guide that answers it, and that guide cites the rules file that owns the requirement rather
  than restating it.

## Guardrails

- **Never edit `reference/` in place.** Override by name in `project/`; the reference copy keeps
  receiving template improvements, and the override records why this project differs.
- **A guide never outranks the rules.** If a guide and `.claude/rules/syntek-media/` disagree,
  the rules win and the guide is wrong; report it to the author.
- **Defer, do not restate.** A guide that copies a rule's wording drifts from it.
- **Short guides get read.** Keep each guide under 300 lines; most should run 54–82.

## Output & naming

- **Hand-written:** guides in `project/`, kebab-case, named for the question they answer.
- **Template-owned:** everything in `reference/`.
