@./CONTEXT.md

# CLAUDE.md — brand/docs/project/

Read order: `.claude/CLAUDE.md` → `.claude/MEMORY.md` → `brand/CONTEXT.md` → `brand/CLAUDE.md`
→ `brand/docs/CONTEXT.md` → `brand/docs/CLAUDE.md` → this folder's `CONTEXT.md` (imported
above) → this file.

## Purpose (one line)

Hold the author's own brand guides, which take precedence over the template's.

## How to work here

- **Routing:** a guide here is read before the reference guide of the same name. Write one only
  on the author's instruction, after reading the reference guide it overrides or extends.
- **Model:** **Opus** for writing a guide (`.claude/rules/syntek-media/05-model-allocation.md`).
- **Concrete steps:**
  1. Agree with the author what the guide must settle, and why the reference guide does not.
  2. Write it in the reference shape (`brand/docs/CLAUDE.md`), citing its rules file.
  3. Where it extends rather than replaces a reference guide, say so under
     `## How we apply it here` and keep the reference guide's name only if it replaces it.
  4. Add a line for it under `## What's here` in this folder's `CONTEXT.md`.
- **Definition of done:** the author has approved the guide, and it states plainly which
  reference guide, if any, it overrides.

## Guardrails

- **Author-owned.** `copier update` never touches files here, this seeded pair included;
  nothing here is improved by the template, so keep each guide current yourself.
- **An override replaces, it does not merge.** A same-named guide hides the reference guide
  completely; copy across anything from it you still need.
- **Never overwrite** an existing guide without confirming with the author.

## Output & naming

- **Hand-written:** `<question>.md`, kebab-case, under 300 lines.
