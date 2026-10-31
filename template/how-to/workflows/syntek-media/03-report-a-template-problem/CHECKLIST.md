---
workflow: 03-report-a-template-problem
phase: review
skills: []
model: opus
---

# CHECKLIST.md — report a template problem

**Last Updated**: <%DATE%> **Version**: 0.1.0 **Maintained By**: <%OWNER_NAME%>
**Language**: British English (en_GB)

> **See** `how-to/docs/syntek-media/reporting-a-template-problem.md`. No gate in `scripts/docs/reference/the-piece-ladder.md` applies to this procedure.

## Pre-Conditions

- [ ] Read `.claude/CLAUDE.md` and `.claude/MEMORY.md`, then this folder's `CONTEXT.md` and `CLAUDE.md`. · _sonnet_
- [ ] The author has described the fault, and is at hand to read what is collected. · _opus_
- [ ] Any stopped update already taken through `how-to/workflows/syntek-media/05-recover-a-stopped-update/`. · _sonnet_

## Execution Checklist

**Whose fault**

- [ ] The fault reproduced, without spending a credit or running a stopped update again. · _sonnet_
- [ ] **The project's own edits ruled out: for a file, its history read and the fault found in a fresh render of the recorded version.** · _opus_
- [ ] No copy run over the real project; the temporary folder removed by the author afterwards. · _sonnet_

**What is collected**

- [ ] `_commit` and `_src_path` read from `.copier-answers.syntek-media.yml`, and syntek-author's `_commit` where present. · _sonnet_
- [ ] The exact command and its whole output, the error included. · _sonnet_
- [ ] `python3 toolkit/media.py check --setup` and the Copier, Python, git and system versions collected. · _sonnet_

**Before anything is shown**

- [ ] **Every key, voice ID, account ID, Claude Design link, real person's detail and private message taken out.** · _opus_
- [ ] Home paths written as `~`, and a local `_src_path` described, not quoted. · _opus_
- [ ] **A security problem sent only to the source's private vulnerability reporting, never a public issue.** · _opus_

**The draft**

- [ ] Title, what happened, what was expected, steps to reproduce, full output and versions all present. · _opus_
- [ ] The draft given to the author in the session, never saved in the project. · _sonnet_

## Done When

- [ ] **The author files the issue at the source `_src_path` names; no session filed it, and no web address was written.** · _opus_
- [ ] Nothing in the project changed, and nothing under `how-to/` was edited. · _sonnet_
