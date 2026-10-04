---
workflow: 05-prepare-a-post
phase: publish
skills: [prepare-post]
model: opus
---

# CHECKLIST.md — prepare a post and schedule it

**Last Updated**: <%DATE%> **Version**: 0.1.0 **Maintained By**: <%OWNER_NAME%>
**Language**: British English (en_GB)

> **See** `publishing/docs/reference/posting-and-the-log.md`,
> `publishing/docs/reference/ai-disclosure.md` and the `prepare-post` skill. This procedure serves
> M7 (captioned → scheduled) of `scripts/docs/reference/the-piece-ladder.md`; the gate is cited
> by number and the move it guards, and this list never restates it.

## Pre-Conditions

- [ ] Read `.claude/CLAUDE.md` and `.claude/MEMORY.md`, then this folder's `CONTEXT.md` and `CLAUDE.md`. · _sonnet_
- [ ] Read `posting-and-the-log.md`, `ai-disclosure.md`, the `prepare-post` skill and its mode file. · _opus_
- [ ] **The brief dates M5, and M6 or its `n/a`;** every deliverable rendered and `checked`; thumbnails approved where taken. · _sonnet_
- [ ] The content calendar's entries for this piece read where syntek-author's is present; otherwise the platform profiles. · _opus_

## Execution Checklist

**Before writing**

- [ ] **Every rights row the piece uses is `cleared`;** any other sent to the rights procedure, its deliverable held. · _opus_
- [ ] The disclosure decided per deliverable: the label by that platform's rule, named; the description line written; any spoken or on-screen line noted. · _opus_
- [ ] Any unclear disclosure put to the author, and the decision dated with its reason. · _opus_

**Writing and checking**

- [ ] One section per deliverable in the package's skeleton, every bullet filled. · _opus_
- [ ] **One section per placement** (`— <platform>:<slug>`), with its channel guide's bullets: only the words outside its written piece, its images as bullets, its date cited from the written piece. · _opus_
- [ ] A feed episode's section cites its show register; its register part of M7 sent through the podcast-feed workflow; each episode page on another site a placement. · _opus_
- [ ] Every count written beside its `platforms.toml` key under **Limits**; hashtags warned above `platform.instagram.hashtags_max`. · _sonnet_
- [ ] Every count inside its limit; every `verify` key relied on named. · _sonnet_
- [ ] The spelling, grammar and fact-check skills run as a supportive report, where present; where absent, the missing skill named. · _opus_
- [ ] Nothing invented: no claim, quotation, statistic, testimonial, endorsement or link the author did not give or a source did not confirm. · _opus_
- [ ] **`media.py flags --piece <piece> --strict` reports none** across the piece's files. · _sonnet_

**Approval and the schedule**

- [ ] The author approved the whole package; `approved` dated. · _opus_
- [ ] One schedule row per deliverable and per placement (`<platform>:<slug>`), status `planned`, the calendar entry or the written piece cited in Notes where present. · _sonnet_
- [ ] Every placement on a site or list the brand does not own has a dated agreement in its profile row; a written piece not `final` reported as a warning. · _opus_
- [ ] M7's checks confirmed against this run; only then each row set to `ready` and the brief's `status` and `verified` set. · _sonnet_
- [ ] Handed back: the package, the rows, each disclosure decision, every `verify` key; the author asked to report each post. · _opus_

## Done When

- [ ] **The author holds an approved package for every deliverable, and nothing was posted.** · _opus_
- [ ] Every deliverable's disclosure follows its platform's rule, with the description line always. · _opus_
- [ ] Every deliverable has a schedule row, and M7 is recorded in the brief. · _sonnet_
