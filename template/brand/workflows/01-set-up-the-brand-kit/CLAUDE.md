@./CONTEXT.md

# CLAUDE.md — brand/workflows/01-set-up-the-brand-kit/

Read order: `.claude/CLAUDE.md` → `.claude/MEMORY.md` → `brand/CONTEXT.md` → `brand/CLAUDE.md`
→ `brand/workflows/CONTEXT.md` → `brand/workflows/CLAUDE.md` → this folder's `CONTEXT.md`
(imported above) → this file → `STEPS.md` (with `CHECKLIST.md` open).

## Purpose (one line)

Settle every token and both layouts with the author once, check them with the toolkit and
approve them in proof, so that no piece improvises the brand.

## How to work here

- **Routing:** no media skill runs this procedure; it opens with the grill-with-docs skill
  (syntek-author), where present, or the same questions in rounds. Guide
  `brand/docs/reference/the-brand-kit.md`; checks `python3 toolkit/media.py tokens` and
  `uv run toolkit/card.py check`; proofs `uv run toolkit/card.py render`.
- **Model:** **Opus** for every question, recommendation and judgement of a proof; the mechanical
  tier for running the checks and writing values the author has decided
  (`.claude/rules/syntek-media/05-model-allocation.md`). The checklist tags are authoritative.
- **Concrete steps:** follow `STEPS.md` in order and tick `CHECKLIST.md` as you go: grill the kit
  → reconcile with the written brand → colours → type and fonts → space → captions → check the
  tokens → adapt the two layouts → check every card and render proofs → record → hand back.
- **Definition of done:** `media.py tokens` and `card.py check` pass; the author has approved a
  landscape and a vertical proof of each layout and a proof of the captions card; no
  `AUTHOR TO CONFIRM` slot is left in `tokens.css` or the two layouts; the decisions are dated in
  `.claude/MEMORY.md`.

## Guardrails

- **The author decides every value.** Offer options with one recommendation and say why; never
  set a colour, a face or a layout because it seemed obvious.
- **Read the written brand first.** Where syntek-author's brand guide is present, its palette and
  faces are the starting point; a difference on screen is the author's decision, recorded.
- **No font without its licence.** A face enters the fonts folder only with a `font` row in the
  rights register saying what its licence allows; a generic family stands in until then.
- **Tokens, never values, in a layout.** A colour or a size typed into a card is one the next
  brand change will miss.
- **Line 1 of every card stays its `@dsCard` comment.** Claude Design reads nothing else.
- **Never overwrite** `tokens.css` or a card without confirming with the author, and never touch
  a piece's copied thumbnail or card from here.

## Output & naming

- **Produces:** the decided `tokens.css`; the brand's fonts; the adapted `thumbnail.html` and
  `card.html`.
- **Also writes:** a `font` row per licence in `production/src/rights-register.md`; dated
  decisions in `.claude/MEMORY.md`; proofs in the git-ignored `production/src/renders/`.
- **Does not touch:** any piece's thumbnail or card, `toolkit/templates/`, or the Claude Design
  project (that is `brand/workflows/02-sync-with-claude-design/`).
