---
workflow: 01-plan-the-cut-downs
phase: convert
skills: [repurpose]
model: opus
---

# CHECKLIST.md — plan the cut-downs of a master

**Last Updated**: <%DATE%> **Version**: 0.1.0 **Maintained By**: <%OWNER_NAME%>
**Language**: British English (en_GB)

> **See** `publishing/docs/reference/cut-downs.md`. No gate in `scripts/docs/reference/the-piece-ladder.md` applies to this procedure.

## Pre-Conditions

- [ ] Read `.claude/CLAUDE.md` and `.claude/MEMORY.md`, then this folder's `CONTEXT.md` and `CLAUDE.md`. · _sonnet_
- [ ] Read `cut-downs.md`, the `repurpose` skill and its mode file. · _opus_
- [ ] **The brief's `verified` dates M4, and the master is in `production/src/renders/`.** · _sonnet_
- [ ] Read the brief, the script or transcript, and the calendar entries for this piece where syntek-author's calendar is present. · _opus_

## Execution Checklist

**Limits and timing**

- [ ] Each candidate deliverable's preset read with `media.py presets`; overrides and `verify` keys noted. · _sonnet_
- [ ] In and Out read from the master-timed captions or the edit decision list; a recorded piece's captions retimed to the master first. · _sonnet_

**Choosing**

- [ ] **Every cut stands alone from its first line,** its lines cited as `beat.line`. · _opus_
- [ ] Every cut opens on its hook, in words and on screen. · _opus_
- [ ] Every vertical deliverable framed (`crop x=<px>` or `pad`), faces, titles and captions inside `safe_zone`. · _opus_
- [ ] Every cut inside the `max_seconds` of each of its deliverables. · _sonnet_
- [ ] **No near-identical cuts;** any dropped or merged, with the reason. · _opus_

**Agreeing and writing**

- [ ] The plan proposed with a reason per cut; the author decided each one. · _opus_
- [ ] `publishing/src/cut-downs/<piece>.md` written in its skeleton, one sentence per line; nothing overwritten without confirmation. · _sonnet_
- [ ] Handed back: the cuts, their deliverables, every `verify` key relied on, the cuts needing their own thumbnail, and the next procedure. · _opus_

## Done When

- [ ] **The author has approved every cut in the plan, and `approved` is dated.** · _opus_
- [ ] Every cut is timed on the master, framed, inside its limits, and stands alone. · _opus_
- [ ] Nothing was rendered, and no calendar entry was rewritten. · _sonnet_
