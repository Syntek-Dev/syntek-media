# CONTEXT.md — brand/src/design-system/

The brand kit as files: one stylesheet of tokens, the font files it loads, and the preview cards
that show the kit to Claude Design. It is plain HTML and CSS by decision: no React, no Node, no
package and no `tokens.json`, so every renderer in the toolkit reads exactly what the author
edits. This folder is the source of truth; the brand's design-system project in Claude Design is
kept in step with it, one component at a time. Exported design assets are not here
(`brand/src/exports/`), and neither is a piece's own thumbnail or card.

## Directory Tree

```text
brand/src/design-system/
├── CONTEXT.md          ← this file
├── CLAUDE.md           ← operating rules
├── tokens.css          ← seed: every custom property a layout or a burned caption reads
├── fonts/              ← the brand's font files, loaded by tokens.css; licences in the rights register
└── previews/           ← colors · type · spacing · brand · captions · thumbnail · card (.html)
```

## What's here

- `tokens.css` — **the one stylesheet every layout imports.** One `:root` block holds the
  required custom properties (colour, type, space and caption groups) and any the brand adds;
  one `@font-face` rule per file in `fonts/` loads the brand's faces. It ships with neutral greys,
  generic font families and an `AUTHOR TO CONFIRM` slot per group.
- `fonts/` — font files the author supplies, referenced from `tokens.css` as `url("fonts/…")`.
- `previews/` — seven cards, each opening on line 1 with the `@dsCard` comment Claude Design
  indexes and linking ../tokens.css. `thumbnail.html` and `card.html` are the brand's layout
  components: `thumbnail-brief` and `cut-for-platform` copy them for every new piece.

`python3 toolkit/media.py tokens` checks that every required token is present and parses;
`uv run toolkit/card.py check` checks a card against the layout contract.

## Cross-references

- `brand/docs/reference/the-brand-kit.md` — the required tokens, fonts and the two layouts.
- `brand/docs/reference/claude-design.md` — how this folder and the Claude Design project stay
  in step.
- `brand/workflows/01-set-up-the-brand-kit/` — the procedure that settles the kit.
- `toolkit/templates/` — the fallback layouts, used only where the brand's are absent.
