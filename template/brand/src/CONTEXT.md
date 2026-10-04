# CONTEXT.md — brand/src/

The brand itself: the design system every layout is drawn from, the exported design assets and
their register, the spoken voice, and the brand's profile for each platform it posts to. These
files are records, not pieces: a thumbnail or a card made for one piece is a copy that lives with
the piece (`publishing/src/thumbnails/`, `production/src/cards/`), and a platform's own facts
live in `toolkit/data/platforms.toml`, not here.

## Directory Tree

```text
brand/src/
├── CONTEXT.md                  ← this file
├── CLAUDE.md                   ← operating rules
├── design-register.md          ← seed: one row per design, its Claude Design link and its export
├── design-system/              ← the kit Claude Design syncs with
│   ├── tokens.css              ← seed: the custom properties every layout imports
│   ├── fonts/                  ← the brand's font files; each licence is in the rights register
│   └── previews/               ← seven @dsCard cards; thumbnail.html and card.html are the layouts
├── exports/                    ← small exported design assets, committed as ordinary files
│   └── large/                  ← large exports, stored by Git LFS through its own .gitattributes
├── voice/                      ← voice.md (seed): spoken style, narrators, pronunciations
└── platforms/                  ← one profile per selected platform, plus overrides.toml
<: if 'youtube' in PLATFORMS :>    ├── youtube.md              ← seed: the brand on YouTube
<: endif :><: if 'tiktok' in PLATFORMS :>    ├── tiktok.md               ← seed: the brand on TikTok
<: endif :><: if 'instagram' in PLATFORMS :>    ├── instagram.md            ← seed: the brand on Instagram
<: endif :><: if 'linkedin' in PLATFORMS :>    ├── linkedin.md             ← seed: the brand on LinkedIn
<: endif :><: if 'facebook' in PLATFORMS :>    ├── facebook.md             ← seed: the brand on Facebook
<: endif :><: if 'podcast' in PLATFORMS :>    ├── podcast.md              ← seed: the brand's podcast shows and where each feed is served
<: endif :><: if 'website' in PLATFORMS :>    ├── website.md              ← seed: the sites the brand publishes media to
<: endif :><: if 'blog' in PLATFORMS :>    ├── blog.md                 ← seed: the blogs that carry the brand's media
<: endif :><: if 'newsletter' in PLATFORMS :>    ├── newsletter.md           ← seed: the lists whose issues carry the brand's media
<: endif :>    └── overrides.toml          ← seed: confirmed corrections to platforms.toml
```

## What's here

- `brand/src/design-system/` — **the source of truth for how the brand looks.** `tokens.css`
  holds every colour, typeface, space and caption style; the preview cards show them to Claude
  Design, and two of them, `design-system/previews/thumbnail.html` and
  `design-system/previews/card.html`, are the brand's thumbnail and title-card layouts, which
  every later piece copies.
- `brand/src/design-register.md` — one row per design: the brand's design-system project, and
  every design exported from Claude Design, with where its file sits and how Git stores it.
- `brand/src/exports/` — exported assets of 10 MB or less; anything larger goes in
  `brand/src/exports/large/`, which Git LFS stores.
- `brand/src/voice/` — **`voice.md`, the one record of how the brand sounds aloud**: pace and
  register, a narrator for each use, and every pronunciation a narrator needs.
- `brand/src/platforms/` — the brand's own choices for each platform it posts to, one profile
  per platform chosen when the project was generated, and `overrides.toml`, which ships always.

The seeds ship with headings, writing rules and `AUTHOR TO CONFIRM` slots but no entries.
`copier update` recreates a seed you delete and never touches one you have edited; a platform
profile is the exception, deleted with everything else when its platform is removed from the
answers.

## Cross-references

- `brand/docs/reference/the-brand-kit.md` — the required tokens and the two layout components.
- `brand/docs/reference/design-exports.md` — small and large exports, and the register.
- `brand/docs/reference/the-spoken-voice.md` — what `voice.md` holds, and consent.
- `brand/docs/reference/platform-profiles.md` — what a profile holds, and overrides.
- `production/src/rights-register.md` — font licences and voice consent, by ID.
