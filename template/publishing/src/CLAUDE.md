@./CONTEXT.md

# CLAUDE.md — publishing/src/

Read order: `.claude/CLAUDE.md` → `.claude/MEMORY.md` → `publishing/CONTEXT.md` →
`publishing/CLAUDE.md` → this folder's `CONTEXT.md` (imported above) → this file → the target
folder's `CONTEXT.md` and `CLAUDE.md`, where it is a folder.

## Purpose (one line)

Keep every piece's publishing record (plans, captions, thumbnails, packages, the schedule and the
log) current, consistent with each other and true to what the author did.

## How to work here

- **Routing:** each file or folder has one writer and one procedure.

| File or folder | Written by | Procedure |
|---|---|---|
| `cut-downs/` | `repurpose`, with the author | `publishing/workflows/01-plan-the-cut-downs/` |
| `renders/` (deliverables) | `cut-for-platform` | `publishing/workflows/02-cut-for-a-platform/` |
| `captions/` | `captions` | `publishing/workflows/03-caption-a-piece/` |
| `thumbnails/` | `thumbnail-brief`, with the author | `publishing/workflows/04-brief-a-thumbnail/` |
| `posts/`, `schedule.md` | `prepare-post`, with the author | `publishing/workflows/05-prepare-a-post/` |
| `schedule.md`, `publish-log.md` (after a post) | `prepare-post`, from the author's report | `publishing/workflows/06-record-a-publication/` |

- **Model:** **Opus** for any plan, caption, brief, package or judgement; the mechanical tier for
  renders, a row the author has dictated, renames and ticks
  (`.claude/rules/syntek-media/05-model-allocation.md`).
- **Concrete steps:** read the governing guide (`publishing/docs/reference/CONTEXT.md`); run the
  procedure in the table; after any change, check that the brief, the plan, the package, the
  schedule and the log still agree with each other.
- **Definition of done:** no two files here contradict each other or the piece's brief, and the
  schedule and log match what the author reported.

## Guardrails

- **One sentence per line** in every artefact here, applied when a paragraph is edited, never by
  mass reflow (`.claude/rules/syntek-media/06-global-rules.md`).
- **Report contradictions; never silently repair them.** When a package and the schedule, or the
  schedule and the log, disagree, tell the author which is which; they decide which is wrong.
- **IDs are permanent.** A cut keeps its `cNN` for life; a dropped cut keeps its row.
- **No invented entries.** A row records something the author agreed or reported. Never fill a
  seed with plausible examples, and never write a log row, a URL or a disclosure the author did
  not report.
- **Renders are generated.** Never hand-edit, commit or force-add anything in `renders/`.
- **Never overwrite** a plan, a caption file, a layout, a package or a row without confirming
  with the author; correct the log by a dated note, never by editing history.

## Output & naming

- **Hand-written (with the author):** plans, briefs, layouts and packages, named `<piece>` and,
  for one cut, `<piece>--cNN`.
- **Written by skills:** captions; schedule and log rows.
- **Generated (never hand-edit):** everything in `renders/`, named
  `<piece>[--cNN].<platform>-<format>[.burned].<ext>` for a deliverable and
  `<html-stem>.<platform>-<format>.png` for a thumbnail.
- **Template-owned:** this pair, `.gitignore` and `renders/README.md`.
- Files kebab-case; dates DD/MM/YYYY in prose and DD-MM-YYYY in filenames.
