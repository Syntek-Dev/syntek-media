# CONTEXT.md — publishing/

The publishing layer: everything between an approved master and a post the author has made. Here a
master becomes platform deliverables (full-length encodes, cut-downs, captions, thumbnails and
covers), each deliverable gets its post package and its row in the schedule, and every upload the
author reports gets its row in the publish log; on the brand's own sites, blogs and newsletters a
deliverable goes out as a placement in a page, post or issue the written side owns. Nothing in
this layer posts, uploads or sends: the author does, and the log records what the author says
happened. The master and its edit decision list are made in
`production/`; the brief, the script and the storyboard live in `scripts/`; the brand's tokens,
layouts and platform profiles live in `brand/`.

## Directory Tree

```text
publishing/
├── CONTEXT.md            ← this file
├── CLAUDE.md             ← operating rules for the layer
├── docs/                 ← guides: reference/ (template-owned) and project/ (yours)
├── src/                  ← cut-down plans, captions, thumbnails, post packages, the schedule and the log
└── workflows/            ← plan · cut · caption · thumbnail · post · record · refresh the specs<: if 'podcast' in PLATFORMS :> · the podcast feed<: endif :>
```

## What's here

- `docs/` — **how a deliverable is made and posted here.** `docs/reference/` ships with the
  template and is updated by `copier update`, with one guide for each platform the project posts
  to; `docs/project/` is yours, and a same-named guide there overrides the reference one.
- `src/` — **the publishing record of every piece**: what it is cut into, the captions and
  thumbnails each cut carries, the package each post is made from, when it goes out and what
  happened when it did. Renders land in `src/renders/` and never enter Git. **`src/CONTEXT.md`
  names every file and folder.**
- `workflows/` — **the procedures**, numbered in the order a piece usually meets them; your own
  sit at `workflows/local/NN-name/` and win over a template procedure with the same slug.<: if 'podcast' in PLATFORMS :>
  A self-hosted podcast adds `publishing/workflows/08-publish-the-podcast-feed/` and its show
  registers in `publishing/src/podcast/`.<: endif :>

A *deliverable*, throughout this layer, is one file made for one platform format and named by its
key in `toolkit/data/platforms.toml` (`youtube.short`, `podcast.apple_rss_audio`). A piece's
full-length deliverables are listed in its brief; its cut-downs live only in its cut-down plan.

## Cross-references

- `.claude/rules/syntek-media/01-layout-and-routing.md` — the layer table, the pair rule and the
  piece.
- `scripts/docs/reference/the-piece-ladder.md` — the gates this layer moves a piece through, from
  produced to published.
- `toolkit/data/platforms.toml` — every platform limit, by key; no guide restates one.
- `publishing/src/CONTEXT.md` — the files of the publishing record, and where each lives.
- `publishing/workflows/CLAUDE.md` — 'You want to… | Procedure'.
