# CONTEXT.md — publishing/workflows/07-refresh-the-platform-specs/

The procedure for keeping the platform data honest: finding every table of
`toolkit/data/platforms.toml` that was checked too long ago, re-reading its source at the
platform, and recording each confirmed difference as an `[[override]]` row in
`brand/src/platforms/overrides.toml`, never by editing the data file, which `copier update`
replaces. It re-reads the AI-disclosure rules the project relies on in the same pass. It moves no
piece; it keeps every later render and package from trusting a limit that has changed.

## Directory Tree

```text
publishing/workflows/07-refresh-the-platform-specs/
├── CONTEXT.md        ← this file: when to use it, what it produces
├── CLAUDE.md         ← how to run it; guardrails
├── STEPS.md          ← the ordered procedure
└── CHECKLIST.md      ← tick as you go; model-tagged
```

## When to use this

- About every six months, or whenever `media.py presets --stale-after` lists a stale table.
- A platform has announced a change to a limit, a format or its AI label.
- A render or a package is about to rely on a `verify` key.
- After a `copier update` that refreshed the data file, to retire overrides it made redundant.

Reach for a **different** procedure when the task is the brand's own choices on a platform, such
as its handle or cadence (`brand/workflows/04-set-up-a-platform/`), or remaking a deliverable that
a corrected limit affects (`publishing/workflows/02-cut-for-a-platform/`).

## What it produces, and where

- **Override rows** in `brand/src/platforms/overrides.toml`, each with its source and the date it
  was checked, confirmed by the author.
- **A project guide** in `publishing/docs/project/`, on the author's word, where a disclosure rule
  has changed.
- **A dated hand-back** of every table re-read, every value still unconfirmed, and the next
  refresh.

## The failure this procedure exists to prevent

A limit that was true when the template shipped and quietly stopped being true: a length extended,
a hashtag cap imposed, a caption upload withdrawn. The toolkit verifies every render against what
the data says, so stale data passes a render that the platform then rejects or crops. Dated
tables, a fixed refresh and corrections kept where the toolkit applies and prints them prevent it.

Refresh the Jev scorecard's platform/surface sources and project rubric through
`publishing/docs/reference/scoring-options.md`, preserving earlier evaluation records.

## Cross-references

- `publishing/docs/reference/platform-specs.md` — `verify`, `chosen`, absent keys, overrides and
  staleness.
- `toolkit/data/platforms.toml` — the template-owned data, re-read and never edited here.
- `brand/src/platforms/overrides.toml` — where the brand's confirmed corrections live.
- `publishing/docs/reference/ai-disclosure.md` — the disclosure rules re-read in the same pass.
