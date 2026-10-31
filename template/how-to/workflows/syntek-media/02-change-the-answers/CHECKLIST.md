---
workflow: 02-change-the-answers
phase: plan
skills: []
model: opus
---

# CHECKLIST.md — change the answers

**Last Updated**: <%DATE%> **Version**: 0.1.0 **Maintained By**: <%OWNER_NAME%>
**Language**: British English (en_GB)

> **See** `how-to/docs/syntek-media/changing-the-answers.md`. No gate in `scripts/docs/reference/the-piece-ladder.md` applies to this procedure.

## Pre-Conditions

- [ ] Read `.claude/CLAUDE.md` and `.claude/MEMORY.md`, then this folder's `CONTEXT.md` and `CLAUDE.md`. · _sonnet_
- [ ] The author wants an answer changed, and is at hand to settle it and read the update's report. · _opus_
- [ ] No other template's update is under way in this project. · _sonnet_

## Execution Checklist

**The answer**

- [ ] The question named as the answers file names it, and its new value agreed word for word. · _opus_
- [ ] **A change of `BRAND_KIND` refused, with the reason: a different brand kind is a new project.** · _opus_
- [ ] Every list answer written out whole, each kept value with the new one, none left out by accident. · _opus_
- [ ] **For each departing platform or media kind, every file it deletes read with the author; what they need copied out and committed.** · _opus_

**The update**

- [ ] Steps 1 to 3 of `how-to/workflows/syntek-media/04-update-the-template/` passed: clean tree on `update-syntek-media`, syntek-author first where present, the three names checked. · _sonnet_
- [ ] The update run with `uvx --python '>=3.14'`, the five `GIT_CONFIG_*` variables, `-a .copier-answers.syntek-media.yml` and one `--data` per changed answer; `--defaults` added only where a session ran it, on the author's word. · _sonnet_
- [ ] It ended with the update report; a stop with an error went to `how-to/workflows/syntek-media/05-recover-a-stopped-update/`, with nothing committed. · _sonnet_

**After the update**

- [ ] The migration output, every report section, `git status` and `git diff` read with the author, as steps 6 and 7 of `how-to/workflows/syntek-media/04-update-the-template/` say. · _opus_
- [ ] Every `DELETED` entry is on the list read at step 4; a `restore` run only on the author's word. · _opus_
- [ ] The files that describe the options, and a removed platform's rows in `brand/src/platforms/overrides.toml`, edited by hand with the author. · _opus_
- [ ] A new platform or a new coding agent noted for its follow-on procedure. · _sonnet_

## Done When

- [ ] **`.copier-answers.syntek-media.yml` changed only by the update, never by hand.** · _opus_
- [ ] Nothing under `how-to/` edited by hand: every change there came from the update or the commands its report printed. · _opus_
- [ ] The update committed with `.copier-answers.syntek-media.yml`, and `git status` reports nothing to commit. · _sonnet_
