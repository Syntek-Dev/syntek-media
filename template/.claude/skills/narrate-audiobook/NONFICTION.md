# NONFICTION.md — narrate-audiobook, non-fiction mode

The domain for narrating a non-fiction book: an argument read so that a listener can follow it,
with its scripture references, its Greek and Hebrew words and its quotations said as a reader
would say them, and its notes and citations kept off the audio unless the author asks.

## Paths and unit

- **Unit:** one audiobook piece. **Chapter:** one chapter of the book, one file.
- **Procedures:** `production/workflows/05-narrate-an-audiobook/` and
  `production/workflows/06-master-an-audiobook/`.
- **Source:** the chapter's file in syntek-author's manuscript layer, where present, whose status
  is `final`; otherwise the text the author provided.
- **Register:** `production/src/audiobook/<piece>.md`; chunks and takes in the generated folder
  beside it, masters in the renders folder (both git-ignored).
- **Narrator:** the `narration` row of `brand/src/voice/voice.md`.
- **Footnotes:** `--footnotes drop` by default; `inline` for a chapter whose notes carry the
  argument, on the author's word. Citation keys are always stripped; the reference list is never
  read.

## Additions to the steps

- **Step 3 — also write the credits the book needs.** The closing credits say where the notes and
  references are (the print or ebook edition), because the audio carries neither; a credit a
  translation's terms ask for goes in the credits word for word from those terms.
- **Step 3 — also check every quotation's permission covers audio.** A quotation from another
  work, scripture included, needs its row in `production/src/rights-register.md`; a translation's
  permission for print may not cover a recording, and M7 needs each row `cleared`.
- **Step 5 — also give every reference a spoken form.** The command lists a scripture reference
  ('Romans 8:28') and a Greek or Hebrew word that has none; settle each with the author as a
  `voice.md` row, its Respelling the spoken form ('Romans, chapter eight, verse twenty-eight'),
  never guessed from a transliteration.
- **Step 10 — also check every quotation word for word.** A take that drops, adds or swaps a word
  in a quotation is taken again, however good its delivery.

## Domain rules

- **Reading scripture aloud needs the translation's permission for audio**: a `scripture` row,
  `cleared` before M7 (`.claude/rules/syntek-media/03-production-ethics.md` Section 6).
- **A quotation is read exactly as the source prints it**; its grammar is never smoothed for the
  ear, and its attribution is spoken where the text speaks it.
- **A citation key is never voiced**, and a footnote is voiced only where the author chose
  `inline` for that chapter.
- **AI narration is disclosed** on every channel that carries it, as
  `publishing/docs/reference/ai-disclosure.md` sets out.

## Examples

An invented line from Robin Example's book, carried from the source to the chunk:

```text
source    Love here is agape [@example2019, 41], the word of Romans 8:28.
listed    'agape': no spoken form · 'Romans 8:28': no spoken form
voice.md  | agape | /aˈɡaːpeː/ | ah-GAH-pay | author | the Greek word |
voice.md  | Romans 8:28 | — | Romans, chapter eight, verse twenty-eight | author | |
chunk     Love here is /aˈɡaːpeː/, the word of Romans, chapter eight, verse twenty-eight.
```

The source is unchanged; only the chunk, which is never tracked, carries the spoken forms.
