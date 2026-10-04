# CONTEXT.md — toolkit/data/

Reference data the toolkit reads, kept apart from the code so that it can be read, dated and
re-checked as data. It holds one file: the delivery specs of every platform deliverable the
toolkit cuts, encodes, captions or renders a thumbnail for, and the house's loudness decision.
Nothing here describes this brand: its own choices live in its platform profiles beside
`brand/src/platforms/overrides.toml`, and its confirmed corrections in that file.

## Directory Tree

```text
toolkit/data/
├── CONTEXT.md          ← this file
├── CLAUDE.md           ← operating rules
└── platforms.toml      ← one table per deliverable and per audiobook store, each with checked and source
```

## What's here

- `platforms.toml` — **every platform number the project uses, and nowhere else.** A
  `[platform.<name>.<format>]` table is one deliverable, named by its key (`youtube.short`,
  `podcast.apple_rss_audio`); a `[platform.<name>]` table holds platform-wide limits such as title
  and caption characters, hashtag rules and the grid crop; an `[audiobook.<store>]` table is a
  mastering and delivery target (`audiobook.acx`). `[house]` holds decisions, not platform facts:
  social video's loudness target, because no social platform publishes one. Every table carries
  `checked` (DD/MM/YYYY) and `source`.
- **How it is read** (its header says the same): a key named in `verify` was not confirmed from an
  official source and is flagged wherever it is used; an absent key means no published value
  (keep the source's rate, or skip that check); `chosen` marks a house choice inside an official
  range; `max_size` is copied as the platform states it; `safe_zone` is in pixels at the table's
  size, `0` meaning none published; `caption_formats = []` means captions are burned in. No table
  has an `fps`, so no preset forces a frame rate unless a source exceeds `fps_max`.
- **The brand's corrections** are `[[override]]` tables in `brand/src/platforms/overrides.toml`,
  which `media.py` and `card.py` apply and print; `media.py presets` shows each table with them
  applied, and `media.py presets --stale-after DAYS --today DD/MM/YYYY` lists tables checked longer
  ago than that.

## Cross-references

- `toolkit/media_common.py` — reads this file and applies the overrides.
- `publishing/docs/reference/platform-specs.md` — the guide to reading it, for people.
- `publishing/workflows/07-refresh-the-platform-specs/` — the six-monthly re-check.
- `production/docs/reference/sound-and-loudness.md` — the loudness targets `[house]` and the
  podcast and audiobook tables set.
