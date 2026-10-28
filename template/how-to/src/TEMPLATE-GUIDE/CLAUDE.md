@./CONTEXT.md

# CLAUDE.md — how-to/src/TEMPLATE-GUIDE/

Read order: `.claude/CLAUDE.md` → `.claude/MEMORY.md` → `how-to/CONTEXT.md` →
`how-to/CLAUDE.md` → `how-to/src/CONTEXT.md` → `how-to/src/CLAUDE.md` → this folder's
`CONTEXT.md` (which chapter to read for what, imported above) → this file.

## Purpose (one line)

Answer how this project works from the chapter that owns the answer, and route to the rule that
decides.

## How to work here

- **Routing:** the table in this folder's `CONTEXT.md` names the chapter for each kind of
  question: a shared chapter here, or the asking template's folder. Each chapter's 'Where the
  rules live' names the rules in `.claude/rules/` that decide, and its 'Next' what to read after
  it.
- **Model:** **Opus**: matching a question to the chapter and the rule that own it is judgement.
- **Concrete steps:** read the table → read the chapter → read the rule it routes to → answer
  from the rule, citing the chapter for the explanation → where the answer is a job a procedure
  covers, run that template's procedure under `how-to/workflows/`.
- **Definition of done:** the question is answered, the deciding rule is cited, and nothing under
  `how-to/` changed except through a template's update, its recovery and the commands its report
  prints.

## Guardrails

- **A chapter explains; the project's rules decide where they differ.** Never quote a chapter as
  a rule, and tell the owner when a chapter and a rule disagree.
- **Never edit, write, move or delete a chapter, even when asked**, except through a template's
  update, its recovery and the commands its update report prints for a file here (taking the
  template's version, `git add`, removing a `.rej` file). Claude Code denies it, a hook refuses
  it, and the next update puts the file back.
- **Never add a chapter here**, in a template's folder or beside the shared ones. A departure
  from a chapter is recorded where the project's rules in `.claude/rules/` say.
- **A shared chapter names no template.** Where it sends the reader to 'your template's
  procedure', use the procedure of the template the job concerns.

## Output & naming

- **Writes nothing.** Every chapter here is a template's.
- **Names:** shared chapters are `kebab-title.md`, directly in this folder; a template's chapters
  are `NN-kebab-title.md` in its `<template>/` folder, numbered from 01, their numbers frozen.
  Every chapter opens with its title and a short gloss, carries no header, and ends with 'Where
  the rules live' and then 'Next'.
