# CONTEXT.md — brand/src/design-system/previews/

The preview cards: one small HTML page per part of the kit, each opening on line 1 with the
`@dsCard` comment Claude Design reads to build its Design System pane, and each linking
`../tokens.css` so it shows the tokens as they stand. Five cards only show the kit. Two are the
brand's layout components: `thumbnail.html` is the layout every thumbnail and cover is copied
from, and `card.html` the layout every title and end card is copied from. All seven are seeds,
written once and then the author's.

## Directory Tree

```text
brand/src/design-system/previews/
├── CONTEXT.md          ← this file
├── CLAUDE.md           ← operating rules and the layout contract
├── colors.html         ← seed (Colors): every colour token as a swatch
├── type.html           ← seed (Type): the display and body faces at their weights
├── spacing.html        ← seed (Spacing): multiples of the space unit, and the radius
├── brand.html          ← seed (Brand): the brand's name as it appears on screen
├── captions.html       ← seed (Components): a burned caption in the caption tokens, over a frame
├── thumbnail.html      ← seed (Components): the brand's thumbnail and cover layout
└── card.html           ← seed (Components): the brand's title and end card layout
```

## What's here

- **Line 1 of every card is `<!-- @dsCard group="…" -->`,** with the group `Colors`, `Type`,
  `Spacing`, `Brand` or `Components`. Claude Design builds its card index from that line alone.
- **The two layout components** meet the layout contract (`CLAUDE.md` here): one file serves
  every aspect ratio, text stays inside the safe zone the renderer sets, and nothing loads over
  the network. `thumbnail-brief` copies `thumbnail.html` for each piece's thumbnails and covers;
  `cut-for-platform` copies `card.html` for its title and end cards. Each falls back to
  `toolkit/templates/` only where the brand's file is absent.
- A change to a layout here reaches every piece copied **after** it, and never a copy already
  made, which belongs to its piece.

## Cross-references

- `brand/docs/reference/the-brand-kit.md` — the tokens these cards show, and the two layouts.
- `brand/docs/reference/claude-design.md` — how a card is synced with the design project.
- `publishing/docs/reference/thumbnails.md` — how a piece's thumbnail is briefed and rendered.
- `toolkit/templates/` — the fallback layouts.
