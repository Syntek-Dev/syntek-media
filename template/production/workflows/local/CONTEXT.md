# CONTEXT.md — production/workflows/local/

The author's own production procedures: jobs this project repeats that the template's
procedures do not cover (recording a guest remotely, mastering a series intro, logging a whole
shoot day), or a template procedure changed to suit this project. The template ships only this
pair; everything else here is yours, and `copier update` never touches it.

## Directory Tree

```text
production/workflows/local/
├── CONTEXT.md              ← this file: your index of local procedures
├── CLAUDE.md               ← operating rules
└── NN-verb-first-name/     ← one procedure: CONTEXT · CLAUDE · STEPS · CHECKLIST
```

## What's here

No local procedures yet. **A folder here with the same slug as a template procedure (for
example 02-make-a-voiceover) replaces that procedure for this project**; `run-media-workflow`
checks this folder first. A folder with a new slug adds a procedure.

| Procedure | What it does | Overrides |
|---|---|---|

## Cross-references

- `production/workflows/` — the template's procedures, and the shape to copy.
- `.claude/rules/syntek-media/01-layout-and-routing.md` — the local numbering and override rule
  for every layer.
