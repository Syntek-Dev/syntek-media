# CONTEXT.md — production/src/assets/

Small stills, logos, graphics and text captures a piece shows on screen, committed with the project:
a logo, diagram, product shot, book cover or terminal/page capture. Each is under
10 MB. Anything larger, and anything recorded, is source media and goes through the footage
manifest (`production/src/footage/`); the brand's fonts are in
`brand/src/design-system/fonts/`, and its exported designs in `brand/src/exports/`.

## Directory Tree

```text
production/src/assets/
├── CONTEXT.md          ← this file
├── CLAUDE.md           ← operating rules
└── <kebab-name>.<ext>  ← one image or text capture, under 10 MB
```

## What's here

- Stills, logos and graphics, each named in kebab-case for what it shows. **An edit decision
  list cites one by its path** (a clip's or an overlay's `source`), and a card may show one by a
  relative path; renaming an asset breaks every list and card that names it.
- Until a piece needs one, this folder holds only its pair.
- Text captures are `.txt`, `.ansi` or `.html`, never `.log` or `.out`. Remove every home path
  and host name before committing. Name each by its full `production/src/assets/` path.
- A scene's shot-list Source column names its images and captures; `media.py real <piece>`
  hashes those named assets, reads footage-image hashes from the manifest without opening the
  mirror, and prints the index. Accept it through `-o` in `production/src/scenes/`.

## Cross-references

- `production/docs/reference/edit-decision-lists.md` — how a still is held, pushed in and faded.
- `production/src/rights-register.md` — the row an image needs when someone else owns it or it
  shows a person.
- `production/src/footage/` — where anything large or recorded is logged instead.
- `production/docs/reference/scenes-as-code.md` — how a scene uses the accepted real-source index.
