# FICTION.md — media-tone, fiction mode

The domain for a tone pass on a novelist's pieces: trailers, readings, behind-the-book clips and
their posts. A book's media has two voices, the author's own and the book's, and the pass keeps
each where it belongs.

## Paths and unit

- **Unit:** one piece.
- **The words in scope:** `scripts/src/pieces/<piece>/script.md` (spoken lines and `TEXT:` cues),
  `scripts/src/pieces/<piece>/storyboard.md` (on-screen text), `publishing/src/thumbnails/<piece>.md`
  (its words) and `publishing/src/posts/<piece>.md` (the words media owns).
- **The creator:** `brand/src/voice/voice.md`; syntek-author's voice notes, where present
  (standards/style/voice-notes.md), read as an input and never edited.
- **The book:** the promoted chapter a reading quotes, where syntek-author's layers are present
  (under manuscript/src/), read and never edited.
- **Where it is posted:** each profile in `brand/src/platforms/` the piece's deliverables go to.
- **Guides:** `brand/docs/reference/the-spoken-voice.md` and
  `brand/docs/reference/platform-profiles.md`; the trailers guide, where the project makes
  trailers.

## Additions to the steps

- **Step 2 — also freeze every line quoted from the book,** a character's name and every word a
  `character:<name>` narrator says: the book's text is the book's, and a reading says it as
  written.
- **Step 3 — also tell the two voices apart.** The author's own lines (an introduction, a call to
  action) are read against the spoken style; a line from the book is read only for whether it
  suits the piece, never retoned.
- **Step 4 — also read for genre and for spoilers.** A trailer's tone should promise the book's
  genre and mood; a line that gives away what the brief says to withhold is raised with the
  author, never softened into a hint.

## Domain rules

- **The book's words are never retoned.** A quoted line that does not suit a piece is replaced by
  another the author chooses from the book, or cut, on the author's word.
- **The author's voice is not the narrator's.** The author speaks as themselves in an
  introduction; a narrator reads the book in the book's voice.
- **The genre sets the register.** A cosy mystery's trailer and a thriller's differ, as the
  Register line's sub-bullets set them for each type of content.

## Examples

An invented proposal for a trailer's end beat:

```text
5 · 4.2 · TEXT: The must-read thriller of the year! · Register (trailer: quiet, unsettling)
    · TEXT: Some lights are kept for a reason. · The superlative is a claim no source makes; the brief's tagline is kept instead.
```

An invented tone handed on: 'On a reading, slow and close; on a trailer, quiet and unsettling' —
for `brand/workflows/05-write-the-spoken-voice/`, as two sub-bullets of the Register line.
