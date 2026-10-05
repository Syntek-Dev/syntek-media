---
workflow: 08-bring-in-a-recording
phase: produce
skills: [captions]
model: opus
---

# CHECKLIST.md — bring in a recording

**Last Updated**: <%DATE%> **Version**: 0.1.0 **Maintained By**: <%OWNER_NAME%>
**Language**: British English (en_GB)

> **See** `production/docs/reference/recorded-pieces.md` and the `captions` skill. This procedure
> passes M2 (briefed → scripted) for a recorded piece and records M3 (scripted → storyboarded) as
> `n/a — recorded`; gates are cited from `scripts/docs/reference/the-piece-ladder.md` by number
> and never restated here.

## Pre-Conditions

- [ ] Read `.claude/CLAUDE.md` and `.claude/MEMORY.md`, then this folder's `CONTEXT.md` and `CLAUDE.md`. · _sonnet_
- [ ] **The brief reads `origin: recorded` and `status: briefed`, and the recording is confirmed with the author.** · _opus_

## Execution Checklist

**The recording**

- [ ] Logged with `footage add` (copied, never moved), with its rights ID where it shows other people; a recording already in the manifest not logged again. · _sonnet_
- [ ] Its footage ID added to the brief's `source_media`. · _sonnet_
- [ ] Its audio extracted with `extract-audio … -o production/src/renders/<piece>/<stem>.wav`, into the piece's own folder. · _sonnet_

**The words**

- [ ] The author chose speech-to-text or their own words; or, for an episode cut from its parent's recording, the parent's approved beats it keeps copied with their anchors. · _opus_
- [ ] For speech-to-text: `check --setup` clean on its ElevenLabs lines; minutes, calls and credits stated; the author said yes. · _sonnet_
- [ ] One call, with `save_transcript_to_file: false` and `return_transcript_to_client_directly: true`; its credits-log row written. · _sonnet_
- [ ] On 'outside of allowed directory', the re-add command given with a base path containing the project; no audio copied elsewhere. · _sonnet_

**The transcript**

- [ ] Written in the script's format, beats agreed with the author, each anchored `(at HH:MM:SS.mmm)`. · _opus_
- [ ] Spoken lines only, as said; every uncertain word `[unclear]` and flagged `VERIFY`. · _opus_
- [ ] The spelling and grammar skills (syntek-author), where present, and the fact-check skill (syntek-author), where present, run as reports, or each absent one named. · _sonnet_
- [ ] Only mis-transcriptions fixed; every finding decided by the author. · _opus_

**Approval and captions**

- [ ] The author approved the transcript; `approved` dated. · _opus_
- [ ] M2 dated, M3 recorded as `n/a — recorded`, `status` set to `scripted`. · _sonnet_
- [ ] `captions align --anchors` run; the recording-timed captions written, every unplaced or stretched cue reported. · _sonnet_

## Done When

- [ ] **The transcript is approved, anchored beat by beat, and holds only what was said.** · _opus_
- [ ] Nothing was spent without a yes, and the recording was neither moved nor committed. · _sonnet_
- [ ] Handed back: footage ID, beats and length, how the words were made and their cost, findings and decisions, the captions file. · _opus_
