@./CONTEXT.md

# CLAUDE.md — how-to/docs/

Read order: `.claude/CLAUDE.md` → `.claude/MEMORY.md` → `how-to/CONTEXT.md` →
`how-to/CLAUDE.md` → this folder's `CONTEXT.md` (what a guide is, imported above) → this file.

## Purpose (one line)

Read a template's guide to learn why a practice works as it does, then follow the procedure it
names.

## How to work here

- **Routing:** the template's own folder here → the guide for the practice → the procedure it
  names in that template's folder under `how-to/workflows/` → the rule it cites in
  `.claude/rules/`. A project that departs from a guide records it where the project's rules in
  `.claude/rules/` say; that departure wins.
- **Model:** **Opus**: a guide is read to decide how a practice applies here, which is judgement.
- **Concrete steps:** find the template's folder → read its `CONTEXT.md` → read the guide →
  check for a departure where the project's rules say one is recorded → follow the procedure the
  guide names.
- **Definition of done:** the practice is understood, the procedure is chosen, and nothing under
  `how-to/` changed except through a template's update, its recovery and the commands its report
  prints.

## Guardrails

- **Never edit, write, move or delete a guide, even when asked**, except through a template's
  update, its recovery and the commands its update report prints for a file here. Claude Code
  denies it, a hook refuses it, and the next update puts the file back.
- **Never add a guide here.** The owner's own guides belong where the project's rules put them,
  and a departure from a template's guide is recorded where the project's rules say.
- **A guide explains; the rules decide.** Where a guide and a rule differ, follow the rule and
  tell the owner.

## Output & naming

- **Writes nothing.** Every guide here is a template's.
- **Names:** each template's guides sit in its own `<template>/` folder, as `kebab-title.md`.
