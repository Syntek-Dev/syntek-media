---
type: guide
skills: [prepare-post, cut-for-platform]
model: opus
---

# LinkedIn — landscape and vertical video, clear edges and no thumbnail table

**Last Updated**: <%DATE%> **Version**: 0.1.0 **Maintained By**: <%OWNER_NAME%>
**Language**: British English (en_GB)

**What it is.** How this project's deliverables meet LinkedIn: the keys of
`toolkit/data/platforms.toml` each one reads, how its captions travel, why its thumbnail is
rendered at the video's own size, and how disclosure works on a platform with no AI toggle.
LinkedIn publishes ranges rather than targets, so its sizes and codecs are house choices inside
those ranges (`chosen`). Every limit is cited by key and read with
`python3 toolkit/media.py presets KEY`, overrides applied. The brand's own handle, cadence and
tone on LinkedIn live in its profile in `brand/src/platforms/`.

## Deliverables and their keys

| Deliverable | Key | Captions | Thumbnail |
|---|---|---|---|
| A landscape video | `linkedin.video_landscape` | SRT sidecar, reported but unconfirmed (`verify`) | no table: the video's size, `VERIFY` |
| A vertical video | `linkedin.video_vertical` | SRT sidecar, reported but unconfirmed (`verify`) | no table: the video's size, `VERIFY` |

- Both tables give a length range, a frame-rate range and a bitrate range; a cut is planned
  inside them, and `media.py cut` verifies its length against `max_seconds`.

## Words

- The post text is held to `platform.linkedin.post_max_chars`, and the disclosure line is part of
  it.
- LinkedIn's table has no title or hashtag keys: a title, where the uploader asks for one, is the
  package's **Title**, kept short; hashtags follow the brand's profile, or the social media plan
  where syntek-author's is present.

## Thumbnails and safe edges

- No thumbnail size is published, so `thumbnail-brief` renders at the video deliverable's own
  size, flagged `VERIFY` in the brief, until a size is confirmed and added as an override.
- No safe-zone numbers are published either: LinkedIn asks only that the edges are kept clear of
  key elements. The table has no `safe_zone`, so keep titles and captions well inside every edge.

## Disclosure

LinkedIn documents no AI toggle. Its policy forbids synthetic or manipulated media that shows a
person saying or doing something they did not, without clear disclosure; the rule, source and
checked date are in `publishing/docs/reference/ai-disclosure.md`. Whether an owner's own cloned
voice reading the owner's own script falls under it is `VERIFY`; the description line in the post
text covers it either way. Files signed with Content Credentials show LinkedIn's own icon.

## Traps

- **An old help page:** the video page was about two years old when it was checked; read the
  `notes` of each table, and re-check before relying on a limit near its edge.
- **Captions on mobile:** the SRT upload is documented by third parties for desktop only; burn
  captions in where the author posts from a phone.

## How we apply it here

- Read `presets` for both keys before a render or a package, and name each `verify` key relied on.
- Treat the thumbnail as unconfirmed every time, and say so in the hand-back.

## Who implements it

- **Workflows:** `publishing/workflows/05-prepare-a-post/` writes the LinkedIn package;
  `publishing/workflows/02-cut-for-a-platform/` renders the deliverables against their presets.
- **Skills:** `prepare-post` keeps the post text inside its key and writes the disclosure line;
  `cut-for-platform` renders and verifies each deliverable.

## Governing standard

`.claude/rules/syntek-media/03-production-ethics.md` Section 5 owns disclosure and Section 7 owns
never fabricating a platform rule or limit. The rules own the requirement; this guide owns how
LinkedIn's keys and rules are applied to this project's deliverables.
