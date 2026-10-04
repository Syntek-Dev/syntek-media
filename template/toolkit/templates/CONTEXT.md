# CONTEXT.md — toolkit/templates/

The toolkit's fallback layouts: a thumbnail and a card, in plain HTML and CSS, reading every
colour, face, weight and space from the brand's `brand/src/design-system/tokens.css`. They are used
only where the brand has no layout of its own: the brand's components,
`brand/src/design-system/previews/thumbnail.html` and `brand/src/design-system/previews/card.html`,
always win, and they are what a change in Claude Design reaches. A piece never edits a file here;
it copies one.

## Directory Tree

```text
toolkit/templates/
├── CONTEXT.md          ← this file
├── CLAUDE.md           ← operating rules
├── thumbnail.html      ← one thumbnail and cover layout for every aspect: 16:9, 1:1, 4:5 and 9:16
└── card.html           ← title and end cards: a lower-third title or a centred end card
```

## What's here

- `thumbnail.html` — **the fallback for the brand's thumbnail.** `thumbnail-brief` copies it to
  `publishing/src/thumbnails/<piece>[--cNN].html` and changes only the copy: the words, and the
  picture, set on the frame as `style="--picture: url('../renders/<still>.png')"`. The title sits
  low on a 16:9 frame, full width on a square or 4:5 cover, and in the middle band of a 9:16 cover,
  inside the profile grid's crop.
- `card.html` — **the fallback for the brand's card.** `cut-for-platform` copies it to
  `production/src/cards/<piece>.<card>.html` and changes only the copy: the words and the body's
  class. `title` is a lower-third title; `end` is a centred end card with its call to action. The
  background is transparent, so an `[[overlay]]` rendered with `--transparent` lays it over the
  picture; a card used as a `[[clip]]` adds the class `solid`, or it renders on white.
- **The layout contract** both meet, as every piece's copy must: `<!doctype html>` and
  `<html lang="en-GB">`; one stylesheet link to `tokens.css` by relative path, fixed on copy (from
  `publishing/src/thumbnails/` or `production/src/cards/` it climbs three folders,
  ../../../brand/src/design-system/tokens.css); `html, body` at the full frame with no margin or
  overflow; one file for every aspect through `aspect-ratio` media queries; words inside
  `--safe-top`, `--safe-right`, `--safe-bottom` and `--safe-left`, which `uv run toolkit/card.py`
  sets on `:root` with `--frame-width` and `--frame-height`; images by relative path; nothing
  over the network. Neither carries an `@dsCard` line: that marks the brand's preview cards only.
- **Each carries an `AUTHOR TO CONFIRM` flag** on its words, so a copy lists in `media.py flags`
  until the author has written the piece's own.

## Cross-references

- `toolkit/card.py` — renders a layout to PNG and checks it against the contract.
- `brand/docs/reference/the-brand-kit.md` — the tokens and the brand's two layout components.
- `publishing/docs/reference/thumbnails.md` — per-cut thumbnails, small sizes and the grid crop.
- `production/docs/reference/edit-decision-lists.md` — cards as clips and as overlays.
