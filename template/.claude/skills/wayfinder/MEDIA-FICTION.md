# MEDIA-FICTION.md — wayfinder, media fiction mode

The domain for charting a novelist's media work too big for one sitting: a book's launch
campaign, a series of teasers, or, where the project makes audiobooks, the audiobook from plan to
release. It names where a map's nodes come from and where each settled one lands in media's
files.

## Paths and unit

- **Unit:** a body of media work across several pieces; each piece in it is still briefed on its
  own through `scripts/workflows/01-brief-a-piece/`.
- **Decision-maps folder:** the path `.claude/rules/syntek-media/02-skills.md` Section 4 gives
  that role; where none is agreed yet, agree one with the author before step 7.
- **The outline:** `scripts/src/piece-register.md` for which pieces exist, and
  `publishing/src/schedule.md` for their order and dates.
- **Open-flags check:** `python3 toolkit/media.py flags`.

## Additions to the steps

- **Step 1 — also read the stalled media work**: a brief whose `status` has not moved, a
  schedule row with no deliverable behind it, a rights row still `needed`, and every open flag.
- **Step 4 — also pin the campaign's reveal line** with the destination: how far any piece of
  the campaign may reveal.
- **Step 5 — also walk** the piece register, the schedule, the character voices in
  `brand/src/voice/voice.md` and syntek-author's story bible, where present.
- **Step 11 — also route media's task nodes.** A cover, an illustration or a review quote's
  permission goes to a `needed` row in `production/src/rights-register.md` and
  `production/workflows/07-clear-the-rights/`. A credit-spending call is never a task node: it is
  the author's decision, agreed in the procedure that makes it.
- **Step 12 — also graduate to the media homes:**

| A settled decision that is… | Graduates to… |
|---|---|
| about one piece's job, hook, reveal line or call to action | that piece's brief |
| a new piece | a row in `scripts/src/piece-register.md`, then its own brief |
| a date for a post, such as launch morning | `publishing/src/schedule.md` |
| a narrator or a character's voice | `brand/src/voice/voice.md` |
| a platform added or dropped | an update with the new answer (`.claude/rules/syntek-media/06-global-rules.md` Section 11) |

## Domain rules

- **Each piece's work:** the procedure `run-media-workflow` resolves for it.
- **The campaign's reveal line:** `.claude/rules/syntek-media/03-production-ethics.md` Sections 1
  and 9; a node that would cross it goes to the author.
- **A node about the story itself:** syntek-author's work, where present.

## Examples

```text
## Destination
A launch campaign of four teasers and one trailer, revealing nothing past chapter three.
## Frontier
- Grilling: which character's voice carries the trailer (blocks the voice design).
- Task: the cover's animation licence (to the rights register, 24/10/2026).
## Out of scope
A reading of the first chapter: it waits for the audiobook.
```
