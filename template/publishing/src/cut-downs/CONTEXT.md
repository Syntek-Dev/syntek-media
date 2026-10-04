# CONTEXT.md — publishing/src/cut-downs/

One cut-down plan per piece: the short deliverables its master is cut into, each with the lines
it carries, its In and Out on the master, its frame and its hook. A plan is agreed with the author
before anything is cut, and every procedure that renders, captions, thumbnails or posts a cut
reads it. The cuts themselves are renders, in `publishing/src/renders/`; the master they are cut
from is in `production/src/renders/`; the full-length deliverables are listed in the brief.

## Directory Tree

```text
publishing/src/cut-downs/
├── CONTEXT.md        ← this file
├── CLAUDE.md         ← operating rules, and the plan's skeleton
└── <piece>.md        ← one cut-down plan per piece, named for the piece's folder
```

## What's here

- `<piece>.md` — a plan, written by `repurpose` with the author. **The shape is fixed by
  `publishing/docs/reference/cut-downs.md`**: frontmatter `piece`, `master`, `approved`; the table
  `Cut · Deliverables · Lines · In · Out · Frame · Hook · Status`; then one `## cNN — <hook>`
  section per cut. The skeleton is fenced in this folder's `CLAUDE.md`.
- **The cut-downs of a piece live only here,** never in its brief, which lists only full-length
  deliverables. A silent loop for a web page is a cut too, its Lines `—`; a GIF preview is not:
  it is the thumbnail brief's, in `publishing/src/thumbnails/`.
- A generated project may hold one worked example plan, where it was kept; delete it, with the
  other example files, once you no longer need it, and none of them will come back.

## Cross-references

- `publishing/docs/reference/cut-downs.md` — moments, framing, safe zones and near-identical
  batches.
- `publishing/workflows/01-plan-the-cut-downs/` — the procedure that writes a plan.
- `publishing/workflows/02-cut-for-a-platform/` — the procedure that renders it.
- `scripts/src/pieces/` — the brief and the script or transcript whose lines a plan cites.
