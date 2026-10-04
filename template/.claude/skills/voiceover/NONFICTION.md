# NONFICTION.md — voiceover, non-fiction mode

The domain for voicing a non-fiction author's pieces: the spoken frame of a talk clip, an
explainer's narration, and a podcast's introduction and close, where a quotation, its attribution
and the sound of a technical, Greek or Hebrew term carry the argument.

## Paths and unit

- **Unit:** one piece. **Segment:** one spoken sentence, or one short beat read as one breath.
- **Procedure:** `production/workflows/02-make-a-voiceover/`.
- **Voiced lines:** the script's `VO:` and `NARRATOR:` lines, and `HOST:` lines where the author
  has chosen a synthetic host voice for an introduction or a close.
- **Register:** `production/src/voiceover/<piece>.toml`; takes in
  `production/src/voiceover/generated/` (git-ignored).
- **Narrators:** the `voiceover` row of `brand/src/voice/voice.md`, or its `podcast-host` row.
- **Written voice:** syntek-author's voice notes, standards/style/voice-notes.md, where present;
  the spoken style in `voice.md` follows them and never restates them.
- **Guides:** `production/docs/reference/voiceover.md`,
  `brand/docs/reference/the-spoken-voice.md` and
  `production/docs/reference/rights-and-consent.md` (quotations and scripture translations).

## Additions to the steps

- **Step 2 — also check every quotation's rights row.** A quotation from another work, scripture
  included, is voiced only once its row exists in `production/src/rights-register.md`; it must be
  `cleared` before M7, and a translation's permission for print may not cover audio.
- **Step 5 — also say each reference as a listener hears it.** A scripture reference reaches the
  server in its spoken form, as the script writes it for the ear ('Romans, chapter eight'); a
  Greek or Hebrew word takes its IPA or respelling from `voice.md`, settled with the author, never
  guessed from the transliteration.
- **Step 9 — also check every quotation word for word.** The author compares each quoted take with
  its source: a take that drops, adds or swaps a word in a quotation is rejected, however good its
  delivery.

## Domain rules

- **Reading scripture aloud needs the translation's permission for audio**: a `scripture` row in the
  rights register, `cleared` before M7 (`.claude/rules/syntek-media/03-production-ethics.md`
  Section 6).
- **Attribution is spoken where the script speaks it, and never invented**
  (`.claude/rules/syntek-media/03-production-ethics.md` Section 7).
- **A quotation is voiced exactly**: its grammar is never smoothed by the request text, and an
  ellipsis in the source stays a pause the author has approved.
- **A synthetic host is still synthetic**: a podcast introduced in an AI voice says so in the audio
  and in the episode notes, as `publishing/docs/reference/ai-disclosure.md` sets out.

## Examples

An invented line from Robin Example's talk clip, and the request it becomes:

```text
script.md   VO: The whole argument turns on one Greek word: agape.
voice.md    | agape | /aˈɡaːpeː/ | ah-GAH-pay | author, 12/03/2027 | the Greek word, not the English 'agape' |
text        The whole argument turns on one Greek word: agape.
request     The whole argument turns on one Greek word: /aˈɡaːpeː/.
```

The caption keeps the script's spelling; only the request carries the IPA.
