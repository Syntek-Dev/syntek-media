# BUSINESS.md — narrate-audiobook, business mode

The domain for narrating a business's book or long guide: a text the owner wrote for clients or
for the trade, read so that a listener can follow its steps, figures and names without the page.

## Paths and unit

- **Unit:** one audiobook piece. **Chapter:** one chapter or part of the book, one file.
- **Procedures:** `production/workflows/05-narrate-an-audiobook/` and
  `production/workflows/06-master-an-audiobook/`.
- **Source:** the text the author provides, normally; a document in syntek-author's library
  layer, where present, only on the author's word and only in its `final` version.
- **Register:** `production/src/audiobook/<piece>.md`; chunks and takes in the generated folder
  beside it, masters in the renders folder (both git-ignored).
- **Narrator:** the `narration` row of `brand/src/voice/voice.md`.
- **Footnotes:** `--footnotes drop`, unless the author asks for `inline`: a listener cannot follow
  a reference in the middle of a sentence.

## Additions to the steps

- **Step 3 — also check what the credits promise.** The opening credits say the business's name as
  `voice.md` gives it; the closing credits say where a listener finds what the audio cannot carry
  (the tables, the figures, the references).
- **Step 5 — also treat a table, a chart or a checklist as having no spoken form.** Where the
  command lists one, the author either writes a spoken version into the source, through that
  source's own procedure, or drops it with a line pointing to the companion PDF. Never summarise
  one yourself.
- **Step 5 — also read every figure as the source writes it**, with its unit; a figure that cannot
  be said cleanly is the author's to rewrite at the source.
- **Step 12 — also list every client, partner and product name the book voices**, so the author can
  confirm each is cleared for audio.

## Domain rules

- **A client's or a partner's name is voiced only with their recorded permission**, a `cleared` row
  in `production/src/rights-register.md` (`.claude/rules/syntek-media/03-production-ethics.md`
  Section 6).
- **Nothing confidential is narrated**: a client document, or any text written under a client's
  confidence, never becomes a source, whatever the route.
- **No statistic, result or testimonial is voiced unsourced**
  (`.claude/rules/syntek-media/03-production-ethics.md` Section 7).
- **The owner's own cloned voice is still synthetic**, and is disclosed on every channel that
  carries it.

## Examples

An invented chapter of Harbour Lane Studio's guide, what `audiobook text` listed, and how each
item was settled:

```text
Chapter ch02 of 014-running-a-small-studio: listed with no spoken form
  table 'Booking checklist'   the author wrote two spoken sentences into the source;
                              the closing credits point to the PDF
  'HLS'                       a voice.md row, respelled 'aitch-ell-ess'
Run again: exit 0; four chunks written.
```
