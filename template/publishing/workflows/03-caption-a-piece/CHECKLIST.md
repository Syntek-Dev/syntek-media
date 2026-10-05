---
workflow: 03-caption-a-piece
phase: publish
skills: [captions]
model: opus
---

# CHECKLIST.md — caption a piece's deliverables

**Last Updated**: <%DATE%> **Version**: 0.1.0 **Maintained By**: <%OWNER_NAME%>
**Language**: British English (en_GB)

> **See** `publishing/docs/reference/captions.md` and the `captions` skill. This procedure serves
> M6 (cut → captioned) of `scripts/docs/reference/the-piece-ladder.md`; the gate is cited by
> number and the move it guards, and this list never restates it.

## Pre-Conditions

- [ ] Read `.claude/CLAUDE.md` and `.claude/MEMORY.md`, then this folder's `CONTEXT.md` and `CLAUDE.md`. · _sonnet_
- [ ] Read `captions.md` and the `captions` skill. · _opus_
- [ ] **The words exist:** an approved `script.md`, or a recorded piece's approved `transcript.md`. · _sonnet_
- [ ] The brief and the cut-down plan read; the master, and any cut already rendered, located. · _sonnet_

## Execution Checklist

**Choosing**

- [ ] Every deliverable listed; each with speech and picture marked for captions, each other one `n/a` with its reason. · _opus_
- [ ] **Every profile-site placement and feed episode found:** a `.vtt` for each self-hosted video, a published transcript for each piece or cut placed and for a feed episode. · _opus_
- [ ] Burned or sidecar noted per deliverable, from its table's `caption_formats` and the brief. · _sonnet_
- [ ] A timing route chosen per file; no speech-to-text run in this procedure. · _opus_

**Making**

- [ ] The master's captions made with `from-segments`, `from-words`, `align` or `retime --edl`, written as `<piece>.en-GB.srt`. · _sonnet_
- [ ] Route four: printed words check reviewed, findings decided, accepted words and check written through `-o`; fetch left to the author. · _opus_
- [ ] Each cut's captions retimed from the master's, or aligned on its own audio and lines where it drifted. · _sonnet_
- [ ] Files rewrapped where a deliverable needs its own width, named with the `.<platform>-<format>` qualifier. · _sonnet_

**Checking and delivering**

- [ ] **Every file passes `captions check --script`;** each finding decided, and a mis-transcription fixed in the transcript first, with the author. · _opus_
- [ ] Line breaks at clauses, never inside a name; no braced direction or audio tag in any cue. · _opus_
- [ ] Route four's word boundaries preserved; short-gap findings decided and timing estimates checked in the preview. · _opus_
- [ ] Burned deliverables burned (or re-cut with their captions); sidecars kept, with a VTT where a platform takes one, a profile site's video and a feed episode included. · _sonnet_
- [ ] Each published transcript written with `captions transcript` (`--lines` for a cut), described where the picture says more, and approved by the author. · _opus_
- [ ] No caption-font fallback accepted. · _sonnet_
- [ ] A burned preview watched with the author: in time, inside the safe zone, readable. · _opus_
- [ ] The brief's `status` and `verified` set: M6 dated, or `n/a` with its reason. · _sonnet_
- [ ] Handed back: each file and what it is timed to, burned or sidecar, every finding and its decision. · _opus_

## Done When

- [ ] **Every deliverable that needs captions has a checked file, burned where its platform takes no sidecar.** · _opus_
- [ ] Every caption says what was scripted or said, and nothing else. · _opus_
- [ ] M6 is recorded in the brief. · _sonnet_
