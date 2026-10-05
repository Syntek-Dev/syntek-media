---
workflow: 01-set-up-the-brand-kit
phase: author
skills: []
model: opus
---

# CHECKLIST.md — set up the brand kit

**Last Updated**: <%DATE%> **Version**: 0.1.0 **Maintained By**: <%OWNER_NAME%>
**Language**: British English (en_GB)

> **See** `brand/docs/reference/the-brand-kit.md`. No gate in `scripts/docs/reference/the-piece-ladder.md` applies to this procedure.

## Pre-Conditions

- [ ] Read `.claude/CLAUDE.md` and `.claude/MEMORY.md`, then this folder's `CONTEXT.md` and `CLAUDE.md`. · _sonnet_
- [ ] **The author asked to set up or change the kit, and said what is changing.** · _opus_
- [ ] The current `tokens.css` and the seven preview cards read; nothing assumed from memory. · _sonnet_

## Execution Checklist

**The written brand**

- [ ] Grilling pass run with the grill-with-docs skill (syntek-author), where present, or the same questions in rounds, each with a recommended answer. · _opus_
- [ ] syntek-author's brand guide and voice notes read, where present; every difference reported with both values and decided by the author. · _opus_

**The tokens**

- [ ] Six colours chosen by the author as `#RRGGBB`; text, surface and accent pairs checked at 4.5:1 or more. · _opus_
- [ ] Display and body faces and weights chosen; each font's licence read and recorded in a `font` row of the rights register. · _opus_
- [ ] Each font file in the fonts folder, named `<family>-<weight>.<ext>`, loaded by a font-face rule with a relative source. · _sonnet_
- [ ] Space unit and radius set in relative units. · _sonnet_
- [ ] Caption face, weight, size and outline width (in `vh`) and colours (`#RRGGBB`) chosen; the caption face is in the fonts folder or installed. · _opus_
- [ ] `python3 toolkit/media.py tokens` exits 0. · _sonnet_

**The layouts**

- [ ] `thumbnail.html` and `card.html` adapted with the author, using tokens only, line 1 unchanged. · _opus_
- [ ] Layout contract kept: one file for every aspect ratio, text inside the safe-zone variables, nothing over the network, the card's background transparent. · _sonnet_
- [ ] `uv run toolkit/card.py check` exits 0 on all seven cards. · _sonnet_
- [ ] Landscape and vertical proofs of each layout, and a vertical proof of the captions card, rendered with `-o` into `production/src/renders/proofs/brand-kit-DD-MM-YYYY/` and approved by the author. · _opus_

**Record**

- [ ] Each decision dated in `.claude/MEMORY.md`, under the heading syntek-author's 00-project.md maps it to, where present. · _sonnet_
- [ ] `python3 toolkit/media.py flags` shows no `AUTHOR TO CONFIRM` in `tokens.css` or the two layouts. · _sonnet_
- [ ] The kit committed, with the author's agreement, before any sync. · _sonnet_

## Done When

- [ ] **Every required token is the author's decision, and both layouts are approved in proof.** · _opus_
- [ ] Every font in the kit has its licence row. · _sonnet_
- [ ] No piece's copied thumbnail or card was changed. · _sonnet_
- [ ] Handed back: values, fonts, proofs, differences from the written brand, flags left. · _opus_
