# CONTEXT.md — publishing/src/thumbnails/

The thumbnails and covers of every piece, as tracked source: a brief in words, and an HTML layout
copied from the brand's own thumbnail component and filled for this piece, or for one cut. The
PNGs a platform receives are rendered from these files by `uv run toolkit/card.py` into
`publishing/src/renders/`, so a thumbnail can always be remade, and a change to the brand's tokens
reaches it on the next render.

## Directory Tree

```text
publishing/src/thumbnails/
├── CONTEXT.md            ← this file
├── CLAUDE.md             ← operating rules, and the brief's skeleton
├── <piece>.md            ← the brief for the piece's full-length deliverables
├── <piece>.html          ← its layout, copied from the brand's thumbnail component
└── <piece>--cNN.md/.html ← a brief and layout for one cut, where the cut needs its own
```

## What's here

- `<piece>[--cNN].md` — a brief, written by `thumbnail-brief` with the author. **The shape is
  fixed by `publishing/docs/reference/thumbnails.md`**: frontmatter `piece`, `cut`, `deliverables`,
  `html`, `approved`; then `## Promise` · `## Words on the image` · `## Image` · `## Variants` ·
  `## Checks`. The skeleton is fenced in this folder's `CLAUDE.md`.
- `<piece>[--cNN].html` — the layout, a copy of `brand/src/design-system/previews/thumbnail.html`
  (or of `toolkit/templates/thumbnail.html` where the brand has none), with its stylesheet link
  fixed to reach `brand/src/design-system/tokens.css` from this folder, by relative path. It loads
  nothing over the network.
- A generated project may hold one worked example brief and layout, where they were kept; delete
  them, with the other example files, once you no longer need them, and none of them will come
  back.

## Cross-references

- `publishing/docs/reference/thumbnails.md` — the brief, the layout, which deliverables take one,
  and the checks.
- `publishing/workflows/04-brief-a-thumbnail/` — the procedure that writes and renders them.
- `brand/docs/reference/the-brand-kit.md` — the tokens and the brand's layout components.
