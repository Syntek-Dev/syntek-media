# MEDIA-NONFICTION.md — handoff, media non-fiction mode

What a non-fiction author's media handoff must never drop: whatever has cost credits, is
mid-render, is approved and not yet archived or posted, and every quotation or guest whose
permission is still open.

## Paths and unit

- **Unit:** one piece, a teaching clip, a recorded talk or a podcast episode, in
  `scripts/src/pieces/<piece>/`, with its brief, its script or transcript and its storyboard; or,
  where the project makes audiobooks, a chapter of the audiobook, by its row in the chapter
  register.
- **The rule:** `.claude/rules/syntek-media/07-session-boundaries.md`; the folder and filename it
  gives (Section 2), and its list of what never drops (Section 3).
- **Anchors** for in-flight work point into the script or transcript, the storyboard, the edit
  decision list in `production/src/edits/`, the segment register in `production/src/voiceover/`,
  the brief's `verified`, or a row of a register or log.

## Additions to the steps

- **Step 1 — also** record a pronunciation settled this session in `brand/src/voice/voice.md`, a
  spend in `production/src/credits-log.md`, and a permission or consent in
  `production/src/rights-register.md`, before writing the handoff.
- **Step 4 — also** give each piece touched its status and the gate it stands at, and say which
  take, master or cut is live and which is superseded, by its register row, never by listing an
  output folder (`.claude/rules/syntek-media/06-global-rules.md` Section 12).
- **Step 5 — also carry what is spent, running or unpublished.** The part is headed
  `## Media in flight` and lists, each with its path and what blocks it, every item of
  `.claude/rules/syntek-media/07-session-boundaries.md` Section 3, and also:
  - every quotation or translation whose rights row is still `needed`;
  - every guest's or audience's consent still awaited;
  - every claim still marked `VERIFY` in a piece due to post.
- **Step 6 — also** name `run-media-workflow` and the procedure by its full folder name.
- **Step 8 — also** never paste a voice ID, a key, a guest's contact details or a release form's
  personal details; name and locate them.

## Domain rules

- **What a media handoff never drops:** `.claude/rules/syntek-media/07-session-boundaries.md`
  Section 3.
- **Spends:** `production/src/credits-log.md`, under
  `.claude/rules/syntek-media/03-production-ethics.md` Section 4.
- **An open permission:** its row in `production/src/rights-register.md`;
  `.claude/rules/syntek-media/03-production-ethics.md` Sections 6 and 9.

## Examples

```markdown
## Media in flight

- Credits: the episode's speech-to-text agreed for one file, not run.
- Permission: the passage on the clip's card, video use not yet granted
  (production/src/rights-register.md, its row still needed).
- Consent: the guest's release for the recorded talk, requested, not returned.
- Flags: two claims in the clip's script still VERIFY (python3 toolkit/media.py flags).
```
