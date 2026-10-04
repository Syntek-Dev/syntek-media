# podcast.md — <%BRAND_NAME%> as a podcast

**Last Updated**: <%DATE%> **Version**: 0.1.0 **Maintained By**: <%OWNER_NAME%>
**Language**: British English (en_GB)

> **This file is a seeded stub, and it is deliberately unfinished.**
> It ships with the project so that the skills which route here point at something real from day one.
> Until `brand/workflows/04-set-up-a-platform/` has set up the podcast with the author, each section below holds an `AUTHOR TO CONFIRM` flag and no entries.

The brand's own choices for its podcast: the account, the deliverables it uses, and how it posts there.
The podcast platforms' own facts (audio formats, loudness, artwork sizes and their AI labels) live in `toolkit/data/platforms.toml`, never here, and `publishing/docs/reference/podcast.md` says how they are applied.
A self-hosted show's feed values (its title, author, owner, category, description, cover, feed URL and identity) live in its show register in `publishing/src/podcast/`, never here, and `publishing/docs/reference/podcast-feed.md` says how the feed is made.
`prepare-post` reads this file for every podcast deliverable.
Removing podcast from the project's platforms deletes this file, filled in or not, so copy out anything you need first.

## Account

<!-- AUTHOR TO CONFIRM: one row per show. Show: its register's slug, the name of its file in publishing/src/podcast/, frozen once the feed is live. Name: as the directories show it. Served from: the slug of the website profile's site that serves its feed, where the project has the website platform; otherwise the web server the brand controls that serves it; or the podcast host, for a show kept on one. Apple Podcasts, Spotify, YouTube playlist: each listing exactly as the author reports it, once it exists. -->

| Show | Name | Served from | Apple Podcasts | Spotify | YouTube playlist | Notes |
|---|---|---|---|---|---|---|

A row never holds a password, an ownership code or an account ID; the feed's own values stay in the show register.

## The social plan

Where syntek-author's social-media documents are present, whichever of them sets a value for this platform (the social media plan, the content calendar or an operating procedure) owns it, and the four sections below hold only what none sets.

## Cadence

<!-- AUTHOR TO CONFIRM: how often an episode is released, on which day and at what time (<%TIMEZONE%>), and how seasons are numbered, unless a social-media document sets it. -->

## Tone on this platform

<!-- AUTHOR TO CONFIRM: how the brand's spoken and written voice shifts on the podcast (shorter, warmer, plainer or more formal), unless a social-media document sets it. -->

## Call to action

<!-- AUTHOR TO CONFIRM: what a listener is asked to do after a podcast episode, in the brand's words, unless a social-media document sets it. -->

## Hashtag sets

<!-- AUTHOR TO CONFIRM: whether the show uses hashtags at all, and if so where. -->

A feed has no use for hashtags: they belong to the posts on other platforms that promote an episode, so this section usually stays empty.

## Deliverables used

<!-- AUTHOR TO CONFIRM: which of the podcast's deliverables the brand uses; the keys `python3 toolkit/media.py presets` lists for it are at present `podcast.feed_audio`, `podcast.id3_cover`, `podcast.apple_rss_audio`, `podcast.apple_connect_audio`, `podcast.spotify_audio`, `podcast.cover` and `podcast.episode_art`. A self-hosted show delivers `podcast.feed_audio` through its feed; a show kept on a podcast host delivers `podcast.apple_rss_audio` to that host. -->

A brief names these keys in its `deliverables`, and a cut-down plan names them for each cut.
A key not listed here is not used, whatever `platforms.toml` offers.

## Overrides

Confirmed differences from `toolkit/data/platforms.toml` go in `brand/src/platforms/overrides.toml`, never here.
