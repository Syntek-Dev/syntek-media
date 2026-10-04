# piece-register.md — every piece <%BRAND_NAME%> has opened, by number

**Last Updated**: <%DATE%> **Version**: 0.1.0 **Maintained By**: <%OWNER_NAME%>
**Language**: British English (en_GB)

> **This file is a seeded stub, and it is deliberately unfinished.**
> It ships with the project so that the procedures which route here point at something real from day one.
> Until the first piece is briefed with `scripts/workflows/01-brief-a-piece/`, the table below has no rows.

The one place a piece number is assigned: one row per piece, in number order, kept for life.
Each piece's plan and status live in its brief at `scripts/src/pieces/<piece>/brief.md`, never here.
Number 000 belongs to the worked example, which is never entered in this register.

## Writing rules

1. **One row per piece, in number order.**
   The number is the next free one, written with three digits, and it is frozen once assigned.
2. **Never reuse a number or delete a row.**
   A retired piece keeps its row, with its date in the Retired column and the reason in Notes, so an old file name still leads somewhere.
3. **No status column.**
   Status lives in the brief's `status` and `verified`; a copy here would drift.
4. **The Piece column is the folder name.**
   It reads `NNN-kebab-title`, exactly as the folder in `scripts/src/pieces/` and every file the piece makes in the production and publishing layers.
5. **The Kind column takes one of `short-video · long-video · podcast · audiobook · trailer · voiceover`.**
   It matches the brief's `kind`.
6. **The Origin column takes `scripted` or `recorded`.**
   A recorded piece is a talk, interview or conversation that already exists as a recording.
7. **The Parent column names the piece this one was cut or adapted from, or stays empty.**
   A cut-down is not a piece of its own: it lives only in its parent's cut-down plan in `publishing/src/cut-downs/`.
8. **Dates DD/MM/YYYY, and one sentence per line**, applied when a row is edited.

## Register

| No. | Piece | Kind | Origin | Parent | Opened | Retired | Notes |
|---|---|---|---|---|---|---|---|
