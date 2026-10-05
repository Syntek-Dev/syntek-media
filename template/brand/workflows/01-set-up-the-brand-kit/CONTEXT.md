# CONTEXT.md — brand/workflows/01-set-up-the-brand-kit/

The procedure for settling the brand kit with the author: the screen colours, the display and
body faces and their fonts, the spacing, the burned-caption style, and the brand's two layout
components, the thumbnail and the title card. It opens with a grilling pass, reads
syntek-author's brand guide first where it is present, and ends with every token checked by the
toolkit and a proof of each layout approved. It changes no piece: a thumbnail or card already
copied keeps the layout it was made with.

## Directory Tree

```text
brand/workflows/01-set-up-the-brand-kit/
├── CHECKLIST.md        ← model-tagged checklist; tick it as you go
├── CLAUDE.md           ← operating rules for this procedure
├── CONTEXT.md          ← this file: when to use it, what it produces
└── STEPS.md            ← the ordered steps, each naming its skill and guide
```

## When to use this

- A new project, before the first thumbnail, card or burned caption is made.
- The brand changes a colour, a face, the caption style or a layout.
- A font is added, replaced or found to lack a licence for video.
- `python3 toolkit/media.py tokens` or `uv run toolkit/card.py check` fails.

Reach for a **different** procedure when a component is to be brought across from or to Claude
Design (`brand/workflows/02-sync-with-claude-design/`), an exported asset is to be filed
(`brand/workflows/03-record-a-design-export/`), or one piece's thumbnail is being briefed
(`publishing/workflows/04-brief-a-thumbnail/`).

## What it produces, and where

- **`brand/src/design-system/tokens.css`**, every required token decided by the author and each
  group's flag removed.
- **Font files** in `brand/src/design-system/fonts/`, each with a `font` row in
  `production/src/rights-register.md`.
- **The two layouts**, `brand/src/design-system/previews/thumbnail.html` and
  `brand/src/design-system/previews/card.html`, adapted and approved in proof.
- **Proofs** in the git-ignored `production/src/renders/proofs/brand-kit-DD-MM-YYYY/`, and the
  decisions dated in `.claude/MEMORY.md`.

## The failure this procedure exists to prevent

A brand improvised piece by piece: a colour typed into one thumbnail, a caption face only one
machine has, a title card nobody approved. Every piece then looks slightly different, the next
change has to be made file by file, and a font with no licence for video reaches a published
video. Settled once, checked by the toolkit and approved in a proof, the kit makes every later
piece the brand's without anyone having to remember it.

## Cross-references

- `brand/docs/reference/the-brand-kit.md` — the required tokens, fonts and the two layouts.
- `brand/src/design-system/` — the kit itself, with the layout contract in its previews pair.
- `toolkit/templates/` — the fallback layouts the brand's own replace.
