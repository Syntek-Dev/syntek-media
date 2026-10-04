# CONTEXT.md — <%BRAND_SLUG%>/

<: if BRAND_KIND == 'business' :>The production repository for the video and audio of <%BRAND_NAME%>, a business.
<: endif :><: if BRAND_KIND == 'author-fiction' :>The production repository for the video and audio of <%BRAND_NAME%>, a novelist's brand.
<: endif :><: if BRAND_KIND == 'author-nonfiction' :>The production repository for the video and audio of <%BRAND_NAME%>, a non-fiction author's brand.
<: endif :>The deliverables are finished video and audio, made from plain files: every file in a `src/` folder
is part of a piece, or the plans, registers and source records behind it. The brand brief lives
in `.claude/rules/syntek-media/01-layout-and-routing.md` Section 1, and the rules beside it in
`.claude/rules/syntek-media/`, not here. This file is orientation only.

## Directory Tree

```text
<%BRAND_SLUG%>/
├── .claude/                ← Claude Code: the manual, the template's rules, memory, settings, skills
│   ├── CLAUDE.md           ← the project brief and where the rules live (read first)
│   ├── MEMORY.md           ← project memory (read second)
│   ├── rules/syntek-media/ ← loaded at launch: the brand brief (01, Section 1) and the template's rules (never edit)
│   └── skills/             ← one folder per skill
├── brand/                  ← LAYER (production): design tokens and layouts, design exports, the spoken voice, platform profiles
├── scripts/                ← LAYER (production): one folder per piece (brief, script or transcript, storyboard, shot list)
├── production/             ← LAYER (production): source media, voiceover, edit decision lists, cards, rights, credits<: if 'audiobook' in MEDIA_KINDS :>, audiobooks<: endif :>
├── publishing/             ← LAYER (production): cut-down plans, captions, thumbnails, post packages, schedule, publish log
├── toolkit/                ← SUPPORTING: media.py and card.py, the platform data, the fallback layouts
├── CONTEXT.md              ← this file
├── README.md               ← the human-facing overview
├── .gitignore              ← what Git never tracks (media's own ignore rules are nested in its folders)
├── .mcp.json               ← project MCP servers (none: ElevenLabs is configured at user scope)
└── .copier-answers.syntek-media.yml ← Copier's record of the answers; never edit by hand
```

## What's here

- **Production layers** — `brand/`, `scripts/`, `production/` and `publishing/`. Each splits into
  `docs/` (guides: `reference/` from the template, `project/` your own), `src/` (the artefact)
  and `workflows/` (numbered procedures, with `local/` for your own). **The unit of work is the
  piece**: one folder in `scripts/src/pieces/` per short, explainer, talk, trailer, episode or
  audiobook.
- **Supporting layer** — `toolkit/`: the one command line every render runs through, the
  platform data and the fallback layouts. Flat, run rather than produced inside.
- **Generated output** — the renders and generated folders inside `production/src/` and
  `publishing/src/`: masters, deliverables, card and thumbnail PNGs and generated audio. They are
  git-ignored and never edited by hand; everything in them can be made again except an approved
  take or audiobook master, which is archived as source media.
- **Source footage** — kept in external storage and listed in
  `production/src/footage/manifest.toml`; the local mirror beside it is git-ignored.
- **Every folder carries a `CONTEXT.md` and a `CLAUDE.md`**, with the exceptions listed in
  `.claude/rules/syntek-media/01-layout-and-routing.md` Section 6. Read both before working
  inside a folder.

## Cross-references

- `.claude/CLAUDE.md` — the project brief and the project's own rules; read it first.
- `.claude/rules/syntek-media/01-layout-and-routing.md` — the brand brief, the layers, the folder
  pair, who owns which files, and the read order.
- `.claude/rules/syntek-media/03-production-ethics.md` — who decides, the piece ladder, credits,
  disclosure and rights.
- `README.md` — the overview for people, including how to render and how to update from the
  template.
