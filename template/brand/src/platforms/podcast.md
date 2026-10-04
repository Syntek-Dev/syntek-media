# podcast.md — <%BRAND_NAME%> as a podcast

**Last Updated**: <%DATE%> **Version**: 0.1.0 **Maintained By**: <%OWNER_NAME%>
**Language**: British English (en_GB)

> **This file is a seeded stub, and it is deliberately unfinished.**
> It ships with the project so that the skills which route here point at something real from day one.
> Until `brand/workflows/04-set-up-a-platform/` has set up the podcast with the author, each section below holds an `AUTHOR TO CONFIRM` flag and no entries.

The brand's own choices for its podcast: the account, the deliverables it uses, and how it posts there.
The podcast platforms' own facts (audio formats, loudness, artwork sizes and their AI labels) live in `toolkit/data/platforms.toml`, never here, and `publishing/docs/reference/podcast.md` says how they are applied.
`prepare-post` reads this file for every podcast deliverable.
Removing podcast from the project's platforms deletes this file, filled in or not, so copy out anything you need first.

## Account

<!-- AUTHOR TO CONFIRM: the show's name, its RSS feed URL and its listing URLs on Apple Podcasts and Spotify, exactly as each shows them. -->

- **Show name:** —
- **Feed URL:** —
- **Apple Podcasts:** —
- **Spotify:** —

## The social plan

Where syntek-author's social media plan is present, it owns cadence, tone, call to action, hashtags and bios, and the four sections below hold only what it lacks.

## Cadence

<!-- AUTHOR TO CONFIRM: how often an episode is released, on which day and at what time (<%TIMEZONE%>), and how seasons are numbered, unless the social media plan sets it. -->

## Tone on this platform

<!-- AUTHOR TO CONFIRM: how the brand's spoken and written voice shifts on the podcast (shorter, warmer, plainer or more formal), unless the social media plan sets it. -->

## Call to action

<!-- AUTHOR TO CONFIRM: what a listener is asked to do after a podcast episode, in the brand's words, unless the social media plan sets it. -->

## Hashtag sets

<!-- AUTHOR TO CONFIRM: whether the show uses hashtags at all, and if so where. -->

A feed has no use for hashtags: they belong to the posts on other platforms that promote an episode, so this section usually stays empty.

## Deliverables used

<!-- AUTHOR TO CONFIRM: which of the podcast's deliverables the brand uses; the keys `python3 toolkit/media.py presets` lists for it are at present `podcast.apple_rss_audio`, `podcast.apple_connect_audio`, `podcast.spotify_audio`, `podcast.cover` and `podcast.episode_art`. -->

A brief names these keys in its `deliverables`, and a cut-down plan names them for each cut.
A key not listed here is not used, whatever `platforms.toml` offers.

## Overrides

Confirmed differences from `toolkit/data/platforms.toml` go in `brand/src/platforms/overrides.toml`, never here.
