---
workflow: 03-storyboard-a-piece
phase: plan
skills: [storyboard]
model: opus
---

# STEPS.md — storyboard a piece, from approved script to approved boards

**Last Updated**: <%DATE%> **Version**: 0.1.0 **Maintained By**: <%OWNER_NAME%>
**Language**: British English (en_GB)

The ordered procedure for giving every spoken line of an approved script a picture, and every
picture a source. Each step names the skill and guide it uses. **Run in order** — the ordering
is load-bearing — and tick `CHECKLIST.md` as you go.

> Read the read-order files first (this folder's `CONTEXT.md` and `CLAUDE.md`). The `storyboard`
> skill is this procedure in skill form; read it and its mode file before step 1.

## 1. Confirm the piece is ready for boards

> **Skill:** `storyboard` · **Guide:** `scripts/docs/reference/the-piece-ladder.md`

Read the piece's brief in `scripts/src/pieces/<piece>/`. It is at `scripted` with M2 dated, its
script is `approved`, `picture: true` and `origin: scripted`. A piece with no picture, or a
recorded one, is never boarded: where its brief does not already say so, record
`M3: 'n/a — no picture'` or `M3: 'n/a — recorded'` in `verified`, then name the procedure that
comes next and stop. _Mechanical._

## 2. Confirm you will not clobber a storyboard

> **Skill:** none · **Guide:** `scripts/docs/reference/storyboards-and-shot-lists.md`

Look for `storyboard.md` and `shot-list.md` in the piece's folder. If they exist, this run
revises them: read both in full, note the `version` and whether the storyboard is `approved`, and
confirm with the author before changing anything. Board and shot IDs already used are kept;
replacing a shot after M3 clears M3 and every later gate, so say so first. _Mechanical._

## 3. Read the script, the brief and the guides

> **Skill:** `storyboard` · **Guide:** `scripts/docs/reference/storyboards-and-shot-lists.md`

Read the approved script and the brief in full; this procedure's guide and the guide for the
piece's kind, where the project makes that kind (listed in `scripts/docs/reference/CONTEXT.md`);
each deliverable's aspect and safe zone (`python3 toolkit/media.py presets <key>`); the brand's
components in `brand/src/design-system/`; and what already exists in
`production/src/footage/manifest.toml`, `production/src/assets/` and
`production/src/rights-register.md`. _Substantive._

## 4. Board every spoken line

> **Skill:** `storyboard` · **Guide:** `scripts/docs/reference/storyboards-and-shot-lists.md`

Write `storyboard.md`: frontmatter `piece`, `version`, an empty `approved:`, then one row per
board, `B01` onwards, with its beat, its time, the picture in one sentence, the script lines it
covers as `beat.line`, the words of its `TEXT:` cues and the sounds under it. Every spoken line
sits in exactly one board's range. A still or a card that should push in, or a board that should
fade in, says so in its Picture cell. _Substantive._

## 5. Frame every vertical deliverable

> **Skill:** `storyboard` · **Guide:** `scripts/docs/reference/storyboards-and-shot-lists.md`

For every vertical deliverable in the brief, fill each board's Vertical framing: `centre`,
`crop x=<px>` or `pad`. Keep faces and on-screen words inside the deliverable's safe zone; a value
the preset lists as `verify` is unconfirmed, so check it by eye and say so. _Substantive._

## 6. Give every shot a source

> **Skill:** `storyboard` · **Guide:** `scripts/docs/reference/storyboards-and-shot-lists.md`

Write `shot-list.md`: one row per shot, `S01` onwards, naming its board, its type, its source (a
footage ID, an asset under `production/src/assets/`, a card under `production/src/cards/`, a
colour `#RRGGBB`, or `to shoot`), its framing, its seconds and its status. A shot typed
`generated` must agree with the brief's `ai_visuals`; where it does not, stop and settle the
brief's disclosure plan with the author first. _Substantive._

## 7. Open the rights rows

> **Skill:** `storyboard` · **Guide:** `production/docs/reference/rights-and-consent.md`

For every licensed or identifiable thing a shot shows or plays, add a `needed` row to
`production/src/rights-register.md` with the next `RR` ID, or reuse the row the item already
has; write the ID in the shot's Rights column and in the brief's `rights:` list. A voice or a
likeness is used only with the person's recorded consent
(`.claude/rules/syntek-media/03-production-ethics.md` Section 6). _Mechanical (writing rows);
deciding what needs one is substantive._

## 8. Read it back and record M3

> **Skill:** `storyboard` · **Guide:** `scripts/docs/reference/the-piece-ladder.md`

Walk the author through the boards in order against the script, then the shot list. Apply their
corrections. Check M3 (scripted → storyboarded) against the ladder guide, item by item. When the
author approves, date `approved:` in the storyboard, set the brief's `status: storyboarded`,
record `M3` with today's date in `verified`, and update `last_updated`. _Mechanical (writing);
the read-back is substantive._

## 9. Hand on

> **Skill:** none · **Guide:** `scripts/docs/reference/the-piece-ladder.md`

Tell the author what is boarded, what is still `to shoot`, and which rights rows are `needed`.
Name the next procedures by their full folder names: `production/workflows/01-log-source-media/`
for footage, `production/workflows/02-make-a-voiceover/` for the voice,
`production/workflows/07-clear-the-rights/` for the rows just opened, and then
`production/workflows/03-assemble-the-master/` for M4. Offer to start the one that brings the
master nearest. _Substantive._
