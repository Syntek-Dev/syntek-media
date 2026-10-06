# CONTEXT.md — toolkit/data/

Reference data the toolkit reads, kept apart from the code so that it can be read, dated and
re-checked as data. It holds delivery specs, the house's loudness decision and the versioned
editorial rubric for title–thumbnail scoring.
Nothing here describes this brand: its own choices live in its platform profiles beside
`brand/src/platforms/overrides.toml`, and its confirmed corrections in that file.

## Directory Tree

```text
toolkit/data/
├── CONTEXT.md          ← this file
├── CLAUDE.md           ← operating rules
├── packaging-score.toml ← house Jev questions, weights and review thresholds
└── platforms.toml      ← one table per deliverable and per audiobook store, each with checked and source
```

## What's here

- `platforms.toml` — **every platform number the project uses, and nowhere else.** A
  `[platform.<name>.<format>]` table is one deliverable, named by its key (`youtube.short`,
  `podcast.apple_rss_audio`); a `[platform.<name>]` table holds platform-wide limits such as title
  and caption characters, hashtag rules and the grid crop, and for the brand's own channels the
  embed, share-image and email limits and the accessibility markers, and for the podcast the
  feed's limits and chapter rules; an `[audiobook.<store>]` table is a mastering and delivery
  target (`audiobook.acx`). `[house]` holds decisions, not platform facts: the loudness target of
  every video deliverable, social or for the brand's own sites, because no social or web platform
  publishes one. Every table carries `checked` (DD/MM/YYYY) and `source`.
- **The brand's own channels:** `website`, `blog` and `newsletter` publish no delivery spec, so
  every size and rate in their tables is a house choice inside browser, standards-body or
  email-vendor guidance, named in `chosen`, and every value from a third party sits in `verify`.
  One `website` platform covers every site the brand publishes to: a site is a row of the
  brand's website profile, never a table here. The podcast's `feed_audio` is the file a
  self-hosted feed encloses, and `id3_cover` the cover copy tagged into it.
- **Keys the toolkit reads, and keys it never reads** (the file's header lists both): since
  0.2.0 it reads `formats` (an image's file formats, the first being `media.py image`'s default;
  `["gif"]` marks a GIF `cut` makes), `alpha`, `min_width`, `audio_tracks` (`0`: no sound track),
  `colours_max`, `cbr`, `enclosure_type`, `id3_version` and the chapter, length and type keys of
  `[platform.podcast]`. Documentary keys (`pix_fmt`, `min_height`, `max_width`, the own channels'
  embed, structured-data and email keys, and the rest of `[platform.podcast]`) are read by people,
  guides and checklists only.
- **How it is read** (its header says the same): a key named in `verify` was not confirmed from an
  official source and is flagged wherever it is used; an absent key means no published value
  (keep the source's rate, or skip that check); `chosen` marks a house choice inside an official
  range; `max_size` is copied as the platform states it; `safe_zone` is in pixels at the table's
  size, `0` meaning none published; `caption_formats = []` means captions are burned in, and a
  table with `kind = "image"` or `audio_tracks = 0` carries no `caption_formats` and takes no
  captions. No table has an `fps`, so no preset forces a frame rate unless a source exceeds
  `fps_max`.
- **The brand's corrections** are `[[override]]` tables in `brand/src/platforms/overrides.toml`,
  which `media.py` and `card.py` apply and print; `media.py presets` shows each table with them
  applied, and `media.py presets --stale-after DAYS --today DD/MM/YYYY` lists tables checked longer
  ago than that.

`packaging-score.toml` supplies the seven Jev score questions. Its thresholds and weights are
house choices, not platform facts. Copy it to publishing's project guides and use `--rubric`
for revisions; optional platform/surface selectors add questions only where they apply.
Dated current guidance travels in each input and remains preserved in its result.

## Cross-references

- `toolkit/media_common.py` — reads this file and applies the overrides.
- `publishing/docs/reference/platform-specs.md` — the guide to reading it, for people.
- The website, blog, newsletter and podcast-feed guides, where the project has those channels —
  each in `publishing/docs/reference/` — cite their keys by name, never their numbers.
- `publishing/workflows/07-refresh-the-platform-specs/` — the six-monthly re-check.
- `production/docs/reference/sound-and-loudness.md` — the loudness targets `[house]` and the
  podcast and audiobook tables set.
