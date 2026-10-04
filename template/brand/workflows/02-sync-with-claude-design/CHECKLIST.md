---
workflow: 02-sync-with-claude-design
phase: author
skills: []
model: opus
---

# CHECKLIST.md — sync with Claude Design

**Last Updated**: <%DATE%> **Version**: 0.1.0 **Maintained By**: <%OWNER_NAME%>
**Language**: British English (en_GB)

> **See** `brand/docs/reference/claude-design.md`. No gate in `scripts/docs/reference/the-piece-ladder.md` applies to this procedure.

## Pre-Conditions

- [ ] Read `.claude/CLAUDE.md` and `.claude/MEMORY.md`, then this folder's `CONTEXT.md` and `CLAUDE.md`. · _sonnet_
- [ ] **The author asked for this sync, and named each component and its direction.** · _opus_
- [ ] The kit committed and clean in `git status`; `media.py tokens` and `card.py check` pass before anything moves. · _sonnet_

## Execution Checklist

**The route**

- [ ] Earlier syncs read in `.claude/MEMORY.md`; the route chosen and explained to the author. · _opus_
- [ ] `/design-sync` started by the author, never by Claude, with the hint naming the kit as a hand-authored HTML kit. · _sonnet_
- [ ] Anything it proposed beyond the named components cancelled by the author; route two used instead. · _opus_
- [ ] Route two only through a scratch folder outside `brand/`, kept out of Git; where each verb writes checked before first use. · _sonnet_

**One component at a time**

- [ ] Each component shown to the author against the kit, and applied only on a yes, under its existing name. · _opus_
- [ ] No card deleted, no required token renamed, no line 1 moved, no value typed in place of a token. · _sonnet_
- [ ] `media.py tokens` and `card.py check` pass after each component. · _sonnet_
- [ ] For either layout, proofs rendered and the author told the change reaches later pieces only. · _opus_

**Record**

- [ ] The project's row in `brand/src/design-register.md`, the first time, with the link the author gave. · _sonnet_
- [ ] What was synced, its direction and route, and what the first `/design-sync` did, dated in `.claude/MEMORY.md`. · _sonnet_
- [ ] Committed with the author's agreement, the message naming the components. · _sonnet_

## Done When

- [ ] **Every named component came across approved, and nothing else in the kit changed.** · _opus_
- [ ] The checks pass on the kit as it now stands. · _sonnet_
- [ ] Handed back: components and directions, route, checks, anything still unsynced on either side. · _opus_
