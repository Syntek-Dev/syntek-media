# CONTEXT.md — publishing/src/thumbnails/

The thumbnails, covers and other images of every piece, as tracked source: a brief in words, and
an HTML layout copied from the brand's own thumbnail component and filled for this piece, or for
one cut. Every image deliverable is briefed here: a thumbnail or cover, a podcast episode's art, a
web page's poster and share image, a blog's featured image, a newsletter's preview image and its
GIF preview. The files a platform or page receives are rendered from these by
`uv run toolkit/card.py`, encoded or framed by `python3 toolkit/media.py image`, and, for the GIF,
cut by `media.py cut` under the layout's overlay, all into `publishing/src/renders/`, so every
image can be remade, and a change to the brand's tokens reaches it on the next render.

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
  `## Checks`. `## Image` records every moment taken from a render: each poster's `--at` on its
  video's render, and the GIF's In and Out on the master and what its first frame shows. The
  skeleton is fenced in this folder's `CLAUDE.md`.
- `<piece>[--cNN].html` — the layout, a copy of `brand/src/design-system/previews/thumbnail.html`
  (or of `toolkit/templates/thumbnail.html` where the brand has none), with its stylesheet link
  fixed to reach `brand/src/design-system/tokens.css` from this folder, by relative path. It loads
  nothing over the network. For a newsletter image it carries the play-button hook, an element
  with `data-play-button`, added to the copy where the brand's layout lacks it.
- A generated project may hold one worked example brief and layout, where they were kept; delete
  them, with the other example files, once you no longer need them, and none of them will come
  back.

Option/context JSON and score results are author-owned flat files here, named
`<piece>[--cNN].<platform>-<surface>.options.json` and `.scores.json`; a new evaluation uses a new
suffix. Follow `publishing/docs/reference/scoring-options.md`. Variants records candidate IDs
and author selection; Checks cites results, versions and visual review. Jev never approves pixels.

## Cross-references

- `publishing/docs/reference/thumbnails.md` — the brief, the layout, which deliverables take one,
  and the checks.
- `publishing/workflows/04-brief-a-thumbnail/` — the procedure that writes and renders them.
- `brand/docs/reference/the-brand-kit.md` — the tokens and the brand's layout components.
