# BUSINESS.md — thumbnail-brief, business mode

The domain for a business's thumbnails and covers: the outcome a viewer gets, said in the brand's
words and shown in its colours, with nothing on the image the business could not stand behind.

## Paths and unit

- **Unit:** one piece; a cut with its own thumbnail is briefed as `<piece>--cNN`.
- **Procedure:** `publishing/workflows/04-brief-a-thumbnail/`.
- **Brief and layout:** `publishing/src/thumbnails/<piece>[--cNN].md` and `.html`; renders in
  `publishing/src/renders/`.
- **Brand:** `brand/src/design-system/` (the tokens and the layout); syntek-author's brand guide
  and brand voice, where present (by default in standards/brand/; its project settings file,
  00-project.md, names the brand folder).
- **Images:** stills, logos and graphics in `production/src/assets/`; the business's own logo
  from the brand's exports, `brand/src/exports/`.
- **Guides:** `publishing/docs/reference/thumbnails.md` and
  `brand/docs/reference/the-brand-kit.md`.

## Additions to the steps

- **Step 1 — also** read the brief's `## Purpose` and `## Call to action`: the thumbnail's promise
  is the outcome the purpose names, for the customer the audience test describes.
- **Step 4 — also** the words name the problem or the result in the customer's terms, never a
  superlative ('best', 'ultimate', 'game-changing'). A figure goes on the image only with its
  evidence, checked with the fact-check skill (syntek-author), where present.
- **Step 5 — also** a client's logo, product or premises, and any person other than the owner,
  needs its row (`artwork`, `location` or `likeness`) `cleared` before approval. Stock keeps its
  licence row, and the licence must allow promotional use on every platform the piece serves.
- **Step 8 — also** check the words against the brand voice's register and its banned words,
  where syntek-author's brand voice is present, and the logo against the brand guide's clear
  space and minimum size.

## Domain rules

- **A thumbnail is advertising.** Its words are a claim about the business, held to the same
  evidence as a post: specific, checkable and true of this piece.
- **The brand guide outranks taste.** Colour, type and logo use come from `tokens.css` and
  syntek-author's brand guide, where present; a clash between the two is reported to the author,
  never resolved here.
- **No result without its evidence.** A before-and-after, a saving or a growth figure appears only
  where the business can show it, with the client's permission where it is the client's result.
- **Clients appear only by permission.** A client's name, logo or face is on the image only with a
  `cleared` row that covers promotional use.

## Examples

An invented brief for an invented Harbour Lane Studio explainer:

```markdown
---
piece: 004-price-it-once
cut: ""
deliverables: [youtube.thumbnail, linkedin.video_landscape]
html: 004-price-it-once.html
approved: ""
---

## Promise

A quote you can defend line by line.

## Words on the image

Price it once.

## Image

The owner at the workbench, a still from the master at 00:02:14.500, copied to the assets folder.

## Variants

None asked for.

## Checks

linkedin.video_landscape rendered at the video's size: the platform has no thumbnail table. <!-- VERIFY: LinkedIn thumbnail size -->
Words readable at feed size; inside the safe zone at both sizes.
```
