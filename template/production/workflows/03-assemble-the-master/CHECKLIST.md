---
workflow: 03-assemble-the-master
phase: produce
skills: [cut-for-platform]
model: opus
---

# CHECKLIST.md — assemble the master

**Last Updated**: <%DATE%> **Version**: 0.1.0 **Maintained By**: <%OWNER_NAME%>
**Language**: British English (en_GB)

> **See** `production/docs/reference/edit-decision-lists.md`,
> `production/docs/reference/sound-and-loudness.md` and the `cut-for-platform` skill. This
> procedure passes M4 (storyboarded → produced); gates are cited from
> `scripts/docs/reference/the-piece-ladder.md` by number and never restated here.

## Pre-Conditions

- [ ] Read `.claude/CLAUDE.md` and `.claude/MEMORY.md`, then this folder's `CONTEXT.md` and `CLAUDE.md`. · _sonnet_
- [ ] **The brief reads `storyboarded`, or `scripted` with M3 recorded as not applicable, and its script or transcript is approved.** · _opus_
- [ ] Every open gate before M4 named to the author and routed, or none open. · _sonnet_

## Execution Checklist

**Sources**

- [ ] Every shot in the shot list (or every beat of the transcript) has a source. · _opus_
- [ ] `footage verify` passes for every footage ID the edit uses. · _sonnet_
- [ ] Every voiceover segment the edit uses is `approved` and archived. · _sonnet_
- [ ] Every licensed or identifiable item has its rights row. · _sonnet_

**Cards and the list**

- [ ] Each card copied from the brand's component (or the toolkit's fallback), its tokens link fixed, the brand's own layout flag deleted from the copy, `card.py check` clean. · _sonnet_
- [ ] Each card's words agreed with the author; the brand's component left unedited. · _opus_
- [ ] The list written with the author: frame, rate, loudness target, clips in order, overlays, voice, beds with fades and ducking. · _opus_

**Assembling**

- [ ] `assemble` run; any exit 2 reported with its install hint, any exit 1 fixed in the list and assembled again. · _sonnet_
- [ ] `probe` and `loudness measure` run; duration, frame, streams, loudness and true peak quoted against the target. · _sonnet_
- [ ] A recorded piece's captions retimed to the master with `captions retime --edl`, or the step marked skipped for a scripted piece. · _sonnet_

**Approval**

- [ ] The author watched or heard the whole master; every change made in the list as a new `version`. · _opus_
- [ ] All four `M4.*` sub-checks recorded `n/a` with the footage or no picture reason before M4; missing entries filled for older pieces. · _sonnet_
- [ ] M4 dated in `verified` and `status` set to `produced`, on the author's yes. · _sonnet_

## Done When

- [ ] **The master rebuilds from the list, probes clean, meets its target, and the author approved it whole.** · _opus_
- [ ] No render was hand-edited or committed. · _sonnet_
- [ ] Handed back: the master's name and measurements, the list's version, the sources and takes used, the next procedures. · _opus_
