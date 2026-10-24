# MEDIA-BUSINESS.md — grill-with-docs, media business mode

Where a business's media decisions are written: the homes this kind of work adds to the table in
`SKILL.md`, and the media procedure whose steps record a piece's brief.

## Paths and unit

- **Unit:** one piece, a social short, an explainer or a recorded talk. **Brief:**
  `scripts/src/pieces/<piece>/brief.md`, in the shape `scripts/docs/reference/the-piece-ladder.md`
  gives it; its settled positions go under `## Key points` and its draft notes under `## Notes`.
- **Planning procedure:** `scripts/workflows/01-brief-a-piece/`: questioning in steps 3 to 7, the
  brief and M1 in steps 8 and 9, recording in step 10. The brand kit and the spoken voice are
  recorded by `brand/workflows/01-set-up-the-brand-kit/` and
  `brand/workflows/05-write-the-spoken-voice/`.
- **Memory:** `.claude/MEMORY.md`, through the gate in
  `.claude/rules/syntek-media/08-naming-and-memory.md` Section 3, in the form of its Section 4.

## Additions to the steps

- **Step 1 — also read the media homes below** that the subject touches, so a decision they
  already hold opens the round as a `Settled` line.
- **Step 3 — also record in the media homes:**

| When a decision… | Record it in |
|---|---|
| sets a piece's kind, origin, deliverables, voice, visuals or music | the brief's frontmatter, in the guide's vocabulary |
| settles its purpose, viewer, hook, key points, call to action, disclosure plan or rights needs | the brief's section of that name |
| names a narrator, a voice, a model or a pronunciation | `brand/src/voice/voice.md` |
| sets a token or a layout | `brand/src/design-system/`, with its row in `brand/src/design-register.md` |
| sets what one platform carries, where no social media plan owns it | that platform's profile in `brand/src/platforms/` |
| confirms a platform limit that differs from the data | an `[[override]]` in `brand/src/platforms/overrides.toml` |
| needs a licence, a permission, a release or a consent | a `needed` row in `production/src/rights-register.md` |
| dates a planned post | `publishing/src/schedule.md` |
| changes the brand's name, kind, platforms or media kinds | no file: an update with the new answer (`.claude/rules/syntek-media/06-global-rules.md` Section 11) |

- **Step 6 — also date M1 only on the author's agreement**, in the brief's `verified`, with its
  `status` set to `briefed`, as `scripts/workflows/01-brief-a-piece/` step 9 says.

## Domain rules

- **A client's facts:** syntek-author's client facts, where present, at the path its project
  settings give; otherwise where `.claude/rules/syntek-media/08-naming-and-memory.md` Section 2
  puts a fact.
- **A decision the social media plan owns:** the social-media-documents skill (syntek-author),
  where present (`.claude/rules/syntek-media/02-skills.md` Section 4).
- **A platform value:** `.claude/rules/syntek-media/03-production-ethics.md` Sections 7 and 8.

## Examples

A decision that passed the gate, as Harbour Lane Studio's `MEMORY.md` would hold it:

```markdown
- **24/10/2026** — **Explainers end on the booking page, never a phone number.** A number on
  screen goes stale in every reposted clip; the booking page can change behind its link.
  Rejected: a number in the description only, because shorts are watched without it.
```

A decision that failed the gate, in its narrower home, the brief's `## Notes`:

```markdown
- The author declined a second call to action: one ask per piece (24/10/2026).
```
