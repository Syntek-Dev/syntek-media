# MEDIA-FICTION.md — grilling, media fiction mode

The domain for grilling a novelist's media work: a trailer's or a teaser's brief, the brand kit,
the spoken voice and its character voices, and a platform's profile, before any of it is
scripted, voiced or cut. It names the media procedure each pass belongs to; the round shape stays
in `SKILL.md`.

## Paths and unit

- **Unit:** one piece, a trailer, a teaser short, a reading or an author-to-camera clip, in
  `scripts/src/pieces/NNN-kebab-title/`, whose brief is `scripts/src/pieces/<piece>/brief.md`; or,
  for work across the brand, the brand kit, the spoken voice or one platform's profile.
- **Procedures that open with a grilling pass:** `scripts/workflows/01-brief-a-piece/` (steps 3
  to 7), `brand/workflows/01-set-up-the-brand-kit/` (step 1) and
  `brand/workflows/05-write-the-spoken-voice/` (step 1). Each one's `STEPS.md` governs the pass,
  against its `CHECKLIST.md`.
- **Lookup order (step 1):** `.claude/MEMORY.md` → the target folder's `CONTEXT.md`, then its
  `CLAUDE.md` → the piece's brief and `scripts/src/piece-register.md` →
  `brand/src/voice/voice.md` (the narrator and every `character:<name>` row) and
  `brand/src/design-system/tokens.css` → `production/src/rights-register.md` → the platform data,
  by key, through `python3 toolkit/media.py presets` → syntek-author's story bible, names register
  and promoted chapters (under world/src/ and manuscript/src/), where present, read and never
  edited.
- **Guides:** `scripts/docs/reference/the-piece-ladder.md` (what a brief settles, and M1),
  `brand/docs/reference/the-brand-kit.md` and `brand/docs/reference/the-spoken-voice.md`.

## Additions to the steps

- **Step 1 — the reveal line opens the first round alone.** How far into the book a piece may
  reveal gates its hook, its key points and every line it quotes; ask it first where the brief's
  `## Notes` do not already settle it.
- **Step 1 — also wire media's blocking order.** Then the purpose and the viewer before the hook;
  the kind and origin before the deliverables; the voices, visuals and music before the
  disclosure plan; the rights needs before a storyboard.
- **Step 1 — also look up every name.** A character's or place's name, and a constructed word,
  comes from the book or the names register, where present, never from the author's memory in
  the session; a platform's limit comes from the data by key.
- **Step 4 — also name the spend and the voices.** Where the design implies a synthetic character
  voice or a voiceover, the summary says so, unpriced; the cost is agreed in the procedure that
  makes the call (`.claude/rules/syntek-media/03-production-ethics.md` Section 4).

## Domain rules

| Surface | The decisions it turns on |
|---|---|
| A piece's brief | the reveal line; the book's question the piece sells; the hook image; the kind and origin; the deliverables; the call to action (a pre-order, a first chapter, a launch date); the disclosure plan; the rights needs |
| The brand kit | the cover and the series look; the thumbnail and title-card layouts |
| The spoken voice | the narrator; each character voiced, and whether that voice is human or designed; how every name is said |
| A platform's profile | the deliverables used there, and what an author's channel posts between launches |

- **The reveal line:** `.claude/rules/syntek-media/03-production-ethics.md` Section 9, and step 2
  and the Domain rules of `.claude/skills/write-script/FICTION.md`; a decision that would cross it
  goes back to the author (Section 1).
- **A blurb, a review quote or an endorsement:**
  `.claude/rules/syntek-media/03-production-ethics.md` Sections 6 and 7.
- **A cloned, designed or remixed voice:** `.claude/rules/syntek-media/03-production-ethics.md`
  Sections 5 and 6.

## Examples

Morgan Example briefs a teaser for an invented novel:

```text
**Settled — Reveal line:** nothing past chapter three (the brief's Notes)
**Settled — Narrator:** the author, recorded (brand/src/voice/voice.md)

**Q1 — The hook**

1. **The lighthouse going dark** — one image from chapter one; asks the book's question
2. **The first line, read aloud** — the book's own voice; slower on a muted feed
3. **The map** — shows the world; says nothing about what is at stake

**Recommendation: 1** — it carries the question in a picture and works with the sound off.
```

Held for the next round: the character voices, because the hook decides who speaks.
