@./CONTEXT.md

# CLAUDE.md — how-to/docs/syntek-media/

Read order: `.claude/CLAUDE.md` → `.claude/MEMORY.md` → `how-to/CONTEXT.md` →
`how-to/CLAUDE.md` → `how-to/docs/CONTEXT.md` → `how-to/docs/CLAUDE.md` → this folder's
`CONTEXT.md` (imported above) → this file.

## Purpose (one line)

Explain why each practice of keeping the project in step with syntek-media works as it does, and
send the work to the procedure that carries it out.

## How to work here

- **Routing:** each guide names its procedure, in `how-to/workflows/syntek-media/`:
  - `finishing-a-copy.md` → `how-to/workflows/syntek-media/01-finish-a-copy/`;
  - `changing-the-answers.md` → `how-to/workflows/syntek-media/02-change-the-answers/`;
  - `reporting-a-template-problem.md` →
    `how-to/workflows/syntek-media/03-report-a-template-problem/`;
  - `updating-the-template.md` → `how-to/workflows/syntek-media/04-update-the-template/`, and
    `how-to/workflows/syntek-media/05-recover-a-stopped-update/` when an update stopped;
  - `enabling-a-coding-agent-client.md` →
    `how-to/workflows/syntek-media/06-enable-a-coding-agent-client/`.

  Check first for a departure: in syntek-author's project settings file, under Overrides or
  Workflow aliases, where it is present, and otherwise in `.claude/CLAUDE.md` under the heading
  'Project-specific rules'. A departure recorded there wins.
- **Model:** **Opus**: reading a guide into a decision about this project is judgement, and the
  procedures it leads to change the template's files or a settings file
  (`.claude/rules/syntek-media/05-model-allocation.md`).
- **Concrete steps:** find the guide in `CONTEXT.md` → read it → check for a recorded departure →
  run the procedure the guide names, as `how-to/workflows/syntek-media/` says, never through
  `run-media-workflow`.
- **Definition of done:** the practice is understood, the procedure is chosen, and nothing under
  `how-to/` changed except through the template's update, its recovery and the commands its
  report prints.

## Guardrails

- **Read-only.** Never edit, write, move or delete a guide here, even when asked, except through
  the template's update, its recovery and the commands its update report prints for a file here.
  `.claude/settings.json` denies it, the guide guard (`.claude/hooks/how-to-read-only.sh`)
  refuses it, and the next update puts the file back
  (`.claude/rules/syntek-media/06-global-rules.md` Section 3).
- **No `docs/project/` here.** This project's own way of doing one of these practices is a
  recorded departure, never a copy of the guide.
- **A guide explains; the rules decide.** Where a guide and its governing standard differ, follow
  the standard and tell the author.
- **Commands come from the procedure.** A guide names commands to explain them; run each one from
  the procedure's `STEPS.md`, in its order, and never from a guide or from memory.

## Output & naming

- **Writes nothing.** Every file here is template-owned.
- **Names:** `kebab-title.md`; each guide opens with its title and a gloss as one H1, then the
  metadata header and `**What it is.**`, and ends with `## Governing standard`.
