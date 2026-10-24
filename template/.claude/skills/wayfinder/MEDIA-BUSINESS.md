# MEDIA-BUSINESS.md — wayfinder, media business mode

The domain for charting a business's media work too big for one sitting: a series of
explainers, a launch across platforms, or a channel's first season. It names where a map's
nodes come from and where each settled one lands in media's files.

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
- **Step 5 — also walk** the piece register, the schedule, the profiles in `brand/src/platforms/`
  and syntek-author's social media plan and content calendar, where present.
- **Step 11 — also route media's task nodes.** A licence, a release or a consent goes to a
  `needed` row in `production/src/rights-register.md` and
  `production/workflows/07-clear-the-rights/`; a client's sign-off to a questionnaire or the
  `Open questions` heading. A credit-spending call is never a task node: it is the author's
  decision, agreed in the procedure that makes it.
- **Step 12 — also graduate to the media homes:**

| A settled decision that is… | Graduates to… |
|---|---|
| about one piece's job, viewer, deliverables or call to action | that piece's brief |
| a new piece | a row in `scripts/src/piece-register.md`, then its own brief |
| a date for a post | `publishing/src/schedule.md` |
| a narrator or how the brand is said | `brand/src/voice/voice.md` |
| a platform added or dropped | an update with the new answer (`.claude/rules/syntek-media/06-global-rules.md` Section 11) |

## Domain rules

- **Each piece's work:** the procedure `run-media-workflow` resolves for it.
- **Platform limits:** `.claude/rules/syntek-media/03-production-ethics.md` Section 7.
- **A node that changes the social media plan:** the social-media-documents skill (syntek-author),
  where present (`.claude/rules/syntek-media/02-skills.md` Section 4).

## Examples

```text
## Destination
Six explainers on pricing, one a fortnight, each cut for the platforms the brand uses.
## Frontier
- Grilling: the order of the six (blocks the schedule).
- Task: the workshop's filming terms (to a questionnaire, 24/10/2026).
## Out of scope
A paid campaign: the brand has decided against one this season.
```
