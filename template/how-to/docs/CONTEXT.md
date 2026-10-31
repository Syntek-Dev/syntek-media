# CONTEXT.md — how-to/docs/

The guides of the user guide. A guide explains one practice, such as updating the template: what
it is, how this kind of project applies it, which procedure carries it out and which rule governs
it. Each template's guides sit in a folder named for it. Like the rest of `how-to/`, this folder
is read-only: read it, and never edit it.

## Directory Tree

```text
how-to/docs/
├── CONTEXT.md     ← this file (shared)
├── CLAUDE.md      ← how to use the guides (shared)
└── <template>/    ← each template's guides, with that folder's own pair
```

## What's here

- **`<template>/`**: one folder for each template applied to the project, named exactly as its
  answers file `.copier-answers.<template>.yml` names it. Its `CONTEXT.md` lists its guides.
- **A guide explains; a procedure acts.** Each guide names the procedure, in the same template's
  folder under `how-to/workflows/`, that gives the steps and the commands, and the rule in
  `.claude/rules/` that decides.

**Ownership.** This pair is shared, the same bytes in every template of the family that ships it;
each guide belongs to the template whose folder holds it. Every update of a template puts its
files here back as it wrote them, and lists each in its report; what you had stays in Git. Only
a template's update, its recovery and the commands its report prints change a file here. A
project that works differently from a guide records the difference where the project's rules in
`.claude/rules/` say a departure is recorded, never here.

## Cross-references

- `how-to/CONTEXT.md`: the whole guide, and who owns each file in it.
- `how-to/workflows/`: the procedures the guides name.
- `how-to/src/TEMPLATE-GUIDE/`: the chapters, which explain the same practices at more length.
- `.claude/rules/`: the rules each guide cites, which win wherever a guide only explains.
