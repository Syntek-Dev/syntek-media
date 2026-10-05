---
workflow: 08-publish-the-podcast-feed
phase: publish
skills: [prepare-post, cut-for-platform]
model: opus
---

# STEPS.md — publish the podcast feed

**Last Updated**: <%DATE%> **Version**: 0.1.0 **Maintained By**: <%OWNER_NAME%>
**Language**: British English (en_GB)

The ordered procedure for a feed episode's part of M7, beside
`publishing/workflows/05-prepare-a-post/`, which packages the piece's other deliverables and
records the gate. Each step names the skill and guide it uses. **Run in order** — the ordering
is load-bearing — and tick `CHECKLIST.md` as you go.

> Read the read-order files first (this folder's `CONTEXT.md` and `CLAUDE.md`), then
> `publishing/docs/reference/podcast-feed.md` and the register's skeleton in
> `publishing/src/podcast/CLAUDE.md`. Every command below is `python3 toolkit/media.py feed …`.

## 1. Confirm the episode

> **Skill:** `prepare-post` · **Guide:** `scripts/docs/reference/the-piece-ladder.md`

The brief lists `podcast.feed_audio`, and its `verified` dates M6. The M5 render
`publishing/src/renders/<piece>/<piece>.podcast-feed-audio.mp3`, in the piece's own folder,
exists, and so do the master-timed `.vtt` and the published transcript in
`publishing/src/captions/`. A missing render goes back to
`publishing/workflows/02-cut-for-a-platform/`, and a missing caption file or transcript to
`publishing/workflows/03-caption-a-piece/`; nothing is encoded or transcribed here. **A render an
earlier release left flat**, at the top of `publishing/src/renders/`, is one `feed tag` never
reads (exit 2, as for a missing render): before step 5, with the author's agreement, move it
unchanged into the piece's folder, or encode it again through
`publishing/workflows/02-cut-for-a-platform/`. _Mechanical._

## 2. Open the show, once

> **Skill:** `prepare-post` · **Guide:** `publishing/docs/reference/podcast-feed.md`

Where `publishing/src/podcast/<show>.toml` is absent, run `feed new SHOW --feed-url URL`, adding
`--site SLUG` (the website profile's slug of the site serving the feed) where the project has the
website platform. The feed URL is the show's for life: confirm it with the author first. Then
write the show's details with the author: title, author, owner name and a role address,
copyright, Apple's category as Apple spells it, type, explicit, link, `media_base`, and a
description, one sentence per line, with the disclosure sentence where any episode uses a
synthetic voice. `cover` and `id3_cover` name the renders of the cover's design export
(`brand/workflows/03-record-a-design-export/`). On the author's approval, date `approved`. A
wrong feed URL is corrected with `feed new SHOW --rekey --feed-url URL`, only while nothing is
published. _Substantive._

## 3. Add the episode

> **Skill:** `prepare-post` · **Guide:** `publishing/src/podcast/CLAUDE.md`

Run `feed add SHOW --piece PIECE`: the row is appended, `planned`, with its `guid` written once.
A piece already in the register is refused; it is never added twice, and a row is never
deleted. _Mechanical._

## 4. Write the episode's words and chapters

> **Skill:** `prepare-post` · **Guide:** `publishing/docs/reference/podcast-feed.md`

In the row, with the author: the title (no episode number, no show name), the description (plain
text, one sentence per line, the disclosure sentence where a synthetic voice speaks), number,
season, type, explicit, `pub_date` (the time the episode goes out, which the schedule row takes),
`art` (the episode art's published name), `page` (the feed site's episode page) and
`transcript` (the master-timed `.vtt`'s published name). Then the chapters, timed on the master
from its beats, inside the `[platform.podcast]` chapter keys. Count every length against its key
with `media.py presets`. The author approves the row; on a change, this step runs again.
_Substantive._

## 5. Tag the file

> **Skill:** `cut-for-platform` · **Guide:** `publishing/docs/reference/podcast-feed.md`

Run `feed tag SHOW --piece PIECE`. It re-muxes the M5 render without re-encoding, with the row's
title, the show's title and author, the number, the chapters and the show's `id3_cover`, then
writes `render`, `bytes` and `seconds` into the row. Exit 1 names what the row lacks: go back to
step 4. Exit 2 naming the cut procedure means the render is missing: go back to step 1. On a
`published` row, the file now differs from the live one, and needs a new `audio_url` before it is
uploaded. _Mechanical._

## 6. Write the chapters file

> **Skill:** `prepare-post` · **Guide:** `publishing/docs/reference/podcast-feed.md`

Run `feed chapters SHOW --piece PIECE`, which writes
`publishing/src/renders/<piece>/<piece>.chapters.json` from the row's chapters. _Mechanical._

## 7. Check, and mark the row ready

> **Skill:** `prepare-post` · **Guide:** `publishing/docs/reference/podcast-feed.md`

Run `feed check SHOW`. It compares the register with the show's tracked feed and with the render,
and reads the cover and the art against their keys. Every finding is fixed in the register, never
in a feed, and the check runs again until it exits 0. Then set the row's `status` to `ready`.
The episode's schedule row (Platform `podcast`, Deliverable `podcast.feed_audio`) is written by
`publishing/workflows/05-prepare-a-post/`, at `pub_date`, and becomes `ready` there with the
piece's other rows when M7 passes. _Mechanical._

## 8. Write the upload copy

> **Skill:** `prepare-post` · **Guide:** `publishing/docs/reference/podcast-feed.md`

Run `feed write SHOW --as-of '<pub_date>' -o publishing/src/renders/<show>.feed.xml`, at the
folder's top, since no piece owns it. It holds every `ready` or `published` episode due by then,
and writes nothing while a GUID of the tracked feed has vanished or a length changed under an
old URL: fix the register, never the feed. _Mechanical._

## 9. Hand back

> **Skill:** `prepare-post` · **Guide:** `publishing/docs/reference/podcast-feed.md`

Give the author the upload list, in order: the audio, the art, the `.vtt`, the chapters file;
then the upload copy of the feed, **at `pub_date` and not before**, and step 8 again first if
another episode of the show becomes `ready` in the meantime. On the show's first episode or a new
host, the guide's `curl` tests. The hand steps: upload the transcript in Spotify for Creators
(whether Spotify reads the feed's transcript is `VERIFY`), and add the episode's YouTube upload,
where the piece has one, to the show's podcast playlist. Each episode page on a site other than
the feed's is a placement of its own in `publishing/workflows/05-prepare-a-post/`. Ask the author
to report the feed live, so `publishing/workflows/06-record-a-publication/` can set the row
`published` and write the tracked feed. _Substantive._
