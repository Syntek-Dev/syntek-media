---
type: guide
skills: [prepare-post, cut-for-platform]
model: opus
---

# YouTube — long videos, Shorts and thumbnails, by key

**Last Updated**: <%DATE%> **Version**: 0.1.0 **Maintained By**: <%OWNER_NAME%>
**Language**: British English (en_GB)

**What it is.** How this project's deliverables meet YouTube: the keys of
`toolkit/data/platforms.toml` each one reads, whether its captions are uploaded or burned in,
which thumbnail it takes, where YouTube's AI label lives, and the traps that cost an upload its
reach or its monetisation. Every limit is cited by key and read with
`python3 toolkit/media.py presets KEY`, overrides applied. The brand's own handle, cadence and
tone on YouTube live in its profile in `brand/src/platforms/`.

## Deliverables and their keys

| Deliverable | Key | Captions | Thumbnail |
|---|---|---|---|
| A long video | `youtube.long` | SRT sidecar, among its `caption_formats` | `youtube.thumbnail` |
| A Short | `youtube.short` | sidecar unconfirmed (`caption_formats` is in `verify`): burn in, or check first | `youtube.short_thumbnail` |
| An audio piece as video | `youtube.long`, made with `media.py still-video` | as a long video | `youtube.podcast_thumbnail` for a podcast playlist (no pixel size published: `width` and `height` are in `verify`) |

## Words

- Title and description: `platform.youtube.title_max_chars` and
  `platform.youtube.description_max_chars`.
- Hashtags: above `platform.youtube.hashtags_ignored_over`, YouTube ignores every hashtag on the
  upload; it shows `platform.youtube.hashtags_shown_by_title` of them by the title, chosen from
  the description, so the ones that matter go first.
- The disclosure line sits near the top of the description, where it is read without expanding.

## Disclosure

YouTube's label is the altered or synthetic content question, answered in YouTube Studio at
upload. Its rule, source and checked date are in `publishing/docs/reference/ai-disclosure.md`:
realistic content that AI made or altered needs it, and the owner's own cloned voice used for a
voiceover is exempt. The description line goes in either way.

## Traps

- **An unverified account** is held to `youtube.long.max_seconds_unverified`, far below
  `max_seconds`: check the account before planning a long talk as one upload.
- **Claimed music in a Short:** read the `notes` of `youtube.short`. A Short carrying music with
  a Content ID claim is blocked above a length shorter than the Short's own limit, so a cut with
  licensed music stays inside it, or uses music the brand owns.
- **The Short's safe zone** is Google's diagram for vertical ads, used as a proxy (`verify`):
  keep captions and titles clear of the right-hand controls and the bottom.
- **Frame rate:** YouTube asks for the source's own rate, so no preset forces one.
- **Inauthentic content:** near-identical batches of cuts threaten monetisation
  (`publishing/docs/reference/cut-downs.md`).

## How we apply it here

- Read `presets` for every key above before a render or a package, and name each `verify` key
  relied on in the hand-back.
- A long video's captions go up as its SRT sidecar; a Short's are burned in until its
  `caption_formats` is confirmed.
- An audio piece goes to YouTube as a still under its audio, with its own thumbnail.
- A podcast episode's upload, a talk's video or a still under the episode, goes into the show's
  podcast playlist by hand, and its package section adds **Playlist** (the podcast guides).

## Who implements it

- **Workflows:** `publishing/workflows/05-prepare-a-post/` writes the YouTube package;
  `publishing/workflows/02-cut-for-a-platform/` renders the deliverables against their presets.
- **Skills:** `prepare-post` keeps the words inside the keys and sets out the disclosure;
  `cut-for-platform` renders and verifies each deliverable.

## Governing standard

`.claude/rules/syntek-media/03-production-ethics.md` Section 5 owns disclosure and Section 7 owns
never fabricating a platform rule or limit. The rules own the requirement; this guide owns how
YouTube's keys and rules are applied to this project's deliverables.
