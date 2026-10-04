# NONFICTION.md — thumbnail-brief, non-fiction mode

The domain for a non-fiction author's thumbnails and covers: the question the piece answers, the
author's face where it helps, and every quoted word or reference with its source.

## Paths and unit

- **Unit:** one piece (a talk, a podcast episode, an explainer); a cut with its own thumbnail is
  briefed as `<piece>--cNN`.
- **Procedure:** `publishing/workflows/04-brief-a-thumbnail/`.
- **Brief and layout:** `publishing/src/thumbnails/<piece>[--cNN].md` and `.html`; renders in
  `publishing/src/renders/`.
- **Images:** stills from the master and the book's cover, as tracked files in
  `production/src/assets/`; the cover with its `artwork` row.
- **Guides:** `publishing/docs/reference/thumbnails.md`,
  `brand/docs/reference/the-brand-kit.md`, and `production/docs/reference/rights-and-consent.md`
  for scripture and quotations.

## Additions to the steps

- **Step 1 — also** for a podcast episode, read the episode art's `notes` beside any video
  platform's thumbnail: episode art may take no words at all. One layout gives one design per
  aspect, so square deliverables share their words: where one takes none, none goes on either,
  and a conflict between them is a question for the author.
- **Step 4 — also** the words are the question the piece answers, in plain words the audience
  test's listener would use; never a verdict the piece does not reach, and never a rival's view
  as a caricature.
- **Step 5 — also** the author's own face needs no row; a guest's or an audience member's does
  (`likeness`), and covers the thumbnail, not only the recording. A scripture reference on the
  image shows the reference alone, or the words with their translation credited and a `scripture`
  row that covers it.
- **Step 8 — also** check every reference and quoted word on the image against its source,
  character for character.

## Domain rules

- **Ask the piece's question, honestly.** A thumbnail that promises a settled answer to a
  contested question oversells the piece and the author.
- **Quoted words keep their source.** A line from another writer or from scripture is on the image
  only with its source visible and its permission recorded.
- **Guests consent to the image as well as the recording.** A guest's face on a thumbnail is a
  separate use; the row says it is covered.
- **The book's cover is licensed artwork.** It appears as its row allows, with its credit where the
  licence asks.

## Examples

An invented brief for episode art and a video thumbnail of a Robin Example podcast episode:

```markdown
---
piece: 007-the-long-table-episode-3
cut: ""
deliverables: [podcast.episode_art, youtube.podcast_thumbnail]
html: 007-the-long-table-episode-3.html
approved: ""
---

## Promise

Why an open table is harder, and better, than a full one.

## Words on the image

None: the episode art's notes ask for no text, and both deliverables are square, so one wordless image serves both.

## Image

A long table laid for twelve, from a photograph the author took, copied to the assets folder.

## Variants

None asked for.

## Checks

youtube.podcast_thumbnail has no width or height: rendered at the size the author agreed. <!-- VERIFY: square size -->
Episode art carries no words.
```
