# NONFICTION.md — media-tone, non-fiction mode

The domain for a tone pass on a non-fiction author's pieces: teaching clips, talks and podcast
episodes, and their posts. A non-fiction piece earns trust by saying what kind of claim each line
makes, so the pass never trades a hedge or a careful term for a smoother line.

## Paths and unit

- **Unit:** one piece.
- **The words in scope:** `scripts/src/pieces/<piece>/script.md` (spoken lines and `TEXT:` cues),
  `scripts/src/pieces/<piece>/storyboard.md` (on-screen text), `publishing/src/thumbnails/<piece>.md`
  (its words) and `publishing/src/posts/<piece>.md` (the words media owns).
- **The creator:** `brand/src/voice/voice.md`; syntek-author's voice notes and method standard,
  where present (under standards/), read as an input and never edited.
- **Where it is posted:** each profile in `brand/src/platforms/` the piece's deliverables go to.
- **Guides:** `brand/docs/reference/the-spoken-voice.md`,
  `brand/docs/reference/platform-profiles.md` and `scripts/docs/reference/writing-for-the-ear.md`;
  the podcast-episode guide, where the project makes podcasts.

## Additions to the steps

- **Step 2 — also freeze every quotation and reference,** every technical term, and every hedge
  that marks a claim's kind ('the text says', 'one reading is', 'I think'), word for word.
- **Step 4 — also read for certainty.** A line that sounds surer than the claim it carries, a
  contested point said as settled, or an opposing view put so its holders would not recognise it,
  is raised with the author: the fix may change what the line claims, which is outside a tone
  pass.
- **Step 4 — also read for the listener.** Teaching tone is warm and exact: one idea per clip, an
  example before the abstraction, and no talking down to the audience test's listener.

## Domain rules

- **A claim's kind is never collapsed for tone.** What a source says, how it is read and what the
  author holds stay distinct, however the line is reworded.
- **A quotation is said as its source gives it.** A tone change never paraphrases one.
- **A podcast's register is not a clip's.** The Register line's sub-bullets can set a looser
  conversation for an episode and a tighter one for a clip, while the voice stays the author's.

## Examples

An invented proposal for a teaching clip:

```text
2 · 2.3 · ON: Everyone agrees this passage is about rest. · Raised, not proposed
    · 'Everyone agrees' changes the claim's kind; the author decides whether it is 'one reading is'.
```

An invented tone handed on: 'In a clip, a teacher at the front; in an episode, a friend across the
table' — for `brand/workflows/05-write-the-spoken-voice/`, as two sub-bullets of the Register
line.
