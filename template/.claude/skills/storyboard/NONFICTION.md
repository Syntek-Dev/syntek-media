# NONFICTION.md — storyboard, non-fiction mode

The domain for boarding a non-fiction author's pieces: talks and teaching clips in which the
speaker, the text under discussion and its reference on screen carry the argument, and every
quotation shown is permitted for video.

## Paths and unit

- **Unit:** one piece. **Board row:** one picture, usually the speaker or a text card, carrying
  one step of the argument.
- **Procedure:** `scripts/workflows/03-storyboard-a-piece/`.
- **Script:** `scripts/src/pieces/<piece>/script.md`. **Board and shot list:**
  `scripts/src/pieces/<piece>/storyboard.md` and `scripts/src/pieces/<piece>/shot-list.md`.
- **The book:** the cover and the book's own figures, held in `production/src/assets/` under
  licence; where syntek-author's non-fiction layers are present, the promoted chapter the script
  draws on (under manuscript/src/), read and never edited.
- **Rights:** `production/src/rights-register.md` — every quotation, translation, venue and
  audience.
- **Guides:** `scripts/docs/reference/storyboards-and-shot-lists.md` and
  `production/docs/reference/rights-and-consent.md`.

## Additions to the steps

- **Step 4 — also show the text being discussed.** A quotation the script reads gets a card, or
  On screen text, with its words exactly as the named translation gives them and its reference; a
  long passage is split across cards at its sentence breaks, never scrolled or shrunk to fit.
- **Step 4 — also make each claim's kind visible.** A card that shows an interpretation says so
  ('one reading'), so a picture never presents an inference as the text itself.
- **Step 6 — also source the setting.** Footage of a venue needs the venue's permission
  (`location`); an audience that can be recognised needs a release (`footage-release`) or is
  framed out; a book cover on screen is `artwork`, cleared with its publisher.
- **Step 7 — also clear every quotation shown.** A translation's terms for showing its text in a
  video can differ from its terms for print and for audio. Record its permission statement and any
  credit line it asks for in a `scripture` or `quotation` row, flagged `VERIFY` until it has been
  read at source, and board the credit where the terms say it must appear.

## Domain rules

- **A quotation is shown exactly as the named translation has it**
  (`.claude/rules/syntek-media/03-production-ethics.md` Section 7).
- **Permissions differ for print, audio and video** (Section 6): a quotation on screen has its own
  rights row, and M7 needs it `cleared`.
- **An audience is filmed only with consent**, or framed out of the shot.
- **An interpretation is never shown as the text.**

## Examples

Invented board rows for one of Robin Example's teaching clips:

```markdown
| # | Beat | Time | Picture | Spoken | On screen | Sound | Vertical framing |
|---|---|---|---|---|---|---|---|
| B03 | 2 | 00:20–00:32 | Card: the passage in three lines, the repeated verb in the accent colour | 2.1 | [reference to be supplied] | voice; room tone | centre |
| B04 | 2 | 00:32–00:40 | The speaker at the lectern, mid-shot | 2.2–2.3 | One reading | voice; room tone | crop x=600 |
```

An invented rights row this board opens:

```markdown
| ID | Item | Kind | Pieces | Holder | Licence or permission | Evidence | Expires | Status | Notes |
|---|---|---|---|---|---|---|---|---|---|
| RR0007 | The passage, default translation, on a card | scripture | 007-what-the-passage-says | <!-- AUTHOR TO CONFIRM: the publisher --> | <!-- VERIFY: the terms for showing the text in a video, and any credit line --> | — | — | needed | — |
```
