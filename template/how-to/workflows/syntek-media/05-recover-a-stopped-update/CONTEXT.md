# CONTEXT.md — how-to/workflows/syntek-media/05-recover-a-stopped-update/

The procedure for getting back from a syntek-media update that stopped part way with an error.
By then Copier has written the new version's files and moved the answers file forward, but
nothing that runs after it has run: no migration, no report, no refresh, no guide put back. This
procedure puts back a held .agents link, lists what a discard would delete, discards the stopped
update with the author's agreement, makes `how-to` a real folder where it was not one, and runs
the update again.

## Directory Tree

```text
how-to/workflows/syntek-media/05-recover-a-stopped-update/
├── CONTEXT.md          ← this file (when to use, what it produces)
├── CLAUDE.md           ← operating rules for this procedure
├── STEPS.md            ← ordered steps to execute, with every command
└── CHECKLIST.md        ← verification checklist before marking complete
```

## When to use this

- An update ended with `OSError: [Errno 39] Directory not empty` instead of its report.
- An update ended with `FileExistsError: [Errno 17]` or `NotADirectoryError` naming `how-to`,
  because `how-to` in the project is a file rather than a folder.
- An update ended with `ForbiddenPathError` naming a path in `how-to`, because `how-to` is a
  link that leads outside the project.
- An update ended with `ForbiddenPathError` naming a path in .agents, after a message framed in
  lines of `=` that says `agents-outside-link did NOT run`: .agents is a link that leads outside
  the project, and Copier ran on a Python older than 3.14.
- An update stopped with any other error, and `git status` shows that it had begun writing.
- `.agents.syntek-held` stands in the project, from an update that stopped before it ended.

Reach for a **different** procedure when: the update finished with its report, conflicts and
all (step 6 of `how-to/workflows/syntek-media/04-update-the-template/`); Copier refused to start
and `git status` shows no change, which needs no recovery: fix what it named and run
`how-to/workflows/syntek-media/04-update-the-template/` again; or the stop was syntek-author's
update, which syntek-author's own recovery procedure covers, in its folder under
`how-to/workflows/`, where it is present.

## What it produces, and where

- The project back at its last commit, with nothing of the author's lost: anything untracked
  was committed or moved out first.
- An .agents link outside the project back in place, where one was held aside.
- `how-to` renamed and committed, where it was a file or a link, so the update can write the
  user guide.
- The update run again, ending with a report that reads from the version the project had.

## The failure this procedure exists to prevent

Committing what a stopped update left. The answers file already names the new version, so the
next update takes it as reached: it skips that version's migrations, refreshes and the guide's
restore, and nothing ever runs them. A careless discard is the other failure: `git clean -fd`
deletes a held .agents link and every untracked file of the author's, which is why the link is
put back and the dry run read first.

## Cross-references

- `how-to/docs/syntek-media/updating-the-template.md`: why an update stops, and why it is
  discarded and run again.
- `how-to/src/TEMPLATE-GUIDE/updating-and-recovery.md`: the same recovery, explained.
- `how-to/src/TEMPLATE-GUIDE/agent-clients-and-mcp.md`: every case of .agents.
- `.claude/syntek-media-agents.md`, 'Client setup': the held link, put back in the same order.
- `how-to/workflows/syntek-media/04-update-the-template/`: where the work goes on afterwards.
