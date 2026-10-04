@./CONTEXT.md

# CLAUDE.md — brand/src/design-system/

Read order: `.claude/CLAUDE.md` → `.claude/MEMORY.md` → `brand/CONTEXT.md` → `brand/CLAUDE.md`
→ `brand/src/CONTEXT.md` → `brand/src/CLAUDE.md` → this folder's `CONTEXT.md` (imported above)
→ this file.

## Purpose (one line)

Keep the brand's tokens, fonts and layouts in plain files that every render reads and Claude
Design can sync, so a brand change is made once and every later piece follows.

## How to work here

- **Routing:** workflow `brand/workflows/01-set-up-the-brand-kit/` for any change to the kit;
  `brand/workflows/02-sync-with-claude-design/` to bring a component across; guide
  `brand/docs/reference/the-brand-kit.md`.
- **Model:** **Opus** for every token and layout decision and for judging a proof; the
  mechanical tier for running `media.py tokens` and `card.py check`
  (`.claude/rules/syntek-media/05-model-allocation.md`).
- **Concrete steps:** read the guide → change one token group or one card with the author →
  `python3 toolkit/media.py tokens` → `uv run toolkit/card.py check` on every card the change
  touches → render a proof at a landscape and a vertical size into `production/src/renders/` →
  the author approves → commit before any sync.
- **Definition of done:** every required token is present and parses; every card passes
  `card.py check`; the author has seen a proof; no `AUTHOR TO CONFIRM` slot is left in a token
  group a layout uses.

## Guardrails

- **Every layout reads `tokens.css`.** Never write a colour value, a font name or a pixel margin
  into a card; add a token instead.
- **The required tokens are never renamed or removed.** The toolkit reads them by name; a brand
  may add tokens of its own beside them.
- **Nothing loads over the network.** Fonts and images are referenced by relative path;
  `card.py` aborts every http(s) request and fails the render.
- **Line 1 of every preview card is its `@dsCard` comment.** Anything above it hides the card from
  Claude Design.
- **A font enters with its licence.** No font file is added without a `font` row in
  `production/src/rights-register.md`, checked against use in video.
- **Never overwrite** `tokens.css` or a card without confirming with the author, and never
  replace the kit wholesale from Claude Design.

## Output & naming

- **Hand-written (with the author):** `tokens.css`, the cards in `previews/`, fonts in `fonts/`.
- **Copied from here by skills:** `previews/thumbnail.html` to `publishing/src/thumbnails/`
  (`thumbnail-brief`) and `previews/card.html` to `production/src/cards/` (`cut-for-platform`),
  each copy fixing its relative path to `tokens.css`.
- **Generated (never hand-edit):** nothing here; proofs go to the git-ignored
  `production/src/renders/`.
