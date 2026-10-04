# CONTEXT.md — scripts/docs/

The scripts layer's guides: short explanations of how a piece is planned, written and boarded in
this project, each answering one question. Guides explain and route; the rules they serve live in
`.claude/rules/syntek-media/`, and the procedures that apply them live in `scripts/workflows/`.
No brief, script or storyboard is written here.

## Directory Tree

```text
scripts/docs/
├── CONTEXT.md        ← this file
├── CLAUDE.md         ← operating rules
├── reference/        ← template-owned guides, updated by `copier update`
└── project/          ← your own guides; a same-named file overrides reference/
```

## What's here

- `reference/` — **the guides that ship with the template.** Never edit them in place:
  `copier update` merges template changes into them, and a local edit turns every update into a
  merge conflict. Extend or override them in `project/` instead. The guides for each kind of
  piece ship only where the project makes that kind.
- `project/` — **guides written for this project.** A file here with the same name as one in
  `reference/` overrides it; a new name adds a guide. The one limit is the ladder: a project
  guide of the same name may add a check to a gate, never remove or weaken one. The template
  ships only this folder's pair.

## Cross-references

- `scripts/docs/reference/CONTEXT.md` — the guide index for this project's kinds of piece.
- `.claude/rules/syntek-media/01-layout-and-routing.md` — the ownership classes behind the
  split.
- `.claude/rules/syntek-media/03-production-ethics.md` — Section 3, which keeps the ladder's
  gates binding over any project guide.
