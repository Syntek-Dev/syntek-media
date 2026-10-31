# CONTEXT.md — how-to/workflows/syntek-media/02-change-the-answers/

The procedure for changing an answer this project gave syntek-media: a platform or a media kind
added or removed, the brand's description or audience test reworded, a coding agent recorded,
the place binary files are kept. An answer changes only through an update, so this procedure
names the answer and its new value with the author, refuses what can never change, has
everything a removal deletes copied out and committed first, runs the update with the new value,
reads what it did, and makes the hand edits the change leaves.

## Directory Tree

```text
how-to/workflows/syntek-media/02-change-the-answers/
├── CONTEXT.md          ← this file (when to use, what it produces)
├── CLAUDE.md           ← operating rules for this procedure
├── STEPS.md            ← ordered steps to execute, with every command
└── CHECKLIST.md        ← verification checklist before marking complete
```

## When to use this

- The brand starts publishing somewhere new, or stops publishing somewhere.
- The project starts or stops making a kind of media, such as audiobooks or podcast episodes.
- The brand's description, its audience test or another recorded answer no longer holds.
- The author starts using a coding agent besides Claude Code, or changes where binary files
  are kept.

Reach for a **different** procedure when: the author only wants the template's latest changes
(`how-to/workflows/syntek-media/04-update-the-template/`); the update stopped part way with an
error (`how-to/workflows/syntek-media/05-recover-a-stopped-update/`); or the brand kind itself
must change, which no update allows, because a different brand kind is a new project.

## What it produces, and where

- `.copier-answers.syntek-media.yml` recording the new answer, and the files that answer ships
  added, or those it no longer ships deleted, committed together on the branch
  `update-syntek-media`.
- The brand section of `.claude/rules/syntek-media/01-layout-and-routing.md` rewritten by the
  update to match, and the files that describe the options edited by hand.
- For a new platform, its profile ready to fill in through `brand/workflows/04-set-up-a-platform/`;
  for a new coding agent, its row in the model table, with its files still to add.

## The failure this procedure exists to prevent

A hand edit in the answers file, which the next update silently overrules or turns into a
conflict, and a platform or media kind removed without warning, which deletes every file it
generated: the platform profile the author filled in among them. A list answer given in part
removes every value it leaves out.

## Cross-references

- `how-to/docs/syntek-media/changing-the-answers.md`: why each step is there.
- `how-to/src/TEMPLATE-GUIDE/syntek-media/05-the-answers.md`: every answer, and what it costs to
  change.
- `how-to/src/TEMPLATE-GUIDE/syntek-media/11-platforms-and-media-kinds.md`: adding or removing a
  platform or a media kind, and what each removal deletes.
- `how-to/workflows/syntek-media/04-update-the-template/`: the update this procedure runs.
