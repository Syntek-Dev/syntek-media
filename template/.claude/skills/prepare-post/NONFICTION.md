# NONFICTION.md — prepare-post, non-fiction mode

The domain for packaging a non-fiction author's talks, podcast episodes and explainers for
posting: claims and quotations with their sources, guests who agreed to be shown, and a podcast's
disclosure in the audio as well as the notes.

## Paths and unit

- **Unit:** one piece; its package is `publishing/src/posts/<piece>.md`, one section per
  deliverable, every agreed cut included.
- **Procedures:** `publishing/workflows/05-prepare-a-post/` and
  `publishing/workflows/06-record-a-publication/`.
- **The social plan:** in a book project the platform profile holds it all:
  `brand/src/platforms/<platform>.md`, its cadence, tone, call to action and hashtag sets.
- **Sources:** the script's or transcript's sources, and the book's, in syntek-author's content and
  research layers, where present; read, never edited.
- **Guides:** `publishing/docs/reference/posting-and-the-log.md`,
  `publishing/docs/reference/ai-disclosure.md`, `production/docs/reference/rights-and-consent.md`,
  and the podcast guide in `publishing/docs/reference/`, where the project posts podcasts.

## Additions to the steps

- **Step 1 — also** for a podcast episode, the deliverables are the feed's audio
  (`podcast.feed_audio` for a show served from the brand's own feed) and any video platform's
  still-video, the talk's own video or clips; the show's own description is not the piece's, but
  it must carry the disclosure too.
- **Step 4 — also** a quotation in a description keeps its author and source; a scripture
  reference keeps its translation, credited as that translation's permission requires
  (`<!-- VERIFY: … -->` until the row says how). A guest is named and linked only as the guest
  agreed, and the episode notes say what the episode claims, never more.
- **Step 7 — also** for a podcast, check the master carries the spoken disclosure at the point the
  synthetic voice begins, and that the show description carries it; where the show description
  does not, the hand-over asks the author to add it before the episode is `ready`.
- **Step 9 — also** every guest heard or shown has a `cleared` row that covers this platform, and
  every quotation or scripture reading heard in the piece has its row.

## Domain rules

- **A claim travels with its source.** A description never states the piece's argument more
  strongly than the piece does, and a contested claim keeps its 'I argue' or 'some hold'.
- **Quotations and scripture are credited as their permissions require.** A translation's credit
  line is copied exactly as its permission asks.
- **Guests agree to each use.** The recording, the clips and the thumbnail are separate uses, and
  the guest's row says which are covered.
- **A podcast discloses where it is heard.** The spoken line, the episode notes and the show
  description, every one of them, wherever a synthetic voice is used.

## Examples

An invented section of Robin Example's post package for a podcast episode:

```markdown
## podcast.apple_rss_audio

- **Title:** The long table, part 3: who gets a seat?
- **Description:** the fenced block below.
- **Hashtags:** none: the platform uses none.
- **Disclosure:** no platform toggle; the guide's Apple Podcasts row asks for disclosure in the audio and the metadata (checked 03/10/2026). Spoken line at 00:00:02.000: 'Our introduction is read by an AI voice.' Description line: the second line below. Show description: carries the line. <!-- AUTHOR TO CONFIRM: show description updated? -->
- **Captions:** none: transcript not asked for in the brief.
- **Thumbnail:** 007-the-long-table-episode-3.podcast-episode-art.png
- **Render:** 007-the-long-table-episode-3.podcast-apple-rss-audio.m4a
- **Calendar:** none: no social plan of syntek-author's in this project.
- **Scheduled:** 21/01/2027 06:00, <%TIMEZONE%>
- **Limits:** no title or description key for this deliverable in platforms.toml: title 40, description 253, recorded.
```

Its description, one sentence per line:

```text
Robin Example asks why an open table is harder, and better, than a full one.
The introduction to this episode is read by an AI voice.
Hebrews 13:2 is read from [translation], used by permission.
Chapter 3 of The Long Table is the basis for this episode.
```
