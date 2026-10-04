# FICTION.md — storyboard, fiction mode

The domain for boarding a novelist's pieces: trailers and teasers built from stills, cards, colour,
cross-fades and slow push-ins, set in the book's world, and showing nothing the story has not yet
given away.

## Paths and unit

- **Unit:** one piece. **Board row:** one still, card or clip, carrying one spoken line, one cue or
  a short run of lines.
- **Procedure:** `scripts/workflows/03-storyboard-a-piece/`.
- **Script:** `scripts/src/pieces/<piece>/script.md`. **Board and shot list:**
  `scripts/src/pieces/<piece>/storyboard.md` and `scripts/src/pieces/<piece>/shot-list.md`.
- **The book's look:** the cover and any commissioned art, held in `production/src/assets/` under
  licence; where syntek-author's fiction layers are present, the story bible's character and place
  files (under world/src/), read and never edited.
- **Rights:** `production/src/rights-register.md`.
- **Guides:** `scripts/docs/reference/storyboards-and-shot-lists.md`, and the trailers guide beside
  it where this project makes trailers.

## Additions to the steps

- **Step 2 — also read how the world looks.** Read the story bible's file for every character and
  place the board will show, where present, and the cover. A picture that contradicts the book (an
  age, a scar, a building, a season) is reported to the author, never drawn.
- **Step 4 — also board a trailer in stills and cards.** A trailer row is a still (with a slow
  push-in where it should move), a card for each `TEXT:` cue, or a colour clip between beats; each
  holds long enough to be read twice, and a cross-fade marks a change of beat, not every cut.
- **Step 4 — also keep the pictures behind the reveal line.** No image shows what the script holds
  back: a face the reader should not yet know, a place the story reaches later, an object that
  gives the turn away.
- **Step 6 — also source every image honestly.** The cover and commissioned art come under licence
  (`artwork`), stock with its licence (`stock`), and an image made by a generator is Type
  `generated`, noted for the brief's `ai_visuals` and the disclosure. A stock face cast as a
  character is a `likeness` question for that licence, flagged `VERIFY` until its terms are read.
- **Step 7 — also clear the type and the art.** The cover's typeface on a card needs a font
  licence that covers video (`font`), and the cover or any illustration shown needs the artist's
  or the publisher's permission for video (`artwork`).

## Domain rules

- **No spoilers in pictures either**: the board keeps the reveal line the script keeps.
- **The book is the source of truth for how things look**; a contradiction is reported, never
  repaired.
- **Generated pictures are disclosed** (`.claude/rules/syntek-media/03-production-ethics.md`
  Section 5) and recorded in the brief's `ai_visuals`.
- **Art and type are licensed for video, not only for print** (Section 6).

## Examples

Invented board rows for Morgan Example's teaser:

```markdown
| # | Beat | Time | Picture | Spoken | On screen | Sound | Vertical framing |
|---|---|---|---|---|---|---|---|
| B01 | 1 | 00:00–00:05 | Still: the mill town at dusk, a clock in every window; slow push-in | 1.1 | One night a year, time turns back | narrator; low drone | centre |
| B02 | 2 | 00:05–00:12 | Still: a figure at the riverbank, seen from behind, face unseen | 2.1 | Who comes back? | whisper; water rising, then silence | crop x=420 |
| B03 | 3 | 00:12–00:17 | Card: the cover, then the call to action | 3.1 | Read chapter one | narrator; music out | centre |
```

The shot list behind them:

```markdown
| Shot | Board | Type | Source | Framing | Seconds | Status | Rights |
|---|---|---|---|---|---|---|---|
| S01 | B01 | still | F0012 | centre | 5.0 | logged | RR0004 |
| S02 | B02 | generated | production/src/assets/riverbank-figure.png | crop x=420 | 7.0 | captured | RR0005 |
| S03 | B03 | card | production/src/cards/002-the-flood-teaser.end.html | centre | 5.0 | needed | RR0006 |
```
