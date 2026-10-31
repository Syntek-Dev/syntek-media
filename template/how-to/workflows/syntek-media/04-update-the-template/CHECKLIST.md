---
workflow: 04-update-the-template
phase: review
skills: []
model: opus
---

# CHECKLIST.md — update the template

**Last Updated**: <%DATE%> **Version**: 0.1.0 **Maintained By**: <%OWNER_NAME%>
**Language**: British English (en_GB)

> **See** `how-to/docs/syntek-media/updating-the-template.md`. No gate in `scripts/docs/reference/the-piece-ladder.md` applies to this procedure.

## Pre-Conditions

- [ ] Read `.claude/CLAUDE.md` and `.claude/MEMORY.md`, then this folder's `CONTEXT.md` and `CLAUDE.md`. · _sonnet_
- [ ] The author wants this update, and is at hand to answer its questions and read its report. · _opus_
- [ ] No other template's update is under way in this project. · _sonnet_

## Execution Checklist

**Before the update**

- [ ] The project is its own repository, `git status` reports nothing to commit (untracked files included), and the work is on the branch `update-syntek-media`. · _sonnet_
- [ ] Where `.copier-answers.syntek-author.yml` stands, syntek-author updated first, at v0.6.0 or later, by its own procedure, and committed. · _opus_
- [ ] `ls -ld .agents .agents.syntek-held how-to` read: no held link, and `how-to` a real folder or absent. · _sonnet_
- [ ] Every changed answer agreed with the author, each list given whole and `BRAND_KIND` unchanged; for a platform or media kind going, every file it deletes that the author needs copied out and committed. · _opus_

**The update**

- [ ] The update run with `uvx --python '>=3.14'`, the five `GIT_CONFIG_*` variables and `-a .copier-answers.syntek-media.yml`; `--defaults` added only where a session ran it, on the author's word. · _sonnet_
- [ ] It ended with the line starting `▸ syntek-media update report`; a stop with an error went to `how-to/workflows/syntek-media/05-recover-a-stopped-update/`, with nothing committed; a framed `family-update did NOT run` told to the author and the update run again on Python 3.14 or later. · _sonnet_

**The output**

- [ ] Every migration's output read with the author, the 0.6.0 crossing report among it where this update crossed 0.6.0, and each hand edit it names made. · _opus_
- [ ] Every `CONFLICT` resolved with the author; under `how-to/`, nothing edited, only the `git add` its `RESTORED` entry gives. · _opus_
- [ ] Every `.rej` file dealt with; under `how-to/`, removed only with the `rm` line the report prints, by the author in their own terminal where Claude Code refuses it. · _sonnet_
- [ ] `RESTORED` and `LEFT AS IT IS` read with the author and each reason acted on; any departure recorded in syntek-author's project settings file where present, otherwise under 'Project-specific rules' in `.claude/CLAUDE.md`, never in `how-to/`. · _opus_
- [ ] Every `NOT UPDATED`, `DELETED`, `NOT RESTORED`, `NOT ADDED` and `NOT COMPARED` entry decided with the author; `take:` and `restore:` run only on their word. · _opus_
- [ ] The settings entries and MCP servers the report says it added noted; any entry it names for adding by hand added with the author. · _opus_
- [ ] `git diff` read with the author; after a platform or media-kind change, the files that describe the options edited by hand. · _opus_
- [ ] Where the update added deny or ask rules, the permissions script run with `--check`, and with `--write` on the author's word. · _sonnet_

## Done When

- [ ] **Nothing under `how-to/` was edited by hand:** every change there came from the update or the commands its report printed. · _opus_
- [ ] The update is committed with `.copier-answers.syntek-media.yml`, and `git status` reports nothing to commit. · _sonnet_
- [ ] Any other template's update is left for its own procedure, after this commit. · _sonnet_
