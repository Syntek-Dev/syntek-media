# MEDIA-NONFICTION.md — wayfinder, media non-fiction mode

The domain for charting a non-fiction author's media work too big for one sitting: a season of
episodes, a series of teaching clips from one book, or a talk turned into many cuts. It names
where a map's nodes come from and where each settled one lands in media's files.

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
- **Step 5 — also walk** the piece register, the schedule, the rights register's quotations and
  syntek-author's chapters and argument maps, where present, one piece's claim per node.
- **Step 11 — also route media's task nodes.** A translation's or a venue's permission and a
  guest's release go to a `needed` row in `production/src/rights-register.md` and
  `production/workflows/07-clear-the-rights/`; a guest's topics to a questionnaire. A claim's
  truth is a research node for the fact-check skill (syntek-author), where present, never a task.
- **Step 12 — also graduate to the media homes:**

| A settled decision that is… | Graduates to… |
|---|---|
| about one piece's claim, listener, hook or call to action | that piece's brief |
| a new piece | a row in `scripts/src/piece-register.md`, then its own brief |
| a date for a post or an episode | `publishing/src/schedule.md` |
| a narrator or how a name or borrowed word is said | `brand/src/voice/voice.md` |
| a platform added or dropped | an update with the new answer (`.claude/rules/syntek-media/06-global-rules.md` Section 11) |

## Domain rules

- **Each piece's work:** the procedure `run-media-workflow` resolves for it.
- **A piece's claim:** its brief, and the Domain rules of
  `.claude/skills/write-script/NONFICTION.md`.
- **A node about the argument itself:** syntek-author's work, where present
  (`.claude/rules/syntek-media/03-production-ethics.md` Section 9).

## Examples

```text
## Destination
Eight teaching clips from the chapter on hospitality, one claim each, in the book's order.
## Frontier
- Grilling: which translation the cards use (blocks every quotation's rights row).
- Research: the passage's date and source (to the fact-check skill, where present).
## Out of scope
A podcast season on the same chapter: a second map, once the clips are out.
```
