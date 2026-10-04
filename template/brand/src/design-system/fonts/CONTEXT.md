# CONTEXT.md — brand/src/design-system/fonts/

The brand's font files, supplied by the author and loaded by `tokens.css`, so that every
thumbnail, card and burned caption renders in the brand's own faces on any machine, without a
network. The template ships only this folder's pair: it ships no font. A font's licence is not
kept here but in the rights register, where every piece that uses it can be checked.

## Directory Tree

```text
brand/src/design-system/fonts/
├── CONTEXT.md          ← this file
├── CLAUDE.md           ← operating rules
└── <family>-<weight>.<ext>   ← one file per face and weight, loaded by a font-face rule in tokens.css
```

## What's here

- Font files the author has added, each named for its family and weight in kebab-case. **Until
  the author adds one, this folder holds only its pair**, and the kit uses generic families.
- Each file is loaded by one font-face rule in `../tokens.css`, its source given relative to
  that file (`fonts/<file>`), and its family is then named in `--font-display`, `--font-body`
  or `--caption-font`.
- `captions burn` passes this folder to ffmpeg as its fonts folder, and fails rather than burn a
  caption in a fallback face.

## Cross-references

- `brand/docs/reference/the-brand-kit.md` — fonts, and how the kit names them.
- `production/src/rights-register.md` — one `font` row per licence, by ID.
- `brand/src/design-system/tokens.css` — where each font is loaded and named.
