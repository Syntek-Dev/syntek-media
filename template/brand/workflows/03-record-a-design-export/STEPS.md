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
exported; never guess a link. Ask whether it replaces an earlier export, and read the design
register for that export's row. _Substantive._

## 2. Check what it carries

> **Skill:** none · **Guide:** `brand/docs/reference/design-exports.md`

Ask what the design uses that someone else owns: a font, a photograph, an illustration, a piece
of music. Each needs a row in `production/src/rights-register.md`, opened `needed` and cleared
through `production/workflows/07-clear-the-rights/` before a piece using the export is
scheduled. Note each rights ID for the register row. _Substantive._

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
(`<design>-<variant>.<ext>`). If a file of that name exists, never overwrite it: a revision takes
a new name, agreed with the author. Place it in the folder step 3 chose.

For sprite art, retain `<sprite>-<pose>-mouth-<shape>` whole frames or the pose and mouth-layer
names, and optional `<sprite>-<pose>-blink`. Record native mouth origin and whole-number scale
with each export; see `production/docs/reference/scenes-as-code.md`. _Mechanical._

## 6. Write the register row

> **Skill:** none · **Guide:** `brand/docs/reference/design-exports.md`

Add one row to `brand/src/design-register.md`: the design, its link exactly as the author gave
it, the export path from the repository root, the storage, the date exported (DD/MM/YYYY), and
the rights IDs in Notes. Where it replaces an export, mark the old row 'superseded DD/MM/YYYY'
with the new file's name. _Mechanical._

## 7. Run the checks

> **Skill:** none · **Guide:** `brand/docs/reference/design-exports.md`

For a large file, run `git check-attr filter -- <path>` and confirm it reports `lfs`. Once the
author has added the file to Git, run `python3 toolkit/media.py check` and confirm it reports
neither a large file outside the LFS folder nor a plain blob inside it. _Mechanical._

## 8. Encode it for its deliverables, where it is one

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

## 9. Hand back

> **Skill:** none · **Guide:** `brand/docs/reference/design-exports.md`

Report the file's path and storage, its register row, any export it superseded, any encode and
its render, and any rights row still `needed`. _Substantive._
