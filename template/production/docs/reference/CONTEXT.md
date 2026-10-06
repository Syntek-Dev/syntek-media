# CONTEXT.md — production/docs/reference/

The template's guides for the production layer, one per question a production job raises. They
are template-owned: `copier update` replaces them, so changes for this project belong in
`production/docs/project/` under the same filename.

## Directory Tree

```text
production/docs/reference/
├── CONTEXT.md                  ← this file
├── CLAUDE.md                   ← operating rules
<: if 'audiobook' in MEDIA_KINDS :>├── audiobook-narration.md      ← three routes chosen per channel; chapter text; the ACX targets
<: endif :>├── edit-decision-lists.md      ← the master as a list of clips, overlays and sounds, rebuilt on demand
├── elevenlabs.md               ← the user-scope server, the base path, cost before spend, one call at a time
├── recorded-pieces.md          ← a recording in, a transcript as its script, captions to every cut
├── rights-and-consent.md       ← what needs a row; clearing it; consent before a likeness or a voice
├── scenes-as-code.md           ← deterministic sprite movement, real sources, stills and native masters
├── sound-and-loudness.md       ← the loudness targets; where a music bed goes; ducking and fades
├── source-media.md             ← the footage manifest, external storage and the checked local mirror
└── voiceover.md                ← one segment per spoken sentence or beat; the segment register
```

## What's here

- `source-media.md` — **read before logging any file:** why footage lives outside Git, the
  manifest field by field, the mirror, and music beds, stock and archived takes.
- `edit-decision-lists.md` — the edit decision list field by field: clips, stills, cards,
  colour clips, fades, push-ins, overlays and sound.
- `scenes-as-code.md` — the scene kit, frame clock, sprite slot, movement and anchor interactions;
  first/middle stills and the preview review, then a master rendered natively per aspect.
- `sound-and-loudness.md` — the loudness targets and where each comes from; where a music bed
  goes, how it ducks under the voice and how it fades.
- `rights-and-consent.md` — every kind of item that needs a rights row, the register's statuses,
  consent before a likeness or a voice, and quotations and scripture.
- `elevenlabs.md` — **read before any credit-spending call:** setting up the user-scope server so
  its base path contains the project, stating the cost first, one call at a time into a
  git-ignored folder, `take add`, speech-to-text, and the espeak-ng fallback.
- `voiceover.md` — why a segment is a sentence or a beat and never a caption cue, the segment
  register, and how a script line becomes a request.
- `recorded-pieces.md` — a recorded talk or interview as a piece: the transcript and its
  anchors, M2 and M3 for a recorded piece, and the chain of captions from the recording to
  every cut.
<: if 'audiobook' in MEDIA_KINDS :>- `audiobook-narration.md` — the human, AI and external routes, where each channel stands on
  synthetic narration (dated, with `VERIFY` where unconfirmed), chapter text, and the ACX
  targets.
<: endif :>
## Cross-references

- `production/docs/project/` — the author's own guides; a same-named file there wins.
- `production/workflows/` — the procedures that apply these guides step by step.
- `.claude/rules/syntek-media/03-production-ethics.md` — the rules every guide here serves.
