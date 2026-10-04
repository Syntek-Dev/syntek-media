---
piece: 000-example-piece
master: 000-example-piece.master.mp4
approved: ""
---

<: if BRAND_KIND == 'business' :># One line before every meeting — cut-down plan

<!-- WORKED EXAMPLE: the cut-down plan of the example piece, waiting for a master that is never made.
     A 30-second piece has little to cut: the full-length vertical video is each platform's main deliverable, and is listed in the brief, not here.
<: if 'instagram' in PLATFORMS or 'facebook' in PLATFORMS :>     What is left is a shorter cut for a platform's stories, with its own moment, and the platforms that get no cut say why below.
     Cut numbers are fixed per platform in this example, so a gap means a platform this project does not use.
     In and Out sit on the master's beat boundaries, the same times as the storyboard, the edit decision list and the captions. -->

| Cut | Deliverables | Lines | In | Out | Frame | Hook | Status |
|---|---|---|---|---|---|---|---|
<: if 'instagram' in PLATFORMS :>| c01 | instagram.story | 1.1–2.3 | 00:00:00.000 | 00:00:15.000 | centre | Every meeting you call needs one line | planned |
<: endif :><: if 'facebook' in PLATFORMS :>| c02 | facebook.story | 2.1–3.3 | 00:00:05.000 | 00:00:24.000 | centre | Put the decision in the invite | planned |
<: endif :><: else :>     What would be left is a shorter cut for a platform's stories, and no platform this project uses takes one, so each platform says why it gets no cut below. -->

No story cuts: no platform this project uses takes one.
<: endif :><: if 'instagram' in PLATFORMS :>
## c01 — Every meeting you call needs one line

- Opens on the hook line, 1.1, with the title card over it, exactly as the master does.
- Ends on 2.3, the example of a good first line, so the story carries the whole idea without the ask.
- The story's end points the viewer to the reel for the rest.
- 15.0 seconds, inside `platform.instagram.story.max_seconds`; captions 32 characters a line, burned, from `000-example-piece--c01.en-GB.srt` retimed from the master's.
- No thumbnail of its own: `toolkit/data/platforms.toml` has no thumbnail table for a story.
<: endif :><: if 'facebook' in PLATFORMS :>
## c02 — Put the decision in the invite

- Opens on 2.1, the instruction itself, with no hook line before it.
- Carries the instruction and the reason for it, 2.1 to 3.3, and leaves out the ask.
- A viewer who never saw the reel still has the whole habit by its last line.
- No on-screen title: the title card ends at 00:00:04.000 on the master, before this cut's In.
- 19.0 seconds, inside `platform.facebook.story.max_seconds`; captions 32 characters a line, burned, from `000-example-piece--c02.en-GB.srt` retimed from the master's.
- No thumbnail of its own: `toolkit/data/platforms.toml` has no thumbnail table for a story.
<: endif :><: elif BRAND_KIND == 'author-fiction' :># Count the stones — cut-down plan

<!-- WORKED EXAMPLE: the cut-down plan of the example piece, waiting for a master that is never made.
     A 30-second piece has little to cut: the full-length vertical video is each platform's main deliverable, and is listed in the brief, not here.
<: if 'instagram' in PLATFORMS or 'facebook' in PLATFORMS :>     What is left is a shorter cut for a platform's stories, with its own moment, and the platforms that get no cut say why below.
     Cut numbers are fixed per platform in this example, so a gap means a platform this project does not use.
     In and Out sit on the master's beat boundaries, the same times as the storyboard, the edit decision list and the captions. -->

| Cut | Deliverables | Lines | In | Out | Frame | Hook | Status |
|---|---|---|---|---|---|---|---|
<: if 'instagram' in PLATFORMS :>| c01 | instagram.story | 1.1–2.3 | 00:00:00.000 | 00:00:15.000 | centre | Count the stones | planned |
<: endif :><: if 'facebook' in PLATFORMS :>| c02 | facebook.story | 2.1–3.3 | 00:00:05.000 | 00:00:24.000 | centre | Tam taught Maren the count | planned |
<: endif :><: else :>     What would be left is a shorter cut for a platform's stories, and no platform this project uses takes one, so each platform says why it gets no cut below. -->

No story cuts: no platform this project uses takes one.
<: endif :><: if 'instagram' in PLATFORMS :>
## c01 — Count the stones

- Opens on the saying, 1.1, with the title card over it, exactly as the master does.
- Ends on 2.3, the crossing in the dark, so the story leaves the viewer at the edge of the water.
- The story's end points the viewer to the reel for what happens next.
- 15.0 seconds, inside `platform.instagram.story.max_seconds`; captions 32 characters a line, burned, from `000-example-piece--c01.en-GB.srt` retimed from the master's.
- No thumbnail of its own: `toolkit/data/platforms.toml` has no thumbnail table for a story.
<: endif :><: if 'facebook' in PLATFORMS :>
## c02 — Tam taught Maren the count

- Opens on 2.1, Tam and Maren by name, with no saying before it.
- Carries the count and the crossing, 2.1 to 3.3, and stops on 'Then something upstream moves'.
- Ending on the turn, with no ask, makes it a cliffhanger of its own.
- No on-screen title: the title card ends at 00:00:04.000 on the master, before this cut's In.
- 19.0 seconds, inside `platform.facebook.story.max_seconds`; captions 32 characters a line, burned, from `000-example-piece--c02.en-GB.srt` retimed from the master's.
- No thumbnail of its own: `toolkit/data/platforms.toml` has no thumbnail table for a story.
<: endif :><: else :># The second visit — cut-down plan

<!-- WORKED EXAMPLE: the cut-down plan of the example piece, waiting for a master that is never made.
     A 30-second piece has little to cut: the full-length vertical video is each platform's main deliverable, and is listed in the brief, not here.
<: if 'instagram' in PLATFORMS or 'facebook' in PLATFORMS :>     What is left is a shorter cut for a platform's stories, with its own moment, and the platforms that get no cut say why below.
     Cut numbers are fixed per platform in this example, so a gap means a platform this project does not use.
     In and Out sit on the master's beat boundaries, the same times as the storyboard, the edit decision list and the captions. -->

| Cut | Deliverables | Lines | In | Out | Frame | Hook | Status |
|---|---|---|---|---|---|---|---|
<: if 'instagram' in PLATFORMS :>| c01 | instagram.story | 1.1–2.3 | 00:00:00.000 | 00:00:15.000 | centre | Making a newcomer welcome once | planned |
<: endif :><: if 'facebook' in PLATFORMS :>| c02 | facebook.story | 2.1–3.3 | 00:00:05.000 | 00:00:24.000 | centre | The real test of a welcome | planned |
<: endif :><: else :>     What would be left is a shorter cut for a platform's stories, and no platform this project uses takes one, so each platform says why it gets no cut below. -->

No story cuts: no platform this project uses takes one.
<: endif :><: if 'instagram' in PLATFORMS :>
## c01 — Making a newcomer welcome once

- Opens on the hook, 1.1, with the title card over it, exactly as the master does.
- Ends on 2.3, the two questions, so the story leaves the viewer asking them of their own group.
- The story's end points the viewer to the reel for the claim itself.
- 15.0 seconds, inside `platform.instagram.story.max_seconds`; captions 32 characters a line, burned, from `000-example-piece--c01.en-GB.srt` retimed from the master's.
- No thumbnail of its own: `toolkit/data/platforms.toml` has no thumbnail table for a story.
<: endif :><: if 'facebook' in PLATFORMS :>
## c02 — The real test of a welcome

- Opens on 2.1, the test, with no hook line before it.
- Carries the test and the claim, 2.1 to 3.3, and leaves out the ask.
- It is the argument in miniature, so it stands without the rest of the clip.
- No on-screen title: the title card ends at 00:00:04.000 on the master, before this cut's In.
- 19.0 seconds, inside `platform.facebook.story.max_seconds`; captions 32 characters a line, burned, from `000-example-piece--c02.en-GB.srt` retimed from the master's.
- No thumbnail of its own: `toolkit/data/platforms.toml` has no thumbnail table for a story.
<: endif :><: endif :><: if 'youtube' in PLATFORMS or 'tiktok' in PLATFORMS or 'linkedin' in PLATFORMS or 'podcast' in PLATFORMS or 'website' in PLATFORMS or 'blog' in PLATFORMS or 'newsletter' in PLATFORMS :>
## Platforms with no cut

<: if 'youtube' in PLATFORMS :>- **youtube:** none, because the whole piece is already its Short, and a shorter Short of the same lines on the same channel would be a near-identical upload.
<: endif :><: if 'tiktok' in PLATFORMS :>- **tiktok:** none, because the whole piece is already its video, and a second, shorter upload of the same lines would be a near-identical batch.
<: endif :><: if 'linkedin' in PLATFORMS :>- **linkedin:** none, because the whole piece goes to the feed as its vertical video, and thirty seconds needs no shorter version there.
<: endif :><: if 'podcast' in PLATFORMS :>- **podcast:** none, because the feed carries episodes, and a 30-second clip with no episode around it is not one.
<: endif :><: if 'website' in PLATFORMS :>- **website:** none, because no page places this piece, and a silent loop for a page would need a landscape master.
<: endif :><: if 'blog' in PLATFORMS :>- **blog:** none, because no post carries this piece.
<: endif :><: if 'newsletter' in PLATFORMS :>- **newsletter:** none, because an issue shows a preview image or GIF, which a thumbnail brief makes, never a cut.
<: endif :><: endif :>