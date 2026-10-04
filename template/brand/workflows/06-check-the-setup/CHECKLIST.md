---
workflow: 06-check-the-setup
phase: review
skills: []
model: opus
---

# CHECKLIST.md — check the setup

**Last Updated**: <%DATE%> **Version**: 0.1.0 **Maintained By**: <%OWNER_NAME%>
**Language**: British English (en_GB)

> **See** `production/docs/reference/elevenlabs.md`. No gate in `scripts/docs/reference/the-piece-ladder.md` applies to this procedure.

## Pre-Conditions

- [ ] Read `.claude/CLAUDE.md` and `.claude/MEMORY.md`, then this folder's `CONTEXT.md` and `CLAUDE.md`. · _sonnet_
- [ ] Working from the repository root, with `python3` 3.11 or later available, or its absence reported. · _sonnet_

## Execution Checklist

**The report**

- [ ] `python3 toolkit/media.py check --setup` run; its exit code read (0 clean, 1 findings, 2 could not run). · _sonnet_
- [ ] Nothing from the user's Claude Code configuration printed or copied beyond what the report prints. · _sonnet_
- [ ] Each finding explained to the author with what it blocks and its fix. · _opus_

**The fixes**

- [ ] Each fix given as an exact command; installs and the server re-add done by the author. · _sonnet_
- [ ] The base-path fix taken from `production/docs/reference/elevenlabs.md`; the key exported in the shell, never typed or written. · _sonnet_
- [ ] **A permission entry added to `.claude/settings.json` only on the author's explicit word, exactly as printed, nothing else changed.** · _opus_
- [ ] The check run again after the fixes, until it exits 0 or each open finding is accepted. · _sonnet_
- [ ] **No credit-spending call made while an ElevenLabs line is open.** · _opus_

**Record**

- [ ] A dated Status line in `.claude/MEMORY.md`, under the heading syntek-author's 00-project.md maps it to, where present; an earlier line superseded, not deleted. · _sonnet_

## Done When

- [ ] **The check exits 0, or every open finding is recorded with what it blocks and accepted by the author.** · _opus_
- [ ] No line reported as passed that could not run. · _sonnet_
- [ ] Handed back: each finding, fixed or open, and the commands and skills each open one blocks. · _opus_
