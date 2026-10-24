# MEDIA-FICTION.md — handoff, media fiction mode

What a novelist's media handoff must never drop: whatever has cost credits, is mid-render, is
approved and not yet archived or posted, or is promised for a launch, and every line that would
reveal past what the book allows.

## Paths and unit

- **Unit:** one piece, a trailer, a teaser short, a reading or an author-to-camera clip, in
  `scripts/src/pieces/<piece>/`, with its brief, its script and its storyboard; or, where the
  project makes audiobooks, a chapter of the audiobook, by its row in the chapter register.
- **The rule:** `.claude/rules/syntek-media/07-session-boundaries.md`; the folder and filename it
  gives (Section 2), and its list of what never drops (Section 3).
- **Anchors** for in-flight work point into the script, the storyboard, the edit decision list in
  `production/src/edits/`, the segment register in `production/src/voiceover/`, the brief's
  `verified`, or a row of a register or log.

## Additions to the steps

- **Step 1 — also** record a character's voice or a name's pronunciation settled this session in
  `brand/src/voice/voice.md`, a spend in `production/src/credits-log.md`, and a right or consent
  in `production/src/rights-register.md`, before writing the handoff.
- **Step 4 — also** give each piece touched its status and the gate it stands at, and say which
  take, master or cut is live and which is superseded, by its register row, never by listing an
  output folder (`.claude/rules/syntek-media/06-global-rules.md` Section 12).
- **Step 5 — also carry what is spent, running or unpublished.** The part is headed
  `## Media in flight` and lists, each with its path and what blocks it, every item of
  `.claude/rules/syntek-media/07-session-boundaries.md` Section 3, and also:
  - every piece's reveal line, where a line in flight comes near it;
  - every audiobook chapter approved and not yet archived, where the project makes audiobooks;
  - every launch-date post, with its date.
- **Step 6 — also** name `run-media-workflow` and the procedure by its full folder name.
- **Step 8 — also** never paste a voice ID, a key or a narrator's personal details, and never
  quote an unpublished chapter: name and locate it.

## Domain rules

- **What a media handoff never drops:** `.claude/rules/syntek-media/07-session-boundaries.md`
  Section 3.
- **Spends:** `production/src/credits-log.md`, under
  `.claude/rules/syntek-media/03-production-ethics.md` Section 4.
- **A spoiler risk:** `.claude/rules/syntek-media/03-production-ethics.md` Sections 1 and 9; the
  handoff names it and the author decides.

## Examples

```markdown
## Media in flight

- Credits: the teaser's three character lines designed and taken
  (production/src/voiceover/<piece>.toml, segments 02 to 04); the narrator's line agreed, not made.
- Not archived: segment 03's approved take (its register row, archived empty).
- Reveal: beat 4 names the keeper; the brief's reveal line is chapter three. Author to decide.
- Scheduled: the teaser, launch morning, on the platforms its brief names.
```
