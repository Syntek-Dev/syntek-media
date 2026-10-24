# MEDIA-NONFICTION.md — grilling, media non-fiction mode

The domain for grilling a non-fiction author's media work: a talk's, a teaching clip's or an
episode's brief, the brand kit, the spoken voice and a platform's profile, before any of it is
scripted, voiced or cut. It names the media procedure each pass belongs to; the round shape stays
in `SKILL.md`.

## Paths and unit

- **Unit:** one piece, a teaching clip, a recorded talk or a podcast episode, in
  `scripts/src/pieces/NNN-kebab-title/`, whose brief is `scripts/src/pieces/<piece>/brief.md`; or,
  for work across the brand, the brand kit, the spoken voice or one platform's profile.
- **Procedures that open with a grilling pass:** `scripts/workflows/01-brief-a-piece/` (steps 3
  to 7), `brand/workflows/01-set-up-the-brand-kit/` (step 1) and
  `brand/workflows/05-write-the-spoken-voice/` (step 1). Each one's `STEPS.md` governs the pass,
  against its `CHECKLIST.md`.
- **Lookup order (step 1):** `.claude/MEMORY.md` → the target folder's `CONTEXT.md`, then its
  `CLAUDE.md` → the piece's brief and `scripts/src/piece-register.md` →
  `brand/src/voice/voice.md` and `brand/src/design-system/tokens.css` →
  `production/src/rights-register.md` (every quotation and translation) → the platform data, by
  key, through `python3 toolkit/media.py presets` → syntek-author's promoted chapters, argument
  maps and evidence verdicts (under manuscript/src/, planning/src/ and research/src/), where
  present, read and never edited.
- **Guides:** `scripts/docs/reference/the-piece-ladder.md` (what a brief settles, and M1),
  `brand/docs/reference/the-brand-kit.md` and `brand/docs/reference/the-spoken-voice.md`.

## Additions to the steps

- **Step 1 — the one claim opens the first round alone.** What the piece argues, in one
  sentence, and the chapter or source it comes from, gates the hook, the key points and every
  quotation; ask it first where the brief does not already hold it.
- **Step 1 — also wire media's blocking order.** Then the purpose and the listener before the
  hook; the kind and origin before the deliverables; the quotations and the translation before
  the rights needs; the voice, visuals and music before the disclosure plan.
- **Step 1 — also set aside every claim's evidence.** Whether a claim is true is a fact for the
  fact-check skill (syntek-author), where present, or a named source, never a question for the
  author in a round.
- **Step 4 — also name the spend and the guests.** Where the design implies a voiceover or
  speech-to-text, the summary says so, unpriced; where a guest, a co-host or an audience appears,
  it names the consent each needs (`.claude/rules/syntek-media/03-production-ethics.md`
  Sections 4 and 6).

## Domain rules

| Surface | The decisions it turns on |
|---|---|
| A piece's brief | the one claim and its source; the listener and what they already know; the hook; the kind and origin; the quotations and the translation each uses; the call to action; the disclosure plan; the rights needs |
| The brand kit | the book's cover and the teaching look; the card layout a quotation sits on |
| The spoken voice | the narrator; the pace for teaching; how names and borrowed words are said; how scripture or a quotation is read aloud |
| A platform's profile | the deliverables used there, and what an author's channel posts between books |

- **A reading beside its source, and a quotation in its context:**
  `.claude/rules/syntek-media/03-production-ethics.md` Section 9, and the Domain rules of
  `.claude/skills/write-script/NONFICTION.md`.
- **A quotation's or a translation's permissions**, for print, audio and video apart:
  `.claude/rules/syntek-media/03-production-ethics.md` Sections 6 and 9.

## Examples

Robin Example briefs a teaching clip from a chapter of the book:

```text
**Settled — Claim:** an open table is harder than a closed one (the brief's Key points)
**Settled — Translation:** the project's default, permission recorded (production/src/rights-register.md)

**Q1 — The hook**

1. **The question to camera** — 'why is an open table harder?'; direct, and it frames the claim
2. **The passage on a card** — the text first; slower, and needs the card's permission row
3. **A story from the chapter** — warm; takes twenty seconds to reach the point

**Recommendation: 1** — it states the claim in the first line and needs no new permission.
```

Held for the next round: the card, because the hook decides whether the passage is shown.
