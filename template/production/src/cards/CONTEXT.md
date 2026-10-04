# CONTEXT.md — production/src/cards/

The title and end cards a piece's master uses (and any other card its storyboard names), one HTML
file each. Every card is a copy of the brand's card component,
`brand/src/design-system/previews/card.html` (or `toolkit/templates/card.html` where the brand
has none), given the piece's words. `python3 toolkit/media.py assemble` renders each card to PNG
with `uv run toolkit/card.py` whenever the PNG is missing or older than the HTML or the brand's
tokens, so a master always rebuilds from tracked files. Thumbnails are not cards: they live in
`publishing/src/thumbnails/`.

## Directory Tree

```text
production/src/cards/
├── CONTEXT.md              ← this file
├── CLAUDE.md               ← operating rules
└── <piece>.<card>.html     ← one card (title, end, …), copied from the brand's component
```

## What's here

Each card keeps the layout contract of its component:

- `<!doctype html>` and `<html lang="en-GB">`, and a stylesheet link to
  `../../../brand/src/design-system/tokens.css` by relative path (the copy fixes the path);
  nothing is loaded over the network, and `card.py` fails a card that tries.
- One file serves every frame size through `aspect-ratio` media queries; text stays inside the
  safe-zone variables `card.py` sets for the frame being rendered.
- A card used as an overlay leaves its background transparent; images are linked by relative
  path, usually from `production/src/assets/`.
- **The words are the piece's; the layout is the brand's.** A layout change is made in the
  brand's component and synced, so it reaches every later piece.

A generated project may hold the worked example's title card, where it was kept; delete it with
the rest of the worked example once you no longer need it, and it will not come back.

## Cross-references

- `production/workflows/03-assemble-the-master/` — the procedure that copies a card and renders it.
- `production/docs/reference/edit-decision-lists.md` — a card as a clip, held, pushed in or
  overlaid.
- `brand/src/design-system/previews/card.html` — the brand's card component.
- `production/src/renders/` — where each card's PNG lands, git-ignored.
