---
workflow: 01-finish-a-copy
phase: review
skills: []
model: opus
---

# CHECKLIST.md — finish a copy

**Last Updated**: <%DATE%> **Version**: 0.1.0 **Maintained By**: <%OWNER_NAME%>
**Language**: British English (en_GB)

> **See** `how-to/docs/syntek-media/finishing-a-copy.md`. No gate in `scripts/docs/reference/the-piece-ladder.md` applies to this procedure.

## Pre-Conditions

- [ ] Read `.claude/CLAUDE.md` and `.claude/MEMORY.md`, then this folder's `CONTEXT.md` and `CLAUDE.md`. · _sonnet_
- [ ] syntek-media has just been copied, and nothing has been committed since. · _sonnet_
- [ ] The author is at hand to agree each settings entry and to run the commands that reach outside the project. · _opus_

## Execution Checklist

**What the copy printed**

- [ ] Every `conflict` then `skip` and `identical` line read as expected; any other existing path treated as a collision, removed with the author and reported through `how-to/workflows/syntek-media/03-report-a-template-problem/`. · _opus_
- [ ] A warning that syntek-author is older than v0.6.0 acted on first, by syntek-author's own procedure. · _opus_
- [ ] Noted whether `family-update did NOT run` was printed, and whether the copy took `--skip-tasks`. · _sonnet_

**Settings**

- [ ] **Each entry from item 2 of the message added only on the author's word, exactly as printed, nothing else in the file changed.** · _opus_
- [ ] The data-root guard added where `.claude/settings.json` lacks it. · _opus_
- [ ] `python3 .claude/syntek-media-permissions.py --check` run, and `--write` on the author's word. · _sonnet_
- [ ] Any index line naming the media layers or `.claude/rules/syntek-media/` added only where the author wanted it. · _sonnet_

**Outside the project**

- [ ] The ElevenLabs server removed and added again by the author, at user scope, with a base path that contains the project, or left for later with the author's agreement. · _sonnet_
- [ ] **The key exported in the author's shell; never typed, printed or written into a file.** · _opus_
- [ ] `git lfs install` run by the author where large exports will be kept. · _sonnet_
- [ ] `brand/workflows/06-check-the-setup/` run; each finding fixed, or accepted with what it blocks. · _opus_

## Done When

- [ ] **No credit spent, and no ElevenLabs tool called, during this procedure.** · _opus_
- [ ] Nothing under `how-to/` and nothing in `.copier-answers.syntek-media.yml` edited by hand. · _opus_
- [ ] The copy committed with `.copier-answers.syntek-media.yml`, and `git status` reports nothing to commit. · _sonnet_
