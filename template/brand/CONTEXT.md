# CONTEXT.md — brand/

How the brand looks and sounds on screen and on air: the visual tokens every thumbnail, card and
caption is drawn from, the brand's two layout components, the exported design assets, the
spoken voice and its narrators, and one profile per platform the brand posts to. Nothing here is
a piece of work: briefs and scripts live in `scripts/`, footage, voice and masters in
`production/`, and cut-downs, captions, thumbnails and posts in `publishing/`. Nor does this
layer hold the written voice or the brand guide's words: where syntek-author is applied, those
stay in its brand and style files, and this layer cites them rather than copying them.

## Directory Tree

```text
brand/
├── CONTEXT.md                  ← this file
├── CLAUDE.md                   ← operating rules for the layer
├── docs/                       ← the guides: the kit, Claude Design, exports, the voice, profiles
│   ├── reference/              ← template-owned guides, updated by copier update
│   └── project/                ← your own guides; a same-named file overrides reference/
├── src/                        ← the brand itself
│   ├── design-register.md      ← seed: one row per design, with its Claude Design link
│   ├── design-system/          ← tokens.css, fonts/ and previews/: the source of every layout
│   ├── exports/                ← exported design assets: small ones in Git, large/ in Git LFS
│   ├── voice/                  ← voice.md: the spoken voice, narrators and pronunciations
│   └── platforms/              ← one profile per selected platform, plus overrides.toml
└── workflows/                  ← the procedures, one folder per brand job
    ├── NN-verb-first-name/     ← template procedures: CONTEXT · CLAUDE · STEPS · CHECKLIST
    └── local/                  ← your own procedures; a same-slug local workflow wins
```

## What's here

- `brand/docs/reference/` — five guides: `the-brand-kit.md`, `claude-design.md`,
  `design-exports.md`, `the-spoken-voice.md` and `platform-profiles.md`.
- `brand/docs/project/` — your own guides. The template ships only the folder's pair.
- `brand/src/` — the brand. **`brand/src/design-system/tokens.css` is the one source of every
  colour, typeface, space and caption style** a layout uses, and **`brand/src/voice/voice.md` is
  the one record of every narrator and pronunciation** a voiceover uses.
- `brand/workflows/` — six procedures, numbered and frozen: set up the brand kit, sync with
  Claude Design, record a design export, set up a platform, write the spoken voice, and check the
  setup before the first credit is spent.

Set the brand up before the first piece is cut: a thumbnail, a title card or a burned caption
made before the kit is settled has to be made again once it is.

## Cross-references

- `.claude/rules/syntek-media/01-layout-and-routing.md` — the layer table, the pair rule and the
  ownership classes this layer follows.
- `.claude/rules/syntek-media/03-production-ethics.md` — who decides what, credits, and consent
  before a voice is cloned.
- `toolkit/templates/` — the fallback layouts, used only where the brand's own are absent.
- `production/src/rights-register.md` — the licence behind every font and the consent behind
  every cloned voice.
- `publishing/docs/reference/platform-specs.md` — the platform facts a profile never restates.
