@./CONTEXT.md

# CLAUDE.md — publishing/workflows/06-record-a-publication/

Read order: `.claude/CLAUDE.md` → `.claude/MEMORY.md` → `publishing/CONTEXT.md` →
`publishing/CLAUDE.md` → `publishing/workflows/CONTEXT.md` → `publishing/workflows/CLAUDE.md` →
this folder's `CONTEXT.md` (imported above) → this file → `STEPS.md` (with `CHECKLIST.md` open) →
**the schedule**.

## Purpose (one line)

Keep the schedule and the publish log true to what the author actually did, and close a piece as
published only when all of it is out.

## How to work here

**Follow `STEPS.md` in order and tick `CHECKLIST.md` as you go.** The model tags in the checklist
are authoritative: `opus` items are judgement; `sonnet` items belong to the mechanical tier.

- **Routing:** skill `prepare-post`, which writes the log row only from the author's report.
  Guide: `publishing/docs/reference/posting-and-the-log.md`.
- **Model:** the mechanical tier for moving a row and writing a reported row; **Opus** for
  anything needing judgement: what the author's report means, and whether what was set matches
  the package (`.claude/rules/syntek-media/05-model-allocation.md`).
- **Concrete steps:** read the row and the package → establish what the author did → move the
  schedule row on → write the log row → compare what was set with the package → append any
  correction → close the piece when all of it is out → hand back.
- **Definition of done:** the schedule and the log say what happened; every `posted` row has its
  log row; the piece is `published` only when every row is `posted` or `dropped`; nothing was
  overwritten.

## Guardrails

- **Log what happened, not what was planned.** Only the author's report moves a row to `posted`,
  dated to when the author posted it.
- **The URL is the author's.** Never guess one, build one from a handle, or copy one from another
  row.
- **Record what was set, exactly.** If the label or the description line differs from the package,
  say so at once; never record the plan as the fact.
- **Never overwrite history.** A schedule row is never deleted; a log row is corrected by a dated
  note under `## Corrections`.
- **Published is earned.** A piece with any row still `planned`, `ready` or `moved` is still
  `scheduled`.

## Output & naming

- **Produces:** updated rows in `publishing/src/schedule.md`; new rows in
  `publishing/src/publish-log.md`.
- **Also writes:** the brief's `status`, once the piece is published; for a feed episode, its
  show register row's `status` and the show's tracked feed, through `media.py feed write -o`.
- **Does not produce:** a post, an upload, or any change to a package or a render.
