# MEDIA-BUSINESS.md — handoff, media business mode

What a business's media handoff must never drop: whatever has cost credits, is mid-render, is
approved and not yet archived or posted, or is promised to a client or a platform by a date.

## Paths and unit

- **Unit:** one piece, a social short, an explainer or a recorded talk, in
  `scripts/src/pieces/<piece>/`, with its brief, its script or transcript and its storyboard.
- **The rule:** `.claude/rules/syntek-media/07-session-boundaries.md`; the folder and filename it
  gives (Section 2), and its list of what never drops (Section 3).
- **Anchors** for in-flight work point into the script or transcript, the storyboard, the edit
  decision list in `production/src/edits/`, the segment register in `production/src/voiceover/`,
  the brief's `verified`, or a row of a register or log.

## Additions to the steps

- **Step 1 — also** record a narrator, a voice or a pronunciation settled this session in
  `brand/src/voice/voice.md`, a spend in `production/src/credits-log.md`, and a right or consent
  in `production/src/rights-register.md`, before writing the handoff.
- **Step 4 — also** give each piece touched its status and the gate it stands at, and say which
  take, master or cut is live and which is superseded, by its register row, never by listing an
  output folder (`.claude/rules/syntek-media/06-global-rules.md` Section 12).
- **Step 5 — also carry what is spent, running or unpublished.** The part is headed
  `## Media in flight` and lists, each with its path and what blocks it, every item of
  `.claude/rules/syntek-media/07-session-boundaries.md` Section 3, and also:
  - every client approval awaited, with the deliverable it holds back;
  - every rights row still `needed` for a piece due to post.
- **Step 6 — also** name `run-media-workflow` and the procedure by its full folder name.
- **Step 8 — also** never paste a voice ID, a key, a client's contact details or a release form's
  personal details; name and locate them.

## Domain rules

- **What a media handoff never drops:** `.claude/rules/syntek-media/07-session-boundaries.md`
  Section 3.
- **Spends:** `production/src/credits-log.md`, under
  `.claude/rules/syntek-media/03-production-ethics.md` Section 4.
- **Client approvals and open rights:** the brief's `verified` and
  `production/src/rights-register.md` (`.claude/rules/syntek-media/03-production-ethics.md`
  Sections 1 and 6).

## Examples

```markdown
## Media in flight

- Credits: two of five voiceover segments taken for the pricing explainer
  (production/src/voiceover/<piece>.toml, segments 01 and 02); three more agreed, not made.
- Rendering: the master, assemble run, not yet probed (production/src/edits/<piece>.toml).
- Not archived: segment 01's approved take (its register row, archived empty).
- Awaiting approval: the client's sign-off on the testimonial line; the vertical cut waits on it.
- Scheduled: the explainer, Thursday 09:00, on the platforms its brief names.
```
