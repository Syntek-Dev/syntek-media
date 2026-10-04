---
type: guide
skills: [voiceover]
model: opus
---

# The spoken voice — how the brand sounds aloud, and who says it

**Last Updated**: <%DATE%> **Version**: 0.1.0 **Maintained By**: <%OWNER_NAME%>
**Language**: British English (en_GB)

**What it is.** The spoken voice is how the brand sounds when it is heard rather than read: its
pace, its register, how its own name is said, the words it never says aloud, the narrator for
each use, and how every hard word is pronounced. It lives in one file,
`brand/src/voice/voice.md`, which `voiceover` reads before every call, so pieces voiced months
apart sound like one brand. It is not the written voice, and it never restates it.

## Spoken against written

- The written voice is syntek-author's, where present: its voice notes,
  standards/style/voice-notes.md, and in a business its brand voice,
  standards/brand/brand-voice.md (or the Brand folder its 00-project.md Paths name). `voice.md`
  cites it in one line; a contradiction is reported to the author, never resolved silently.
- What changes aloud is the delivery: pace in words a minute, sentences short enough to hear
  once, numbers said as a listener hears them, and the words that read well but sound wrong.
  How a script is written for the ear is `scripts/docs/reference/writing-for-the-ear.md`.

## A narrator for each use

| Use | For |
|---|---|
| `voiceover` | explainers, trailers and pieces that are only a voiceover |
| `narration` | a book read by a synthetic voice, where the project makes audiobooks |
| `podcast-host` | a synthetic host's links and intros |
| `character:<name>` | one character's voice in a trailer or a dramatised reading |

- Each row records the service, the voice and its ID, the model, the settings sent on every call
  (stability, similarity, style, speed), the output format, the consent and the date chosen.
- The model is found with `mcp__elevenlabs__list_models` and recorded per use, never assumed;
  voices are listed with `mcp__elevenlabs__search_voices`. Both calls are free.
- **One narrator per use.** A second voice for the same use makes the brand sound like two;
  changing one is the author's decision, recorded with the date.
- Hearing a candidate costs credits. Say so before any trial, and run it as a voiceover
  through `production/workflows/02-make-a-voiceover/`, which states the cost and waits for a yes.

## Pronunciations

- Every word a narrator might say wrongly gets a row: the brand's own name first, then people,
  places, products, borrowed words and invented names.
- The IPA is stored once, here, and substituted into the request text only, never written back
  into a script; models differ in how they read IPA, so check the first word of a batch.
- An invented name takes its IPA from syntek-author's names register or lexicon, where present;
  the pronounce skill (syntek-author), where present, is never run from here. A real name comes
  from its owner or an authoritative reference, named in the Source column.

## Consent

- No voice is cloned without the person's recorded consent: a `voice-consent` row in
  `production/src/rights-register.md`, `cleared`, whose ID goes in the narrator's Consent column
  before the first call.
- The brand owner's own clone needs its consent row like any other, and every synthetic voice
  is disclosed, the owner's clone included (`publishing/docs/reference/ai-disclosure.md`).

## How we apply it here

- The spoken voice is settled with the author in a grilling pass before the first voiceover.
- The pace in `voice.md` is what a script is timed at, unless its brief sets its own.
- Voice IDs stay in `voice.md`; a segment register names its narrator by Use, never by ID.

## Who implements it

- **Workflows:** `brand/workflows/05-write-the-spoken-voice/` and
  `production/workflows/02-make-a-voiceover/`.
- **Skill:** `voiceover` reads `voice.md` before every call and records a narrator the first time
  it needs one; audiobook narration, where the project makes audiobooks, reads it too.

## Governing standard

`.claude/rules/syntek-media/03-production-ethics.md` Section 6 owns consent before a voice or a
likeness, and Section 4 never spending credits unasked;
`.claude/rules/syntek-media/06-global-rules.md` Section 10 owns where a voice ID may be kept. The
rules own the requirements; this guide owns how the voice is written down and used.
