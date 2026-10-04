# newsletter.md — <%BRAND_NAME%> in its newsletters

**Last Updated**: <%DATE%> **Version**: 0.1.0 **Maintained By**: <%OWNER_NAME%>
**Language**: British English (en_GB)

> **This file is a seeded stub, and it is deliberately unfinished.**
> It ships with the project so that the skills which route here point at something real from day one.
> Until `brand/workflows/04-set-up-a-platform/` has set up the brand's newsletters with the author, each section below holds an `AUTHOR TO CONFIRM` flag and no entries.

The brand's own choices for the email newsletters that carry its media: the lists, the deliverables it uses, and how it publishes there.
An issue reaches a reader's inbox as a linked still or a short GIF, never as video; the issue itself (its body, blurbs, subject line, preheader, send time, consent and unsubscribe) is the written side's, and media never sends an email or holds a subscriber list.
The newsletters' own facts (the display width, the clipping size, the image formats email clients show) live in `toolkit/data/platforms.toml`, never here, and `publishing/docs/reference/newsletter.md` says how they are applied.
`prepare-post` reads this file for every newsletter placement.
Removing newsletter from the project's platforms deletes this file, filled in or not, so copy out anything you need first.

## Lists

<!-- AUTHOR TO CONFIRM: one row per list whose issues carry the brand's media. List: a kebab slug, frozen once a schedule row uses it. Sender: the sending name, exactly as you give it. Service: the sending service. Owner: brand, or who owns the list. Images hosted at: where the issue's images are served from. Agreement: own, or the dated record of the agreement for a list the brand does not own. -->

| List | Sender | Service | Owner | Images hosted at | Agreement | Notes |
|---|---|---|---|---|---|---|

A row never holds a subscriber, an address, a count, a password or an account ID.
No placement in a list the brand does not own is `ready` until its row's Agreement names a dated record.

## The social plan

Where a social-media document of syntek-author is present and covers this platform (names it with a cadence), it owns what it sets, and the four sections below hold only what none sets.

## Cadence

<!-- AUTHOR TO CONFIRM: how often an issue carries the brand's media, unless a social-media document sets it; a placement takes its date and time from the issue's send time. -->

## Tone on this platform

<!-- AUTHOR TO CONFIRM: how the brand's voice reads in the words media writes for an issue (alt text that names the video and says it opens it), unless a social-media document sets it. -->

## Call to action

<!-- AUTHOR TO CONFIRM: where a reader who clicks the preview lands (the watch page or the post that plays the video), unless a social-media document sets it; the issue's own words are the issue's. -->

## Hashtag sets

An email takes no hashtags, so this section stays empty.

## Deliverables used

<!-- AUTHOR TO CONFIRM: which of the newsletter's deliverables the brand uses; the keys `python3 toolkit/media.py presets` lists for it are at present `newsletter.preview_image` and `newsletter.preview_gif`. -->

A thumbnail brief names these keys; a newsletter carries no video deliverable.
A key not listed here is not used, whatever `platforms.toml` offers.

## Overrides

Confirmed differences from `toolkit/data/platforms.toml` go in `brand/src/platforms/overrides.toml`, never here.
