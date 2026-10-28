# CONTEXT.md — how-to/workflows/

The procedures of the user guide. A procedure gives every step and every command for one job
about the project's template, such as updating it or getting back from an update that stopped.
Each template's procedures sit in a folder named for it, numbered from 01.
Like the rest of `how-to/`, this folder is read-only: read it, and never edit it.

## Directory Tree

```text
how-to/workflows/
├── CONTEXT.md     ← this file (shared)
├── CLAUDE.md      ← how to run a procedure (shared)
└── <template>/    ← each template's procedures, one numbered folder each, with that folder's pair
```

## What's here

- **`<template>/`**: one folder for each template applied to the project that ships procedures,
  named exactly as its answers file `.copier-answers.<template>.yml` names it. Its pair lists
  its procedures and says which job each does.
- **Each procedure carries its own commands**, so it works even where a shared chapter is
  missing; the chapters and guides explain why, never the steps.
- **A session runs a procedure** as its template's folder here says, step by step with its
  checklist open, and stops for the owner at every step that changes the template's files or a
  settings file.
- **A project's own way can replace one.** Where the project's rules in `.claude/rules/` provide
  an alias or an override for a procedure, it is recorded where they say, and it wins.

**Ownership.** This pair is shared, the same bytes in every template of the family that ships it;
each procedure belongs to the template whose folder holds it. Every update of a template puts its
files here back as it wrote them, and lists each in its report; what you had stays in Git. Only
a template's update, its recovery and the commands its report prints change a file here.

## Cross-references

- `how-to/CONTEXT.md`: the whole guide, and who owns each file in it.
- `how-to/docs/`: the guides that explain each practice a procedure carries out.
- `how-to/src/TEMPLATE-GUIDE/`: the chapters, which explain what a procedure's steps do.
- `.claude/rules/`: the project's rules, including where a project records its own way of doing a
  job.
