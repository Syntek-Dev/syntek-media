---
workflow: 02-write-a-script
phase: produce
skills: [write-script]
model: opus
---

# CHECKLIST.md — write a script, from agreed brief to approved script

**Last Updated**: <%DATE%> **Version**: 0.1.0 **Maintained By**: <%OWNER_NAME%>
**Language**: British English (en_GB)

> **See** `scripts/docs/reference/writing-for-the-ear.md` and the `write-script` skill with its
> mode file. This procedure passes gate M2 (briefed → scripted) for a scripted piece. Gates are
> cited from `scripts/docs/reference/the-piece-ladder.md` by number and the move they guard, and
> never restated here.

## Pre-Conditions

- [ ] Read `.claude/CLAUDE.md` and `.claude/MEMORY.md`, then this folder's `CONTEXT.md` and `CLAUDE.md`. · _sonnet_
- [ ] Read the `write-script` skill and its mode file. · _sonnet_
- [ ] **The brief is at `briefed` with M1 dated, and the piece is scripted, not recorded or an audiobook.** · _opus_

## Execution Checklist

**Before writing**

- [ ] Checked for an existing script; if one exists, the author confirmed a revision, and was told if it clears M2. · _sonnet_
- [ ] Brief, voice file, guides and any parent or source read; the written work was not edited. · _opus_
- [ ] Every factual claim listed and checked with the fact-check skill (syntek-author), where present, or against a named source; nothing invented. · _opus_

**The script**

- [ ] Written in the guide's format: frontmatter, H1, beats with target times, one spoken sentence per line, every line tagged. · _sonnet_
- [ ] The hook is the first line; the call to action is the last beat; every key point of the brief is carried. · _opus_
- [ ] No IPA in the script; directions in braces; cues never written as speech. · _sonnet_
- [ ] Timed with `script time --write`: within 10% of `target_seconds` and inside every deliverable's `max_seconds`. · _sonnet_
- [ ] A long script was cut or reshaped with the author, not fitted by raising the rate. · _opus_

**Reports and revision**

- [ ] Companion reports run where present, each missing companion named; every finding decided by the author. · _opus_
- [ ] Revisions applied only from the author's notes and accepted findings; no ledger entry made; `version` raised and the script re-timed. · _opus_

**Approval**

- [ ] `media.py flags` on the piece's folder lists nothing in the script. · _sonnet_
- [ ] On the author's approval, `approved:` dated and M2 (briefed → scripted) recorded: `status: scripted` and `M2` dated in `verified`. · _sonnet_
- [ ] For a piece with `picture: false`, `M3` recorded `n/a — no picture` with M2, and the author told why. · _sonnet_

## Done When

- [ ] **The author has approved the script, it fits its target and every deliverable, and it carries zero flags.** · _opus_
- [ ] Nothing was generated and no credit was spent. · _sonnet_
- [ ] The hand-back names the next procedure by its full folder name and offers to start it. · _opus_
