# FICTION.md — write-script, fiction mode

The domain for scripting a novelist's pieces: trailers, teasers and author socials that sell the
book's world and its question without giving away its answers, in the book's own names and words.

## Paths and unit

- **Unit:** one piece: a trailer, a teaser short, an author-to-camera clip or a reading.
  **Beat:** one image, one question or one line from the book, typically one to three spoken
  lines.
- **Procedure:** `scripts/workflows/02-write-a-script/`.
- **Brief:** `scripts/src/pieces/<piece>/brief.md`. **Script:**
  `scripts/src/pieces/<piece>/script.md`.
- **The book:** the brief's `source` (a chapter or a passage) and, where syntek-author's fiction
  layers are present, its story bible, names register and promoted chapters (under world/src/ and
  manuscript/src/), read and never edited.
- **Voices:** `brand/src/voice/voice.md` — the narrator for each use, a `character:<name>` row for
  every character voiced, and the pronunciation of every name and constructed word.
- **Guides:** `scripts/docs/reference/writing-for-the-ear.md`, and the trailers and short-video
  guides beside it where this project makes those kinds.

## Additions to the steps

- **Step 2 — also settle the reveal line.** Read the brief's `## Notes` for how far into the book
  the piece may reveal. Where they say nothing, ask before writing, recommending nothing past the
  opening chapters. Read the story bible's file for every character and place the piece names,
  where present, and the book's cover line, where the author has one.
- **Step 3 — also take every name and line from the book.** A name is spelled as the names
  register spells it, where present, or as the source does. A line quoted from the book is copied
  from the promoted chapter or the source the brief names, never paraphrased and passed off as the
  book's. A review quote, a blurb or an endorsement is the author's to supply, with the reviewer's
  permission, and is listed for a `quotation` rights row; never invent one.
- **Step 5 — also sell the question, never the answer.** The hook is an image or a question from
  the book's world. No beat reveals a twist, a death, an identity, the ending, or anything past the
  reveal line. The last beat names the book and where to find it, as the brief's call to action
  gives it (a pre-order, the first chapter, a launch date).
- **Step 5 — also cast the voices.** A line spoken in character opens with the character's name as
  its tag (`ILSA:`) and needs a `character:<name>` narrator in `voice.md` before any of it is
  voiced; a synthetic character voice is disclosed through the brief's `synthetic_voice`. A
  constructed word stays as the book spells it: its sound goes in `voice.md` under
  `## Pronunciations`, from the language's IPA in syntek-author's lexicon, where present, and is
  never respelled in the script.
- **Step 5 — also write a trailer for stills and cards.** A trailer here is built from stills,
  cards, colour, fades and slow push-ins: each `TEXT:` card is a few words that can hold the screen
  for its beat, and the narration runs over the pictures, never against them. Where a picture holds
  after a line, end the line with `{pause S}`: it becomes that segment's `pause_after`, and step 7
  counts it, so the script meets its target without padding the narration.
- **Step 10 — also list the reveal.** Name every plot fact the script discloses, by its line and
  the chapter it comes from, so the author can confirm that none of it spoils.

## Domain rules

- **No spoilers.** Nothing past the reveal line the author set; a doubt is an
  `AUTHOR TO CONFIRM`, never a guess.
- **The book is the source of truth**: names, places and quoted lines as the book has them; a
  contradiction with the story bible is reported, never repaired.
- **Reviews and endorsements are real and permitted, or absent**
  (`.claude/rules/syntek-media/03-production-ethics.md` Sections 6 and 7).
- **A synthetic voice for a character is disclosed** (Section 5), and no voice is cloned without
  its owner's recorded consent (Section 6).

## Examples

An invented teaser for Morgan Example's novel, its reveal held back:

```markdown
## 1. Hook (target 00:07)

NARRATOR: {low} In the mill town, every clock runs backwards on the night of the flood. {pause 1}
TEXT: One night a year, time turns back

## 2. The question (target 00:08)

ILSA: {whisper} If I cross the river tonight, who comes back? {pause 4}
SFX: water rising, then silence
TEXT: Who comes back? <!-- AUTHOR TO CONFIRM: does this line give away more than chapter 4 does? -->

## 3. Call to action (target 00:05)

NARRATOR: The first chapter is waiting for you now. {pause 2}
TEXT: Read chapter one <!-- AUTHOR TO CONFIRM: where the first chapter is published -->
```

An invented reveal list from the hand-back:

```text
Reveal (for the author to confirm that none of it spoils):
- The clocks run backwards on the night of the flood · 1.1 · chapter 1
- Ilsa thinks of crossing the river · 2.1 · chapter 4
```
