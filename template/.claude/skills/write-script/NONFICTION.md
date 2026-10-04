# NONFICTION.md — write-script, non-fiction mode

The domain for scripting a non-fiction author's pieces: talks, teaching clips and podcast
episodes, in which every claim says what kind of claim it is and every quotation is said exactly as
its source gives it. An audiobook is never scripted here: its credits are written with its chapter
register, by the audiobook narration skill, where the project makes audiobooks.

## Paths and unit

- **Unit:** one piece: a teaching clip, a talk or a podcast episode. **Beat:** one step of the
  argument, typically two to five spoken lines.
- **Procedure:** `scripts/workflows/02-write-a-script/`.
- **Brief:** `scripts/src/pieces/<piece>/brief.md`. **Script:**
  `scripts/src/pieces/<piece>/script.md`.
- **The book:** the brief's `source` and, where syntek-author's non-fiction layers are present,
  the promoted chapter, its argument map and the evidence verdicts behind it (under
  manuscript/src/, planning/src/ and research/src/), read and never edited.
- **Rights:** `production/src/rights-register.md` — every quotation and translation read aloud
  or shown.
- **Guides:** `scripts/docs/reference/writing-for-the-ear.md`, and the long-video, short-video
  and podcast-episode guides beside it where this project makes those kinds.

## Additions to the steps

- **Step 2 — also read the argument.** Read the source chapter's claims as the book makes them,
  and map each key point of the brief to the claim it carries, so no beat says more than the book
  does.
- **Step 3 — also check every quotation and reference word for word.** A quotation is copied from
  the named edition or translation, never recalled; a verse comes from the translation the author
  names, with its reference. Permission for audio and video differs from print: a translation's
  own permission statement says what may be read aloud or shown, and what credit it asks for. Each
  quotation read aloud is listed for a `quotation` or `scripture` rights row, and carries `VERIFY`
  until its terms have been read at source.
- **Step 5 — also make each claim's kind audible.** 'The text says…', 'one reading is…', 'I
  think…': what a source says, how it is read and what the author concludes are never collapsed,
  and a contested point is said to be contested. An objection is stated so that those who hold it
  would recognise it.
- **Step 5 — also teach one thing per piece.** One idea per clip; an example before the
  abstraction; a quotation cut to the words the point needs, with its reference spoken or shown as
  a `TEXT:` cue. The call to action names the book, the talk or the next episode, as the brief
  gives it.
- **Step 5 — also write the credit a permission asks for.** Where a translation's terms ask for a
  spoken or shown credit, it goes in the script (an episode's last beat, or an on-screen `TEXT:`
  cue), word for word from those terms.
- **Step 9 — also keep the author's precision.** A revision never loosens a technical term, drops a
  hedge that is doing honest work, or turns 'one reading is' into 'the text says' for the sake of
  rhythm; a line that is hard to say is offered a simpler order, with its claim intact.
- **Step 10 — also list the quotations.** Each by its line, with its source and translation, its
  rights row once opened, and any credit its terms ask for.

## Domain rules

- **Quotations and references are checked, never recalled**
  (`.claude/rules/syntek-media/03-production-ethics.md` Section 7): a verse quoted from memory is a
  fabrication even when it happens to be right.
- **Permission to print is not permission to read aloud or to show** (Section 6): every quotation
  and translation used has a rights row, and M7 needs it `cleared`.
- **A claim's kind is never collapsed**: what the text says, how it is read and what the author
  holds stay distinct, and the author's conclusion is owned in the first person.
- **Opposing views are stated fairly**, so that those who hold them would recognise them.

## Examples

An invented teaching-clip beat for Robin Example, the reference still to be checked:

```markdown
## 2. What the passage says (target 00:20)

ON: The passage repeats one verb three times.
TEXT: [reference to be supplied] <!-- VERIFY: the reference, the translation's wording and its terms for video -->
ON: {pause 0.4} On this reading, the repetition marks a change of speaker.
ON: I hold that rest is commended here, not commanded.
```

An invented quotations list from the hand-back:

```text
Quotations (for the rights register):
- 2.1 · the passage, in the default translation · scripture · terms for audio and video: VERIFY · credit: as the terms ask
```
