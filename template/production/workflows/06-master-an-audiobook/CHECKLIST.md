---
workflow: 06-master-an-audiobook
phase: produce
skills: [narrate-audiobook]
model: opus
---

# CHECKLIST.md — master an audiobook

**Last Updated**: <%DATE%> **Version**: 0.1.0 **Maintained By**: <%OWNER_NAME%>
**Language**: British English (en_GB)

> **See** `production/docs/reference/audiobook-narration.md` and the `narrate-audiobook` skill.
> This procedure passes M4 (storyboarded → produced) and M5 (produced → cut); gates are cited
> from `scripts/docs/reference/the-piece-ladder.md` by number and never restated here.

## Pre-Conditions

- [ ] Read `.claude/CLAUDE.md` and `.claude/MEMORY.md`, then this folder's `CONTEXT.md` and `CLAUDE.md`. · _sonnet_
- [ ] **Every chapter to master, the credits included, is on the `human` or `ai` route, with every part approved or its recording logged.** · _opus_
- [ ] M2 dated, and M3 recorded as `n/a — no picture` in `verified`. · _sonnet_

## Execution Checklist

**Mastering and checking**

- [ ] `audiobook master` run per chapter and credit, each scene break's pause read from the chapter's chunks sidecar; Master and Duration recorded, row `mastered`. · _sonnet_
- [ ] `audiobook check` run on every file; each failure reported with its measurement. · _sonnet_
- [ ] Every failure fixed at its source, never by loosening the check; passing rows `checked`. · _opus_

**Approval and archiving**

- [ ] The author heard every chapter whole; faults sent back to be mastered, regenerated or re-recorded. · _opus_
- [ ] Each approved master archived with `footage add` (`--kind generated` or `--kind audio`), the chapter noted; chunk takes archived only where the author wants them. · _sonnet_
- [ ] All four `M4.*` sub-checks recorded `n/a` with the no picture reason before M4; missing entries filled for older pieces. · _sonnet_
- [ ] M4 dated in `verified` and `status` set to `produced` once every master was approved and archived. · _sonnet_

**Packaging**

- [ ] Opening and closing credits are files of their own; chapters in order; a retail sample cut with `media.py cut --deliverable audiobook.acx`, within `sample_max_seconds`, where taken. · _sonnet_
- [ ] Each channel's own targets read from its `[audiobook.<store>]` table, with every `verify` key flagged. · _sonnet_
- [ ] The disclosure each synthetic narration channel asks for noted for the post package. · _opus_
- [ ] Nothing mastered or packaged for a channel on the `external` route. · _opus_

## Done When

- [ ] **Every chapter passes `audiobook check`, has been heard and approved by the author, and is archived.** · _opus_
- [ ] M5 dated, M6 recorded as `n/a — audiobook`, and `status` set to `cut`. · _sonnet_
- [ ] Handed back: durations and checks, masters archived, each channel's package and disclosure, open `VERIFY` items. · _opus_
