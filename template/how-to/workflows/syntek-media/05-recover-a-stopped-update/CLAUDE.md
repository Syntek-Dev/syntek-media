@./CONTEXT.md

# CLAUDE.md — how-to/workflows/syntek-media/05-recover-a-stopped-update/

Read order: `.claude/CLAUDE.md` → `.claude/MEMORY.md` → `how-to/CONTEXT.md` →
`how-to/CLAUDE.md` → `how-to/workflows/CONTEXT.md` → `how-to/workflows/CLAUDE.md` →
`how-to/workflows/syntek-media/CONTEXT.md` → `how-to/workflows/syntek-media/CLAUDE.md` → this
folder's `CONTEXT.md` (imported above) → this file → `STEPS.md` (with `CHECKLIST.md` open).

## Purpose (one line)

Undo an update that stopped part way, losing nothing of the author's, and run it again so it
delivers what an update that never stopped delivers.

## How to work here

- **Routing:** no skill; this is a recovery procedure, and `run-media-workflow` never routes
  it. Guide `how-to/docs/syntek-media/updating-the-template.md`; the .agents cases are explained
  in `how-to/src/TEMPLATE-GUIDE/agent-clients-and-mcp.md` and in `.claude/syntek-media-agents.md`.
- **Model:** **Opus** for recognising the stop, reading the dry run with the author and
  deciding about `how-to`; the mechanical tier only for running a command the author has agreed
  (`.claude/rules/syntek-media/05-model-allocation.md`).
- **Concrete steps:** follow `STEPS.md` in order and tick `CHECKLIST.md` as you go; once the
  update has run again, continue at step 6 of
  `how-to/workflows/syntek-media/04-update-the-template/`.
- **Definition of done:** the update has run again and ended with its report, read from the
  version the project had, and nothing of the author's was lost on the way.

## Guardrails

- **Commit nothing the stopped update left**, not even to save it.
- **The held link comes first.** `git clean -fd` deletes an `.agents.syntek-held` that Git does
  not track; put it back before any discard.
- **Read the dry run with the author.** `git reset --hard && git clean -fd` discards every
  uncommitted change in the repository and deletes every untracked file the dry run lists; it
  runs only with the author's agreement, and only in a project that is its own repository.
- **Never `rm -r` an .agents link, never with a trailing slash**, and never run
  `mv .agents.syntek-held .agents` while .agents stands.
- **Renaming `how-to` is the author's call**, and never touches anything inside it.
- **A session reruns the update only in the `--defaults` form** step 6 gives, on the author's
  word: the other form needs a terminal, and without one it can leave an .agents link held.
- **Never edit under `how-to/`**: the update run again puts the guide back
  (`.claude/rules/syntek-media/06-global-rules.md` Section 3).
- **Only syntek-media's update.** A stopped syntek-author update follows syntek-author's own
  recovery procedure, where it is present, never this one.

## Output & naming

- **Writes:** nothing but what the commands in `STEPS.md` do: the link put back, the discard,
  the rename of `how-to` and its commit, and the update run again.
- **Sets aside:** `.agents.from-update`, where .agents had to be moved; the author checks it at
  step 3, anything in it they want is moved out of the project, and the discard removes the rest.
