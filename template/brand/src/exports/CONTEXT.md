# CONTEXT.md — brand/src/exports/

Design assets exported from Claude Design, or made from a design, and kept in the repository so a
piece can use them: a logo, a cover, a background plate, a lower-third, a print file. Files of
10 MB or less are committed here as ordinary files; larger ones go in `large/`, which Git LFS
stores. Every file here has a row in `brand/src/design-register.md`. Renders are not exports
(they are regenerable and git-ignored), and recorded or licensed footage is not either (it is
listed in `production/src/footage/manifest.toml` and kept in external storage).

## Directory Tree

```text
brand/src/exports/
├── CONTEXT.md          ← this file
├── CLAUDE.md           ← operating rules
├── large/              ← exports over 10 MB, stored by Git LFS
└── <design>.<ext>      ← one exported file, named for its design in kebab-case
```

## What's here

- Exported files of 10 MB or less, each named in kebab-case for the design it came from. **Until
  the first export is recorded, this folder holds only its pair and `large/`.**
- `large/` — the same, for files over 10 MB, which Git would otherwise commit whole; its own
  `.gitattributes` marks them for Git LFS.
- Each file's row in `brand/src/design-register.md` gives its Claude Design link, its storage
  (`git` here) and the date it was exported.

- Sprite exports keep pose/mouth and optional blink names for the scene kit; whole frames or
  pose plus native mouth layer, all registered with their origin and scale notes.
## Cross-references

- `brand/docs/reference/design-exports.md` — small and large, LFS, and the register.
- `brand/workflows/03-record-a-design-export/` — the procedure that files an export.
- `production/src/assets/` — where a still or logo is copied when an edit uses it directly.
