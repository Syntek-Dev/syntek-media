@./CONTEXT.md

# CLAUDE.md — brand/src/design-system/fonts/

Read order: `.claude/CLAUDE.md` → `.claude/MEMORY.md` → `brand/CONTEXT.md` → `brand/CLAUDE.md`
→ `brand/src/CONTEXT.md` → `brand/src/CLAUDE.md` → `brand/src/design-system/CONTEXT.md` →
`brand/src/design-system/CLAUDE.md` → this folder's `CONTEXT.md` (imported above) → this file.

## Purpose (one line)

Hold the brand's licensed font files where every renderer can load them offline.

## How to work here

- **Routing:** workflow `brand/workflows/01-set-up-the-brand-kit/`; guide
  `brand/docs/reference/the-brand-kit.md`; licence rows through
  `production/workflows/07-clear-the-rights/`.
- **Model:** **Opus** for reading a licence and judging whether it covers video; the mechanical
  tier for adding the file and its font-face rule
  (`.claude/rules/syntek-media/05-model-allocation.md`).
- **Concrete steps:** the author supplies the file and its licence → a `font` row in
  `production/src/rights-register.md` → the file here, renamed `<family>-<weight>.<ext>` → a
  font-face rule in `tokens.css` → the family named in its token →
  `python3 toolkit/media.py tokens` and `uv run toolkit/card.py check` on a card that uses it.
- **Definition of done:** the font loads in `card.py check`, its licence row exists, and a burned
  caption in it reports no font fallback.

## Guardrails

- **No font without its licence.** A licence for print or the desktop does not always cover
  video, thumbnails or embedding; read it, and record what it allows in the rights row. Never
  assume.
- **Never fetch a font over the network.** Every face is a file here; `card.py` aborts every
  http(s) request.
- **Never rename or remove a font a piece's copied card or thumbnail still names** without
  telling the author which pieces it would change.
- **A font file over 10 MB is a question for the author.** `media.py check` flags any file that
  large outside the LFS folder; ask before adding one, and prefer a subset of the face.

## Output & naming

- **Hand-written (by the author):** `<family>-<weight>.<ext>`, kebab-case (`.woff2`, `.otf` or
  `.ttf`).
- **Generated (never hand-edit):** nothing here.
