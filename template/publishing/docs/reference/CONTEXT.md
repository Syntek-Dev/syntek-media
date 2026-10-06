# CONTEXT.md — publishing/docs/reference/

The template's publishing guides, one per question. Seven cover the work every piece meets on its
way out: cut-downs, captions, thumbnails, AI disclosure, posting and the log, and how the platform
data is read. One more covers each platform the project posts to, citing its limits by key, and a
podcast the brand serves itself has a second, on its feed. Each names the skill and workflow that
carry it out and the media rules file that owns the requirement.
These files are template-owned: `copier update` keeps them current, and a same-named guide in
`publishing/docs/project/` overrides any of them.

## Directory Tree

```text
publishing/docs/reference/
├── CONTEXT.md                ← this file
├── CLAUDE.md                 ← operating rules
├── cut-downs.md              ← one long piece, several short ones that stand alone
├── captions.md               ← three timing routes, the house limits, burned or sidecar
├── scoring-options.md         ← Jev questions, dated platform guidance and author selection
├── thumbnails.md             ← the brief, the brand's layout, and checks at thumbnail size
├── ai-disclosure.md          ← each platform's rule for its label; the description line always
├── posting-and-the-log.md    ← the package, the schedule, the author posts, the log
<: if 'youtube' in PLATFORMS :>├── youtube.md                ← long videos, Shorts and thumbnails, by key
<: endif :><: if 'tiktok' in PLATFORMS :>├── tiktok.md                 ← vertical video, burned captions and the AI-generated label
<: endif :><: if 'instagram' in PLATFORMS :>├── instagram.md              ← reels, stories and covers; the hashtag cap and the grid crop
<: endif :><: if 'linkedin' in PLATFORMS :>├── linkedin.md               ← landscape and vertical video, no thumbnail table
<: endif :><: if 'facebook' in PLATFORMS :>├── facebook.md               ← every video a reel; feed and story values from the ads guide
<: endif :><: if 'podcast' in PLATFORMS :>├── podcast.md                ← Apple Podcasts and Spotify: audio, artwork, disclosure in the audio
├── podcast-feed.md           ← a self-hosted show: its register, its feed, the order of upload
<: endif :><: if 'website' in PLATFORMS :>├── website.md                ← the brand's sites: self-hosted or embedded video, posters, share images
<: endif :><: if 'blog' in PLATFORMS :>├── blog.md                   ← posts: video, transcripts, featured and share images
<: endif :><: if 'newsletter' in PLATFORMS :>├── newsletter.md             ← email issues: a linked preview image or GIF, never video
<: endif :>└── platform-specs.md         ← how platforms.toml is read: verify, chosen, overrides, staleness
```

## What's here

- `cut-downs.md` — **read before planning or cutting anything short.** The cut-down plan, finding
  moments that stand alone, framing and safe zones, and why a near-identical batch is refused.
- `captions.md` — the house caption limits, file names, the three timing routes, captions made
  before the cut, and when captions are burned in rather than uploaded.
- `scoring-options.md` — title–thumbnail candidates, versioned rubrics, paid-call approval and visual review.
- `thumbnails.md` — the thumbnail brief, the brand's layout component, which deliverables take a
  thumbnail, and the checks at the size it is seen.
- `ai-disclosure.md` — **read before any post that uses a synthetic voice, generated visuals or
  generated music.** Each platform's rule for its label, with sources and dates, and the house's
  description line.
- `posting-and-the-log.md` — the post package, the schedule, the author's post, the publish log,
  and when a piece counts as published.
- `platform-specs.md` — how `toolkit/data/platforms.toml` is read, how the brand corrects it, and
  how it is kept fresh.
<: if 'youtube' in PLATFORMS :>- `youtube.md` — the YouTube deliverables and their keys, the altered or synthetic content
  setting, and YouTube's traps.
<: endif :><: if 'tiktok' in PLATFORMS :>- `tiktok.md` — the TikTok deliverable and its key, burned captions, the AI-generated content
  label, and what TikTok bans even when labelled.
<: endif :><: if 'instagram' in PLATFORMS :>- `instagram.md` — the Instagram deliverables and their keys, the hashtag cap, the grid crop,
  and the AI info label.
<: endif :><: if 'linkedin' in PLATFORMS :>- `linkedin.md` — the LinkedIn deliverables and their keys, edges kept clear, thumbnails at the
  video's size, and disclosure without a toggle.
<: endif :><: if 'facebook' in PLATFORMS :>- `facebook.md` — the Facebook deliverables and their keys, the reel-only upload, and the AI
  info label.
<: endif :><: if 'podcast' in PLATFORMS :>- `podcast.md` — the podcast deliverables and their keys, cover and episode art, and
  disclosure in the audio and in the metadata.
- `podcast-feed.md` — **read before opening a self-hosted show.** The show register and its
  feed, the two routes to an episode, the order and time of upload, and the hand steps.
<: endif :><: if 'website' in PLATFORMS :>- `website.md` — the website keys, placements and agreements on each site, captions and the
  published transcript, a loop's motion, and the hosting tests.
<: endif :><: if 'blog' in PLATFORMS :>- `blog.md` — the blog keys, a post's placement, the transcript under the player, and the
  featured image.
<: endif :><: if 'newsletter' in PLATFORMS :>- `newsletter.md` — the preview image and the GIF, what email clients show, and an issue's
  placement.
<: endif :>
## Cross-references

- `publishing/docs/project/` — your overrides and additions; checked before this folder.
- `publishing/workflows/CLAUDE.md` — the procedures these guides are applied in.
- `scripts/docs/reference/the-piece-ladder.md` — the gates every guide here defers to.
- `toolkit/data/platforms.toml` — the dated platform data every guide cites by key.
