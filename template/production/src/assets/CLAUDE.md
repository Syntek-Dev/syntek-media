@./CONTEXT.md

# CLAUDE.md — production/src/assets/

Read order: `.claude/CLAUDE.md` → `.claude/MEMORY.md` → `production/CONTEXT.md` →
`production/CLAUDE.md` → `production/src/CONTEXT.md` → `production/src/CLAUDE.md` → this
folder's `CONTEXT.md` (imported above) → this file.

## Purpose (one line)

Keep the few small images a piece shows on screen beside the edit that uses them, so a master
rebuilds from tracked files.

## How to work here

- **Routing:** skill `cut-for-platform`; workflow `production/workflows/03-assemble-the-master/`;
  guide `production/docs/reference/edit-decision-lists.md`.
- **Model:** **Opus** for choosing an image and judging its rights; the mechanical tier for
  adding the file the author supplied (`.claude/rules/syntek-media/05-model-allocation.md`).
- **Concrete steps:** confirm the image and its source with the author → check or open its rights
  row → add it under a kebab-case name → cite it from the edit decision list or the card.
- **Definition of done:** the file is under 10 MB, its name says what it shows, and anything
  licensed or showing a person has its rights row.

## Guardrails

- **Under 10 MB each.** `python3 toolkit/media.py check` flags a larger file outside the
  ignored and LFS folders; log it as source media instead.
- **Rights first.** A stock image, a cover, a photograph of a person or someone else's artwork
  has its row in `production/src/rights-register.md` before an edit names it.
- **Never generate an image here unasked**, and record an AI-generated image in the piece's
  brief, because it is disclosed at publish.
- **Never overwrite an asset an edit names.** Add the new version under a new name and change
  the edit, so the old master can still be rebuilt.

## Output & naming

- **Hand-written (with the author):** `<kebab-name>.png`, `.jpg` or `.svg`, under 10 MB.
- **Not here:** fonts (`brand/src/design-system/fonts/`), exported brand designs
  (`brand/src/exports/`), footage and recordings (`production/src/footage/`).
- **Generated:** nothing here.
