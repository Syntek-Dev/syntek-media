---
workflow: 03-record-a-design-export
phase: author
skills: []
model: opus
---

# CHECKLIST.md — record a design export

**Last Updated**: <%DATE%> **Version**: 0.1.0 **Maintained By**: <%OWNER_NAME%>
**Language**: British English (en_GB)

> **See** `brand/docs/reference/design-exports.md`. No gate in `scripts/docs/reference/the-piece-ladder.md` applies to this procedure.

## Pre-Conditions

- [ ] Read `.claude/CLAUDE.md` and `.claude/MEMORY.md`, then this folder's `CONTEXT.md` and `CLAUDE.md`. · _sonnet_
- [ ] **The design, its Claude Design link and its export date given by the author;** none guessed; or, for a revision filed earlier and approved now, its row and its original's read and steps 2 to 6 not repeated. · _opus_
- [ ] The design register read for any export this one replaces. · _sonnet_
- [ ] **For a revision, the author asked whether it replaces the original now or later.** · _opus_

## Execution Checklist

- [ ] Everything licensed in the design named, each with a row in `production/src/rights-register.md`. · _opus_
- [ ] For a revision, the author asked whether each rights row of the original covers it. · _opus_
- [ ] Size measured: 10 MB or less to `brand/src/exports/`, over 10 MB to `brand/src/exports/large/`. · _sonnet_
- [ ] **For a large file, git-lfs installed and its filter configured before the file was added.** · _sonnet_
- [ ] `git lfs track` never run; `filter.lfs.required` never unset. · _sonnet_
- [ ] Named in kebab-case for its design, a revision as `<design>-vN` beside its original; no existing export overwritten, moved or deleted. · _sonnet_
- [ ] Register row complete: design, link, export path, storage, date, rights IDs. · _sonnet_
- [ ] For a revision, its row names the export it revises ('awaiting approval' until approved); the original's row marked superseded with the approval date and the new file's name, keeping its own path, only once the author approved the revision. · _sonnet_
- [ ] **The files to move and to leave shown to the author and agreed before any was changed.** · _opus_
- [ ] **For an approved revision, every agreed reference moved to it:** layouts and cards, project guides, the rights row (extended only where its permission covers the revision), current notes in `.claude/MEMORY.md` superseded by new dated bullets, and the files of every piece before `produced` (asset copies added beside the old ones, real indexes made again, never hand-edited). · _opus_
- [ ] Pieces at `produced` or later, dated records and flags' questions left as they were, each named in the hand-back. · _opus_
- [ ] Every moved piece's cleared sub-check or gate recorded in its brief and named in the hand-back. · _opus_
- [ ] For a large file, `git check-attr filter` reports `lfs`. · _sonnet_
- [ ] `python3 toolkit/media.py check` reports nothing about the file. · _sonnet_
- [ ] `uv run toolkit/card.py check` clean on every layout and card whose reference moved. · _sonnet_
- [ ] A show's cover encoded with `media.py image` to `podcast.cover` and `podcast.id3_cover`, and a partner-branded image to its site's key; never by hand. · _sonnet_
- [ ] Handed back: path, storage, row, anything superseded, references moved and left, rights still needed. · _opus_

- [ ] Sprite pose/mouth/blink names, native mouth origin and scale recorded where applicable. · _opus_

## Done When

- [ ] **The file is where its size requires, stored as Git can bear, and registered with its link.** · _opus_
- [ ] Nothing that a published piece uses was overwritten. · _opus_
- [ ] The original is still in place for reference, and nothing live names it once its revision is approved, unless the hand-back says why. · _opus_
- [ ] The author knows which rights rows must clear before the export is used. · _opus_
