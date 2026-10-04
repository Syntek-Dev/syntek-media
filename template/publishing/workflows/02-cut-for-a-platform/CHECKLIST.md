---
workflow: 02-cut-for-a-platform
phase: convert
skills: [cut-for-platform]
model: opus
---

# CHECKLIST.md — cut and encode a piece for its platforms

**Last Updated**: <%DATE%> **Version**: 0.1.0 **Maintained By**: <%OWNER_NAME%>
**Language**: British English (en_GB)

> **See** `publishing/docs/reference/cut-downs.md`, `publishing/docs/reference/platform-specs.md`
> and the `cut-for-platform` skill. This procedure serves M5 (produced → cut), and
> M6 (cut → captioned) where captions are burned in the same pass, of
> `scripts/docs/reference/the-piece-ladder.md`; gates are cited by number and the move they
> guard, and this list never restates them.

## Pre-Conditions

- [ ] Read `.claude/CLAUDE.md` and `.claude/MEMORY.md`, then this folder's `CONTEXT.md` and `CLAUDE.md`. · _sonnet_
- [ ] Read `cut-downs.md`, `platform-specs.md` and the `cut-for-platform` skill. · _opus_
- [ ] **The brief's `verified` dates M4, and the master is in `production/src/renders/`.** · _sonnet_
- [ ] Where the piece has cuts, its plan is `approved`. · _sonnet_

## Execution Checklist

**Before rendering**

- [ ] Every deliverable listed: each full-length key of the brief and each key of each `approved` cut. · _sonnet_
- [ ] Every preset read with `media.py presets`; overrides, `verify` keys and the platform guide's traps noted. · _sonnet_
- [ ] **Burned or sidecar decided per deliverable;** only caption files that pass `captions check --script` passed to the cut. · _opus_

**Rendering**

- [ ] Full-length deliverables encoded with `media.py encode` (or `still-video` for an audio piece on a video platform). · _sonnet_
- [ ] Each approved cut cut in one pass with `media.py cut`, In, Out and Frame from the plan. · _sonnet_
- [ ] **Every output exited 0;** each exit 1 diagnosed and fixed at its source, each exit 2 named with what it blocks. · _opus_
- [ ] Every output probed with `media.py probe`; nothing hand-edited, nothing stream-copied. · _sonnet_

**The author and the gate**

- [ ] The author has seen or heard every render; burned captions checked by eye. · _opus_
- [ ] Each cut's Status moved to `rendered`, then `checked` on the author's word. · _sonnet_
- [ ] The brief's `status` and `verified` set: M5, and M6 where every needed caption was burned and checked in this pass. · _sonnet_
- [ ] Handed back: the renders, their probes, every `verify` key relied on, and the next procedure. · _opus_

## Done When

- [ ] **Every deliverable of the brief and of the plan is rendered, verified and seen by the author.** · _opus_
- [ ] M5 is dated in the brief, or waived there with the author's reason. · _sonnet_
- [ ] No render was committed or forced past `publishing/src/.gitignore`. · _sonnet_
