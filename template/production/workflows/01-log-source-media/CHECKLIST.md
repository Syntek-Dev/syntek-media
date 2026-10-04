---
workflow: 01-log-source-media
phase: produce
skills: []
model: opus
---

# CHECKLIST.md — log source media

**Last Updated**: <%DATE%> **Version**: 0.1.0 **Maintained By**: <%OWNER_NAME%>
**Language**: British English (en_GB)

> **See** `production/docs/reference/source-media.md`. No gate in `scripts/docs/reference/the-piece-ladder.md` applies to this procedure.

## Pre-Conditions

- [ ] Read `.claude/CLAUDE.md` and `.claude/MEMORY.md`, then this folder's `CONTEXT.md` and `CLAUDE.md`. · _sonnet_
- [ ] **The files, their kinds and their piece (if known) confirmed with the author.** · _opus_
- [ ] A recording that is itself to become a piece sent to `production/workflows/08-bring-in-a-recording/` instead. · _opus_

## Execution Checklist

**Rights and location**

- [ ] Every licensed or identifiable file has its row in `production/src/rights-register.md`, found or opened as `needed`. · _opus_
- [ ] A location label agreed for each master copy; no link carrying a token. · _opus_

**Logging**

- [ ] `footage add` run for each file, with `--kind`, `--location` and `--rights` where there is a row. · _sonnet_
- [ ] Each file copied, never moved; a refused duplicate reported with its existing ID and not logged again. · _sonnet_
- [ ] `recorded` and `notes` filled in each new row with the author. · _sonnet_

**Verifying**

- [ ] `footage verify` run; any mismatch or unlisted file reported, and the manifest left as it was. · _sonnet_

## Done When

- [ ] **Every file has a footage ID, a checksum and a location label, and `footage verify` passes.** · _opus_
- [ ] No footage was committed or forced past `production/src/.gitignore`. · _sonnet_
- [ ] Handed back: footage IDs, kinds, durations, locations, rights rows opened, the verify result. · _opus_
