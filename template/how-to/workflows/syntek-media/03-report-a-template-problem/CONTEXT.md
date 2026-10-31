# CONTEXT.md — how-to/workflows/syntek-media/03-report-a-template-problem/

The procedure for reporting a fault in syntek-media to the people who keep it: from telling a
template fault apart from the project's own edits, through collecting the versions and the
output that let someone else reproduce it, to an issue drafted for the author to file at the
template's source. Everything it collects is redacted first, and a security problem never goes
into a public issue.

## Directory Tree

```text
how-to/workflows/syntek-media/03-report-a-template-problem/
├── CONTEXT.md          ← this file (when to use, what it produces)
├── CLAUDE.md           ← operating rules for this procedure
├── STEPS.md            ← ordered steps to execute, with every command
└── CHECKLIST.md        ← verification checklist before marking complete
```

## When to use this

- A copy stopped on a collision: a path that already existed, other than a shared file Copier
  printed as `conflict` then `skip` or as `identical`.
- An update, a migration or the toolkit fails the same way on a clean, committed tree, after
  `how-to/workflows/syntek-media/05-recover-a-stopped-update/` has been followed.
- A file the template wrote says something the template does not do, or two of its files
  disagree.
- The template could work better, and the author wants to propose the change.

Reach for a **different** procedure when: an update has just stopped and left changes
(`how-to/workflows/syntek-media/05-recover-a-stopped-update/` first); or the fault lies in
syntek-author's files, which are reported at syntek-author's own source.

## What it produces, and where

- A draft issue, handed to the author in the session: what happened, what was expected, the
  steps that reproduce it, the output, and the versions, every line of it redacted.
- Nothing inside the project. The draft is never saved there, because a file there is committed
  and pushed with the project.

## The failure this procedure exists to prevent

A report nobody can act on, or one that does harm. An issue without the template's version, the
exact command and its whole output cannot be reproduced; one about the project's own edit sends
the maintainers after a fault that is not theirs; and one that carries a key, a voice ID or a
home path publishes it with the issue. A security problem filed in public is disclosed before it
is fixed.

## Cross-references

- `how-to/docs/syntek-media/reporting-a-template-problem.md`: why each step is there.
- `how-to/src/TEMPLATE-GUIDE/syntek-media/13-troubleshooting.md`: what to try first, grouped by
  when it breaks.
- `.claude/rules/syntek-media/06-global-rules.md` Section 10: what never leaves the project.
