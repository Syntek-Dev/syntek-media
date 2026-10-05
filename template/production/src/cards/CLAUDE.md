@./CONTEXT.md

# CLAUDE.md — production/src/cards/

Read order: `.claude/CLAUDE.md` → `.claude/MEMORY.md` → `production/CONTEXT.md` →
`production/CLAUDE.md` → `production/src/CONTEXT.md` → `production/src/CLAUDE.md` → this
folder's `CONTEXT.md` (imported above) → this file.

## Purpose (one line)

Give every card a master shows a tracked home, in the brand's own layout, so a master never waits
on a file made somewhere else.

## How to work here

- **Routing:** skill `cut-for-platform`; workflow `production/workflows/03-assemble-the-master/`;
  guide `production/docs/reference/edit-decision-lists.md`. A change to the layout itself is the
  brand layer's job (`brand/workflows/02-sync-with-claude-design/`).
- **Model:** **Opus** for a card's words, with the author; the mechanical tier for copying the
  component, fixing its path and rendering (`.claude/rules/syntek-media/05-model-allocation.md`).
- **Concrete steps:** copy the brand's component to `<piece>.<card>.html` → fix the tokens link
  to `../../../brand/src/design-system/tokens.css` → write the card's words with the author →
  `uv run toolkit/card.py check` → let `assemble` render it.
- **Definition of done:** the card passes `card.py check`, its words are the author's, and its
  PNG renders at the master's frame size.

## Guardrails

- **Copy, never edit the brand's component here.** Its layout reaches every later piece only if
  it is changed at its source.
- **Words only.** Change a card's text, not its layout; a layout the brand needs is a component
  change, agreed with the author.
- **Nothing over the network.** Fonts come from the brand's `@font-face` rules and images by
  relative path; `card.py` aborts every outside request.
- **PNGs are generated.** Never commit a card's PNG, and never hand-edit one.
- **Never overwrite a card** a master already uses without confirming with the author.

## Output & naming

- **Written by skills:** `<piece>.<card>.html`, by `cut-for-platform`, with `<card>` a kebab-case
  word (`title`, `end`).
- **Generated (never hand-edit):** `<piece>.<card>.<W>x<H>.png` in
  `production/src/renders/<piece>/cards/`, rendered by `assemble` through
  `uv run toolkit/card.py render`, and `<piece>.<card>.<W>x<H>.transparent.png` beside it for a
  card laid over the picture, so a card used as a clip and as an overlay at one size keeps both
  renders.
