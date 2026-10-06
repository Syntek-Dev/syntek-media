---
type: guide
skills: [thumbnail-brief, prepare-post]
model: opus
---

# Scoring options — Jev evaluates, the author chooses

**Last Updated**: <%DATE%> **Version**: 0.1.0 **Maintained By**: <%OWNER_NAME%>
**Language**: British English (en_GB)

**What it is.** A short, repeatable scorecard for several title–thumbnail pairs on one platform
and viewing surface. Jev returns typed scores and confidence; it does not write the options,
predict clicks, discover today's ranking rules or approve the package.

## Prepare the context

Write a tracked `publishing/src/thumbnails/<piece>.<platform>-<surface>.options.json`; include
`--cNN` after the piece for a cut. Use a new suffix for every later evaluation.
The JSON object has these fields, and no credentials or image bytes:

| Field | Content |
|---|---|
| `piece` | the frozen piece key |
| `platform`, `surface` | lower-case kebab names; distinguish search, home, profile-grid or feed |
| `audience`, `content` | the intended viewer and what this deliverable actually delivers |
| `guidance` | rows with `version`, `source`, `checked` (DD/MM/YYYY), `basis`, `summary` |
| `options` | several rows with unique `id`, `title`, `thumbnail_words`, `thumbnail_concept` |

Use `basis: published` for advice checked against an official HTTPS source; use `hypothesis`
for an explicitly unproven idea, citing the evidence or project record. State which advice
applies to this surface. A checked date records reading the source, not merely changing a date.
For title-only options use empty strings for both thumbnail fields; image questions are omitted.
These are text concepts. Never describe a thumbnail's pixels as verified by Jev.

## The questions and their levels

`toolkit/data/packaging-score.toml` holds the versioned house rubric: title clarity, audience
relevance, curiosity, accuracy, thumbnail concept, title–image complement and platform fit.
Each question has concrete ordered descriptions, a weight and a title/image scope.
Code normalises the score to its scale before combining it; all component answers remain visible.
The weights, confidence threshold, accuracy threshold and freshness period are house choices.
They are not platform ranking weights or a probability that viewers will click.
For different site questions, copy the rubric as packaging-score.toml in publishing's project guides,
increment `version`, and add focused question tables with optional `platforms` and `surfaces`
lists. Select the copy explicitly with `--rubric`; retain accuracy for every candidate.

## Preview, then make the approved call

Run `python3 toolkit/media.py score plan OPTIONS.json [--rubric RUBRIC.toml]` offline.
Show the exact candidates, shared context, questions, findings and one-call plan to the author.
Check current input-token pricing at https://docs.typesafe.ai/models and state the cost basis;
the plan's byte count is not an exact token count or estimated credit charge. Wait for approval.
Only then run `python3 toolkit/media.py score run OPTIONS.json --approve-call -o SCORES.json`,
using the same rubric and model choices. Keep `TYPESAFE_API_KEY` at user scope, never in Git.
`--model` may pin a Jev version; every result records the version actually returned.
There is one call, no automatic retry; after an error, report it before another paid request.
An existing output is refused. Exit 1 means guidance or score findings need review; exit 2
means the evaluation could not run. Unavailable Jev is reported; explicit author review can proceed.

## How we apply it here

- Keep the result beside the input, with its full context, rubric, model, answers and ranking.
- Record candidate IDs and the author's choice under the brief's Variants, and cite scores
  under Checks; the post package keeps the selected title. Changing an approved image returns
  to `publishing/workflows/04-brief-a-thumbnail/` for another visual review and approval.
- Read low-confidence and accuracy findings individually; the highest total never approves a pair.
- A vision model or the author checks the actual renders at display size for text, crop and controls.
- Refresh stale or unresolved guidance before spending; re-read official sources after announced
  changes, update project guides/rubrics on the author's word, and preserve old evaluations.

## Who implements it

`publishing/workflows/04-brief-a-thumbnail/` and `publishing/workflows/05-prepare-a-post/` use
the scorecard. `publishing/workflows/07-refresh-the-platform-specs/` refreshes its evidence.

## Governing standard

`.claude/rules/syntek-media/03-production-ethics.md` Sections 1 and 4 own author approval and
paid calls; `04-toolkit-pipeline.md` Section 2 owns the commands. API and text-only input:
https://docs.typesafe.ai/api and https://docs.typesafe.ai/concepts/state (checked 06/10/2026).
