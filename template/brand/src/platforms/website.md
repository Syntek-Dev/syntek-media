# website.md — <%BRAND_NAME%> on its websites

**Last Updated**: <%DATE%> **Version**: 0.1.0 **Maintained By**: <%OWNER_NAME%>
**Language**: British English (en_GB)

> **This file is a seeded stub, and it is deliberately unfinished.**
> It ships with the project so that the skills which route here point at something real from day one.
> Until `brand/workflows/04-set-up-a-platform/` has set up the brand's websites with the author, each section below holds an `AUTHOR TO CONFIRM` flag and no entries.

The brand's own choices for the websites it publishes media to: the sites, the deliverables it uses, and how it publishes there.
One website platform covers every site, the brand's own and any it writes for; a site is a row below, named by its slug.
The web's own facts (sizes, rates, the share-image minimums, the embed limits and the accessibility markers) live in `toolkit/data/platforms.toml`, never here, and `publishing/docs/reference/website.md` says how they are applied.
`prepare-post` reads this file for every website placement.
Removing website from the project's platforms deletes this file, filled in or not, so copy out anything you need first.

## Sites

<!-- AUTHOR TO CONFIRM: one row per site the brand publishes media to, its own and any it writes for. Site: a kebab slug, frozen once a schedule row uses it. Domain: exactly as you give it. Owner: brand, or who owns the site. CMS or hosting: what runs it. Player: self-hosted, youtube-embed or both. Captions: track or youtube. Carries: pages, posts, episode pages, or a podcast feed by its show slug. Agreement: own, or the dated record of the agreement for a site the brand does not own. -->

| Site | Domain | Owner | CMS or hosting | Player | Captions | Carries | Agreement | Notes |
|---|---|---|---|---|---|---|---|---|

A row never holds a subscriber, a visitor count, a password or an account ID.
A site's agreement is recorded once, here; the blog profile, where the project has one, cites it as 'see website'.
No placement on a site the brand does not own is `ready` until its row's Agreement names a dated record.

## The social plan

Where a social-media document of syntek-author is present and covers this platform (names it with a cadence), it owns what it sets, and the four sections below hold only what none sets.

## Cadence

<!-- AUTHOR TO CONFIRM: how often the brand places media on its sites, if it keeps a rhythm at all, unless a social-media document sets it; most placements take their date from the page or post they sit in. -->

## Tone on this platform

<!-- AUTHOR TO CONFIRM: how the brand's voice reads in the words media writes for its sites (an embed's or a figure's title, alt text), unless a social-media document sets it. -->

## Call to action

<!-- AUTHOR TO CONFIRM: what a visitor is asked to do after a video on the brand's sites, in the brand's words, unless a social-media document sets it; the page's own call to action is the page's. -->

## Hashtag sets

A website takes no hashtags: they belong to the posts on other platforms that point to a page, so this section stays empty.

## Deliverables used

<!-- AUTHOR TO CONFIRM: which of the website's deliverables the brand uses; the keys `python3 toolkit/media.py presets` lists for it are at present `website.video`, `website.video_720`, `website.hero_loop`, `website.poster`, `website.poster_720` and `website.og_image`. An embed of the YouTube upload is a placement of `youtube.long`, not a deliverable of this platform. -->

A brief names the video keys in its `deliverables`, a cut-down plan names a loop for its cut, and a thumbnail brief names the image keys.
A key not listed here is not used, whatever `platforms.toml` offers.

## Overrides

Confirmed differences from `toolkit/data/platforms.toml` go in `brand/src/platforms/overrides.toml`, never here.
