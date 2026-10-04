# CONTEXT.md — production/src/assets/

Small stills, logos and graphics a piece shows on screen and that are committed with the project:
a logo for an end card, a diagram, a product shot, a book cover for a trailer. Each is under
10 MB. Anything larger, and anything recorded, is source media and goes through the footage
manifest (`production/src/footage/`); the brand's fonts are in
`brand/src/design-system/fonts/`, and its exported designs in `brand/src/exports/`.

## Directory Tree

```text
production/src/assets/
├── CONTEXT.md          ← this file
├── CLAUDE.md           ← operating rules
└── <kebab-name>.<ext>  ← one still, logo or graphic, under 10 MB
```

## What's here

- Stills, logos and graphics, each named in kebab-case for what it shows. **An edit decision
  list cites one by its path** (a clip's or an overlay's `source`), and a card may show one by a
  relative path; renaming an asset breaks every list and card that names it.
- Until a piece needs one, this folder holds only its pair.

## Cross-references

- `production/docs/reference/edit-decision-lists.md` — how a still is held, pushed in and faded.
- `production/src/rights-register.md` — the row an image needs when someone else owns it or it
  shows a person.
- `production/src/footage/` — where anything large or recorded is logged instead.
