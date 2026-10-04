@./CONTEXT.md

# CLAUDE.md — publishing/src/thumbnails/

Read order: `.claude/CLAUDE.md` → `.claude/MEMORY.md` → `publishing/CONTEXT.md` →
`publishing/CLAUDE.md` → `publishing/src/CONTEXT.md` → `publishing/src/CLAUDE.md` → this folder's
`CONTEXT.md` (imported above) → this file.

## Purpose (one line)

Hold each thumbnail's brief and layout as tracked source, so every PNG a platform receives can be
remade from the brand's tokens and an agreed brief.

## How to work here

- **Routing:** skill `thumbnail-brief`, through `publishing/workflows/04-brief-a-thumbnail/`;
  guide `publishing/docs/reference/thumbnails.md`.
- **Model:** **Opus** for the promise, the words and the image; the mechanical tier for copying
  the layout, fixing its path and rendering (`.claude/rules/syntek-media/05-model-allocation.md`).
- **Concrete steps:** brief in words → copy the brand's layout → fill it → `card.py check` →
  render each deliverable → check at thumbnail size → the author approves the PNG.
- **Definition of done:** the brief is approved, the layout passes `uv run toolkit/card.py check`,
  and every deliverable it names is rendered, checked and seen by the author.

## Guardrails

- **Copy the brand's component; never edit it here.** A change to the layout for every piece
  belongs in `brand/src/design-system/previews/thumbnail.html`, on the author's word.
- **Nothing over the network.** Images load by relative path from tracked files; a render is never
  an image source, because renders are ignored by Git.
- **No platform without a table gets a confirmed size.** A thumbnail for one is rendered at its
  video deliverable's size and flagged `VERIFY`.
- **Never overwrite** an approved brief or layout without confirming with the author.

## Output & naming

- **Hand-written (with the author):** `<piece>.md` and `<piece>.html`, or `<piece>--cNN.md` and
  `<piece>--cNN.html` for one cut. The brief's shape:

```markdown
---
piece: NNN-kebab-title             # equals the piece's folder name
cut: ""                            # cNN for one cut's thumbnail; empty for the full-length deliverables
deliverables: []                   # keys: youtube.thumbnail, instagram.reel_cover, podcast.episode_art, …
html: NNN-kebab-title.html         # the layout beside this brief
approved: ""                       # DD/MM/YYYY once the author approves the rendered PNGs
---

# <Title> — thumbnail brief

## Promise
## Words on the image
## Image
## Variants
## Checks
```

- **Generated (never hand-edit):** `<html-stem>.<platform>-<format>.png`, in
  `publishing/src/renders/`.
