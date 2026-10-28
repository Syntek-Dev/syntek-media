@./CONTEXT.md

# CLAUDE.md — how-to/workflows/

Read order: `.claude/CLAUDE.md` → `.claude/MEMORY.md` → `how-to/CONTEXT.md` →
`how-to/CLAUDE.md` → this folder's `CONTEXT.md` (what a procedure is, imported above) → this
file.

## Purpose (one line)

Run a template's procedure exactly as written, with the owner, and never change it.

## How to work here

- **Routing:** the template the job concerns → its folder here → the procedure its pair names
  for the job. Check first for an alias or an override of the procedure, where the project's
  rules say one is recorded; it replaces the procedure.
- **Model:** **Opus**: a procedure can change the template's files, the project's rules or a
  settings file, and a wrong step there is costly to undo.
- **Concrete steps:** read the procedure's files in the order its own `CLAUDE.md` gives → run
  each step in order, stopping for the owner where a step says → confirm each check it lists →
  report what changed.
- **Definition of done:** every step ran or was agreed away with the owner, every check the
  procedure lists holds, and nothing under `how-to/` changed except through a template's update,
  its recovery and the commands its report prints.

## Guardrails

- **Never edit, write, move or delete a procedure, even when asked**, except through a
  template's update, its recovery and the commands its update report prints for a file here.
  Claude Code denies it, a hook refuses it, and the next update puts the file back.
- **The project's own way is an alias or an override, never an edit.** It is recorded where the
  project's rules say, and it wins over the procedure it names.
- **Use the procedure of the template the job concerns.** Never run one template's procedure,
  or its command, for another template's job.
- **Never renumber or add a procedure here.** Numbers are frozen, and the owner's own procedures
  belong where the project's rules put them.
- **Commands run exactly as written**, and only with the owner's agreement where a step asks
  for it; a step that fails stops the procedure, and the owner hears why.

## Output & naming

- **Writes nothing here.** A procedure's steps change the project as they say; this folder takes
  no output.
- **Names:** each template's procedures sit in its own `<template>/` folder, as
  `NN-verb-first-name/` folders numbered from 01, their numbers frozen.
