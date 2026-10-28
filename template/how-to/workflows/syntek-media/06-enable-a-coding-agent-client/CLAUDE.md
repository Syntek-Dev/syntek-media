@./CONTEXT.md

# CLAUDE.md — how-to/workflows/syntek-media/06-enable-a-coding-agent-client/

Read order: `.claude/CLAUDE.md` → `.claude/MEMORY.md` → `how-to/CONTEXT.md` →
`how-to/CLAUDE.md` → `how-to/workflows/CONTEXT.md` → `how-to/workflows/CLAUDE.md` →
`how-to/workflows/syntek-media/CONTEXT.md` → `how-to/workflows/syntek-media/CLAUDE.md` → this
folder's `CONTEXT.md` (imported above) → this file → `STEPS.md` (with `CHECKLIST.md` open).

## Purpose (one line)

Give a coding agent the project was not made with exactly the files a fresh project would have
given it, without touching a file the author already has.

## How to work here

- **Routing:** no skill; this is a command-and-compare procedure, and `run-media-workflow`
  never routes it. Guide `how-to/docs/syntek-media/enabling-a-coding-agent-client.md`; the list
  of client files is the bridge's, in `.claude/syntek-media-agents.md`, 'Enabling an existing
  project'.
- **Model:** **Opus** for comparing files and agreeing each one with the author; the mechanical
  tier only for running a command the author has agreed
  (`.claude/rules/syntek-media/05-model-allocation.md`).
- **Concrete steps:** follow `STEPS.md` in order and tick `CHECKLIST.md` as you go. Run steps 2
  to 8 in one terminal: they share the temporary folder's path in `$FRESH`.
- **Definition of done:** the new client starts in the project and reads the bridge, the rules,
  the memory and the skills; every file it needed is in place; no existing file was
  overwritten; the temporary folder is gone and the change is committed.

## Guardrails

- **Never run a copy over the real project.** The fresh render goes into a temporary folder,
  and only the files the project lacks come out of it.
- **Never overwrite a client file the project already has.** Agree with the author how to
  combine the two, and combine them by hand.
- **The bridge's list is the one list.** Copy only the files it names; leave every other
  difference between the two projects alone.
- **.agents is settled by hand**, with the author: a real skills folder in it, or a skills link
  anywhere but the project's own skill tree, stays as it is; an .agents link outside the project
  stays a link.
- **Never edit `.copier-answers.syntek-media.yml` by hand**, and never edit under `how-to/`
  (`.claude/rules/syntek-media/06-global-rules.md` Sections 11 and 3).
- **A client's permission is never the author's approval.** The spending approval and the
  production rules apply in every client, as the bridge says.

## Output & naming

- **Writes:** the answers file and the model table, through the update; the client's
  entrypoint, settings file and .agents where they were missing; the permission rules in the
  client file, through the permissions script; a line in `.claude/MEMORY.md`; the commit.
- **Does not touch:** any file the project already had, but by the agreed combination.
