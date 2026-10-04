---
piece: 000-example-piece
approved: ""
---

<: if BRAND_KIND == 'business' :># One line before every meeting — post package

<!-- WORKED EXAMPLE: the post package of the example piece, one section per deliverable: the brief's full-length videos and the cut-down plan's stories.
     It is not approved, and it is never scheduled or posted: every render it names waits for a master that is never made.
     The brief's synthetic_voice, ai_visuals and music are all none, so every Disclosure bullet records that no label is set and no line is needed. -->
<: if 'podcast' in PLATFORMS :>
The podcast feed takes nothing from this piece: it has no episode, and a 30-second clip is not one.
<: endif :><: if 'website' in PLATFORMS :>
No page of the brand's websites places this piece: a 30-second vertical video is made for feeds, not for a page.
<: endif :><: if 'blog' in PLATFORMS :>
No blog post carries this piece: the brief places it in none.
<: endif :><: if 'newsletter' in PLATFORMS :>
No newsletter issue shows this piece: an issue's preview links to a page that plays the piece, and this one has none.
<: endif :><: if 'youtube' in PLATFORMS :>
## youtube.short

- **Title:** One line before every meeting
- **Description:**

  ```text
  Put the decision you need in the first line of the invite.
  If you can't write it, skip the meeting and send an email instead.
  Try it on your next invite, then tell us what changed.
  #meetings #smallbusiness #productivity
  ```

- **Hashtags:** #meetings #smallbusiness #productivity
- **Disclosure:** the altered or synthetic content setting ('AI use') off, because nothing in the piece is synthetic or AI-made, so the platform's rule does not ask for it (`publishing/docs/reference/ai-disclosure.md`) · no description line, because there is nothing to disclose · no spoken or on-screen line
- **Captions:** `000-example-piece.en-GB.srt` · burned, as the brief asks, because `platform.youtube.short.caption_formats` is a `verify` key
- **Thumbnail:** `000-example-piece.youtube-short-thumbnail.png`
- **Render:** `000-example-piece.youtube-short.burned.mp4`
- **Calendar:** none; the example never enters a content calendar or the schedule
- **Scheduled:** none; a real package gives DD/MM/YYYY HH:MM, <%TIMEZONE%>, and the example never enters `publishing/src/schedule.md`
- **Limits:** title 29 against `platform.youtube.title_max_chars` · description 219 against `platform.youtube.description_max_chars` · hashtags 3 against `platform.youtube.hashtags_ignored_over` · 30.0 seconds against `platform.youtube.short.max_seconds`
<: endif :><: if 'tiktok' in PLATFORMS :>
## tiktok.video

- **Title:** n/a, because the description below is the post's only text
- **Description:**

  ```text
  Put the decision you need in the first line of the invite.
  If you can't write it, skip the meeting and send an email instead.
  Try it on your next invite, then tell us what changed.
  #meetings #smallbusiness #productivity
  ```

- **Hashtags:** #meetings #smallbusiness #productivity
- **Disclosure:** 'AI-generated content' off, because nothing in the piece is synthetic or AI-made, so the platform's rule does not ask for it (`publishing/docs/reference/ai-disclosure.md`) · no description line, because there is nothing to disclose · no spoken or on-screen line
- **Captions:** `000-example-piece.en-GB.srt` · burned, as the brief asks, because `platform.tiktok.video.caption_formats` is empty
- **Thumbnail:** `000-example-piece.tiktok-video.png`, at the video's size because the platform has no thumbnail table
- **Render:** `000-example-piece.tiktok-video.burned.mp4`
- **Calendar:** none; the example never enters a content calendar or the schedule
- **Scheduled:** none; a real package gives DD/MM/YYYY HH:MM, <%TIMEZONE%>, and the example never enters `publishing/src/schedule.md`
- **Limits:** description 219 against `platform.tiktok.caption_max_chars` · 30.0 seconds against `platform.tiktok.video.max_seconds`, a `verify` key
<: endif :><: if 'instagram' in PLATFORMS :>
## instagram.reel

- **Title:** n/a, because the description below is the post's only text
- **Description:**

  ```text
  Put the decision you need in the first line of the invite.
  If you can't write it, skip the meeting and send an email instead.
  Try it on your next invite, then tell us what changed.
  #meetings #smallbusiness #productivity
  ```

- **Hashtags:** #meetings #smallbusiness #productivity
- **Disclosure:** 'AI info' off, because nothing in the piece is synthetic or AI-made, so the platform's rule does not ask for it (`publishing/docs/reference/ai-disclosure.md`) · no description line, because there is nothing to disclose · no spoken or on-screen line
- **Captions:** `000-example-piece.en-GB.srt` · burned, as the brief asks, because `platform.instagram.reel.caption_formats` is empty
- **Thumbnail:** `000-example-piece.instagram-reel-cover.jpg`, converted from the rendered PNG because `platform.instagram.reel_cover.formats` takes only JPEG
- **Render:** `000-example-piece.instagram-reel.burned.mp4`
- **Calendar:** none; the example never enters a content calendar or the schedule
- **Scheduled:** none; a real package gives DD/MM/YYYY HH:MM, <%TIMEZONE%>, and the example never enters `publishing/src/schedule.md`
- **Limits:** description 219 against `platform.instagram.caption_max_chars` · hashtags 3 against `platform.instagram.hashtags_max`, a `verify` key · 30.0 seconds between `platform.instagram.reel.min_seconds` and `platform.instagram.reel.max_seconds`

## instagram.story — c01

- **Title:** n/a, because a story carries no title
- **Description:** n/a, because nothing is pasted with a story: its words are its burned captions
- **Hashtags:** none
- **Disclosure:** 'AI info' off, because nothing in the piece is synthetic or AI-made, so the platform's rule does not ask for it (`publishing/docs/reference/ai-disclosure.md`) · no description line, because there is nothing to disclose · no spoken or on-screen line
- **Captions:** `000-example-piece--c01.en-GB.srt`, retimed from the master's · burned, because `platform.instagram.story.caption_formats` is empty
- **Thumbnail:** n/a, because `toolkit/data/platforms.toml` has no thumbnail table for a story
- **Render:** `000-example-piece--c01.instagram-story.burned.mp4`
- **Calendar:** none; the example never enters a content calendar or the schedule
- **Scheduled:** none; a real package gives DD/MM/YYYY HH:MM, <%TIMEZONE%>, and the example never enters `publishing/src/schedule.md`
- **Limits:** 15.0 seconds between `platform.instagram.story.min_seconds` and `platform.instagram.story.max_seconds`
<: endif :><: if 'linkedin' in PLATFORMS :>
## linkedin.video_vertical

- **Title:** n/a, because the description below is the post's only text
- **Description:**

  ```text
  Put the decision you need in the first line of the invite.
  If you can't write it, skip the meeting and send an email instead.
  Try it on your next invite, then tell us what changed.
  #meetings #smallbusiness #productivity
  ```

- **Hashtags:** #meetings #smallbusiness #productivity
- **Disclosure:** no label to set (no toggle documented on LinkedIn), and nothing in the piece is synthetic (`publishing/docs/reference/ai-disclosure.md`) · no description line, because there is nothing to disclose · no spoken or on-screen line
- **Captions:** `000-example-piece.en-GB.srt` · burned, as the brief asks, because `platform.linkedin.video_vertical.caption_formats` is a `verify` key
- **Thumbnail:** `000-example-piece.linkedin-video-vertical.png`, at the video's size because the platform has no thumbnail table
- **Render:** `000-example-piece.linkedin-video-vertical.burned.mp4`
- **Calendar:** none; the example never enters a content calendar or the schedule
- **Scheduled:** none; a real package gives DD/MM/YYYY HH:MM, <%TIMEZONE%>, and the example never enters `publishing/src/schedule.md`
- **Limits:** description 219 against `platform.linkedin.post_max_chars` · 30.0 seconds between `platform.linkedin.video_vertical.min_seconds` and `platform.linkedin.video_vertical.max_seconds`
<: endif :><: if 'facebook' in PLATFORMS :>
## facebook.reel

- **Title:** n/a, because the description below is the post's only text
- **Description:**

  ```text
  Put the decision you need in the first line of the invite.
  If you can't write it, skip the meeting and send an email instead.
  Try it on your next invite, then tell us what changed.
  #meetings #smallbusiness #productivity
  ```

- **Hashtags:** #meetings #smallbusiness #productivity
- **Disclosure:** 'AI info' off, because nothing in the piece is synthetic or AI-made, so the platform's rule does not ask for it (`publishing/docs/reference/ai-disclosure.md`) · no description line, because there is nothing to disclose · no spoken or on-screen line
- **Captions:** `000-example-piece.en-GB.srt` · burned, as the brief asks, because `platform.facebook.reel.caption_formats` is a `verify` key
- **Thumbnail:** `000-example-piece.facebook-reel.png`, at the video's size because the platform has no thumbnail table
- **Render:** `000-example-piece.facebook-reel.burned.mp4`
- **Calendar:** none; the example never enters a content calendar or the schedule
- **Scheduled:** none; a real package gives DD/MM/YYYY HH:MM, <%TIMEZONE%>, and the example never enters `publishing/src/schedule.md`
- **Limits:** description 219, and `platform.facebook` publishes no limit to count it against · 30.0 seconds over `platform.facebook.reel.min_seconds`, with no organic maximum published

## facebook.story — c02

- **Title:** n/a, because a story carries no title
- **Description:** n/a, because nothing is pasted with a story: its words are its burned captions
- **Hashtags:** none
- **Disclosure:** 'AI info' off, because nothing in the piece is synthetic or AI-made, so the platform's rule does not ask for it (`publishing/docs/reference/ai-disclosure.md`) · no description line, because there is nothing to disclose · no spoken or on-screen line
- **Captions:** `000-example-piece--c02.en-GB.srt`, retimed from the master's · burned, because `platform.facebook.story.caption_formats` is empty
- **Thumbnail:** n/a, because `toolkit/data/platforms.toml` has no thumbnail table for a story
- **Render:** `000-example-piece--c02.facebook-story.burned.mp4`
- **Calendar:** none; the example never enters a content calendar or the schedule
- **Scheduled:** none; a real package gives DD/MM/YYYY HH:MM, <%TIMEZONE%>, and the example never enters `publishing/src/schedule.md`
- **Limits:** 19.0 seconds between `platform.facebook.story.min_seconds` and `platform.facebook.story.max_seconds`
<: endif :><: elif BRAND_KIND == 'author-fiction' :># Count the stones — post package

<!-- WORKED EXAMPLE: the post package of the example piece, one section per deliverable: the brief's full-length videos and the cut-down plan's stories.
     It is not approved, and it is never scheduled or posted: every render it names waits for a master that is never made.
     The brief's synthetic_voice, ai_visuals and music are all none, so every Disclosure bullet records that no label is set and no line is needed. -->
<: if 'podcast' in PLATFORMS :>
The podcast feed takes nothing from this piece: it has no episode, and a 30-second clip is not one.
<: endif :><: if 'website' in PLATFORMS :>
No page of the brand's websites places this piece: a 30-second vertical video is made for feeds, not for a page.
<: endif :><: if 'blog' in PLATFORMS :>
No blog post carries this piece: the brief places it in none.
<: endif :><: if 'newsletter' in PLATFORMS :>
No newsletter issue shows this piece: an issue's preview links to a page that plays the piece, and this one has none.
<: endif :><: if 'youtube' in PLATFORMS :>
## youtube.short

- **Title:** Count the stones
- **Description:**

  ```text
  Count the stones, and the river lets you pass.
  Tonight Maren has to cross the ford in the dark.
  Follow to see the cover first.
  #fantasybooks #newnovel #comingsoon
  ```

- **Hashtags:** #fantasybooks #newnovel #comingsoon
- **Disclosure:** the altered or synthetic content setting ('AI use') off, because nothing in the piece is synthetic or AI-made, so the platform's rule does not ask for it (`publishing/docs/reference/ai-disclosure.md`) · no description line, because there is nothing to disclose · no spoken or on-screen line
- **Captions:** `000-example-piece.en-GB.srt` · burned, as the brief asks, because `platform.youtube.short.caption_formats` is a `verify` key
- **Thumbnail:** `000-example-piece.youtube-short-thumbnail.png`
- **Render:** `000-example-piece.youtube-short.burned.mp4`
- **Calendar:** none; the example never enters a content calendar or the schedule
- **Scheduled:** none; a real package gives DD/MM/YYYY HH:MM, <%TIMEZONE%>, and the example never enters `publishing/src/schedule.md`
- **Limits:** title 16 against `platform.youtube.title_max_chars` · description 162 against `platform.youtube.description_max_chars` · hashtags 3 against `platform.youtube.hashtags_ignored_over` · 30.0 seconds against `platform.youtube.short.max_seconds`
<: endif :><: if 'tiktok' in PLATFORMS :>
## tiktok.video

- **Title:** n/a, because the description below is the post's only text
- **Description:**

  ```text
  Count the stones, and the river lets you pass.
  Tonight Maren has to cross the ford in the dark.
  Follow to see the cover first.
  #fantasybooks #newnovel #comingsoon
  ```

- **Hashtags:** #fantasybooks #newnovel #comingsoon
- **Disclosure:** 'AI-generated content' off, because nothing in the piece is synthetic or AI-made, so the platform's rule does not ask for it (`publishing/docs/reference/ai-disclosure.md`) · no description line, because there is nothing to disclose · no spoken or on-screen line
- **Captions:** `000-example-piece.en-GB.srt` · burned, as the brief asks, because `platform.tiktok.video.caption_formats` is empty
- **Thumbnail:** `000-example-piece.tiktok-video.png`, at the video's size because the platform has no thumbnail table
- **Render:** `000-example-piece.tiktok-video.burned.mp4`
- **Calendar:** none; the example never enters a content calendar or the schedule
- **Scheduled:** none; a real package gives DD/MM/YYYY HH:MM, <%TIMEZONE%>, and the example never enters `publishing/src/schedule.md`
- **Limits:** description 162 against `platform.tiktok.caption_max_chars` · 30.0 seconds against `platform.tiktok.video.max_seconds`, a `verify` key
<: endif :><: if 'instagram' in PLATFORMS :>
## instagram.reel

- **Title:** n/a, because the description below is the post's only text
- **Description:**

  ```text
  Count the stones, and the river lets you pass.
  Tonight Maren has to cross the ford in the dark.
  Follow to see the cover first.
  #fantasybooks #newnovel #comingsoon
  ```

- **Hashtags:** #fantasybooks #newnovel #comingsoon
- **Disclosure:** 'AI info' off, because nothing in the piece is synthetic or AI-made, so the platform's rule does not ask for it (`publishing/docs/reference/ai-disclosure.md`) · no description line, because there is nothing to disclose · no spoken or on-screen line
- **Captions:** `000-example-piece.en-GB.srt` · burned, as the brief asks, because `platform.instagram.reel.caption_formats` is empty
- **Thumbnail:** `000-example-piece.instagram-reel-cover.jpg`, converted from the rendered PNG because `platform.instagram.reel_cover.formats` takes only JPEG
- **Render:** `000-example-piece.instagram-reel.burned.mp4`
- **Calendar:** none; the example never enters a content calendar or the schedule
- **Scheduled:** none; a real package gives DD/MM/YYYY HH:MM, <%TIMEZONE%>, and the example never enters `publishing/src/schedule.md`
- **Limits:** description 162 against `platform.instagram.caption_max_chars` · hashtags 3 against `platform.instagram.hashtags_max`, a `verify` key · 30.0 seconds between `platform.instagram.reel.min_seconds` and `platform.instagram.reel.max_seconds`

## instagram.story — c01

- **Title:** n/a, because a story carries no title
- **Description:** n/a, because nothing is pasted with a story: its words are its burned captions
- **Hashtags:** none
- **Disclosure:** 'AI info' off, because nothing in the piece is synthetic or AI-made, so the platform's rule does not ask for it (`publishing/docs/reference/ai-disclosure.md`) · no description line, because there is nothing to disclose · no spoken or on-screen line
- **Captions:** `000-example-piece--c01.en-GB.srt`, retimed from the master's · burned, because `platform.instagram.story.caption_formats` is empty
- **Thumbnail:** n/a, because `toolkit/data/platforms.toml` has no thumbnail table for a story
- **Render:** `000-example-piece--c01.instagram-story.burned.mp4`
- **Calendar:** none; the example never enters a content calendar or the schedule
- **Scheduled:** none; a real package gives DD/MM/YYYY HH:MM, <%TIMEZONE%>, and the example never enters `publishing/src/schedule.md`
- **Limits:** 15.0 seconds between `platform.instagram.story.min_seconds` and `platform.instagram.story.max_seconds`
<: endif :><: if 'linkedin' in PLATFORMS :>
## linkedin.video_vertical

- **Title:** n/a, because the description below is the post's only text
- **Description:**

  ```text
  Count the stones, and the river lets you pass.
  Tonight Maren has to cross the ford in the dark.
  Follow to see the cover first.
  #fantasybooks #newnovel #comingsoon
  ```

- **Hashtags:** #fantasybooks #newnovel #comingsoon
- **Disclosure:** no label to set (no toggle documented on LinkedIn), and nothing in the piece is synthetic (`publishing/docs/reference/ai-disclosure.md`) · no description line, because there is nothing to disclose · no spoken or on-screen line
- **Captions:** `000-example-piece.en-GB.srt` · burned, as the brief asks, because `platform.linkedin.video_vertical.caption_formats` is a `verify` key
- **Thumbnail:** `000-example-piece.linkedin-video-vertical.png`, at the video's size because the platform has no thumbnail table
- **Render:** `000-example-piece.linkedin-video-vertical.burned.mp4`
- **Calendar:** none; the example never enters a content calendar or the schedule
- **Scheduled:** none; a real package gives DD/MM/YYYY HH:MM, <%TIMEZONE%>, and the example never enters `publishing/src/schedule.md`
- **Limits:** description 162 against `platform.linkedin.post_max_chars` · 30.0 seconds between `platform.linkedin.video_vertical.min_seconds` and `platform.linkedin.video_vertical.max_seconds`
<: endif :><: if 'facebook' in PLATFORMS :>
## facebook.reel

- **Title:** n/a, because the description below is the post's only text
- **Description:**

  ```text
  Count the stones, and the river lets you pass.
  Tonight Maren has to cross the ford in the dark.
  Follow to see the cover first.
  #fantasybooks #newnovel #comingsoon
  ```

- **Hashtags:** #fantasybooks #newnovel #comingsoon
- **Disclosure:** 'AI info' off, because nothing in the piece is synthetic or AI-made, so the platform's rule does not ask for it (`publishing/docs/reference/ai-disclosure.md`) · no description line, because there is nothing to disclose · no spoken or on-screen line
- **Captions:** `000-example-piece.en-GB.srt` · burned, as the brief asks, because `platform.facebook.reel.caption_formats` is a `verify` key
- **Thumbnail:** `000-example-piece.facebook-reel.png`, at the video's size because the platform has no thumbnail table
- **Render:** `000-example-piece.facebook-reel.burned.mp4`
- **Calendar:** none; the example never enters a content calendar or the schedule
- **Scheduled:** none; a real package gives DD/MM/YYYY HH:MM, <%TIMEZONE%>, and the example never enters `publishing/src/schedule.md`
- **Limits:** description 162, and `platform.facebook` publishes no limit to count it against · 30.0 seconds over `platform.facebook.reel.min_seconds`, with no organic maximum published

## facebook.story — c02

- **Title:** n/a, because a story carries no title
- **Description:** n/a, because nothing is pasted with a story: its words are its burned captions
- **Hashtags:** none
- **Disclosure:** 'AI info' off, because nothing in the piece is synthetic or AI-made, so the platform's rule does not ask for it (`publishing/docs/reference/ai-disclosure.md`) · no description line, because there is nothing to disclose · no spoken or on-screen line
- **Captions:** `000-example-piece--c02.en-GB.srt`, retimed from the master's · burned, because `platform.facebook.story.caption_formats` is empty
- **Thumbnail:** n/a, because `toolkit/data/platforms.toml` has no thumbnail table for a story
- **Render:** `000-example-piece--c02.facebook-story.burned.mp4`
- **Calendar:** none; the example never enters a content calendar or the schedule
- **Scheduled:** none; a real package gives DD/MM/YYYY HH:MM, <%TIMEZONE%>, and the example never enters `publishing/src/schedule.md`
- **Limits:** 19.0 seconds between `platform.facebook.story.min_seconds` and `platform.facebook.story.max_seconds`
<: endif :><: else :># The second visit — post package

<!-- WORKED EXAMPLE: the post package of the example piece, one section per deliverable: the brief's full-length videos and the cut-down plan's stories.
     It is not approved, and it is never scheduled or posted: every render it names waits for a master that is never made.
     The brief's synthetic_voice, ai_visuals and music are all none, so every Disclosure bullet records that no label is set and no line is needed. -->
<: if 'podcast' in PLATFORMS :>
The podcast feed takes nothing from this piece: it has no episode, and a 30-second clip is not one.
<: endif :><: if 'website' in PLATFORMS :>
No page of the brand's websites places this piece: a 30-second vertical video is made for feeds, not for a page.
<: endif :><: if 'blog' in PLATFORMS :>
No blog post carries this piece: the brief places it in none.
<: endif :><: if 'newsletter' in PLATFORMS :>
No newsletter issue shows this piece: an issue's preview links to a page that plays the piece, and this one has none.
<: endif :><: if 'youtube' in PLATFORMS :>
## youtube.short

- **Title:** The second visit
- **Description:**

  ```text
  Making a newcomer welcome once is the easy part.
  The real test is the second visit.
  A welcome is finished only when they're expected back.
  #community #belonging #welcome
  ```

- **Hashtags:** #community #belonging #welcome
- **Disclosure:** the altered or synthetic content setting ('AI use') off, because nothing in the piece is synthetic or AI-made, so the platform's rule does not ask for it (`publishing/docs/reference/ai-disclosure.md`) · no description line, because there is nothing to disclose · no spoken or on-screen line
- **Captions:** `000-example-piece.en-GB.srt` · burned, as the brief asks, because `platform.youtube.short.caption_formats` is a `verify` key
- **Thumbnail:** `000-example-piece.youtube-short-thumbnail.png`
- **Render:** `000-example-piece.youtube-short.burned.mp4`
- **Calendar:** none; the example never enters a content calendar or the schedule
- **Scheduled:** none; a real package gives DD/MM/YYYY HH:MM, <%TIMEZONE%>, and the example never enters `publishing/src/schedule.md`
- **Limits:** title 16 against `platform.youtube.title_max_chars` · description 169 against `platform.youtube.description_max_chars` · hashtags 3 against `platform.youtube.hashtags_ignored_over` · 30.0 seconds against `platform.youtube.short.max_seconds`
<: endif :><: if 'tiktok' in PLATFORMS :>
## tiktok.video

- **Title:** n/a, because the description below is the post's only text
- **Description:**

  ```text
  Making a newcomer welcome once is the easy part.
  The real test is the second visit.
  A welcome is finished only when they're expected back.
  #community #belonging #welcome
  ```

- **Hashtags:** #community #belonging #welcome
- **Disclosure:** 'AI-generated content' off, because nothing in the piece is synthetic or AI-made, so the platform's rule does not ask for it (`publishing/docs/reference/ai-disclosure.md`) · no description line, because there is nothing to disclose · no spoken or on-screen line
- **Captions:** `000-example-piece.en-GB.srt` · burned, as the brief asks, because `platform.tiktok.video.caption_formats` is empty
- **Thumbnail:** `000-example-piece.tiktok-video.png`, at the video's size because the platform has no thumbnail table
- **Render:** `000-example-piece.tiktok-video.burned.mp4`
- **Calendar:** none; the example never enters a content calendar or the schedule
- **Scheduled:** none; a real package gives DD/MM/YYYY HH:MM, <%TIMEZONE%>, and the example never enters `publishing/src/schedule.md`
- **Limits:** description 169 against `platform.tiktok.caption_max_chars` · 30.0 seconds against `platform.tiktok.video.max_seconds`, a `verify` key
<: endif :><: if 'instagram' in PLATFORMS :>
## instagram.reel

- **Title:** n/a, because the description below is the post's only text
- **Description:**

  ```text
  Making a newcomer welcome once is the easy part.
  The real test is the second visit.
  A welcome is finished only when they're expected back.
  #community #belonging #welcome
  ```

- **Hashtags:** #community #belonging #welcome
- **Disclosure:** 'AI info' off, because nothing in the piece is synthetic or AI-made, so the platform's rule does not ask for it (`publishing/docs/reference/ai-disclosure.md`) · no description line, because there is nothing to disclose · no spoken or on-screen line
- **Captions:** `000-example-piece.en-GB.srt` · burned, as the brief asks, because `platform.instagram.reel.caption_formats` is empty
- **Thumbnail:** `000-example-piece.instagram-reel-cover.jpg`, converted from the rendered PNG because `platform.instagram.reel_cover.formats` takes only JPEG
- **Render:** `000-example-piece.instagram-reel.burned.mp4`
- **Calendar:** none; the example never enters a content calendar or the schedule
- **Scheduled:** none; a real package gives DD/MM/YYYY HH:MM, <%TIMEZONE%>, and the example never enters `publishing/src/schedule.md`
- **Limits:** description 169 against `platform.instagram.caption_max_chars` · hashtags 3 against `platform.instagram.hashtags_max`, a `verify` key · 30.0 seconds between `platform.instagram.reel.min_seconds` and `platform.instagram.reel.max_seconds`

## instagram.story — c01

- **Title:** n/a, because a story carries no title
- **Description:** n/a, because nothing is pasted with a story: its words are its burned captions
- **Hashtags:** none
- **Disclosure:** 'AI info' off, because nothing in the piece is synthetic or AI-made, so the platform's rule does not ask for it (`publishing/docs/reference/ai-disclosure.md`) · no description line, because there is nothing to disclose · no spoken or on-screen line
- **Captions:** `000-example-piece--c01.en-GB.srt`, retimed from the master's · burned, because `platform.instagram.story.caption_formats` is empty
- **Thumbnail:** n/a, because `toolkit/data/platforms.toml` has no thumbnail table for a story
- **Render:** `000-example-piece--c01.instagram-story.burned.mp4`
- **Calendar:** none; the example never enters a content calendar or the schedule
- **Scheduled:** none; a real package gives DD/MM/YYYY HH:MM, <%TIMEZONE%>, and the example never enters `publishing/src/schedule.md`
- **Limits:** 15.0 seconds between `platform.instagram.story.min_seconds` and `platform.instagram.story.max_seconds`
<: endif :><: if 'linkedin' in PLATFORMS :>
## linkedin.video_vertical

- **Title:** n/a, because the description below is the post's only text
- **Description:**

  ```text
  Making a newcomer welcome once is the easy part.
  The real test is the second visit.
  A welcome is finished only when they're expected back.
  #community #belonging #welcome
  ```

- **Hashtags:** #community #belonging #welcome
- **Disclosure:** no label to set (no toggle documented on LinkedIn), and nothing in the piece is synthetic (`publishing/docs/reference/ai-disclosure.md`) · no description line, because there is nothing to disclose · no spoken or on-screen line
- **Captions:** `000-example-piece.en-GB.srt` · burned, as the brief asks, because `platform.linkedin.video_vertical.caption_formats` is a `verify` key
- **Thumbnail:** `000-example-piece.linkedin-video-vertical.png`, at the video's size because the platform has no thumbnail table
- **Render:** `000-example-piece.linkedin-video-vertical.burned.mp4`
- **Calendar:** none; the example never enters a content calendar or the schedule
- **Scheduled:** none; a real package gives DD/MM/YYYY HH:MM, <%TIMEZONE%>, and the example never enters `publishing/src/schedule.md`
- **Limits:** description 169 against `platform.linkedin.post_max_chars` · 30.0 seconds between `platform.linkedin.video_vertical.min_seconds` and `platform.linkedin.video_vertical.max_seconds`
<: endif :><: if 'facebook' in PLATFORMS :>
## facebook.reel

- **Title:** n/a, because the description below is the post's only text
- **Description:**

  ```text
  Making a newcomer welcome once is the easy part.
  The real test is the second visit.
  A welcome is finished only when they're expected back.
  #community #belonging #welcome
  ```

- **Hashtags:** #community #belonging #welcome
- **Disclosure:** 'AI info' off, because nothing in the piece is synthetic or AI-made, so the platform's rule does not ask for it (`publishing/docs/reference/ai-disclosure.md`) · no description line, because there is nothing to disclose · no spoken or on-screen line
- **Captions:** `000-example-piece.en-GB.srt` · burned, as the brief asks, because `platform.facebook.reel.caption_formats` is a `verify` key
- **Thumbnail:** `000-example-piece.facebook-reel.png`, at the video's size because the platform has no thumbnail table
- **Render:** `000-example-piece.facebook-reel.burned.mp4`
- **Calendar:** none; the example never enters a content calendar or the schedule
- **Scheduled:** none; a real package gives DD/MM/YYYY HH:MM, <%TIMEZONE%>, and the example never enters `publishing/src/schedule.md`
- **Limits:** description 169, and `platform.facebook` publishes no limit to count it against · 30.0 seconds over `platform.facebook.reel.min_seconds`, with no organic maximum published

## facebook.story — c02

- **Title:** n/a, because a story carries no title
- **Description:** n/a, because nothing is pasted with a story: its words are its burned captions
- **Hashtags:** none
- **Disclosure:** 'AI info' off, because nothing in the piece is synthetic or AI-made, so the platform's rule does not ask for it (`publishing/docs/reference/ai-disclosure.md`) · no description line, because there is nothing to disclose · no spoken or on-screen line
- **Captions:** `000-example-piece--c02.en-GB.srt`, retimed from the master's · burned, because `platform.facebook.story.caption_formats` is empty
- **Thumbnail:** n/a, because `toolkit/data/platforms.toml` has no thumbnail table for a story
- **Render:** `000-example-piece--c02.facebook-story.burned.mp4`
- **Calendar:** none; the example never enters a content calendar or the schedule
- **Scheduled:** none; a real package gives DD/MM/YYYY HH:MM, <%TIMEZONE%>, and the example never enters `publishing/src/schedule.md`
- **Limits:** 19.0 seconds between `platform.facebook.story.min_seconds` and `platform.facebook.story.max_seconds`
<: endif :><: endif :>