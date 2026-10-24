# MEDIA-FICTION.md — grill-with-docs, media fiction mode

Where a novelist's media decisions are written: the homes this kind of work adds to the table in
`SKILL.md`, and the media procedure whose steps record a piece's brief.

## Paths and unit

- **Unit:** one piece, a trailer, a teaser short, a reading or an author-to-camera clip.
  **Brief:** `scripts/src/pieces/<piece>/brief.md`, in the shape
  `scripts/docs/reference/the-piece-ladder.md` gives it; its settled positions go under
  `## Key points` and its draft notes, the reveal line among them, under `## Notes`.
- **Planning procedure:** `scripts/workflows/01-brief-a-piece/`: questioning in steps 3 to 7, the
  brief and M1 in steps 8 and 9, recording in step 10. The brand kit and the spoken voice are
  recorded by `brand/workflows/01-set-up-the-brand-kit/` and
  `brand/workflows/05-write-the-spoken-voice/`.
- **Memory:** `.claude/MEMORY.md`, through the gate in
  `.claude/rules/syntek-media/08-naming-and-memory.md` Section 3, in the form of its Section 4.

## Additions to the steps

- **Step 1 — also read the media homes below** that the subject touches, and the book's own
  record of a name (syntek-author's names register, where present), so a decision already held
  opens the round as a `Settled` line.
- **Step 3 — also record in the media homes:**

| When a decision… | Record it in |
|---|---|
| sets a piece's kind, origin, deliverables, voice, visuals or music | the brief's frontmatter, in the guide's vocabulary |
| settles its purpose, viewer, hook, key points, call to action, disclosure plan or rights needs | the brief's section of that name |
| sets how far the piece may reveal | the brief's `## Notes`, as its reveal line |
| casts a narrator or a character's voice, or settles how a name is said | `brand/src/voice/voice.md` (a `character:<name>` row for each voice) |
| sets a token, the cover's use or a layout | `brand/src/design-system/`, with its row in `brand/src/design-register.md` |
| sets what one platform carries | that platform's profile in `brand/src/platforms/` |
| needs a licence, a permission, a release or a consent | a `needed` row in `production/src/rights-register.md` |
| dates a planned post, such as a launch-day teaser | `publishing/src/schedule.md` |
| changes the brand's name, kind, platforms or media kinds | no file: an update with the new answer (`.claude/rules/syntek-media/06-global-rules.md` Section 11) |

- **Step 6 — also date M1 only on the author's agreement**, in the brief's `verified`, with its
  `status` set to `briefed`, as `scripts/workflows/01-brief-a-piece/` step 9 says.

## Domain rules

- **The book's facts** (a name, a date, a rule of the world): the book, or syntek-author's story
  bible, where present; `.claude/rules/syntek-media/03-production-ethics.md` Sections 7 and 9.
- **A spoken pronunciation:** `brand/docs/reference/the-spoken-voice.md`, and the pronounce skill
  (syntek-author), where present (`.claude/rules/syntek-media/02-skills.md` Section 4).
- **A designed character voice's disclosure:**
  `.claude/rules/syntek-media/03-production-ethics.md` Section 5.

## Examples

A decision that passed the gate, as Morgan Example's `MEMORY.md` would hold it:

```markdown
- **24/10/2026** — **No trailer reveals past chapter three before the launch.** A reveal
  reposted from one teaser spoils every later one. Rejected: a per-piece reveal line, because
  clips travel without their captions.
```

A decision that failed the gate, in its narrower home, the brief's `## Notes`:

```markdown
- Reveal line: nothing past chapter three (24/10/2026).
```
