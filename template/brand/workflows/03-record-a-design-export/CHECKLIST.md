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
- [ ] **The design, its Claude Design link and its export date given by the author;** none guessed. · _opus_
- [ ] The design register read for any export this one replaces. · _sonnet_

## Execution Checklist

- [ ] Everything licensed in the design named, each with a row in `production/src/rights-register.md`. · _opus_
- [ ] Size measured: 10 MB or less to `brand/src/exports/`, over 10 MB to `brand/src/exports/large/`. · _sonnet_
- [ ] **For a large file, git-lfs installed and its filter configured before the file was added.** · _sonnet_
- [ ] `git lfs track` never run; `filter.lfs.required` never unset. · _sonnet_
- [ ] Named in kebab-case for its design; no existing export overwritten. · _sonnet_
- [ ] Register row complete: design, link, export path, storage, date, rights IDs. · _sonnet_
- [ ] Any replaced export's row marked superseded with the date and the new file's name. · _sonnet_
- [ ] For a large file, `git check-attr filter` reports `lfs`. · _sonnet_
- [ ] `python3 toolkit/media.py check` reports nothing about the file. · _sonnet_
- [ ] Handed back: path, storage, row, anything superseded, rights still needed. · _opus_

## Done When

- [ ] **The file is where its size requires, stored as Git can bear, and registered with its link.** · _opus_
- [ ] Nothing that a published piece uses was overwritten. · _opus_
- [ ] The author knows which rights rows must clear before the export is used. · _opus_
