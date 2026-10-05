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
├── thumbnail.html      ← one thumbnail, image and cover layout for every aspect: 1.91:1, 16:9, 1:1, 4:5 and 9:16
└── card.html           ← title and end cards: a lower-third title or a centred end card
```

## What's here

- `thumbnail.html` — **the fallback for the brand's thumbnail.** `thumbnail-brief` copies it to
  `publishing/src/thumbnails/<piece>[--cNN].html` and changes only the copy: the words, and the
  picture, set on the frame as
  `style="--picture: url('../../../production/src/assets/<still>.png')"`: a small committed
  still in `production/src/assets/` (a frame is extracted there with `media.py frame -o`), never
  a git-ignored render, so the layout rebuilds from tracked files. The title sits low on a 16:9
  frame (smaller on a 1.91:1 share image), full width on a square or 4:5 cover, and in the
  middle band of a 9:16 cover, inside the profile grid's crop. The same layout serves the brand's
  own channels' images (share, featured and preview images), which `media.py image` then encodes
  into their formats.
- **The play button** (DESIGN D57): an element carrying `data-play-button`, shown only under
  `:root[data-deliverable^="newsletter."]`, which `card.py render --deliverable` sets with
  `data-platform`. It is a solid disc in `--color-accent` with an outline in `--color-on-accent`
  and a ring of `--color-accent` around that, so it survives an email client's dark-mode
  inversion, with a triangle in `--color-on-accent`; it sits centred in the space above the words.
  Rendered with `--transparent` for a newsletter key, the layout keeps only the play button and
  the words, outlined with `--color-bg`, over a transparent background: that PNG is a newsletter
  GIF's overlay (`media.py cut … --overlay`). The brand's own
  `brand/src/design-system/previews/thumbnail.html` carries the same element and rules; a
  layout without them (a brand kit made before 0.2.0) gets them added to the piece's copy by
  `thumbnail-brief`, copied from this file.
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
