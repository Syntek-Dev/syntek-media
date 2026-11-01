# FICTION.md — media-research, fiction mode

The primary sources a novelist's media questions are answered from. A book's media promotes the
book, so its questions are most often about what may be shown or read of it, the music under a
trailer, and what retailers and platforms accept.

## Paths and unit

- **Unit:** one piece, or one platform table, that the question serves.
- **Procedure:** `publishing/workflows/07-refresh-the-platform-specs/`, step 3, for platform data.
- **Media's records:** `toolkit/data/platforms.toml` with `brand/src/platforms/overrides.toml`
  (through `python3 toolkit/media.py presets`); the brief's `## Draws on` and `## Notes` in
  `scripts/src/pieces/<piece>/brief.md`; `production/src/rights-register.md`;
  `brand/src/voice/voice.md`.
- **syntek-author's records, where present:** its research notes, its names register and its
  language files (under research/src/ and world/src/), read and never edited.
- **Guides:** `publishing/docs/reference/platform-specs.md`,
  `publishing/docs/reference/ai-disclosure.md` and
  `production/docs/reference/rights-and-consent.md`; the trailers and audiobook guides, where the
  project makes those kinds.

## Additions to the steps

- **Step 1 — also send the story's facts away.** A question about the book's world (a period
  detail, a real place) is the book's research, the research skill's (syntek-author), where
  present; this skill takes only how the book is shown, read or heard.
- **Step 3 — also name who holds the rights.** The publisher, the agent or the author may hold
  the right to show the cover or read the text aloud; say which contract or terms the question
  needs, and that only the author can produce them.
- **Step 4 — also read a retailer's own specification** for an audiobook or a sample, where the
  project makes audiobooks, at the retailer's own pages, never a forum's summary.
- **Step 4 — also take an invented name's pronunciation from the book.** Its source is
  syntek-author's names register or lexicon, where present, never a guess; a real name's comes
  from its owner or an authoritative reference.

## Domain rules

| Question | Primary source |
|---|---|
| A platform's limit or format | the platform's own help or developer pages, the table's `source` and `extra_sources` |
| Showing the cover or reading the text aloud | the publishing contract or the publisher's own terms, supplied by the author (`VERIFY` until read) |
| Music under a trailer | the library's own licence text, for each platform the trailer goes to |
| An audiobook retailer's requirements | the retailer's own submission pages, where the project makes audiobooks |
| How a name is said | the names register or lexicon, where present; otherwise the author |

- **No platform rule, retailer rule or limit is written from memory.**
- **A spoiler is the author's call,** never research's: report what a source shows, and leave
  what the piece withholds to the brief.

## Examples

An invented hand-back for a trailer (the values are placeholders):

```text
Question: may the trailer show the cover and read the opening line aloud?
Answer: for the author — the publisher's terms are not in the project.
Source: none read; the publishing contract is needed
Proposed: a rights row for the cover and one for the quoted line, through production/workflows/07-clear-the-rights/.
For the author: who holds the right to the cover image, and what credit does it ask for?
```
