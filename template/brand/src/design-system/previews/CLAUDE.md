@./CONTEXT.md

# CLAUDE.md — brand/src/design-system/previews/

Read order: `.claude/CLAUDE.md` → `.claude/MEMORY.md` → `brand/CONTEXT.md` → `brand/CLAUDE.md`
→ `brand/src/CONTEXT.md` → `brand/src/CLAUDE.md` → `brand/src/design-system/CONTEXT.md` →
`brand/src/design-system/CLAUDE.md` → this folder's `CONTEXT.md` (imported above) → this file.

## Purpose (one line)

Show the kit to Claude Design one card at a time, and hold the two layouts every thumbnail and
card is copied from.

## How to work here

- **Routing:** workflow `brand/workflows/01-set-up-the-brand-kit/` to change a card;
  `brand/workflows/02-sync-with-claude-design/` to bring one across; guide
  `brand/docs/reference/the-brand-kit.md`.
- **Model:** **Opus** for a layout change and for judging its proof; the mechanical tier for
  `card.py check` (`.claude/rules/syntek-media/05-model-allocation.md`).
- **Concrete steps:** change one card with the author → `uv run toolkit/card.py check` on it →
  for a layout, render a proof at a landscape and a vertical size with
  `uv run toolkit/card.py render` (`--size`, and `-o` naming a file in the git-ignored
  `production/src/renders/proofs/<what>-DD-MM-YYYY/`) → the author approves → commit.
- **Definition of done:** the card passes `card.py check`, its line 1 is its `@dsCard` comment,
  and the author has approved a proof of any layout change.

## Guardrails

- **Line 1 is the `@dsCard` comment, always.** Nothing goes above it, not even the doctype.
- **The layout contract binds `thumbnail.html` and `card.html`:** `<!doctype html>` and
  `<html lang="en-GB">`; a stylesheet link to `../tokens.css` and nothing over the network;
  `html, body { margin: 0; width: 100vw; height: 100vh; overflow: hidden }`; one file for every
  aspect ratio, through `aspect-ratio` media queries; text inside `--safe-top`, `--safe-right`,
  `--safe-bottom` and `--safe-left`, which the renderer sets with `--frame-width` and
  `--frame-height`; images by relative path; `card.html` leaves its background transparent so it
  can overlay a picture.
- **Tokens only.** A card names `var(--…)` for every colour, face, weight, space and radius;
  a value typed into a card is a value Claude Design and the toolkit cannot change for you.
- **Placeholder words stay placeholders.** The words in the layouts are replaced per piece by the
  skill that copies them; never write a real title or claim into the brand's layout.
- **Never overwrite** a card without confirming with the author.

## Output & naming

- **Hand-written (with the author):** the seven cards, their names fixed: `colors.html`,
  `type.html`, `spacing.html`, `brand.html`, `captions.html`, `thumbnail.html`, `card.html`. A
  card the brand adds takes a kebab-case name and its own `@dsCard` line.
- **Copied by skills:** `thumbnail.html` to `publishing/src/thumbnails/<piece>[--cNN].html`;
  `card.html` to `production/src/cards/<piece>.<card>.html`.
- **Generated (never hand-edit):** nothing here.
