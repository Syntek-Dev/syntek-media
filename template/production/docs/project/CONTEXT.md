# CONTEXT.md — production/docs/project/

The author's own guides for this project's production: the terms of a music library the brand
uses, a recording set-up, a house mix, how this channel handles a guest's release, anything that
recurs and that the template's reference guides do not cover. The template ships only this
pair; everything else here is yours, and `copier update` never touches it.

## Directory Tree

```text
production/docs/project/
├── CONTEXT.md          ← this file
├── CLAUDE.md           ← operating rules
└── <question>.md       ← one guide per recurring question, kebab-case
```

## What's here

- Nothing yet, until you add a guide. **A guide here with the same filename as one in
  `production/docs/reference/` replaces it** for this project; a guide with a new name adds to
  the set.
- Typical project guides: a music library and its terms, a studio or kitchen-table recording
  set-up, a house mix for a recurring series, the release a guest signs.

## Cross-references

- `production/docs/reference/` — the template's guides, which this folder can override.
- `.claude/rules/syntek-media/01-layout-and-routing.md` — the override rule for every layer.
- `production/src/` — where the material the guides talk about is kept.
