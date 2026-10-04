---
type: guide
skills: [prepare-post, cut-for-platform]
model: opus
---

# Facebook — every video a reel; feed and story values from the ads guide

**Last Updated**: <%DATE%> **Version**: 0.1.0 **Maintained By**: <%OWNER_NAME%>
**Language**: British English (en_GB)

**What it is.** How this project's deliverables meet Facebook: the keys of
`toolkit/data/platforms.toml` each one reads, how its captions travel, why its thumbnail is
rendered at the video's own size, and where Meta's AI label lives. Since 17/06/2025 every video
posted to Facebook is posted as a reel, so the reel is the deliverable that matters; the feed and
story tables hold values from Meta's ads guide, the only published source. Every limit is cited by
key and read with `python3 toolkit/media.py presets KEY`, overrides applied. The brand's own
handle, cadence and tone on Facebook live in its profile in `brand/src/platforms/`.

## Deliverables and their keys

| Deliverable | Key | Captions | Thumbnail |
|---|---|---|---|
| A reel (any organic video) | `facebook.reel` | SRT sidecar, unconfirmed (`verify`) | no table: the video's size, `VERIFY` |
| A feed video (ads-guide values) | `facebook.feed_video` | SRT sidecar, unconfirmed (`verify`) | no table: the video's size, `VERIFY` |
| A story | `facebook.story` | burned in: its `caption_formats` is empty (and in `verify`) | none |

- `facebook.reel.api_max_seconds` binds only uploads made through Meta's publishing API; an
  upload the author makes by hand has no published length limit.
- The reel's safe zone is Meta's one guidance for every vertical placement (`verify`).

## Words

- No limit on a post's text was found: `platform.facebook` names `caption_max_chars` in `verify`
  and has no value. Keep the text as short as the post needs, and the disclosure line in it.
- Hashtags follow the brand's profile, or the social media plan where syntek-author's is present.

## Disclosure

Meta's label is 'AI info', set when posting, under the same rule as Instagram's; the rule, source
and checked date are in `publishing/docs/reference/ai-disclosure.md`. A reel narrated with a
realistic AI-generated voiceover needs it.

## Traps

- **The story's safe zone disagrees with itself:** Meta's pixel figures and its percentages give
  different margins at the table's size. Read the `notes` of `facebook.story`, and follow the
  percentages.
- **Caption file names:** the reported SRT naming convention comes from third parties only.
  Upload a sidecar where the uploader offers one, check it plays, and burn in where it does not.
- **Ads values are not organic values:** the feed table's length and file size are the ads
  guide's; an organic upload is a reel.

## How we apply it here

- Read `presets` for every key above before a render or a package, and name each `verify` key
  relied on in the hand-back.
- Treat the thumbnail as unconfirmed every time, and say so in the hand-back.

## Who implements it

- **Workflows:** `publishing/workflows/05-prepare-a-post/` writes the Facebook package;
  `publishing/workflows/02-cut-for-a-platform/` renders the deliverables against their presets.
- **Skills:** `prepare-post` writes the post text and sets out the disclosure; `cut-for-platform`
  renders and verifies each deliverable.

## Governing standard

`.claude/rules/syntek-media/03-production-ethics.md` Section 5 owns disclosure and Section 7 owns
never fabricating a platform rule or limit. The rules own the requirement; this guide owns how
Facebook's keys and rules are applied to this project's deliverables.
