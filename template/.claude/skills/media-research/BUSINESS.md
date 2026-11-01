# BUSINESS.md — media-research, business mode

The primary sources a business's media questions are answered from. A business posts to sell, so
its questions are most often about paid promotion, licensed music and stock for commercial use,
and the consent of the people its pieces show.

## Paths and unit

- **Unit:** one piece, or one platform table, that the question serves.
- **Procedure:** `publishing/workflows/07-refresh-the-platform-specs/`, step 3, for platform data.
- **Media's records:** `toolkit/data/platforms.toml` with `brand/src/platforms/overrides.toml`
  (through `python3 toolkit/media.py presets`); the brief's `## Draws on` and `## Notes` in
  `scripts/src/pieces/<piece>/brief.md`; `production/src/rights-register.md`;
  `brand/src/voice/voice.md`.
- **syntek-author's records, where present:** its research notes and evidence, and its brand voice
  and disclaimers, read and never edited, at the paths its project settings file gives.
- **Guides:** `publishing/docs/reference/platform-specs.md`,
  `publishing/docs/reference/ai-disclosure.md` and
  `production/docs/reference/rights-and-consent.md`.

## Additions to the steps

- **Step 2 — also read the disclaimers and the brand voice,** where syntek-author's are present:
  a disclosure wording the business already uses is the first thing to check a platform's rule
  against.
- **Step 3 — also name the account type and the region.** A platform's rules for a business or
  creator account, and for paid promotion, can differ from a personal one's, and a regulator's
  rule holds for its own country: say which the question needs.
- **Step 4 — also read a licence for commercial use.** A music or stock library's licence is read
  for use in advertising, in paid promotion and on each platform the piece goes to, never assumed
  from a 'royalty-free' label.
- **Step 7 — also flag every claim about the business.** A price, a result or a comparison a piece
  would say aloud is the author's to supply and evidence; it is never found by research and filled
  in.

## Domain rules

| Question | Primary source |
|---|---|
| A platform's limit or format | the platform's own help or developer pages, the table's `source` and `extra_sources` |
| Paid promotion and its label | the platform's own branded-content or advertising policy, and the regulator's own guidance for the region (`VERIFY` until read) |
| Music, stock or footage for commercial use | the library's own licence text, for the plan the account holds |
| A release for staff or customers on camera | the release the business uses, and the guide on rights and consent |
| A tool's behaviour | the tool's own documentation for the version in use |

- **No platform rule or limit is written from memory** or borrowed from another platform.
- **Never research a competitor's or client's private figures.** A comparison a piece makes rests
  on what the business can show.

## Examples

An invented hand-back for a Harbour Lane Studio short (the values are placeholders):

```text
Question: may the short use the library track in a paid promotion on this platform?
Answer: VERIFY — the licence page was read; the paid-promotion clause names a higher plan.
Source: the library's licence page, read DD/MM/YYYY
Conflict: the library's summary says 'all social use'; the licence text governs.
Proposed: a rights row for the track, through production/workflows/07-clear-the-rights/.
For the author: which plan does the account hold?
```
