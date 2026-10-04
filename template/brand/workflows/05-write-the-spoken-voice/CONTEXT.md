# CONTEXT.md — brand/workflows/05-write-the-spoken-voice/

The procedure for deciding with the author how the brand sounds aloud and who says it: the spoken
style (pace, register, how the brand's name is said, words never said aloud), one narrator for
each use, chosen by listening and recorded with its model and settings, and the pronunciations a
narrator needs. It opens with a grilling pass, reads the written voice first where syntek-author
is present, and records consent before any cloned voice is used. It generates nothing itself: a
trial to hear a voice runs, costed and agreed, through the voiceover procedure.

## Directory Tree

```text
brand/workflows/05-write-the-spoken-voice/
├── CHECKLIST.md        ← model-tagged checklist; tick it as you go
├── CLAUDE.md           ← operating rules for this procedure
├── CONTEXT.md          ← this file: when to use it, what it produces
└── STEPS.md            ← the ordered steps, each naming its skill and guide
```

## When to use this

- A new project, before the first voiceover.
- A new use needs a narrator: a podcast host, a character in a trailer, a narrated book.
- The author wants to change a narrator, or the pace or register of the brand's voice.
- A word keeps being said wrongly.

Reach for a **different** procedure when a piece's voiceover is to be made
(`production/workflows/02-make-a-voiceover/`), or when the written voice itself is changing (the
voice files of syntek-author, where present).

## What it produces, and where

- **`brand/src/voice/voice.md`**, with its spoken style written, one narrator row per use
  (voice, voice ID, model ID, settings, output format, consent, date chosen) and the
  pronunciations known so far, and its flags cleared.
- **A `voice-consent` row** in `production/src/rights-register.md` for every cloned voice, the
  owner's own included, cleared before the voice is used.
- **Dated decisions** in `.claude/MEMORY.md`.

## The failure this procedure exists to prevent

A brand that sounds like a different speaker in every piece, because each voiceover chose its own
narrator, model and settings on the day; or a cloned voice used without the person's recorded
consent. Both are found only after money has been spent and something has been published. One
narrator per use, chosen once by listening and recorded with its model, settings and consent,
makes every later voiceover the brand's without a second choice.

## Cross-references

- `brand/docs/reference/the-spoken-voice.md` — spoken against written, narrators, consent.
- `production/docs/reference/elevenlabs.md` — the server, models, credits and the fallback.
- `production/docs/reference/rights-and-consent.md` — how consent for a voice is recorded.
