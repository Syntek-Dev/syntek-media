---
workflow: 05-prepare-a-post
phase: publish
skills: [prepare-post]
model: opus
---

# STEPS.md — prepare a post and schedule it

**Last Updated**: <%DATE%> **Version**: 0.1.0 **Maintained By**: <%OWNER_NAME%>
**Language**: British English (en_GB)

The ordered procedure for writing a piece's post package and scheduling every deliverable. Each
step names the skill and guide it uses. **Run in order** — the ordering is load-bearing — and tick
`CHECKLIST.md` as you go.

> Read the read-order files first (this folder's `CONTEXT.md` and `CLAUDE.md`), then
> `publishing/docs/reference/posting-and-the-log.md` and
> `publishing/docs/reference/ai-disclosure.md`. The `prepare-post` skill is this procedure in
> skill form; read it, and its mode file, before step 1.

## 1. Confirm the piece is ready to package

> **Skill:** `prepare-post` · **Guide:** `scripts/docs/reference/the-piece-ladder.md`

Read the brief: its `verified` dates M5, and M6 or records it `n/a`. Every deliverable of the brief
and of the cut-down plan is rendered and `checked`; every thumbnail a platform takes is approved
in `publishing/src/thumbnails/`. Read an existing package before writing; a second one for the
same piece is a revision. **Nothing is packaged that has not been seen by the author.**
_Mechanical._

## 2. Read the calendar, or the profiles

> **Skill:** `prepare-post` · **Guide:** `publishing/docs/reference/posting-and-the-log.md`

Where syntek-author's content calendar is present, read this piece's entries: the dates, the
slots and the text-only posts around them are the calendar's, and a change to them belongs to the
social-media-documents skill (syntek-author), where present. Any other social-media document of
syntek-author that sets a value for a platform (the plan, an operating procedure) owns that value;
the brand's profiles, `brand/src/platforms/<platform>.md`, hold only what none sets. Read the
guide for each platform the package goes to. For a placement on the brand's own sites, blogs or
newsletters, read the profile's row for its site or list, and the written piece it sits in (a
post, a page or an issue: read, never edited); its words are the written side's. _Substantive._

## 3. Check the rights

> **Skill:** `prepare-post` · **Guide:** `production/docs/reference/rights-and-consent.md`

Every rights ID the piece uses, in its brief's `rights` and its shot list, is `cleared` in
`production/src/rights-register.md`, and nothing the deliverables show or play lacks a row. **A
row that is not `cleared` stops the package** for that deliverable: send it to
`production/workflows/07-clear-the-rights/` and say so. _Substantive._

## 4. Decide each deliverable's disclosure

> **Skill:** `prepare-post` · **Guide:** `publishing/docs/reference/ai-disclosure.md`

Read the brief's `synthetic_voice`, `ai_visuals` and `music`. For each deliverable, decide the
platform's label from that platform's row of the guide, and name the rule it rests on; write the
description line; note any spoken or on-screen line the piece already carries. An unclear case
goes to the author, and the decision is recorded with its date and reason. _Substantive._

## 5. Write each deliverable's section

> **Skill:** `prepare-post` · **Guide:** `publishing/docs/reference/posting-and-the-log.md`

Write `publishing/src/posts/<piece>.md` in its skeleton (`publishing/src/posts/CLAUDE.md`): one
`## <platform>.<format>` section per deliverable, ` — cNN` for a cut, each with its Title,
Description, Hashtags, Disclosure, Captions, Thumbnail, Render, Calendar and Scheduled bullets.
For `youtube.long` only, add Chapters as fenced `MM:SS <title>` lines, first `00:00`,
then beat starts from tracked cues plus the edit's voice offset, or tracked master captions,
rounded down; beat names unless the author changes them. Check the chapter keys and `verify`.
The Description's fence holds one sentence per line, as every `src/` file does. The words follow
the mode file and the platform's guide, and promise only what the deliverable delivers.

**A placement** on the brand's own channels (the one file a page or an issue plays or shows first)
has its own section, `## <platform>.<format>[ — cNN] — <platform>:<slug>`, with the bullets its
channel's guide gives in place of Title, Description and Hashtags; its other images are bullets of
it, its date the written piece's own, cited. **A feed episode** has `## podcast.feed_audio`, whose
title, description and chapters are cited from its show register, never repeated; its register
part of M7 runs through the podcast-feed workflow, where the project serves its own feed, and each
episode page on a site other than the feed's is a placement here.

Before choosing the words, propose several title–thumbnail pairs and follow
`publishing/docs/reference/scoring-options.md`: write the option/context JSON, preview with
`media.py score plan`, show the current cost basis and wait before `score run --approve-call`.
Retain the rubric, dated platform/surface guidance, resolved model and findings beside the brief;
Jev scores text concepts only. The author selects; unavailable Jev is reported and explicit
manual review remains possible. A changed approved image returns to
`publishing/workflows/04-brief-a-thumbnail/` for visual checks and approval. _Substantive._

## 6. Count every limit against its key

> **Skill:** `prepare-post` · **Guide:** `publishing/docs/reference/platform-specs.md`

Run `python3 toolkit/media.py presets` for each platform and deliverable. Count the title, the
description, the caption or post text, the hashtags and the mentions against their keys, and
write each count beside its key under **Limits**. Warn above `platform.instagram.hashtags_max`;
name every `verify` key relied on. A count over its limit is rewritten, never trimmed by the
platform. _Mechanical._

## 7. Proofread, and check the claims

> **Skill:** spelling, grammar and fact-check (syntek-author), where present · **Guide:** `publishing/docs/reference/posting-and-the-log.md`

Check that `.claude/skills/<skill>/SKILL.md` exists for each before naming the step. Run the
spelling and grammar skills as a supportive report, applying only what the author accepts; run
the fact-check skill on every factual claim in the copy, leaving any unresolved claim flagged
`VERIFY`. Where a skill is absent, say which, and offer a read-through only if the author asks.
_Substantive._

## 8. Clear the flags

> **Skill:** `prepare-post` · **Guide:** `scripts/docs/reference/the-piece-ladder.md`

Run `python3 toolkit/media.py flags --piece <piece> --strict`: it gathers the piece's files by
their house names (its folder under `scripts/src/pieces/`, its edit decision list, cards and
registers, its plan, captions, thumbnail briefs and this package). Each
`AUTHOR TO CONFIRM` and `VERIFY` is resolved by the author, or the deliverable it touches waits.
_Substantive._

## 9. Have the author approve the package

> **Skill:** `prepare-post` · **Guide:** `publishing/docs/reference/posting-and-the-log.md`

Put the whole package to the author: every section, every disclosure decision and its rule, every
`verify` key relied on. On approval, date `approved` in its frontmatter; on a change, go back to
the step it touches. _Substantive._

## 10. Write the schedule rows

> **Skill:** `prepare-post` · **Guide:** `publishing/docs/reference/posting-and-the-log.md`

Add one row per deliverable and per placement to `publishing/src/schedule.md`, with its date,
its time in <%TIMEZONE%>, its platform (`<platform>:<slug>` for a placement), key, piece and
package, status `planned`, and, where syntek-author's content calendar is present, its calendar
entry in Notes. A placement takes its date and time from its written piece, cited in Notes; a
feed episode is one row, `podcast` · `podcast.feed_audio`, at the register's `pub_date`. Never
delete or reuse a row. A row becomes `ready` only at step 11, once M7 passes. _Mechanical._

## 11. Record the gate

> **Skill:** `prepare-post` · **Guide:** `scripts/docs/reference/the-piece-ladder.md`

Read M7 in the ladder guide and confirm each of its checks against this run: for a placement, a
dated agreement where the brand does not own the site or list, its Links to, and its written
piece's status read (a piece not `final` is a warning to report, never a gate); for a feed
episode, its register row `ready` and `feed check` clean. When every one passes, set each of the piece's `planned` schedule rows to `ready`, set the brief's `status` to
`scheduled` and date M7 in `verified`; a check the author waives is recorded there with the date
and the reason. While a check fails, the rows stay `planned`. _Mechanical._

## 12. Hand back

> **Skill:** `prepare-post` · **Guide:** `publishing/docs/reference/posting-and-the-log.md`

Report the package, each schedule row, each disclosure decision and its rule, and every `verify`
key relied on. When the author is ready to post a deliverable, give its title and description in
chat as paste-ready text, the fenced lines joined into paragraphs and video chapters appended; never write it to a file.
**The author posts.** Ask the author to report each post, with its URL and the label they set, so
`publishing/workflows/06-record-a-publication/` can log it. _Substantive._
