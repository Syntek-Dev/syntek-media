---
workflow: 04-set-up-a-platform
phase: author
skills: []
model: opus
---

# CHECKLIST.md — set up a platform

**Last Updated**: <%DATE%> **Version**: 0.1.0 **Maintained By**: <%OWNER_NAME%>
**Language**: British English (en_GB)

> **See** `brand/docs/reference/platform-profiles.md`. No gate in `scripts/docs/reference/the-piece-ladder.md` applies to this procedure.

## Pre-Conditions

- [ ] Read `.claude/CLAUDE.md` and `.claude/MEMORY.md`, then this folder's `CONTEXT.md` and `CLAUDE.md`. · _sonnet_
- [ ] **The platform is one this project posts to, and its profile exists;** none made by hand. · _sonnet_
- [ ] The profile read as it stands. · _sonnet_

## Execution Checklist

**The social media plan**

- [ ] syntek-author's social media plan and calendar read for this platform, where present, or their absence said. · _opus_
- [ ] Where the plan is present, the profile cites it for cadence, tone, call to action, hashtags and bios, and restates none of them. · _opus_

**The profile**

- [ ] Account written exactly as the author gave it; nothing guessed. · _sonnet_
- [ ] Deliverables chosen from `python3 toolkit/media.py presets`, by key; any `verify` key they rely on noted. · _opus_
- [ ] Cadence, tone and call to action decided by the author, only where no plan owns them; times in the project's time zone. · _opus_
- [ ] Hashtag sets agreed, only where no plan owns them, counted against the platform's keys and cited by key. · _opus_
- [ ] No platform number written anywhere in the profile. · _sonnet_

**Overrides**

- [ ] Each override confirmed by the platform's own current words, with key, value, why, source and date. · _opus_
- [ ] `python3 toolkit/media.py presets` shows each override applied. · _sonnet_
- [ ] `toolkit/data/platforms.toml` untouched; any unconfirmed difference sent to the refresh procedure. · _sonnet_

**Record**

- [ ] `python3 toolkit/media.py flags` shows no flag in a section `prepare-post` reads. · _sonnet_
- [ ] Decisions dated in `.claude/MEMORY.md`, under the heading syntek-author's 00-project.md maps it to, where present. · _sonnet_

## Done When

- [ ] **The profile holds what the brand decides on this platform, and nothing the plan or the platform data owns.** · _opus_
- [ ] Every override is sourced and dated. · _sonnet_
- [ ] Handed back: the profile's contents, what it cites, overrides, `verify` keys relied on, flags left. · _opus_
