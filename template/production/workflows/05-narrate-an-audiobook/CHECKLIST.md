---
workflow: 05-narrate-an-audiobook
phase: produce
skills: [narrate-audiobook]
model: opus
---

# CHECKLIST.md — narrate an audiobook

**Last Updated**: <%DATE%> **Version**: 0.1.0 **Maintained By**: <%OWNER_NAME%>
**Language**: British English (en_GB)

> **See** `production/docs/reference/audiobook-narration.md`,
> `production/docs/reference/elevenlabs.md` and the `narrate-audiobook` skill. This procedure
> passes M2 (briefed → scripted) for an audiobook, with M3 recorded `n/a — no picture`, and
> works towards M4 (storyboarded → produced); gates are cited from
> `scripts/docs/reference/the-piece-ladder.md` by number and never restated here.

## Pre-Conditions

- [ ] Read `.claude/CLAUDE.md` and `.claude/MEMORY.md`, then this folder's `CONTEXT.md` and `CLAUDE.md`. · _sonnet_
- [ ] **The author asked for these chapters, and the audiobook piece is confirmed.** · _opus_
- [ ] The brief reads `kind: audiobook` and `picture: false`, its deliverables are `audiobook.<store>` keys, and M1 is dated. · _sonnet_

## Execution Checklist

**Routes and the register**

- [ ] A route agreed with the author for every channel; any `VERIFY` row re-checked before it was relied on. · _opus_
- [ ] ACX and Audible named as human-narration channels unless the author is authorised otherwise; INaudio's synthetic route named as external. · _opus_
- [ ] The register written, its `channels` the stores of `[audiobook.<store>]` keys, every chapter with its source and both credit rows (`ch00`, `ch99`) `planned`; external chapters record their export, location and `external` check. · _sonnet_
- [ ] The credits' words written with the author in `<piece>.ch00.md` and `<piece>.ch99.md`; every chapter's source `final`, or the author's word otherwise recorded. · _opus_
- [ ] On the author's approval, the register's `approved:` dated and M2 (briefed → scripted) recorded, with `M3: 'n/a — no picture'` and `status: scripted`; nothing voiced before it. · _sonnet_

**AI route**

- [ ] `elevenlabs` tools loaded; `media.py check --setup` clean on its ElevenLabs lines. · _sonnet_
- [ ] The narration voice and model read from `brand/src/voice/voice.md`, or chosen by the author and recorded. · _opus_
- [ ] `audiobook text` run from a `final` unit or a provided text; every unspoken word agreed and added to the pronunciations. · _sonnet_
- [ ] No chapter text copied into a tracked file. · _sonnet_
- [ ] Characters, calls and estimated credits stated; the author said yes. · _opus_
- [ ] One call at a time, each with an absolute `output_directory` inside `production/src/audiobook/generated/`; `take add` straight after each. · _sonnet_
- [ ] Stopped and reported at the first error, instead of retrying. · _sonnet_

**Human route**

- [ ] The recording set-up agreed; each recorded chapter logged with `footage add --kind audio`, its ID in Takes. · _sonnet_
- [ ] A narrator other than the author has a cleared release in the rights register. · _opus_

**Listening**

- [ ] The author listened to every part; regeneration or re-recording only on the author's word. · _opus_
- [ ] An approved take archived with `footage add --kind generated` only where the author wants it kept (the master is what must be). · _sonnet_

## Done When

- [ ] **The plan is approved (M2), every chapter asked for has approved takes, a logged recording or a recorded external export, and nothing was generated beyond what the author agreed.** · _opus_
- [ ] Every call has its row in `production/src/credits-log.md`, and nothing generated was committed. · _sonnet_
- [ ] Handed back: chapters and routes, characters and credits spent, voice and model, approved and archived parts, faults heard. · _opus_
