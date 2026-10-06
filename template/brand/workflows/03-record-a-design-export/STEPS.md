---
workflow: 03-record-a-design-export
phase: author
skills: []
model: opus
---

# STEPS.md — record a design export

**Last Updated**: <%DATE%> **Version**: 0.1.0 **Maintained By**: <%OWNER_NAME%>
**Language**: British English (en_GB)

The short procedure for filing an exported design asset. Each step names the guide it uses. **Run
in order** (the size test and the LFS check come before the file is added, because a whole file
in Git history cannot be taken out by a later commit) and tick `CHECKLIST.md` as you go.

> Read the read-order files first (this folder's `CONTEXT.md` and `CLAUDE.md`). No skill runs
> this procedure: it is record-keeping, done with the author.

## 1. Confirm the export

> **Skill:** none · **Guide:** `brand/docs/reference/design-exports.md`

Ask the author which design the file comes from, its Claude Design link, and the date it was
exported; never guess a link. Ask whether it replaces an earlier export, read the design register
for that export's row, and ask whether the author approves it to replace that export now or will
decide later. If the author is approving a revision filed earlier (its row says 'awaiting
approval'), read its row and the original's, confirm the approval, and go straight to step 7,
then step 8 for the files step 7 changed, and step 10: steps 2 to 6 and 9 ran when it was filed.
_Substantive._

## 2. Check what it carries

> **Skill:** none · **Guide:** `brand/docs/reference/design-exports.md`

Ask what the design uses that someone else owns: a font, a photograph, an illustration, a piece
of music. Each needs a row in `production/src/rights-register.md`, opened `needed` and cleared
through `production/workflows/07-clear-the-rights/` before a piece using the export is
scheduled. Note each rights ID for the register row. For a revision, ask whether each rights
row of the original covers it. _Substantive._

## 3. Measure it, and choose its folder

> **Skill:** none · **Guide:** `brand/docs/reference/design-exports.md`

Measure the file's size. 10 MB or less goes in `brand/src/exports/`, with Storage `git`; over
10 MB goes in `brand/src/exports/large/`, with Storage `lfs`. _Mechanical._

## 4. For a large file, check Git LFS first

> **Skill:** none · **Guide:** `brand/docs/reference/design-exports.md`

Run `git lfs version`, then `git config --get filter.lfs.process` (or `filter.lfs.clean`). If
git-lfs is missing or no filter is configured, stop: the author installs git-lfs and runs
`git lfs install` once on the machine (`brand/workflows/06-check-the-setup/` reports both). If
`git add` later fails with `clean filter 'lfs' failed`, that is the tripwire set when the
project was generated, working as meant; never unset it. Never run `git lfs track`.
_Mechanical._

## 5. Name and place the file

> **Skill:** none · **Guide:** `brand/docs/reference/design-exports.md`

Name it in kebab-case for its design, with a variant suffix where one design has several
(`<design>-<variant>.<ext>`). If a file of that name exists, never overwrite it: a revision is
`<design>-vN.<ext>`, `N` the next unused number from 2, beside the original. A sprite revision
renames its pose, so every frame, mouth and blink name built on `<pose>` takes `<pose>-vN`. The
revised pose is filed whole, its unchanged frames, mouths and blink copied under the new name,
because the scene kit loads each by the pose's name. A revised mouth layer
(`<sprite>-mouth-<shape>`), which names no pose, renames the sprite instead: every file of the
sprite is filed again as `<sprite>-vN-…`, and the scene's `Sprite` names `<sprite>-vN`. Place it
in the folder step 3 chose.

For sprite art, retain `<sprite>-<pose>-mouth-<shape>` whole frames or the pose and mouth-layer
names, and optional `<sprite>-<pose>-blink`. Record native mouth origin and whole-number scale
with each export; see `production/docs/reference/scenes-as-code.md`. _Mechanical._

## 6. Write the register row

> **Skill:** none · **Guide:** `brand/docs/reference/design-exports.md`

Add one row to `brand/src/design-register.md`: the design, its link exactly as the author gave
it, the export path from the repository root, the storage, the date exported (DD/MM/YYYY), and
the rights IDs in Notes. For a revision, its Notes also name the export it revises and, until the
author approves it, 'awaiting approval'; the original's row is marked in step 7, once they do.
_Mechanical._

## 7. Move the references, once the author approves the revision

> **Skill:** none · **Guide:** `brand/docs/reference/design-exports.md`

Only for a revision, and only once the author has approved it to replace the original; until
then, nothing else changes. First mark the original's row 'superseded DD/MM/YYYY by
`<new file>`', dated the approval and keeping its own export path, and replace 'awaiting
approval' in the revision's Notes with 'approved DD/MM/YYYY'. Never delete, move or overwrite the
original: it stays for reference, and for any piece that used it.

List every file that names the original (its file name, and for a sprite its pose or sprite
name), searching only what Git tracks or would track
(`.claude/rules/syntek-media/06-global-rules.md` Section 12). Show the author that list, each file
marked to move or to stay with its reason, and move only what they agree: approving the revision
is not approving edits to files not yet shown (`.claude/rules/syntek-media/03-production-ethics.md`
Section 1). Then move each agreed reference:

- the brand's layouts and preview cards, and project guides;
- the rights row, extended to name the revision only where the author confirmed in step 2 that
  its licence or permission covers it; otherwise a new row, opened `needed`;
- each current-state note in `.claude/MEMORY.md`, superseded by a new dated bullet naming the
  revision, never edited in place (`.claude/rules/syntek-media/08-naming-and-memory.md`
  Section 4);
- the scene files, edit decision lists (an approved one raises its `version`), cards and
  thumbnail layouts of every piece whose `status` is before `produced`. Where such a piece uses a
  copy of the original in `production/src/assets/`, copy the revision there under a new name,
  never over the copy, and move that piece's edit decision list, cards and shot-list Source to
  it; a scene's real index is never edited by hand, but made again with
  `python3 toolkit/media.py real <piece>` and accepted with
  `-o production/src/scenes/<piece>.real.json`.

Moving a piece's art is a material change (`scripts/docs/reference/the-piece-ladder.md`,
'Recording a gate'): a scene piece whose sprite or source art moved has `M4.stills` and every
later date cleared from its brief's `verified`, and its new stills reviewed through
`production/workflows/10-animate-a-scene/`. Leave on the original only these, and say why: a
piece at `produced` or later keeps the file its approved master used unless the author reopens it
(its M4 and every later gate then cleared, and its `status` stepped back); dated records (the
superseded row, history bullets, handoffs, the publish log) never change; and a flag that names
the original keeps its question, only the name in it moving. _Substantive._

## 8. Run the checks

> **Skill:** none · **Guide:** `brand/docs/reference/design-exports.md`

For a large file, run `git check-attr filter -- <path>` and confirm it reports `lfs`. Once the
author has added the file to Git, run `python3 toolkit/media.py check` and confirm it reports
neither a large file outside the LFS folder nor a plain blob inside it. For every layout, preview
card, piece card and thumbnail layout step 7 changed, run `uv run toolkit/card.py check <file>`
and confirm it reports nothing. _Mechanical._

## 9. Encode it for its deliverables, where it is one

> **Skill:** none · **Guide:** `brand/docs/reference/design-exports.md`

Some exports are delivered as they are: a podcast show's cover (it belongs to the show, not to a
piece) and an image a partner site wants in its own branding. Encode each with the toolkit, never
by hand: a show's cover to both of its keys, and a partner image to the key the site uses.

```bash
python3 toolkit/media.py image <export> --deliverable podcast.cover
python3 toolkit/media.py image <export> --deliverable podcast.id3_cover
```

Exit 1 names what failed (a size, a shape, transparency): the export is remade in Claude Design,
never stretched. Give the author the renders' names for the show register or the placement.
_Mechanical._

## 10. Hand back

> **Skill:** none · **Guide:** `brand/docs/reference/design-exports.md`

Report the file's path and storage, its register row, any export it superseded, every reference
moved and every one left with the reason (or that the author has not yet approved the revision),
every sub-check or gate a move cleared, any encode and its render, and any rights row still
`needed`. _Substantive._
