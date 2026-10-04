# linkedin.md — <%BRAND_NAME%> on LinkedIn

**Last Updated**: <%DATE%> **Version**: 0.1.0 **Maintained By**: <%OWNER_NAME%>
**Language**: British English (en_GB)

> **This file is a seeded stub, and it is deliberately unfinished.**
> It ships with the project so that the skills which route here point at something real from day one.
> Until `brand/workflows/04-set-up-a-platform/` has set up LinkedIn with the author, each section below holds an `AUTHOR TO CONFIRM` flag and no entries.

The brand's own choices for LinkedIn: the account, the deliverables it uses, and how it posts there.
LinkedIn's own facts (sizes, lengths, limits, codecs and its AI label) live in `toolkit/data/platforms.toml`, never here, and `publishing/docs/reference/linkedin.md` says how they are applied.
`prepare-post` reads this file for every LinkedIn deliverable.
Removing linkedin from the project's platforms deletes this file, filled in or not, so copy out anything you need first.

## Account

<!-- AUTHOR TO CONFIRM: the page's or profile's name and URL, exactly as LinkedIn shows them. -->

- **Page or profile:** —
- **URL:** —

## The social plan

Where syntek-author's social-media documents are present, whichever of them sets a value for this platform (the social media plan, the content calendar or an operating procedure) owns it, and the four sections below hold only what none sets.

## Cadence

<!-- AUTHOR TO CONFIRM: how often the brand posts video on LinkedIn, on which days and at what time (<%TIMEZONE%>), unless a social-media document sets it. -->

## Tone on this platform

<!-- AUTHOR TO CONFIRM: how the brand's spoken and written voice shifts on LinkedIn (shorter, warmer, plainer or more formal), unless a social-media document sets it. -->

## Call to action

<!-- AUTHOR TO CONFIRM: what a viewer is asked to do after a LinkedIn video post, in the brand's words, unless a social-media document sets it. -->

## Hashtag sets

<!-- AUTHOR TO CONFIRM: named sets of hashtags for LinkedIn posts, each set with the kind of piece it serves. -->

Count each set against any hashtag key `toolkit/data/platforms.toml` gives this platform; where it gives none, none was published, and `prepare-post` keeps each set short.

## Deliverables used

<!-- AUTHOR TO CONFIRM: which of LinkedIn's deliverables the brand uses; the keys `python3 toolkit/media.py presets` lists for it are at present `linkedin.video_landscape` and `linkedin.video_vertical`. -->

A brief names these keys in its `deliverables`, and a cut-down plan names them for each cut.
A key not listed here is not used, whatever `platforms.toml` offers.

## Overrides

Confirmed differences from `toolkit/data/platforms.toml` go in `brand/src/platforms/overrides.toml`, never here.
