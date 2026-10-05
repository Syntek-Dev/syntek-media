# FICTION.md — thumbnail-brief, fiction mode

The domain for a novelist's thumbnails and covers: the book's world and mood at a glance, the
book's own look where its artwork is licensed for it, and nothing that gives the story away.

## Paths and unit

- **Unit:** one piece (a trailer, a teaser, a reading, a talk); a cut with its own thumbnail is
  briefed as `<piece>--cNN`.
- **Procedure:** `publishing/workflows/04-brief-a-thumbnail/`.
- **Brief and layout:** `publishing/src/thumbnails/<piece>[--cNN].md` and `.html`; renders in
  `publishing/src/renders/<piece>/`.
- **Artwork:** the book's cover and any commissioned or licensed art, as tracked files in
  `production/src/assets/` or the brand's exports, `brand/src/exports/`, each with its `artwork`
  row in `production/src/rights-register.md`.
- **Type:** the brand's fonts in `brand/src/design-system/fonts/`, each licence in the rights
  register (Kind `font`).
- **Guides:** `publishing/docs/reference/thumbnails.md` and
  `brand/docs/reference/the-brand-kit.md`.

## Additions to the steps

- **Step 1 — also** read the brief's `## Notes` for the spoiler line, and the cut-down plan's
  hooks: a teaser's thumbnail asks the teaser's question.
- **Step 4 — also** the words are the book's title, a short line of the book's own, or the
  teaser's question; never a twist, a death or an ending, and never a review or an endorsement the
  author has not received and been allowed to quote.
- **Step 5 — also** the cover and any commissioned art may be used only as their `artwork` rows
  allow (a cover licensed for print alone does not cover video). AI-generated art is recorded in
  the brief's `ai_visuals` before it is placed, and the author is told the disclosure it brings.
- **Step 8 — also** a series keeps one look: compare the render with the series' earlier
  thumbnails, and report a drift rather than correct it silently.

## Domain rules

- **Never past the spoiler line.** A thumbnail is seen by everyone who scrolls past it, including
  readers who have not reached the twist.
- **The cover is someone's work.** Cover art, illustration and lettering keep their licence terms,
  and their credit where the licence asks for one.
- **The book's look, not a lookalike.** A thumbnail that imitates another book's cover, or a famous
  author's series style, misleads readers; it is the brand's look or the book's own.
- **Names are spelled as the book spells them.** An invented name on the image matches the
  manuscript exactly, accents and hyphens included.

## Examples

An invented reel-cover brief for a teaser cut from Morgan Example's trailer for an invented novel,
*The Lantern Weir*:

```markdown
---
piece: 002-the-lantern-weir-trailer
cut: c01
deliverables: [instagram.reel_cover, tiktok.video]
html: 002-the-lantern-weir-trailer--c01.html
approved: ""
---

## Promise

A drowned village, and the one light still burning in it.

## Words on the image

Who lights the weir?

## Image

The cover's lantern detail, cropped from the licensed cover art (RR0004 covers video and social use).

## Variants

The same words over the river still from the trailer, for the author to choose between.

## Checks

The title sits inside the centre crop of platform.instagram.grid_aspect (a verify key).
tiktok.video rendered at the video's size: no thumbnail table. <!-- VERIFY: TikTok cover size -->
```
