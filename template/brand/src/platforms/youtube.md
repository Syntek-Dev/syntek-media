# youtube.md — <%BRAND_NAME%> on YouTube

**Last Updated**: <%DATE%> **Version**: 0.1.0 **Maintained By**: <%OWNER_NAME%>
**Language**: British English (en_GB)

> **This file is a seeded stub, and it is deliberately unfinished.**
> It ships with the project so that the skills which route here point at something real from day one.
> Until `brand/workflows/04-set-up-a-platform/` has set up YouTube with the author, each section below holds an `AUTHOR TO CONFIRM` flag and no entries.

The brand's own choices for YouTube: the account, the deliverables it uses, and how it posts there.
YouTube's own facts (sizes, lengths, limits, codecs and its AI label) live in `toolkit/data/platforms.toml`, never here, and `publishing/docs/reference/youtube.md` says how they are applied.
`prepare-post` reads this file for every YouTube deliverable.
Removing youtube from the project's platforms deletes this file, filled in or not, so copy out anything you need first.

## Account

<!-- AUTHOR TO CONFIRM: the channel's handle and URL, exactly as YouTube shows them. -->

- **Handle:** —
- **URL:** —

## The social plan

Where syntek-author's social-media documents are present, whichever of them sets a value for this platform (the social media plan, the content calendar or an operating procedure) owns it, and the four sections below hold only what none sets.

## Cadence

<!-- AUTHOR TO CONFIRM: how often the brand publishes long videos and Shorts on YouTube, on which days and at what time (<%TIMEZONE%>), unless a social-media document sets it. -->

## Tone on this platform

<!-- AUTHOR TO CONFIRM: how the brand's spoken and written voice shifts on YouTube (shorter, warmer, plainer or more formal), unless a social-media document sets it. -->

## Call to action

<!-- AUTHOR TO CONFIRM: what a viewer is asked to do after a YouTube video or Short, in the brand's words, unless a social-media document sets it. -->

## Hashtag sets

<!-- AUTHOR TO CONFIRM: named sets of hashtags for YouTube descriptions, each set with the kind of piece it serves. -->

Count each set against `platform.youtube.hashtags_ignored_over` and `platform.youtube.hashtags_shown_by_title` in `toolkit/data/platforms.toml`, never against a number written here.

## Deliverables used

<!-- AUTHOR TO CONFIRM: which of YouTube's deliverables the brand uses; the keys `python3 toolkit/media.py presets` lists for it are at present `youtube.long`, `youtube.short`, `youtube.thumbnail`, `youtube.short_thumbnail` and `youtube.podcast_thumbnail`. -->

A brief names these keys in its `deliverables`, and a cut-down plan names them for each cut.
A key not listed here is not used, whatever `platforms.toml` offers.

## Overrides

Confirmed differences from `toolkit/data/platforms.toml` go in `brand/src/platforms/overrides.toml`, never here.
