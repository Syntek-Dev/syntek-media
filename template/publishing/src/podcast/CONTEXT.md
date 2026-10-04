# CONTEXT.md — publishing/src/podcast/

One show register per podcast the brand serves itself, and beside it the show's feed as last
published. The register is the single source of every value the feed carries: the show's details
and one row per episode, its words, its chapters, its file and its status. The feed is written
from it by `python3 toolkit/media.py feed` and never by hand. Episode audio, chapters files and
the upload copy of a feed are renders, in `publishing/src/renders/`; a show kept on a podcast
host has no register here.

## Directory Tree

```text
publishing/src/podcast/
├── CONTEXT.md          ← this file
├── CLAUDE.md           ← operating rules and the register skeleton
├── <show>.toml         ← one show's register, named by its frozen kebab slug
└── <show>.feed.xml     ← that show's feed as last published, written only after the author reports it live
```

## What's here

- `<show>.toml` — written first by `feed new SHOW --feed-url URL`, which sets the show's identity
  once; `feed add` appends one `[[episode]]` row per episode, never deleted; `feed tag` writes
  each row's `render`, `bytes` and `seconds`. Every other value is written with the author.
  **`publishing/docs/reference/podcast-feed.md` explains the feed**, the two routes to an
  episode, the order of upload and the hand steps.
- `<show>.feed.xml` — the bytes the directories read, written by `feed write -o` with the same
  `--as-of` as the upload, once the author reports the feed live, so every public change shows as
  a diff. It is the one tracked file the toolkit overwrites, and only after its GUID comparison.
- Both are the author's: removing the podcast platform deletes this pair, never a register or a
  feed.

## Cross-references

- `publishing/workflows/08-publish-the-podcast-feed/` — opening a show and taking an episode
  through its part of M7.
- `publishing/workflows/06-record-a-publication/` — the row set `published` and the tracked feed
  written, on the author's report.
- `brand/src/platforms/podcast.md` — the shows by slug, where each feed is served, and their
  listings.
- `toolkit/data/platforms.toml` — `[platform.podcast]` and `podcast.feed_audio`, the limits the
  register is checked against.
