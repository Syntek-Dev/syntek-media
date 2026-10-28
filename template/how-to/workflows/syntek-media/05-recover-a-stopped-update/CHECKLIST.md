---
workflow: 05-recover-a-stopped-update
phase: review
skills: []
model: opus
---

# CHECKLIST.md — recover a stopped update

**Last Updated**: <%DATE%> **Version**: 0.1.0 **Maintained By**: <%OWNER_NAME%>
**Language**: British English (en_GB)

> **See** `how-to/docs/syntek-media/updating-the-template.md`. No gate in `scripts/docs/reference/the-piece-ladder.md` applies to this procedure.

## Pre-Conditions

- [ ] Read `.claude/CLAUDE.md` and `.claude/MEMORY.md`, then this folder's `CONTEXT.md` and `CLAUDE.md`. · _sonnet_
- [ ] The stop recognised: `OSError: [Errno 39]`, or `FileExistsError: [Errno 17]` or `NotADirectoryError` naming `how-to`, or `ForbiddenPathError` naming a path in `how-to`, or `ForbiddenPathError` naming a path in .agents after a framed `agents-outside-link did NOT run`, or another error after which `git status` shows changes, or a held `.agents.syntek-held`. · _opus_
- [ ] The stop was syntek-media's update, not syntek-author's, which has its own recovery procedure. · _opus_
- [ ] Nothing the stopped update left has been committed. · _sonnet_
- [ ] The author is at hand to agree the discard and any rename. · _opus_

## Execution Checklist

**Before the discard**

- [ ] `ls -ld .agents .agents.syntek-held` read; a held link put back with `rm .agents` (a link) or `mv .agents .agents.from-update` (a folder or a file), then `mv .agents.syntek-held .agents`, and never while .agents stood. · _sonnet_
- [ ] `git clean -n -d` read with the author, and everything of theirs it listed committed or moved out of the project, anything they want from an `.agents.from-update` included. · _opus_

**The discard**

- [ ] `git reset --hard && git clean -fd` run only with the author's agreement, in a project that is its own repository. · _sonnet_
- [ ] `git status` reports nothing to commit, and the answers file names the version the project had. · _sonnet_

**Before the rerun**

- [ ] `ls -ld how-to` read; where `how-to` was a file or a link, it was renamed with the author and the rename committed. · _opus_

**The rerun**

- [ ] The update run again with `uvx --python '>=3.14'`, the five `GIT_CONFIG_*` variables and `-a .copier-answers.syntek-media.yml`, any answer the stopped run changed given again; `--defaults` added only where a session ran it, on the author's word. · _sonnet_

## Done When

- [ ] **Copier printed 'Updating to template version', and the update ended with its report**, read from the version the project had, never the new version on both sides. · _opus_
- [ ] Nothing of the author's was lost: every untracked file of theirs kept, and anything they wanted from an `.agents.from-update` moved out of the project before the discard. · _opus_
- [ ] The work continues at step 6 of `how-to/workflows/syntek-media/04-update-the-template/`. · _sonnet_
