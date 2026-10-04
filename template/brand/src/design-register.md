# design-register.md — every design <%BRAND_NAME%> has made in Claude Design

**Last Updated**: <%DATE%> **Version**: 0.1.0 **Maintained By**: <%OWNER_NAME%>
**Language**: British English (en_GB)

> **This file is a seeded stub, and it is deliberately unfinished.**
> It ships with the project so that the skills which route here point at something real from day one.
> Until `brand/workflows/03-record-a-design-export/` has recorded an export, the table below has no rows.

The register is the one list of the brand's designs: its design-system project in Claude Design, and every design exported from Claude Design into this repository.
Each row gives the design's Claude Design link, where its exported file sits, and how Git stores it.
Claude Design links are kept here and nowhere else in the repository: never in a guide, a procedure, a post or `.claude/MEMORY.md`.

## How to add a design

- Add rows through `brand/workflows/03-record-a-design-export/`, or by hand keeping every column, one exported file per row, oldest first.
- The brand's design-system project has a row of its own, written the first time `brand/workflows/02-sync-with-claude-design/` runs, with a dash for its Export path, Storage and Exported.
- The Claude Design link column holds the link exactly as Claude Design gives it.
- The Export path column takes the file's path from the repository root, under `brand/src/exports/` or `brand/src/exports/large/`.
- The Storage column takes one of `git · lfs`: `lfs` for every file in `brand/src/exports/large/`, `git` for every other.
- The Exported column takes the date the file was exported, DD/MM/YYYY.
- The Notes column names the rights-register ID of any font, image or music the design uses.
- Never delete a row: a replaced export keeps its row, with 'superseded DD/MM/YYYY' and the new file's name in Notes, and the new file gets a row of its own.
- One sentence per cell.

## Register

| Design | Claude Design link | Export path | Storage | Exported | Notes |
|---|---|---|---|---|---|
