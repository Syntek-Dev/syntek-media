# instagram.md — <%BRAND_NAME%> on Instagram

**Last Updated**: <%DATE%> **Version**: 0.1.0 **Maintained By**: <%OWNER_NAME%>
**Language**: British English (en_GB)

> **This file is a seeded stub, and it is deliberately unfinished.**
> It ships with the project so that the skills which route here point at something real from day one.
> Until `brand/workflows/04-set-up-a-platform/` has set up Instagram with the author, each section below holds an `AUTHOR TO CONFIRM` flag and no entries.

The brand's own choices for Instagram: the account, the deliverables it uses, and how it posts there.
Instagram's own facts (sizes, lengths, limits, codecs and its AI label) live in `toolkit/data/platforms.toml`, never here, and `publishing/docs/reference/instagram.md` says how they are applied.
`prepare-post` reads this file for every Instagram deliverable.
Removing instagram from the project's platforms deletes this file, filled in or not, so copy out anything you need first.

## Account

<!-- AUTHOR TO CONFIRM: the account's handle and URL, exactly as Instagram shows them. -->

- **Handle:** —
- **URL:** —

## The social plan

Where syntek-author's social-media documents are present, whichever of them sets a value for this platform (the social media plan, the content calendar or an operating procedure) owns it, and the four sections below hold only what none sets.

## Cadence

<!-- AUTHOR TO CONFIRM: how often the brand posts reels and stories on Instagram, on which days and at what time (<%TIMEZONE%>), unless a social-media document sets it. -->

## Tone on this platform

<!-- AUTHOR TO CONFIRM: how the brand's spoken and written voice shifts on Instagram (shorter, warmer, plainer or more formal), unless a social-media document sets it. -->

## Call to action

<!-- AUTHOR TO CONFIRM: what a viewer is asked to do after an Instagram reel or story, in the brand's words, unless a social-media document sets it. -->

## Hashtag sets

<!-- AUTHOR TO CONFIRM: named sets of hashtags for Instagram captions, each set with the kind of piece it serves. -->

Count each set against `platform.instagram.hashtags_max` in `toolkit/data/platforms.toml`, a value still to be verified, above which `prepare-post` warns; never against a number written here.

## Deliverables used

<!-- AUTHOR TO CONFIRM: which of Instagram's deliverables the brand uses; the keys `python3 toolkit/media.py presets` lists for it are at present `instagram.reel`, `instagram.story`, `instagram.reel_cover` and `instagram.feed_image`. -->

A brief names these keys in its `deliverables`, and a cut-down plan names them for each cut.
A key not listed here is not used, whatever `platforms.toml` offers.

## Overrides

Confirmed differences from `toolkit/data/platforms.toml` go in `brand/src/platforms/overrides.toml`, never here.
