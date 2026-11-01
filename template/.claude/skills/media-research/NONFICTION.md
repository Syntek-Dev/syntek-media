# NONFICTION.md — media-research, non-fiction mode

The primary sources a non-fiction author's media questions are answered from. A non-fiction piece
quotes its sources aloud and on screen, so its questions are most often about what a translation
or a publisher allows for audio and video, and the credit each asks for.

## Paths and unit

- **Unit:** one piece, or one platform table, that the question serves.
- **Procedure:** `publishing/workflows/07-refresh-the-platform-specs/`, step 3, for platform data.
- **Media's records:** `toolkit/data/platforms.toml` with `brand/src/platforms/overrides.toml`
  (through `python3 toolkit/media.py presets`); the brief's `## Draws on` and `## Notes` in
  `scripts/src/pieces/<piece>/brief.md`; `production/src/rights-register.md`;
  `brand/src/voice/voice.md`.
- **syntek-author's records, where present:** its research notes, evidence and source notes, and
  the default translation its project settings file names, read and never edited.
- **Guides:** `publishing/docs/reference/platform-specs.md`,
  `publishing/docs/reference/ai-disclosure.md` and
  `production/docs/reference/rights-and-consent.md`; the podcast-episode guide, where the project
  makes podcasts.

## Additions to the steps

- **Step 1 — also send the argument away.** What a passage means, what a study found or whether a
  claim holds is the book's research and fact-check, the research and fact-check skills'
  (syntek-author), where present; this skill takes what may be read aloud or shown, and how.
- **Step 4 — also read a translation's own permission statement.** Permission for audio and video
  differs from print: read what the translation allows to be read aloud or shown, how much, and the
  credit it asks for, at the publisher's own page or in the edition itself.
- **Step 4 — also read a guest's release** against the guide on rights and consent, where a piece
  records a guest; its terms come from the release itself, never from memory.
- **Step 7 — also give each credit word for word,** as the terms ask for it, for the script's last
  beat or an on-screen cue.

## Domain rules

| Question | Primary source |
|---|---|
| A platform's limit or format | the platform's own help or developer pages, the table's `source` and `extra_sources` |
| Reading a translation aloud or showing it | the translation's own permission statement, for audio and video (`VERIFY` until read) |
| Quoting another book aloud | the publisher's own permissions terms |
| A guest's or speaker's consent | the release they signed, recorded in the rights register |
| How a name or term is said | an authoritative reference for the language, named in the Source column |

- **Permission to print is not permission to read aloud or to show.**
- **A quotation is copied from the named edition,** never recalled, even when it is familiar.

## Examples

An invented hand-back for a teaching clip (the values are placeholders):

```text
Question: may the clip read two verses aloud and show them on screen?
Answer: VERIFY — the statement was read; its limit for audio and video is still to check in the edition.
Source: the translation's permission statement, read DD/MM/YYYY
Credit: as the statement words it, for the last beat's TEXT: cue
Proposed: a scripture rights row, through production/workflows/07-clear-the-rights/.
```
