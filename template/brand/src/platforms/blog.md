# blog.md — <%BRAND_NAME%> on its blogs

**Last Updated**: <%DATE%> **Version**: 0.1.0 **Maintained By**: <%OWNER_NAME%>
**Language**: British English (en_GB)

> **This file is a seeded stub, and it is deliberately unfinished.**
> It ships with the project so that the skills which route here point at something real from day one.
> Until `brand/workflows/04-set-up-a-platform/` has set up the brand's blogs with the author, each section below holds an `AUTHOR TO CONFIRM` flag and no entries.

The brand's own choices for the blogs it publishes media in: the sites whose posts carry it, the deliverables it uses, and how it publishes there.
A blog post's words, headings, standfirst, figure captions, link text, slug and date are the written side's; media supplies the video, its captions and transcript, and the images.
The blogs' own facts (sizes, rates, the featured-image and structured-data minimums and the accessibility markers) live in `toolkit/data/platforms.toml`, never here, and `publishing/docs/reference/blog.md` says how they are applied.
`prepare-post` reads this file for every blog placement.
Removing blog from the project's platforms deletes this file, filled in or not, so copy out anything you need first.

## Sites

<!-- AUTHOR TO CONFIRM: one row per site whose blog carries the brand's media, its own and any it writes for. Site: a kebab slug, frozen once a schedule row uses it; where the project also has the website platform, the same slug the website profile gives that site. Domain: exactly as you give it. Owner: brand, or who owns the site. CMS or hosting: what runs the blog. Player: self-hosted, youtube-embed or both. Captions: track or youtube. Carries: posts. Agreement: 'see website' where the website profile lists the site, which holds its agreement once; otherwise own, or the dated record of the agreement for a site the brand does not own. -->

| Site | Domain | Owner | CMS or hosting | Player | Captions | Carries | Agreement | Notes |
|---|---|---|---|---|---|---|---|---|

A row never holds a subscriber, a visitor count, a password or an account ID.
No placement on a site the brand does not own is `ready` until its agreement names a dated record, here or in the website profile's row it cites.

## The social plan

Where a social-media document of syntek-author is present and covers this platform (names it with a cadence), it owns what it sets, and the four sections below hold only what none sets.

## Cadence

<!-- AUTHOR TO CONFIRM: how often a blog post carries the brand's media, unless a social-media document sets it; a placement takes its date and time from the post it sits in. -->

## Tone on this platform

<!-- AUTHOR TO CONFIRM: how the brand's voice reads in the words media writes for a post (a figure's or an embed's title, alt text), unless a social-media document sets it. -->

## Call to action

<!-- AUTHOR TO CONFIRM: what a reader is asked to do after a video in a post, in the brand's words, unless a social-media document sets it; the post's own call to action is the post's. -->

## Hashtag sets

A blog takes no hashtags: they belong to the posts on other platforms that point to it, so this section stays empty.

## Deliverables used

<!-- AUTHOR TO CONFIRM: which of the blog's deliverables the brand uses; the keys `python3 toolkit/media.py presets` lists for it are at present `blog.video`, `blog.poster`, `blog.featured_image` and `blog.og_image`. An embed of the YouTube upload is a placement of `youtube.long`, not a deliverable of this platform. -->

A brief names `blog.video` in its `deliverables`, and a thumbnail brief names the image keys.
A key not listed here is not used, whatever `platforms.toml` offers.

## Overrides

Confirmed differences from `toolkit/data/platforms.toml` go in `brand/src/platforms/overrides.toml`, never here.
