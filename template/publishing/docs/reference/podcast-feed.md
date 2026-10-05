---
type: guide
skills: [prepare-post, cut-for-platform]
model: opus
---

# Podcast feed — a self-hosted show: its register, its feed, and how the directories read it

**Last Updated**: <%DATE%> **Version**: 0.1.0 **Maintained By**: <%OWNER_NAME%>
**Language**: British English (en_GB)

**What it is.** How a show the brand serves itself reaches Apple Podcasts and Spotify: one RSS
feed per show, written by `media.py feed` from the show's register in `publishing/src/podcast/`
and served as a static file, with the audio, art, captions and chapters, from one site the brand
owns; both directories read it and take no upload. Media writes the files; the author uploads
them. Limits are cited by key (`[platform.podcast]`, `podcast.feed_audio`), read with `presets`.

## The register and the feed

- `publishing/src/podcast/<show>.toml` holds every value the feed carries, one `[[episode]]` row
  per episode, never deleted; the post package cites it. **Identity is for life:** the feed URL
  and every GUID are written once (`feed new --rekey` only before anything is published).
- `<show>.feed.xml` beside it is the feed as last published, written after the author reports it
  live, so every public change is a reviewed diff; `feed write` and `feed check` refuse a GUID
  gone from it, or a changed length under an unchanged URL.
- **A corrected file** gets a new URL (`-v2` before its extension), keeping its GUID: Spotify
  refetches only a new path. Check a site-built feed with `feed check --feed FILE`.

## Two routes to an episode, the hosted route, and YouTube

- **A talk as an episode:** one piece, one picture master, deliverables `youtube.long` and
  `podcast.feed_audio` (the master's sound only); no podcast media kind is needed.
- **An episode of its own:** a `kind: podcast` piece (the podcast-episode workflow, where the
  project has it); its video is a still under its audio at `youtube.long`'s size, or its parent's.
- **A show on a podcast host** delivers `podcast.apple_rss_audio` to it, and uses neither the
  register nor this feed (`publishing/docs/reference/podcast.md`).
- **YouTube** takes the episode as video, uploaded into the show's podcast playlist (the YouTube
  guide). Its RSS ingestion (a still of the show art, audio never updatable) suits an audio-only
  show only, is the register's `youtube_route`, and is never used beside uploads for one show.

## Upload order and the hosting tests

- **The files first, then the feed, at `pub_date` and not before:** a static feed has no clock,
  and Spotify fetches every file it names. An episode's audio and chapters sit in
  `publishing/src/renders/<piece>/`, and the upload copy (`feed write --as-of '<pub_date>'`) at
  that folder's top, written again if another episode is `ready` first.
- The author tests the host on the first episode; the toolkit never fetches:

```text
curl -sI <audio_url>     # Content-Length equals the row's bytes; Content-Type: audio/mpeg
curl -s --range 0-99 <audio_url> -o /dev/null -w '%{http_code} %{size_download}\n'   # 206 100
curl -sI <feed_url>      # Content-Type: application/rss+xml; and the cover: Last-Modified
curl -sI -H 'Origin: https://<page domain>' <vtt_url>   # text/vtt; Access-Control-Allow-Origin
```

- The per-episode hand steps (the Spotify transcript upload, `VERIFY`; the playlist) are in
  `publishing/workflows/08-publish-the-podcast-feed/STEPS.md` step 9. The validators, on the live
  feed: the W3C Feed Validation Service, Cast Feed Validator, Podbase, the Podcasting 2.0 one.

## How we apply it here

- The feed site's episode page (the register's `page`) plays the enclosure in a native audio
  player, never autoplaying, with the show notes, the chapters, the published transcript right
  after the player, and the subscribe links reported. **A page on any other site** is a
  placement, `## podcast.feed_audio — website:second-site`, with its own rows, its site's
  agreement (the website profile's row) and the same enclosure URL; it Links to the episode.
- The disclosure sentence goes in the audio, the show's description and every episode's; the
  chapters keep to the `[platform.podcast]` chapter keys, or `feed tag` refuses the row.

## Who implements it

- **Workflows:** `publishing/workflows/02-cut-for-a-platform/` (M5),
  `publishing/workflows/03-caption-a-piece/` (M6),
  `publishing/workflows/08-publish-the-podcast-feed/` and `publishing/workflows/05-prepare-a-post/`
  (M7), then `publishing/workflows/06-record-a-publication/` once the author reports it live.
- **Skills:** `prepare-post` writes the words; `cut-for-platform` encodes and tags the file.

## Governing standard

`.claude/rules/syntek-media/03-production-ethics.md` Section 3 owns the ladder and Section 5
disclosure; `.claude/rules/syntek-media/04-toolkit-pipeline.md` Section 3 the tracked feed. The
rules own the requirement; this guide owns how a self-hosted show's feed is made and published.
