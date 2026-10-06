---
workflow: 04-master-a-podcast-episode
phase: produce
skills: [cut-for-platform]
model: opus
---

# CHECKLIST.md — master a podcast episode

**Last Updated**: <%DATE%> **Version**: 0.1.0 **Maintained By**: <%OWNER_NAME%>
**Language**: British English (en_GB)

> **See** `scripts/docs/reference/podcast-episodes.md`,
> `production/docs/reference/sound-and-loudness.md` and the `cut-for-platform` skill. This
> procedure passes M4 (storyboarded → produced), with M3 (scripted → storyboarded) recorded as
> `n/a — no picture`; gates are cited from `scripts/docs/reference/the-piece-ladder.md` by number
> and never restated here.

## Pre-Conditions

- [ ] Read `.claude/CLAUDE.md` and `.claude/MEMORY.md`, then this folder's `CONTEXT.md` and `CLAUDE.md`. · _sonnet_
- [ ] **The brief reads `kind: podcast` and `picture: false`, and M2 is dated.** · _opus_
- [ ] M3 recorded as `n/a — no picture` in `verified`. · _sonnet_

## Execution Checklist

**Sources**

- [ ] `footage verify` passes for every recording, bed and sting the episode uses. · _sonnet_
- [ ] The bed has its rights row; every guest has a signed release in the register. · _sonnet_
- [ ] Any voiceover segment used is `approved` and archived. · _sonnet_

**The list**

- [ ] The list has `size = ""` and `loudness = "podcast"`; clips from the transcript's anchors or `vo:<piece>`. · _sonnet_
- [ ] Intro and outro bed faded in and out and ducked under speech. · _opus_
- [ ] Every cut beyond a pause or a false start decided by the author; no speaker's meaning changed. · _opus_
- [ ] A spoken disclosure line placed wherever a synthetic voice speaks. · _opus_

**Assembling and measuring**

- [ ] `assemble` run; any failure reported, fixed in the list and assembled again. · _sonnet_
- [ ] `probe` shows audio only at the expected length; `loudness measure` quoted against `[platform.podcast.apple_rss_audio]`. · _sonnet_

**Approval**

- [ ] The author heard the whole episode; every change made in the list as a new `version`. · _opus_
- [ ] All four `M4.*` sub-checks recorded `n/a` with the no picture reason before M4; missing entries filled for older pieces. · _sonnet_
- [ ] M4 dated in `verified` and `status` set to `produced`, on the author's yes. · _sonnet_

## Done When

- [ ] **The master is audio only, on the podcast target, disclosed where it must be, and approved whole by the author.** · _opus_
- [ ] No render was hand-edited or committed. · _sonnet_
- [ ] Handed back: the master's name, length and measurements, the list's version, the disclosure, the next procedures. · _opus_
