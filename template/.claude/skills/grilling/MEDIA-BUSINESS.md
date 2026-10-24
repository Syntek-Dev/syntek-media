# MEDIA-BUSINESS.md — grilling, media business mode

The domain for grilling a business's media work: a piece's brief, the brand kit, the spoken voice
and a platform's profile, before any of it is scripted, voiced or cut. It names the media
procedure each pass belongs to; the round shape stays in `SKILL.md`.

## Paths and unit

- **Unit:** one piece, a social short, an explainer or a recorded talk, in
  `scripts/src/pieces/NNN-kebab-title/`, whose brief is `scripts/src/pieces/<piece>/brief.md`; or,
  for work across the brand, the brand kit, the spoken voice or one platform's profile.
- **Procedures that open with a grilling pass:** `scripts/workflows/01-brief-a-piece/` (steps 3
  to 7), `brand/workflows/01-set-up-the-brand-kit/` (step 1) and
  `brand/workflows/05-write-the-spoken-voice/` (step 1). Each one's `STEPS.md` governs the pass,
  against its `CHECKLIST.md`.
- **Lookup order (step 1):** `.claude/MEMORY.md` → the target folder's `CONTEXT.md`, then its
  `CLAUDE.md` → the piece's brief and `scripts/src/piece-register.md` →
  `brand/src/voice/voice.md`, `brand/src/design-system/tokens.css` and the profiles in
  `brand/src/platforms/` → `production/src/rights-register.md` → the platform data, by key,
  through `python3 toolkit/media.py presets` → syntek-author's brand guide, written voice, social
  media plan and content calendar, where present, read and never restated.
- **Guides:** `scripts/docs/reference/the-piece-ladder.md` (what a brief settles, and M1),
  `brand/docs/reference/the-brand-kit.md` and `brand/docs/reference/the-spoken-voice.md`.

## Additions to the steps

- **Step 1 — also wire media's blocking order.** The purpose and the viewer come before the hook;
  the kind and origin before the deliverables; the deliverables before any platform's limits; the
  voice, visuals and music before the disclosure plan; the rights needs before a storyboard.
- **Step 1 — also look up what the files hold.** A platform's limit comes from the data by key,
  never from the author or from memory (`.claude/rules/syntek-media/03-production-ethics.md`
  Section 7); a narrator from `voice.md`; another piece's status from its brief.
- **Step 1 — also set aside the business's facts.** A client's name, a result, a figure or a
  testimonial on screen is not a question for a round:
  `.claude/rules/syntek-media/03-production-ethics.md` Sections 7 and 9 govern it.
- **Step 4 — also name the spend.** Where the settled design implies a credit-spending call (a
  voiceover, speech-to-text), the summary says so, unpriced: the cost is stated and agreed in the
  procedure that makes the call (`.claude/rules/syntek-media/03-production-ethics.md` Section 4).

## Domain rules

| Surface | The decisions it turns on |
|---|---|
| A piece's brief | its one job and its viewer; the hook; kind and origin; the deliverables; the key points; the call to action; the disclosure plan; the rights needs |
| The brand kit | the tokens every layout reads; the thumbnail and title-card layouts; what syntek-author's brand guide already settles, where present |
| The spoken voice | the narrator for each use; the pace; how the brand's name is said; the words never said aloud |
| A platform's profile | the deliverables used there; what the social media plan already sets, where present |

- **A claim on screen** (a result, a figure, a testimonial, a client named or shown):
  `.claude/rules/syntek-media/03-production-ethics.md` Sections 6, 7 and 9.
- **Cadence, tone and hashtags:** the plan of the social-media-documents skill (syntek-author),
  where present (`.claude/rules/syntek-media/02-skills.md` Section 4).

## Examples

Harbour Lane Studio briefs an explainer on pricing a job:

```text
**Settled — Viewer:** a tradesperson pricing a first job (the brand brief's audience test)
**Settled — Narrator:** the owner, recorded, no synthetic voice (brand/src/voice/voice.md)

**Q1 — The hook**

1. **The mistake on screen** — the wrong quote, then the line that fixes it; concrete and fast
2. **The question** — 'what does a job really cost?'; broad, and slower to land
3. **The result** — a client's saving; needs the client's permission first

**Recommendation: 1** — it shows the point in the first seconds and needs no permission.
```

Held for the next round: the deliverables, because the hook decides whether a vertical cut works.
