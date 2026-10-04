---
workflow: 04-brief-a-thumbnail
phase: publish
skills: [thumbnail-brief]
model: opus
---

# CHECKLIST.md — brief, lay out and render a thumbnail

**Last Updated**: <%DATE%> **Version**: 0.1.0 **Maintained By**: <%OWNER_NAME%>
**Language**: British English (en_GB)

> **See** `publishing/docs/reference/thumbnails.md` and the `thumbnail-brief` skill. This
> procedure serves part of M7 (captioned → scheduled) of
> `scripts/docs/reference/the-piece-ladder.md`: approved thumbnails are among what that gate
> checks. The gate is cited by number and the move it guards, and this list never restates it.

## Pre-Conditions

- [ ] Read `.claude/CLAUDE.md` and `.claude/MEMORY.md`, then this folder's `CONTEXT.md` and `CLAUDE.md`. · _sonnet_
- [ ] Read `thumbnails.md`, the `thumbnail-brief` skill and its mode file. · _opus_
- [ ] The brief's deliverables and the cut-down plan's notes read; any existing thumbnail brief found. · _sonnet_

## Execution Checklist

**The brief**

- [ ] Every deliverable that takes a thumbnail or cover identified from its tables, and every image a placement needs (poster, share, featured, preview image, GIF); unconfirmed sizes flagged `VERIFY`. · _opus_
- [ ] **The promise agreed with the author in one sentence** before any layout was touched. · _opus_
- [ ] Words on the image as few as carry the promise, and never the title repeated. · _opus_

**The layout**

- [ ] The brand's thumbnail component copied (or the toolkit's where the brand has none), its stylesheet path fixed and the brand's own layout flag deleted from the copy; the brand's file untouched. · _sonnet_
- [ ] For a newsletter key, the copy carries the play-button hook; where the brand's layout lacked it, added to the copy and the author told. · _sonnet_
- [ ] Images by relative path from tracked files; a frame kept as a committed still, never a render. · _sonnet_
- [ ] `uv run toolkit/card.py check` passes. · _sonnet_

**Rendering and checking**

- [ ] Every deliverable rendered with `card.py render` to `publishing/src/renders/`; any exit 2 reported with its install command. · _sonnet_
- [ ] Every other format and every poster made with `media.py image`, never ffmpeg by hand; the GIF made with its `--transparent` overlay and `media.py cut --overlay`. · _sonnet_
- [ ] **Each poster's `--at`, and the GIF's In, Out and first frame, recorded under `## Image`.** · _sonnet_
- [ ] **Every PNG read at a fingertip's width.** · _opus_
- [ ] Words clear of the platform's controls; inside `platform.instagram.grid_aspect` where Instagram shows it; the table's `notes` met. · _opus_
- [ ] Every face, stock image or font that needs one has a `cleared` rights row. · _opus_
- [ ] Results recorded under `## Checks`. · _sonnet_
- [ ] The author approved every image, the GIF seen playing; `approved` dated; declined variants recorded. · _opus_
- [ ] Handed back: renders, `VERIFY` sizes, open rights rows, and what M7 still needs. · _opus_

## Done When

- [ ] **Every deliverable that takes a thumbnail has an approved PNG, read at the size it is seen.** · _opus_
- [ ] Each thumbnail promises only what its deliverable delivers. · _opus_
- [ ] No unconfirmed size is presented as confirmed. · _sonnet_
