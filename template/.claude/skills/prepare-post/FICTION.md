# FICTION.md — prepare-post, fiction mode

The domain for packaging a novelist's trailers, teasers and readings for posting: the book's facts
exactly as the author gives them, nothing past the spoiler line, and every synthetic voice or
image said plainly.

## Paths and unit

- **Unit:** one piece; its package is `publishing/src/posts/<piece>.md`, one section per
  deliverable, every agreed cut included.
- **Procedures:** `publishing/workflows/05-prepare-a-post/` and
  `publishing/workflows/06-record-a-publication/`.
- **The social plan:** in a book project the platform profile holds it all:
  `brand/src/platforms/<platform>.md`, its `## Cadence`, `## Tone on this platform`,
  `## Call to action` and `## Hashtag sets`.
- **The book's facts:** the title, series, release or pre-order date and retailer links, as the
  author gives them; the blurb, wherever the author keeps it (in syntek-author's proposal layer,
  where present), for the spoiler line.
- **Guides:** `publishing/docs/reference/posting-and-the-log.md` and
  `publishing/docs/reference/ai-disclosure.md`.

## Additions to the steps

- **Step 2 — also** read the profile's hashtag sets and call to action for each platform; a
  platform whose profile still carries `AUTHOR TO CONFIRM` slots is asked about before its copy
  is drafted.
- **Step 4 — also** the book's title appears exactly as on its cover, the series name and number
  as the author gives them, and a release or pre-order date carries `<!-- VERIFY: … -->` until
  the author confirms it. Retailer links are only those the author gives. A review or an
  endorsement is quoted only when it was received and its writer agreed to be quoted. Nothing goes
  past the spoiler line, in the title, the description or the hashtags.
- **Step 5 — also** a designed or AI character voice, AI-generated art and a generated music bed
  are each disclosed; an audiobook sample follows the disclosure its own channel's rules give.
- **Step 7 — also** the cover art's and any commissioned art's rows cover social posting, and
  every font in the thumbnail its licence for it.

## Domain rules

- **Never past the spoiler line.** A post is seen by readers who have not reached the twist.
- **The book's facts are the author's.** A date, a price, a format or an edition is written as the
  author gives it and flagged until it is confirmed; nothing about the book is guessed.
- **Endorsements are real or absent.** No quoted praise, award or 'bestselling' claim that the
  author cannot show.
- **A character's line keeps its speaker.** A quoted line in a description is attributed to the
  character, never presented as the author's own view.

## Examples

An invented section of Morgan Example's post package for a teaser of an invented novel,
*The Lantern Weir*:

```markdown
## tiktok.video — c01

- **Title:** none: the platform has no title field.
- **Description:** the fenced block below.
- **Hashtags:** #fantasybooks #booktok #newbooks, inside the caption.
- **Disclosure:** AI label on, because the narrator is a designed AI voice and the guide's TikTok row requires a label for realistic AI-generated content (checked 03/10/2026). Description line: the fourth line below. On-screen line: 'AI narrator' on the end card.
- **Captions:** 002-the-lantern-weir-trailer--c01.en-GB.srt, burned.
- **Thumbnail:** 002-the-lantern-weir-trailer--c01.tiktok-video.png, uploaded as the cover.
- **Render:** 002-the-lantern-weir-trailer--c01.tiktok-video.burned.mp4
- **Calendar:** none: no social plan of syntek-author's in this project.
- **Scheduled:** 07/03/2027 19:00, <%TIMEZONE%>
- **Limits:** caption 220 against platform.tiktok.caption_max_chars
```

Its caption, one sentence per line:

```text
Every night someone lights the weir lantern.
Tonight, no one does.
The Lantern Weir, a novel by Morgan Example, is out in the spring.
The narrator's voice in this trailer is AI-generated.
#fantasybooks #booktok #newbooks
```
