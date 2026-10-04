# CONTEXT.md — publishing/docs/project/

Publishing guides written for this project. The template seeds only this pair, once; from then on
the pair and everything else in the folder are yours, and `copier update` never changes them. A
guide here with the same filename as one in `publishing/docs/reference/` overrides it entirely; a
new filename adds a guide the template does not have. This is where the project's own publishing
conventions go — the house rules for its cut-downs, its captions, its thumbnails or its posts that
no other project shares.

## Directory Tree

```text
publishing/docs/project/
├── CONTEXT.md          ← this file
├── CLAUDE.md           ← operating rules
└── <question>.md       ← one guide per question, in the reference guides' shape
```

## What's here

- Guides you have written, each named in kebab-case for the question it answers, with a line
  here for each. **Until you write one, this folder holds only its pair.**

## Cross-references

- `publishing/docs/reference/` — the template's guides, which yours override by name.
- `publishing/docs/CLAUDE.md` — the guide shape and the precedence rule.
