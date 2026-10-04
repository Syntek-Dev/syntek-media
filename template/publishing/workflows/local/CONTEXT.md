# CONTEXT.md — publishing/workflows/local/

Publishing procedures written for this project. The template seeds only this pair, once; from then
on the pair and every procedure in the folder are yours, and `copier update` never changes them.
A procedure here with the same slug as a template procedure (for example one named
`05-prepare-a-post`) overrides it, because `run-media-workflow` looks in this folder first. A new
slug adds a procedure the template does not have.

## Directory Tree

```text
publishing/workflows/local/
├── CONTEXT.md          ← this file
├── CLAUDE.md           ← operating rules
└── NN-verb-first-name/ ← one procedure: CONTEXT.md, CLAUDE.md, STEPS.md, CHECKLIST.md
```

## What's here

- Your own procedures, numbered in this folder's own sequence from `01`, independent of the
  template's numbers. **Until you write one, this folder holds only its pair.**
- An override keeps the template procedure's slug, including its number, so that the router
  matches it.
- When you add one, add a row to this table:

| Procedure | What it is for | Overrides |
|---|---|---|

## Cross-references

- `publishing/workflows/CLAUDE.md` — the template procedures, and the four-file shape.
- `.claude/skills/run-media-workflow/SKILL.md` — how a request is resolved, this folder first.
