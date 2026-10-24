# MEDIA-NONFICTION.md — grill-with-docs, media non-fiction mode

Where a non-fiction author's media decisions are written: the homes this kind of work adds to
the table in `SKILL.md`, and the media procedure whose steps record a piece's brief.

## Paths and unit

- **Unit:** one piece, a teaching clip, a recorded talk or a podcast episode. **Brief:**
  `scripts/src/pieces/<piece>/brief.md`, in the shape `scripts/docs/reference/the-piece-ladder.md`
  gives it; its settled positions, the claims the piece commits to, go under `## Key points` and
  its draft notes under `## Notes`.
- **Planning procedure:** `scripts/workflows/01-brief-a-piece/`: questioning in steps 3 to 7, the
  brief and M1 in steps 8 and 9, recording in step 10. The brand kit and the spoken voice are
  recorded by `brand/workflows/01-set-up-the-brand-kit/` and
  `brand/workflows/05-write-the-spoken-voice/`.
- **Memory:** `.claude/MEMORY.md`, through the gate in
  `.claude/rules/syntek-media/08-naming-and-memory.md` Section 3, in the form of its Section 4.

## Additions to the steps

- **Step 1 — also read the media homes below** that the subject touches, and the chapter the
  piece draws on (the brief's `source`), so a decision already held opens the round as a
  `Settled` line.
- **Step 3 — also record in the media homes:**

| When a decision… | Record it in |
|---|---|
| sets a piece's kind, origin, deliverables, voice, visuals or music | the brief's frontmatter, in the guide's vocabulary |
| settles its purpose, listener, hook, key points, call to action, disclosure plan or rights needs | the brief's section of that name |
| chooses a translation or a quotation | the brief's `## Draws on`, and a `needed` row in `production/src/rights-register.md` |
| names a narrator, a voice or how a name or borrowed word is said | `brand/src/voice/voice.md` |
| sets a token or a layout | `brand/src/design-system/`, with its row in `brand/src/design-register.md` |
| sets what one platform carries | that platform's profile in `brand/src/platforms/` |
| needs a guest's or an audience's consent | a `needed` row in `production/src/rights-register.md` |
| dates a planned post or episode | `publishing/src/schedule.md` |
| changes the brand's name, kind, platforms or media kinds | no file: an update with the new answer (`.claude/rules/syntek-media/06-global-rules.md` Section 11) |

- **Step 6 — also date M1 only on the author's agreement**, in the brief's `verified`, with its
  `status` set to `briefed`, as `scripts/workflows/01-brief-a-piece/` step 9 says.

## Domain rules

- **Whether a claim is true:** the fact-check skill (syntek-author), where present, or a named
  source; `.claude/rules/syntek-media/03-production-ethics.md` Sections 1 and 7.
- **The book's argument:** the chapter the brief's `source` names;
  `.claude/rules/syntek-media/03-production-ethics.md` Section 9.
- **A translation or a quotation:** `production/workflows/07-clear-the-rights/`, under
  `.claude/rules/syntek-media/03-production-ethics.md` Sections 6 and 9.

## Examples

A decision that passed the gate, as Robin Example's `MEMORY.md` would hold it:

```markdown
- **24/10/2026** — **Teaching clips quote the project's default translation only.** One
  translation keeps every card's permission row the same. Rejected: the best rendering per
  passage, because each needs its own video permission.
```

A decision that failed the gate, in its narrower home, the brief's `## Draws on`:

```markdown
- The chapter on hospitality, the passage in the default translation (24/10/2026).
```
