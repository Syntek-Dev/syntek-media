# design-register.md — every design <%BRAND_NAME%> has exported into this repository

**Last Updated**: <%DATE%> **Version**: 0.1.0 **Maintained By**: <%OWNER_NAME%>
**Language**: British English (en_GB)

> **This file is a seeded stub, and it is deliberately unfinished.**
> It ships with the project so that the skills which route here point at something real from day one.
> Until `brand/workflows/03-record-a-design-export/` has recorded an export, the table below has no rows.

The register is the one list of the brand's designs: every design exported into this repository, from whichever app made it.
Each row gives the app the design was made in, where its exported file sits, and how Git stores it.
A design link, where one exists, is kept here and nowhere else in the repository: never in a guide, a procedure, a post or `.claude/MEMORY.md`.

## How to add a design

- Add rows through `brand/workflows/03-record-a-design-export/`, or by hand keeping every column, one exported file per row, oldest first.
- The Made in column names the app and its version, and the label of the project file the design was made in, never its path or a link.
- The Export path column takes the file's path from the repository root, under `brand/src/exports/` or `brand/src/exports/large/`.
- The Storage column takes one of `git · lfs`: `lfs` for every file in `brand/src/exports/large/`, `git` for every other.
- The Exported column takes the date the file was exported, DD/MM/YYYY.
- The Notes column names the rights-register ID of any font, image or music the design uses.
- Never delete a row: a replaced export keeps its row, with 'superseded DD/MM/YYYY' and the new file's name in Notes, and the new file gets a row of its own.
- One sentence per cell.

## Register

| Design | Made in | Export path | Storage | Exported | Notes |
|---|---|---|---|---|---|
