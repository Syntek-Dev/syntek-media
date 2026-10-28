# CONTEXT.md — how-to/src/

The chapters of the user guide, all inside `how-to/src/TEMPLATE-GUIDE/`. Unlike every other
`src/` folder in a project, this one is not the work: it holds no draft, no plan and no
artefact, and a template's lint and flag checks read it only when asked. Like the rest of
`how-to/`, it is read-only: read it, and never edit it.

## Directory Tree

```text
how-to/src/
├── CONTEXT.md          ← this file (shared)
├── CLAUDE.md           ← how to read the chapters (shared)
└── TEMPLATE-GUIDE/     ← the chapters: the shared ones, and each template's in a folder named for it
```

## What's here

- **`how-to/src/TEMPLATE-GUIDE/`**: the shared chapters, which every template of the family
  ships, and one folder of numbered chapters for each template applied to the project. Its
  `CONTEXT.md` says which chapter to read for what.
- **Written like the work, kept apart from it.** A chapter is written one sentence per line, as
  the work is, so the same checks can read it; but no session drafts, revises or promotes
  anything here.

**Ownership.** This pair is shared, the same bytes in every template of the family that ships it;
each chapter belongs to its template, and the shared chapters to every template that ships
them. Every update of a template puts its chapters and the shared ones back as it wrote them, and
lists each in its report; what you had stays in Git. Only a template's update, its recovery and
the commands its report prints change a file here.

## Cross-references

- `how-to/CONTEXT.md`: the whole guide, and who owns each file in it.
- `how-to/src/TEMPLATE-GUIDE/CONTEXT.md`: where reading starts.
- `.claude/rules/`: the project's rules, which name the folders that hold the work.
