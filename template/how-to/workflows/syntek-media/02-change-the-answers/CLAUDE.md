@./CONTEXT.md

# CLAUDE.md — how-to/workflows/syntek-media/02-change-the-answers/

Read order: `.claude/CLAUDE.md` → `.claude/MEMORY.md` → `how-to/CONTEXT.md` →
`how-to/CLAUDE.md` → `how-to/workflows/CONTEXT.md` → `how-to/workflows/CLAUDE.md` →
`how-to/workflows/syntek-media/CONTEXT.md` → `how-to/workflows/syntek-media/CLAUDE.md` → this
folder's `CONTEXT.md` (imported above) → this file → `STEPS.md` (with `CHECKLIST.md` open).

## Purpose (one line)

Change one or more of the project's answers through an update, with nothing the author needs
lost to a removal, and commit the change whole.

## How to work here

- **Routing:** no skill; this is a command-and-review procedure, and `run-media-workflow` never
  routes it. Guide `how-to/docs/syntek-media/changing-the-answers.md`; each answer is explained
  in `how-to/src/TEMPLATE-GUIDE/syntek-media/05-the-answers.md`, and the update itself follows
  `how-to/workflows/syntek-media/04-update-the-template/`.
- **Model:** **Opus** for settling the answer, for every removal and for reading the report and
  the changes with the author; the mechanical tier only for running a command the author has
  agreed (`.claude/rules/syntek-media/05-model-allocation.md`).
- **Concrete steps:** follow `STEPS.md` in order and tick `CHECKLIST.md` as you go. On any stop
  with an error, leave this procedure for
  `how-to/workflows/syntek-media/05-recover-a-stopped-update/`.
- **Definition of done:** the new answer recorded by the update, every file a removal deleted
  either committed beforehand or let go by the author, the hand edits made, the whole committed
  on the branch, and nothing under `how-to/` changed except through the update and the commands
  its report printed.

## Guardrails

- **Never edit `.copier-answers.syntek-media.yml` by hand.** An answer changes only through the
  update (`.claude/rules/syntek-media/06-global-rules.md` Section 11).
- **`BRAND_KIND` never changes.** The update refuses it and touches nothing; a different brand
  kind is a new project. Say so, and stop.
- **A list answer is given whole.** `PLATFORMS`, `MEDIA_KINDS` and `AGENT_CLIENTS` take every
  value the project keeps, the new one included: a value left out is removed.
- **Nothing is removed unread.** Before a platform or a media kind goes, the author hears every
  file it deletes and has what they need copied out and committed.
- **The author decides** every answer and every removal; a session runs the update only on the
  author's word, and only in the `--defaults` form step 6 gives.
- **Never edit under `how-to/`**, even when asked: Claude Code's deny in `.claude/settings.json`
  and the guide guard `.claude/hooks/how-to-read-only.sh` refuse it, and the next update puts
  it back (`.claude/rules/syntek-media/06-global-rules.md` Section 3). A departure is recorded in
  syntek-author's project settings file, 00-project.md, under Overrides or Workflow aliases,
  where that file is present, and otherwise in `.claude/CLAUDE.md` under the heading
  'Project-specific rules' (`.claude/rules/syntek-media/01-layout-and-routing.md` Section 10).

## Output & naming

- **Writes:** the answers file, the files the new answer adds or removes and the commit, through
  Copier and the commands in `STEPS.md`, plus the hand edits of step 8; the branch is
  `update-syntek-media`, and the commit message `Update from syntek-media`.
- **Does not touch:** the author's own files, which no update deletes.
