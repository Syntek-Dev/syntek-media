---
piece: 000-example-piece
<: if BRAND_KIND == 'business' :>title: "One line before every meeting"
kind: short-video
origin: scripted
picture: true
status: storyboarded       # idea · briefed · scripted · storyboarded · produced · cut · captioned · scheduled · published
<: if 'youtube' in PLATFORMS or 'tiktok' in PLATFORMS or 'instagram' in PLATFORMS or 'linkedin' in PLATFORMS or 'facebook' in PLATFORMS :>deliverables:
<: if 'youtube' in PLATFORMS :>  - youtube.short
<: endif :><: if 'tiktok' in PLATFORMS :>  - tiktok.video
<: endif :><: if 'instagram' in PLATFORMS :>  - instagram.reel
<: endif :><: if 'linkedin' in PLATFORMS :>  - linkedin.video_vertical
<: endif :><: if 'facebook' in PLATFORMS :>  - facebook.reel
<: endif :><: else :>deliverables: []              # no platform this project uses takes a vertical video
<: endif :>source_media: []
target_seconds: 30
words_per_minute: 150
parent: ""
source: ""
synthetic_voice: none      # none | stock | designed | own-clone | other-clone
ai_visuals: none           # none | assisted | generated
music: none                # none | licensed | own | generated
rights: [RR0000]           # a placeholder no project has: see Rights needs
verified: {M1: <%DATE%>, M2: <%DATE%>, M3: <%DATE%>}
last_updated: <%DATE%>
---

# One line before every meeting — brief

<!-- WORKED EXAMPLE: a seeded brief that shows the shape of a piece's brief, and the walk-through stops here.
     Its words, its people and its numbers are invented for the example, and it is not part of the channel.
     Its other files are named for it: script.md, storyboard.md and shot-list.md beside it; production/src/edits/000-example-piece.toml and production/src/cards/000-example-piece.title.html; and publishing/src/cut-downs/000-example-piece.md, publishing/src/captions/000-example-piece.en-GB.srt, publishing/src/thumbnails/000-example-piece.md and .html, and publishing/src/posts/000-example-piece.md.
     Once you no longer need it, delete this folder and those seven files, with any renders made while practising.
     They will not come back. -->

## Purpose

Give a busy owner one habit to use on the very next meeting invite they send.
The piece shows how <%BRAND_NAME%> thinks about running a business, in thirty seconds and one idea.

## Audience

<%AUDIENCE_TEST%>
Every line has to work in its captions alone, so each is short enough to read at a glance.

## Hook

'Every meeting you call needs one line before it starts', said to camera while the title card reads 'One line before every meeting'.

## Key points

1. Put the decision you need in the first line of the invite.
2. Name the decision, not the topic.
3. If you cannot write that line, send an email instead of calling the meeting.

## Call to action

Try it on the next invite, then come back and say what changed, in the comments.

## Disclosure plan

Nothing to disclose: the presenter speaks on camera in their own voice, and the piece uses no synthetic voice, no AI-generated visuals and no generated music.
No platform's AI label applies, so each stays off, and no disclosure line goes in any description (`publishing/docs/reference/ai-disclosure.md`).
If a later version adds a voiceover from the `voiceover` skill, or generated music or pictures, record it in the three fields above and plan the disclosure here before M7.

## Rights needs

One row: the likeness of the presenter, who is the only person on camera, filmed against a plain background with nothing else identifiable in frame.
A real piece opens that row as `needed` in `production/src/rights-register.md` when it is boarded, and clears it with the person's recorded consent before M7, even when the face is the owner's own.
The example names it RR0000, an ID no project has, because rights IDs start at RR0001 and the example never enters a register.
No music, stock, quotation or licensed font is used: the title card and the thumbnail take their faces from `brand/src/design-system/tokens.css`, whose fonts are licensed when the brand kit adds them.

## Draws on

Nothing written: the explainer is new to this piece, and it adapts no document.

## Notes

- This is a plan-only walk-through, and it stops at `storyboarded`, before M4 (storyboarded → produced).
- Its edit decision list, `production/src/edits/000-example-piece.toml`, cuts the master from F0000, a recording no project has, so `python3 toolkit/media.py assemble` on it exits 2 and names the missing footage; that stop is expected, not a fault.
- Every later file (the title card, the cut-down plan, the captions, the thumbnail and the post package) is written as the plan it would be once the master existed, and none of them is approved.
<: if 'youtube' in PLATFORMS or 'tiktok' in PLATFORMS or 'instagram' in PLATFORMS or 'linkedin' in PLATFORMS or 'facebook' in PLATFORMS :>- Captions are burned into every deliverable, because no vertical deliverable in `toolkit/data/platforms.toml` has a confirmed sidecar route: each `caption_formats` is empty or named in its table's `verify`.
<: else :>- No platform this project uses takes a vertical video, so the example lists no deliverable: nothing of it would be cut, captioned for a platform or posted, and its later files show only the shape of each plan.
<: endif :>- The example is never entered in `scripts/src/piece-register.md`, `publishing/src/schedule.md` or `publishing/src/publish-log.md`, and it is never posted.
<: elif BRAND_KIND == 'author-fiction' :>title: "Count the stones"
kind: short-video
origin: scripted
picture: true
status: storyboarded       # idea · briefed · scripted · storyboarded · produced · cut · captioned · scheduled · published
<: if 'youtube' in PLATFORMS or 'tiktok' in PLATFORMS or 'instagram' in PLATFORMS or 'linkedin' in PLATFORMS or 'facebook' in PLATFORMS :>deliverables:
<: if 'youtube' in PLATFORMS :>  - youtube.short
<: endif :><: if 'tiktok' in PLATFORMS :>  - tiktok.video
<: endif :><: if 'instagram' in PLATFORMS :>  - instagram.reel
<: endif :><: if 'linkedin' in PLATFORMS :>  - linkedin.video_vertical
<: endif :><: if 'facebook' in PLATFORMS :>  - facebook.reel
<: endif :><: else :>deliverables: []              # no platform this project uses takes a vertical video
<: endif :>source_media: []
target_seconds: 30
words_per_minute: 140
parent: ""
source: ""
synthetic_voice: none      # none | stock | designed | own-clone | other-clone
ai_visuals: none           # none | assisted | generated
music: none                # none | licensed | own | generated
rights: [RR0000]           # a placeholder no project has: see Rights needs
verified: {M1: <%DATE%>, M2: <%DATE%>, M3: <%DATE%>}
last_updated: <%DATE%>
---

# Count the stones — brief

<!-- WORKED EXAMPLE: a seeded brief that shows the shape of a piece's brief, and the walk-through stops here.
     Its words, its people and its numbers are invented for the example, and it is not part of the channel.
     Its other files are named for it: script.md, storyboard.md and shot-list.md beside it; production/src/edits/000-example-piece.toml and production/src/cards/000-example-piece.title.html; and publishing/src/cut-downs/000-example-piece.md, publishing/src/captions/000-example-piece.en-GB.srt, publishing/src/thumbnails/000-example-piece.md and .html, and publishing/src/posts/000-example-piece.md.
     Once you no longer need it, delete this folder and those seven files, with any renders made while practising.
     They will not come back. -->

## Purpose

Make a reader who has never heard of the novel want to know what moves in the river.
The teaser sells a feeling and a question, and holds back the title and the cover for a later piece.

## Audience

<%AUDIENCE_TEST%>
The captions carry the whole teaser, so every line is short and the pauses do the work.

## Hook

'Count the stones, and the river lets you pass', said low to camera while the title card reads 'Count the stones'.

## Key points

1. Tam taught Maren a count for crossing the ford: three stones to the post, four to the willow.
2. Tonight she has to cross it in the dark.
3. The count holds as far as the willow, and then something upstream moves.

## Call to action

Follow to see the cover first; the title arrives with it.

## Disclosure plan

Nothing to disclose: the author speaks on camera in their own voice, and the piece uses no synthetic voice, no AI-generated visuals and no generated music.
No platform's AI label applies, so each stays off, and no disclosure line goes in any description (`publishing/docs/reference/ai-disclosure.md`).
If a later version adds a voiceover from the `voiceover` skill, or generated music or pictures, record it in the three fields above and plan the disclosure here before M7.

## Rights needs

One row: the likeness of the author, who is the only person on camera, filmed against a plain background with nothing else identifiable in frame.
A real piece opens that row as `needed` in `production/src/rights-register.md` when it is boarded, and clears it with the person's recorded consent before M7, even when the face is the owner's own.
The example names it RR0000, an ID no project has, because rights IDs start at RR0001 and the example never enters a register.
No music, stock, quotation or licensed font is used: the title card and the thumbnail take their faces from `brand/src/design-system/tokens.css`, whose fonts are licensed when the brand kit adds them.

## Draws on

The opening of the novel as syntek-author's worked example chapter tells it, where present: Maren, Tam, the count and the ford at night.

## Notes

- This is a plan-only walk-through, and it stops at `storyboarded`, before M4 (storyboarded → produced).
- Its edit decision list, `production/src/edits/000-example-piece.toml`, cuts the master from F0000, a recording no project has, so `python3 toolkit/media.py assemble` on it exits 2 and names the missing footage; that stop is expected, not a fault.
- Every later file (the title card, the cut-down plan, the captions, the thumbnail and the post package) is written as the plan it would be once the master existed, and none of them is approved.
<: if 'youtube' in PLATFORMS or 'tiktok' in PLATFORMS or 'instagram' in PLATFORMS or 'linkedin' in PLATFORMS or 'facebook' in PLATFORMS :>- Captions are burned into every deliverable, because no vertical deliverable in `toolkit/data/platforms.toml` has a confirmed sidecar route: each `caption_formats` is empty or named in its table's `verify`.
<: else :>- No platform this project uses takes a vertical video, so the example lists no deliverable: nothing of it would be cut, captioned for a platform or posted, and its later files show only the shape of each plan.
<: endif :>- The example is never entered in `scripts/src/piece-register.md`, `publishing/src/schedule.md` or `publishing/src/publish-log.md`, and it is never posted.
- The teaser names no book on purpose: the title is held back for the cover reveal.
<: else :>title: "The second visit"
kind: short-video
origin: scripted
picture: true
status: storyboarded       # idea · briefed · scripted · storyboarded · produced · cut · captioned · scheduled · published
<: if 'youtube' in PLATFORMS or 'tiktok' in PLATFORMS or 'instagram' in PLATFORMS or 'linkedin' in PLATFORMS or 'facebook' in PLATFORMS :>deliverables:
<: if 'youtube' in PLATFORMS :>  - youtube.short
<: endif :><: if 'tiktok' in PLATFORMS :>  - tiktok.video
<: endif :><: if 'instagram' in PLATFORMS :>  - instagram.reel
<: endif :><: if 'linkedin' in PLATFORMS :>  - linkedin.video_vertical
<: endif :><: if 'facebook' in PLATFORMS :>  - facebook.reel
<: endif :><: else :>deliverables: []              # no platform this project uses takes a vertical video
<: endif :>source_media: []
target_seconds: 30
words_per_minute: 140
parent: ""
source: ""
synthetic_voice: none      # none | stock | designed | own-clone | other-clone
ai_visuals: none           # none | assisted | generated
music: none                # none | licensed | own | generated
rights: [RR0000]           # a placeholder no project has: see Rights needs
verified: {M1: <%DATE%>, M2: <%DATE%>, M3: <%DATE%>}
last_updated: <%DATE%>
---

# The second visit — brief

<!-- WORKED EXAMPLE: a seeded brief that shows the shape of a piece's brief, and the walk-through stops here.
     Its words, its people and its numbers are invented for the example, and it is not part of the channel.
     Its other files are named for it: script.md, storyboard.md and shot-list.md beside it; production/src/edits/000-example-piece.toml and production/src/cards/000-example-piece.title.html; and publishing/src/cut-downs/000-example-piece.md, publishing/src/captions/000-example-piece.en-GB.srt, publishing/src/thumbnails/000-example-piece.md and .html, and publishing/src/posts/000-example-piece.md.
     Once you no longer need it, delete this folder and those seven files, with any renders made while practising.
     They will not come back. -->

## Purpose

Put the next book's central claim in front of someone who has never heard the author, in the register of a talk.
One claim, stated twice and given its test, so it stays with the viewer after the clip ends.

## Audience

<%AUDIENCE_TEST%>
The claim has to land on a first hearing, with no slide and no context before it.

## Hook

'Making a newcomer welcome once is the easy part', said to camera as if mid-talk while the title card reads 'The second visit'.

## Key points

1. The real test of a welcome is the newcomer's second visit.
2. A welcome is finished only when the newcomer is expected back.
3. The claim holds for any group, a church among them.

## Call to action

Follow for the rest of the argument, which the next book makes in full.

## Disclosure plan

Nothing to disclose: the author speaks on camera in their own voice, and the piece uses no synthetic voice, no AI-generated visuals and no generated music.
No platform's AI label applies, so each stays off, and no disclosure line goes in any description (`publishing/docs/reference/ai-disclosure.md`).
If a later version adds a voiceover from the `voiceover` skill, or generated music or pictures, record it in the three fields above and plan the disclosure here before M7.

## Rights needs

One row: the likeness of the author, who is the only person on camera, filmed against a plain background with nothing else identifiable in frame.
A real piece opens that row as `needed` in `production/src/rights-register.md` when it is boarded, and clears it with the person's recorded consent before M7, even when the face is the owner's own.
The example names it RR0000, an ID no project has, because rights IDs start at RR0001 and the example never enters a register.
No music, stock, quotation or licensed font is used: the title card and the thumbnail take their faces from `brand/src/design-system/tokens.css`, whose fonts are licensed when the brand kit adds them.

## Draws on

The argument of syntek-author's worked example chapter, where present: a welcome is finished only when the guest is expected back.

## Notes

- This is a plan-only walk-through, and it stops at `storyboarded`, before M4 (storyboarded → produced).
- Its edit decision list, `production/src/edits/000-example-piece.toml`, cuts the master from F0000, a recording no project has, so `python3 toolkit/media.py assemble` on it exits 2 and names the missing footage; that stop is expected, not a fault.
- Every later file (the title card, the cut-down plan, the captions, the thumbnail and the post package) is written as the plan it would be once the master existed, and none of them is approved.
<: if 'youtube' in PLATFORMS or 'tiktok' in PLATFORMS or 'instagram' in PLATFORMS or 'linkedin' in PLATFORMS or 'facebook' in PLATFORMS :>- Captions are burned into every deliverable, because no vertical deliverable in `toolkit/data/platforms.toml` has a confirmed sidecar route: each `caption_formats` is empty or named in its table's `verify`.
<: else :>- No platform this project uses takes a vertical video, so the example lists no deliverable: nothing of it would be cut, captioned for a platform or posted, and its later files show only the shape of each plan.
<: endif :>- The example is never entered in `scripts/src/piece-register.md`, `publishing/src/schedule.md` or `publishing/src/publish-log.md`, and it is never posted.
- It is written as a clip from a talk, but it is scripted: a talk that exists as a recording is a recorded piece instead, brought in through `production/workflows/08-bring-in-a-recording/`.
<: endif :>