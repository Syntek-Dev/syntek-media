@./CONTEXT.md

# CLAUDE.md — how-to/workflows/syntek-media/04-update-the-template/

Read order: `.claude/CLAUDE.md` → `.claude/MEMORY.md` → `how-to/CONTEXT.md` →
`how-to/CLAUDE.md` → `how-to/workflows/CONTEXT.md` → `how-to/workflows/CLAUDE.md` →
`how-to/workflows/syntek-media/CONTEXT.md` → `how-to/workflows/syntek-media/CLAUDE.md` → this
folder's `CONTEXT.md` (imported above) → this file → `STEPS.md` (with `CHECKLIST.md` open).

## Purpose (one line)

Bring syntek-media's latest version into the project safely, read every line of its output with
the author, and commit it whole.

## How to work here

- **Routing:** no skill; this is a command-and-review procedure, and `run-media-workflow` never
  routes it. Guide `how-to/docs/syntek-media/updating-the-template.md`; the report's sections
  are explained in `how-to/src/TEMPLATE-GUIDE/updating-and-recovery.md`.
- **Model:** **Opus** for settling answers and for reading the migration output, the report and
  the changes with the author; the mechanical tier only for running a command the author has
  agreed (`.claude/rules/syntek-media/05-model-allocation.md`).
- **Concrete steps:** follow `STEPS.md` in order and tick `CHECKLIST.md` as you go. On any stop
  with an error, leave this procedure for
  `how-to/workflows/syntek-media/05-recover-a-stopped-update/`.
- **Definition of done:** the update and its answers file are committed on the branch, every
  report entry has been read with the author and acted on as they decided, and nothing under
  `how-to/` changed except through the update and the commands its report printed.

## Guardrails

- **syntek-author first.** Where syntek-author has been applied, its update is run and committed
  by its own procedure before this one starts; never the other way round.
- **Never commit what a stopped update left.** Any error before the report means
  `how-to/workflows/syntek-media/05-recover-a-stopped-update/`.
- **Never edit under `how-to/`.** The update puts the guide back; a conflict or a `.rej` file
  there is settled only with the commands the report prints
  (`.claude/rules/syntek-media/06-global-rules.md` Section 3). A departure is recorded in
  syntek-author's project settings file, 00-project.md, under Overrides or Workflow aliases,
  where that file is present, and otherwise in `.claude/CLAUDE.md` under the heading
  'Project-specific rules' (`.claude/rules/syntek-media/01-layout-and-routing.md` Section 10).
- **Never edit `.copier-answers.syntek-media.yml` by hand.** An answer changes only through the
  update (`.claude/rules/syntek-media/06-global-rules.md` Section 11), and `BRAND_KIND` never.
- **The author decides** every answer, every conflict, every `take` and every file put back; a
  session runs the update only on the author's word, and only in the `--defaults` form step 5
  gives, because the other form needs a terminal for Copier's questions.
- **One template at a time.** Another template's update waits until this one is committed.

## Output & naming

- **Writes:** the template's files, the answers file and the commit, through Copier and the
  commands in `STEPS.md`; the branch is `update-syntek-media`, and the commit message
  `Update from syntek-media`.
- **Does not touch:** the author's pieces, registers and logs, which no update changes.
