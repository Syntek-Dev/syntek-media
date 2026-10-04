# CONTEXT.md — production/docs/

The guides for the production layer: how source media is logged and kept, how an edit decision
list is written, where each sound sits and how loud the master lands, how rights and consent are
cleared, and how ElevenLabs is used without spending a credit unasked. Guides explain the
everyday calls; they never outrank the rules in `.claude/rules/syntek-media/`, and they hold no
facts about this project's pieces (those live in `production/src/`).

## Directory Tree

```text
production/docs/
├── CONTEXT.md          ← this file
├── CLAUDE.md           ← operating rules
├── reference/          ← template-owned guides, updated by copier update; do not edit
└── project/            ← your own guides; a same-named file here overrides reference/
```

## What's here

- `production/docs/reference/` — the guides the template ships, one per question a production
  job raises. **Template-owned:** an edit here is lost on the next `copier update`.
- `production/docs/project/` — guides you write for this project (the terms of a music library
  the brand uses, a recording set-up, a house mix). **Author-owned:** the template never touches
  them. A project guide with the same filename as a reference guide replaces it; the
  `## How we apply it here` section is the usual place to extend one instead.

## Cross-references

- `.claude/rules/syntek-media/01-layout-and-routing.md` — the reference/project split and the
  override rule, stated once for every layer.
- `.claude/rules/syntek-media/03-production-ethics.md` — the rules the guides serve.
- `production/workflows/` — the procedures that cite these guides step by step.
