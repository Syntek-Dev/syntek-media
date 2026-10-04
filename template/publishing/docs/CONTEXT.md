# CONTEXT.md — publishing/docs/

The publishing layer's guides: short, practical notes on the judgement calls between a master and
a post. Which moments stand alone as a cut? Is this caption readable at the speed it is shown? Does
this platform want its AI label set for this voice? Where does a limit come from, and how old is
it? Each guide defers to the media rules file that owns its requirement rather than restating it,
and cites platform limits by their key in `toolkit/data/platforms.toml`, never as a number. No
plans, captions or packages live here; they live in `publishing/src/`.

## Directory Tree

```text
publishing/docs/
├── CONTEXT.md            ← this file
├── CLAUDE.md             ← operating rules for the guides
├── reference/            ← template-owned guides, updated by `copier update`
└── project/              ← your own guides; a same-named file here overrides reference/
```

## What's here

- `reference/` — the template's guides: six for the work every piece meets on its way out, and
  one for each platform the project posts to. **Template-owned:** never edit them in place, because
  `copier update` merges template changes into them. `reference/CONTEXT.md` lists the guides this
  project has.
- `project/` — the author's guides, empty at generation. **A same-named guide here overrides the
  reference guide.**

## Cross-references

- `publishing/docs/reference/CONTEXT.md` — the reference guides in this project, one line each.
- `.claude/rules/syntek-media/01-layout-and-routing.md` — the reference/project ownership split.
- `publishing/workflows/CONTEXT.md` — the procedures that cite these guides step by step.
