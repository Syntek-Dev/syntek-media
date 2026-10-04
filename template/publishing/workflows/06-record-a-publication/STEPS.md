---
workflow: 06-record-a-publication
phase: publish
skills: [prepare-post]
model: opus
---

# STEPS.md — record a publication

**Last Updated**: <%DATE%> **Version**: 0.1.0 **Maintained By**: <%OWNER_NAME%>
**Language**: British English (en_GB)

The short procedure for keeping the schedule and the publish log true. Run it every time the
author posts, moves or drops a deliverable. Each step names the skill and guide it uses. **Run in
order** — the ordering is load-bearing — and tick `CHECKLIST.md` as you go.

> Read the read-order files first (this folder's `CONTEXT.md` and `CLAUDE.md`), then
> `publishing/docs/reference/posting-and-the-log.md` and the writing rules at the top of the
> schedule and the log. The `prepare-post` skill writes the rows, and only from the author's
> report.

## 1. Read the schedule row and the package

> **Skill:** `prepare-post` · **Guide:** `publishing/src/CONTEXT.md`

Find the deliverable's row in `publishing/src/schedule.md` and its section in
`publishing/src/posts/<piece>.md`. Never work from memory of an earlier session. A deliverable
with no row was never scheduled: it goes back to `publishing/workflows/05-prepare-a-post/`.
_Mechanical._

## 2. Establish what the author did

> **Skill:** `prepare-post` · **Guide:** `publishing/docs/reference/posting-and-the-log.md`

Posted: when, at which URL, whether the platform's AI label was set and the description line went
in, and how the captions went up. Moved: the new date and time. Dropped: why. Ask the author
wherever the report is unclear; never fill a gap from the package. _Substantive._

## 3. Move the schedule row on

> **Skill:** `prepare-post` · **Guide:** `publishing/docs/reference/posting-and-the-log.md`

Set the row's status to `posted`, `moved` or `dropped`. A moved row takes the new date, with the
old one kept in Notes; a dropped row keeps its place, with the reason in Notes. Never delete a
row. _Mechanical._

## 4. Write the log row

> **Skill:** `prepare-post` · **Guide:** `publishing/docs/reference/posting-and-the-log.md`

For a post only, add a row to `publishing/src/publish-log.md`: the date the author posted it, the
platform, the deliverable's key, the piece, the URL exactly as the author gave it, the disclosure
the author reports setting, and the captions (the file uploaded, `burned`, or `none` with the
reason). _Mechanical._

## 5. Compare what was set with the package

> **Skill:** `prepare-post` · **Guide:** `publishing/docs/reference/ai-disclosure.md`

Where the disclosure set, the captions or the words differ from the package, **report it to the
author at once**, with the rule the package rested on. The log keeps what was actually set; if the
author corrects it on the platform, that correction is a dated note, not a rewritten row.
_Substantive._

## 6. Append corrections; never overwrite

> **Skill:** `prepare-post` · **Guide:** `publishing/src/CONTEXT.md`

An earlier schedule or log entry that turns out to be wrong gets a dated note under that file's
`## Corrections`, saying what was wrong and what is true. History is never edited. _Mechanical._

## 7. Close the piece when all of it is out

> **Skill:** `prepare-post` · **Guide:** `scripts/docs/reference/the-piece-ladder.md`

When every schedule row for the piece is `posted` or `dropped`, and every `posted` row has its log
row, set the brief's `status` to `published`. Published is not a gate, so nothing is dated in
`verified`. A piece with any row still to go stays `scheduled`. _Mechanical._

## 8. Hand back

> **Skill:** `prepare-post` · **Guide:** `publishing/docs/reference/posting-and-the-log.md`

One line per change, plus **everything still to go out**: the next rows due, with their dates and
times in <%TIMEZONE%>, and any disclosure difference still open. That list is the point of the
schedule. _Substantive._
