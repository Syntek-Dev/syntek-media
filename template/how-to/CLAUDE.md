@./CONTEXT.md

# CLAUDE.md — how-to/

Read order: `.claude/CLAUDE.md` → `.claude/MEMORY.md` → this folder's `CONTEXT.md` (what the
guide holds and who owns it, imported above) → this file.

## Purpose (one line)

Read the guide to answer how this project works; never change it.

## How to work here

- **Routing:** a question about how the project works goes to the chapter that owns the answer,
  in the asking template's folder under `how-to/src/TEMPLATE-GUIDE/` or among the shared
  chapters there; a job a procedure covers goes to that template's folder under
  `how-to/workflows/`. Anything a chapter explains, the project's rules in `.claude/rules/`
  decide: follow the rule, and cite it.
- **Model:** **Opus**: answering from the guide means choosing which chapter and which rule
  apply, and a wrong answer is acted on with full confidence.
- **Concrete steps:** find the template's folder (its name is in its answers file,
  `.copier-answers.<template>.yml`) → read the `CONTEXT.md` of its chapter folder for the
  reading order → read the chapter, then the rule it routes to → run a procedure as its
  template's folder under `how-to/workflows/` says, step by step with its checklist open.
- **Definition of done:** the question is answered from the chapter and the rule, and nothing
  under `how-to/` changed except through a template's update, its recovery and the commands its
  report prints.

## Guardrails

- **Never edit, write, move or delete a file here, even when asked**, except through a
  template's update, its recovery and the commands its update report prints for a file here
  (taking the template's version, `git add`, removing a `.rej` file). Claude Code denies it, a
  hook refuses it, and the next update puts the file back.
- **Record a departure where the project's rules in `.claude/rules/` say**: an override for a
  guide or chapter, or, where the rules provide one, an alias for a procedure. Never in the
  guide.
- **Never add a file here.** The owner's own guides, procedures and notes belong where the
  project's rules put them; a file here that no template ships is one no session can edit.
- **Never restate a rule from the guide.** A chapter explains; the rules decide. Quote the rule,
  never the chapter, as the reason for an action.
- **Follow the procedure of the template the job concerns.** Updating one template never
  follows another template's steps or runs its command.

## Output & naming

- **Writes nothing.** Every file here is a template's; this folder takes no output.
- **Names:** a template's folders carry its exact name, `<template>/`; its chapters are
  `NN-kebab-title.md`, numbered from 01; its procedures are `NN-verb-first-name/` folders; the
  shared chapters are `kebab-title.md`; `how-to/src/TEMPLATE-GUIDE/` is the one upper-case
  folder.
