# FICTION.md — repurpose, fiction mode

The domain for cutting down a novelist's long pieces: book trailers, recorded readings and author
talks, cut into teasers that sell the story without spending it.

## Paths and unit

- **Unit:** one piece: a book trailer, a recorded reading, or a talk or interview about the book,
  in `scripts/src/pieces/NNN-kebab-title/`. **Cut:** one teaser, one passage read whole, or one
  answer.
- **Procedure:** `publishing/workflows/01-plan-the-cut-downs/`.
- **Master:** `production/src/renders/<piece>/<piece>.master.mp4`. **Plan:**
  `publishing/src/cut-downs/<piece>.md`.
- **The spoiler line:** how much of the story the book's own blurb gives away. Read the blurb
  wherever the author keeps it (in syntek-author's proposal layer, where present); read, never
  edited.
- **Pronunciations:** `brand/src/voice/voice.md`; every invented name in a cut is said as it
  records.
- **Guides:** `publishing/docs/reference/cut-downs.md`; the trailers and short-video guides in
  `scripts/docs/reference/`, where the project makes those kinds;
  `production/docs/reference/rights-and-consent.md` for artwork, music and quotations.

## Additions to the steps

- **Step 1 — also** find the spoiler line in the brief's `## Notes` or the blurb; where neither
  settles it, ask the author before step 4, because it decides every cut.
- **Step 4 — also** a teaser opens on a question the book answers, never on the answer: a choice,
  a place, a line of dialogue with its speaker clear. From a reading, a cut is a whole passage with
  its own beginning, never a sentence lifted from the middle of a scene.
- **Step 5 — also** a trailer's teasers each take a different image and a different line; the
  same three cards in a new order are one teaser.
- **Step 6 — also** a trailer of stills and cards keeps every card's words inside the safe zone of
  each aspect it is cut to; a still that loses its subject in a vertical crop is `pad`, not
  `crop`.
- **Step 7 — also** list any moment that carries the book's content warnings, and ask whether
  the cut's note should carry the warning too.

## Domain rules

- **Never past the spoiler line.** A twist, a death or an ending stays out of every cut, whatever
  its hook.
- **Every line keeps its speaker.** A character's line read by the author is attributed in the
  voice or on screen, so a viewer never takes a character's view for the author's.
- **Artwork and music are licensed per use.** Cover art, commissioned art and a music bed each
  have a row in `production/src/rights-register.md`, and a cut-down is a use: check the row covers
  every platform the cut serves.
- **An invented word is said one way.** The constructed-language lexicon of syntek-author, where
  present, is the source `voice.md` records; a cut never introduces a second pronunciation.

## Examples

An invented teaser plan cut from Morgan Example's trailer for an invented novel, *The Lantern
Weir*:

```markdown
| Cut | Deliverables | Lines | In | Out | Frame | Hook | Status |
|---|---|---|---|---|---|---|---|
| c01 | tiktok.video, instagram.reel | 1.1–1.3 | 00:00:00.000 | 00:00:14.600 | pad | Every night someone lights the weir lantern. | approved |
| c02 | youtube.short | 3.1–3.2 | 00:00:28.250 | 00:00:41.000 | crop x=420 | Tonight, no one does. | planned |

## c02 — Tonight, no one does

Opening words: NARRATOR, 'Tonight, no one does.'
On-screen title: the book's title card, then the release month.
Stands alone: the question of the whole book in two lines; nothing past chapter 2.
```

An invented cut refused at step 5:

```text
c03 (lines 1.1–1.3 again, cropped instead of padded) is c01 in a new frame: dropped.
```
