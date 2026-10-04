# CONTEXT.md — brand/src/platforms/

The brand's own choices for each platform it posts to: one profile per platform chosen when the
project was generated, and one file of confirmed corrections to the platform data. A profile
holds the account, the deliverables the brand uses there and, where no social media plan covers
them, its cadence, tone, call to action and hashtag sets. The platform's own facts (sizes,
lengths, limits, codecs, its AI label) are not here: they live, dated and sourced, in
`toolkit/data/platforms.toml`, which the template keeps current.

This project posts to: <% PLATFORMS | join(', ') %>.

## Directory Tree

```text
brand/src/platforms/
├── CONTEXT.md          ← this file
├── CLAUDE.md           ← operating rules
<: if 'youtube' in PLATFORMS :>├── youtube.md          ← seed: the account, deliverables and choices for YouTube
<: endif :><: if 'tiktok' in PLATFORMS :>├── tiktok.md           ← seed: the account, deliverables and choices for TikTok
<: endif :><: if 'instagram' in PLATFORMS :>├── instagram.md        ← seed: the account, deliverables and choices for Instagram
<: endif :><: if 'linkedin' in PLATFORMS :>├── linkedin.md         ← seed: the page, deliverables and choices for LinkedIn
<: endif :><: if 'facebook' in PLATFORMS :>├── facebook.md         ← seed: the page, deliverables and choices for Facebook
<: endif :><: if 'podcast' in PLATFORMS :>├── podcast.md          ← seed: the show, its feeds, deliverables and choices
<: endif :>└── overrides.toml      ← seed: confirmed corrections to platforms.toml; ships always
```

## What's here

- **One profile per platform**, each with the same sections: `## Account`, `## The social plan`,
  `## Cadence`, `## Tone on this platform`, `## Call to action`, `## Hashtag sets`,
  `## Deliverables used` and `## Overrides`. `prepare-post` reads the profile for every
  deliverable on its platform.
- **Where syntek-author's social media plan is present** (a business project with its
  social-media family), the plan owns cadence, tone, call to action, hashtags and bios; the
  profile then holds only the account and the deliverables used, and cites the plan for the rest.
- `overrides.toml` — one `[[override]]` table per field of `toolkit/data/platforms.toml` the
  brand has confirmed is different today, with the platform's words, the source and the date.
  It ships whatever platforms are chosen, so removing a platform never deletes a correction.

Removing a platform from the project's answers deletes its profile, filled in or not, at the
next `copier update`; adding one brings its profile, empty.

## Cross-references

- `brand/docs/reference/platform-profiles.md` — what a profile holds, overrides, and the
  social-media family.
- `brand/workflows/04-set-up-a-platform/` — the procedure that fills a profile.
- `publishing/docs/reference/platform-specs.md` — how `platforms.toml` is read, `verify` keys
  included.
- `publishing/src/schedule.md` — where each deliverable's posting date is planned.
