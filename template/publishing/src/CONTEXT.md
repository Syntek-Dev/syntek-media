# CONTEXT.md — publishing/src/

The publishing record of every piece: what its master is cut into, the captions and thumbnails
each deliverable carries, the package each post is made from, when each deliverable goes out, and
what happened when the author posted it. This file names every file and folder here, so the
procedures in `publishing/workflows/` can say 'the schedule' or 'the post package' and mean exactly
one path. The master, its edit decision list and its title cards are not here: they live in
`production/src/`.

## Directory Tree

```text
publishing/src/
├── CONTEXT.md        ← this file: the files, and where each lives
├── CLAUDE.md         ← operating rules
├── .gitignore        ← keeps renders/ out of Git, all but its README
├── schedule.md       ← seed: when each media deliverable goes out
├── publish-log.md    ← seed: every upload, as the author reported it
├── renders/          ← <piece>/: its deliverables, burned versions, images, GIFs, chapters; git-ignored, README.md only
├── cut-downs/        ← <piece>.md: one cut-down plan per piece
├── captions/         ← <piece>[--cNN|.<FID>][.<platform>-<format>].en-GB.srt and .vtt; published transcripts
├── thumbnails/       ← <piece>[--cNN].md brief and .html layout, for every image deliverable
<: if 'podcast' in PLATFORMS :>├── podcast/          ← <show>.toml show registers and <show>.feed.xml, each feed as last published
<: endif :>└── posts/            ← <piece>.md: one post package per piece, a section per deliverable or placement
```

## What's here

| Part | Lives at | Written by |
|---|---|---|
| A piece's cut-down plan | `cut-downs/<piece>.md` | `repurpose`, with the author |
| A deliverable's captions, and a published transcript | `captions/` | `captions` |
| A brief and layout for a piece's images | `thumbnails/<piece>[--cNN].md`, `.html` | `thumbnail-brief`, with the author |
<: if 'podcast' in PLATFORMS :>| A self-hosted show's register and its feed as last published | `podcast/` | `prepare-post` and the `feed` commands, with the author |
<: endif :>
| A piece's post package | `posts/<piece>.md` | `prepare-post`, with the author |
| The schedule | `schedule.md` | `prepare-post`, then the author's reports |
| The publish log | `publish-log.md` | `prepare-post`, from the author's report only |
| A piece's rendered deliverables, images, GIFs and chapters file, in a folder named for it; at the top, what no piece owns (a feed's upload copy, a show's cover encodes) | `renders/` | `cut-for-platform`, `captions`, `thumbnail-brief`, `prepare-post` |

- **The schedule and the log are the single source of truth** for what goes out when, and what
  went out. Where syntek-author's content calendar is present, it owns the plan, and every
  schedule row cites its calendar entry.
- **`.gitignore` is template-owned** and ships with every project: it ignores everything in
  `renders/` except the folder's README, each piece's folder there included, so a render can
  never be committed by accident.
- A generated project may hold one worked example, a short plan, caption file, thumbnail and post
  package, where it was kept; delete them once you no longer need them, and they will not come
  back.

The seeds ship with headings and writing rules but no entries. `copier update` recreates a seed
you delete and never touches one you have edited.

## Cross-references

- `publishing/docs/reference/CONTEXT.md` — the guides each part follows.
- `publishing/workflows/CONTEXT.md` — the procedures that write each part.
- `scripts/src/pieces/` — the briefs, scripts and transcripts every part here reads.
- `production/src/renders/` — the masters every deliverable is cut or encoded from, each in its
  piece's folder.
