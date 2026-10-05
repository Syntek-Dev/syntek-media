# CONTEXT.md — publishing/workflows/08-publish-the-podcast-feed/

The procedure for a feed episode's part of M7, for a show the brand serves itself: the show
opened once in its register, the episode's row with its words and chapters, its audio tagged,
its chapters file written, the feed checked against what is already live, and the upload copy of
the feed written, with the author's upload list in order. Apple Podcasts and Spotify read the
feed; nothing here uploads, and nothing is public until the author puts the files and the feed
on the site. The audio was encoded at M5 and the transcript made at M6: this procedure checks
they exist and never makes them.

## Directory Tree

```text
publishing/workflows/08-publish-the-podcast-feed/
├── CONTEXT.md        ← this file: when to use it, what it produces
├── CLAUDE.md         ← how to run it; guardrails
├── STEPS.md          ← the ordered procedure
└── CHECKLIST.md      ← tick as you go; model-tagged
```

## When to use this

- A piece whose brief lists `podcast.feed_audio` is captioned, and its episode is to go out in
  the show's own feed.
- A show is being opened: its register written and its details approved, before its first
  episode.
- An episode's words, chapters or date change before it goes out, or a published episode needs a
  corrected file.

Reach for a **different** procedure when the task is encoding the episode's audio
(`publishing/workflows/02-cut-for-a-platform/`), its captions and transcript
(`publishing/workflows/03-caption-a-piece/`), the package and schedule rows of the piece's other
deliverables and placements (`publishing/workflows/05-prepare-a-post/`, which runs beside this
one and records M7), recording what the author published
(`publishing/workflows/06-record-a-publication/`), or a show kept on a podcast host, which has no
register and no feed here (`publishing/docs/reference/podcast.md`).

## What it produces, and where

- **The show register** `publishing/src/podcast/<show>.toml`, opened once, and the episode's row
  in it, `ready`, with its words, chapters, `pub_date`, render, bytes and seconds.
- **The tagged audio** `publishing/src/renders/<piece>/<piece>.podcast-feed-audio.mp3`, tagged in place,
  and its chapters file `publishing/src/renders/<piece>/<piece>.chapters.json`.
- **The upload copy of the feed** `publishing/src/renders/<show>.feed.xml`.
- **A hand-back:** the files to upload, in order, the time the feed goes up, the tests and the
  hand steps.

## The failure this procedure exists to prevent

An episode listed twice in every app because its GUID was retyped; a feed uploaded before its
audio, so Spotify fetched a missing file; a feed that went up a day early because a static file
has no clock; a corrected file uploaded under the old URL, which no directory fetches again; or
an episode with no chapters, no transcript and no disclosure, because the feed was written by
hand from memory.

## Cross-references

- `publishing/docs/reference/podcast-feed.md` — the feed, the register, the routes and the
  order of upload.
- `publishing/src/podcast/CLAUDE.md` — the register's skeleton.
- `publishing/docs/reference/podcast.md` — the podcast keys, the cover and episode art, and
  disclosure in the audio.
- `brand/src/platforms/podcast.md` — the shows by slug and where each feed is served.
