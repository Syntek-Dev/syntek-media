# CONTEXT.md — how-to/workflows/syntek-media/04-update-the-template/

The procedure for taking syntek-media's latest changes into this project: from a clean,
committed tree on a branch, through the update and its report, to a commit. Over syntek-author
it updates syntek-author first. It checks for the three things an update must handle with care
(a held .agents link, an .agents link outside the project, and `how-to` that is not a
folder), settles any changed answer with the author, runs the update on Python 3.14 or later
with Git's housekeeping off, and reads the migration output and the update report with the
author before anything is committed.

## Directory Tree

```text
how-to/workflows/syntek-media/04-update-the-template/
├── CONTEXT.md          ← this file (when to use, what it produces)
├── CLAUDE.md           ← operating rules for this procedure
├── STEPS.md            ← ordered steps to execute, with every command
└── CHECKLIST.md        ← verification checklist before marking complete
```

## When to use this

- A newer release of syntek-media is out, and the author wants its improvements.
- An answer must change: a platform or a media kind added or removed, a coding agent recorded,
  the place binary files are kept.
- The template asked for an update, such as a message after a copy or a migration's report.

Reach for a **different** procedure when: an update has already stopped part way with an error
(`how-to/workflows/syntek-media/05-recover-a-stopped-update/`); an answer is the whole point of
the update (`how-to/workflows/syntek-media/02-change-the-answers/`, which runs this one's steps);
a client's files must be added after it is recorded
(`how-to/workflows/syntek-media/06-enable-a-coding-agent-client/`); or the job is
syntek-author's update, which follows syntek-author's own procedure, in its own folder under
`how-to/workflows/`, where it is present.

## What it produces, and where

- syntek-media's newer version merged into the project, and
  `.copier-answers.syntek-media.yml` moved forward, committed together on the branch
  `update-syntek-media`.
- The user guide under `how-to/` put back to the template's text, the shared files the author
  never changed refreshed, and new settings entries and MCP servers offered once each, as the
  report lists.
- Two records inside `.git`, refs/syntek-media/template and refs/syntek-media/yours, that keep
  the template's render and the project as it was before the update, for the report's compare
  and take commands.

## The failure this procedure exists to prevent

An update run over uncommitted work, or committed half-finished. Copier may write over an
untracked file at one of the template's paths; a stopped update that is committed takes the new
version as already reached and skips the migrations that version needed; and a report nobody
reads leaves conflicts, rejected hunks and guide files put back unnoticed until they surface in
a piece. Over syntek-author, updating media first leaves the two templates' shared files and
answers out of step.

## Cross-references

- `how-to/docs/syntek-media/updating-the-template.md`: why each step is there.
- `how-to/src/TEMPLATE-GUIDE/updating-and-recovery.md`: what an update does to each kind of
  file, and every section of the report.
- `how-to/src/TEMPLATE-GUIDE/syntek-media/05-the-answers.md`: each answer, and what it costs to
  change.
- `how-to/workflows/syntek-media/05-recover-a-stopped-update/`: when the update stops.
