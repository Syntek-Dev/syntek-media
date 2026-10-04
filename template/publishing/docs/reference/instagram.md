---
type: guide
skills: [prepare-post, cut-for-platform]
model: opus
---

# Instagram — reels, stories and covers; the hashtag cap and the grid crop

**Last Updated**: <%DATE%> **Version**: 0.1.0 **Maintained By**: <%OWNER_NAME%>
**Language**: British English (en_GB)

**What it is.** How this project's deliverables meet Instagram: the keys of
`toolkit/data/platforms.toml` each one reads, why its captions are burned in, how a reel cover
survives the profile grid, where Meta's AI label lives, and the two limits Instagram changed
recently enough that neither is yet in its own documentation. Every limit is cited by key and
read with `python3 toolkit/media.py presets KEY`, overrides applied. The brand's own handle,
cadence and tone on Instagram live in its profile in `brand/src/platforms/`.

## Deliverables and their keys

| Deliverable | Key | Captions | Cover |
|---|---|---|---|
| A reel | `instagram.reel` | burned in: its `caption_formats` is empty (and in `verify`) | `instagram.reel_cover` |
| A story | `instagram.story` | burned in, as a reel | none |
| A feed image | `instagram.feed_image` | none | the image itself |

- A reel's size is a house choice inside Instagram's range (`chosen`), and its safe zone comes
  from Meta's published percentages for the top, the bottom and the sides.
- A reel longer than `instagram.reel.max_seconds_reach` is reported to reach fewer people who do
  not already follow the account; that value is in `verify`.

## Words

- The caption is held to `platform.instagram.caption_max_chars`, and mentions to
  `platform.instagram.mentions_max`.
- Hashtags: `prepare-post` warns above `platform.instagram.hashtags_max`. That cap was reported in
  the press while Meta's own API documentation still gave a higher figure, so it is in `verify`.
- The disclosure line goes in the caption, as on every platform.

## The grid crop

The profile grid shows a reel's cover cropped to `platform.instagram.grid_aspect`, a value from a
public announcement rather than a help page (`verify`). `thumbnail-brief` keeps every word of the
cover's title inside that crop, so the cover reads in the reel and on the grid.

## Disclosure

Meta's label is 'AI info', set when posting. Its rule, source and checked date are in
`publishing/docs/reference/ai-disclosure.md`: realistic-sounding audio or photorealistic video
made or altered digitally needs it, and Meta names a reel narrated with a realistic AI-generated
voiceover as an example. Still images do not need it, though Meta may label them itself.

## Traps

- **Edit lists and the moov atom:** Meta's specification asks for no edit lists and the index at
  the front of the file; the toolkit's presets write it that way, a file made elsewhere may not.
- **Sidecar captions:** none is documented, so a reel without burned captions is uncaptioned.
- **Two sizes for one reel:** the API's limits and the ads guide's differ; the table holds the
  API's, which is the route an upload takes.

## How we apply it here

- Read `presets` for every key above before a render or a package, and name each `verify` key
  relied on in the hand-back.
- Burn captions into every reel and story; check the cover at grid size before it is approved.

## Who implements it

- **Workflows:** `publishing/workflows/05-prepare-a-post/` writes the Instagram package;
  `publishing/workflows/02-cut-for-a-platform/` renders the deliverables with captions burned.
- **Skills:** `prepare-post` keeps the words inside the keys and sets out the disclosure;
  `cut-for-platform` renders and verifies each deliverable.

## Governing standard

`.claude/rules/syntek-media/03-production-ethics.md` Section 5 owns disclosure and Section 7 owns
never fabricating a platform rule or limit. The rules own the requirement; this guide owns how
Instagram's keys and rules are applied to this project's deliverables.
