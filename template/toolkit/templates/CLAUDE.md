@./CONTEXT.md

# CLAUDE.md — toolkit/templates/

Read order: `.claude/CLAUDE.md` → `.claude/MEMORY.md` → `toolkit/CONTEXT.md` →
`toolkit/CLAUDE.md` → this folder's `CONTEXT.md` (imported above) → this file.

## Purpose (one line)

Give a piece a working thumbnail and card even before the brand has its own layouts, without ever
standing in for the brand's look once it has them.

## How to work here

- **Routing:** `thumbnail-brief` copies `thumbnail.html` and `cut-for-platform` copies `card.html`,
  each only where the brand's own component under `brand/src/design-system/previews/` is absent.
  A change to how the brand looks belongs in those components
  (`brand/workflows/01-set-up-the-brand-kit/`, `brand/workflows/02-sync-with-claude-design/`),
  never here.
- **Model:** the mechanical tier for copying a layout and fixing its path; **Opus** for the words
  a copy carries and for any change to a layout here
  (`.claude/rules/syntek-media/05-model-allocation.md`).
- **Concrete steps (copying a layout for a piece):**
  1. Check for the brand's component first; copy this folder's file only when it is absent, and
     say so to the author.
  2. Fix the copy's stylesheet link: from either folder it climbs three folders,
     ../../../brand/src/design-system/tokens.css.
  3. Write the copy's words with the author and remove its `AUTHOR TO CONFIRM` flag.
  4. Run `uv run toolkit/card.py check` on the copy, then render it at the deliverable's size.
- **Definition of done:** the copy passes `card.py check`, and its PNG renders at the size asked
  with nothing fetched over the network.

## Guardrails

- **Copy, never edit here for one piece.** These files are template-owned and replaced by
  `copier update`; a piece's words live in its copy.
- **Tokens only.** Every colour, face, weight and space comes from `tokens.css`; a value typed
  into a layout drifts from the brand at its next change.
- **Nothing over the network.** No web fonts, no remote images, no scripts from elsewhere;
  `card.py` aborts every outside request and reports it.
- **Keep the brand's classes.** These layouts use the same structure and classes as the brand's
  seeded components, so a piece moves from one to the other without rewriting its words.

## Output & naming

- **Template-owned:** `thumbnail.html`, `card.html`.
- **Written by skills (elsewhere):** `publishing/src/thumbnails/<piece>[--cNN].html` and
  `production/src/cards/<piece>.<card>.html`, copies of these or of the brand's components.
- **Generated (never hand-edit):** their PNGs, in `publishing/src/renders/` and
  `production/src/renders/`.
