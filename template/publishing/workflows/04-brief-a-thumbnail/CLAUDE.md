@./CONTEXT.md

# CLAUDE.md — publishing/workflows/04-brief-a-thumbnail/

Read order: `.claude/CLAUDE.md` → `.claude/MEMORY.md` → `publishing/CONTEXT.md` →
`publishing/CLAUDE.md` → `publishing/workflows/CONTEXT.md` → `publishing/workflows/CLAUDE.md` →
this folder's `CONTEXT.md` (imported above) → this file → `STEPS.md` (with `CHECKLIST.md` open).

## Purpose (one line)

Make each thumbnail or cover a single honest promise, built from the brand's own layout and
checked at the size a viewer sees it, before the author approves it.

## How to work here

**Follow `STEPS.md` in order and tick `CHECKLIST.md` as you go.** The model tags in the checklist
are authoritative: `opus` items are judgement; `sonnet` items belong to the mechanical tier.

- **Routing:** skill `thumbnail-brief` (this procedure in skill form; its mode file carries the
  brand kind's sense of a promise). Guides: `publishing/docs/reference/thumbnails.md` and the
  guide for each platform a thumbnail goes to. Tools: `uv run toolkit/card.py` (`check`,
  `render`) and `python3 toolkit/media.py frame`.
- **Model:** **Opus** for the promise, the words, the image and every check; the mechanical tier
  for copying the layout, fixing its path and rendering
  (`.claude/rules/syntek-media/05-model-allocation.md`).
- **Concrete steps:** confirm the deliverables → decide which take a thumbnail → brief it in
  words → copy the brand's layout → fill it → check it → render each deliverable → check at
  thumbnail size → the author approves → hand back.
- **Definition of done:** every deliverable that takes a thumbnail has a PNG rendered from an
  approved brief, checked at size, inside the safe zone and the grid crop, with its rights
  cleared; every unconfirmed size is flagged `VERIFY`.

Title–thumbnail options use `publishing/docs/reference/scoring-options.md` and
`media.py score plan/run`: one approved paid call, retained provenance and author selection.
Jev scores text concepts; actual images still need visual review.

## Guardrails

- **Words before pixels.** No layout is filled before the brief's promise is agreed.
- **Copy the brand's component; never edit it.** A change for every piece belongs in
  `brand/src/design-system/previews/thumbnail.html`, on the author's word, through the brand
  layer.
- **Nothing over the network, and nothing from a render.** Images are tracked files loaded by
  relative path.
- **No size is guessed.** A table without one, or a platform without a table, renders at a size
  the author confirms or at the video's size, flagged `VERIFY`.
- **The author approves the PNG,** at the size it will be seen, never the HTML.
- **Never overwrite** an approved brief or layout without confirming with the author.

## Output & naming

- **Produces:** `publishing/src/thumbnails/<piece>[--cNN].md` and `.html`; PNGs in
  `publishing/src/renders/`, `<html-stem>.<platform>-<format>.png`; the encodes `media.py image`
  writes (`<stem>.<platform>-<format>.<ext>`) and a GIF (`<piece>[--cNN].newsletter-preview-gif.gif`).
- **Also writes:** a still taken from the master, where the image is a frame, as a small
  committed file in `production/src/assets/`.
- **Does not touch:** the brand's layout component, `tokens.css` or any other render.
