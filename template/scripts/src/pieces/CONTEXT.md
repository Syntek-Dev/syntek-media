# CONTEXT.md — scripts/src/pieces/

One folder per piece: the plan a piece is produced from, and the record of where it stands. Each
folder holds the piece's brief, its words (a script, or a recorded piece's transcript) and its
plan for the picture, and carries its own pair, written when the piece is opened. The template
ships only this pair; every piece folder is yours. A project generated with examples holds one
worked example piece; delete its folder, with the example files named for it in the production
and publishing layers, once you no longer need it, and none of them will come back.

## Directory Tree

```text
scripts/src/pieces/
├── CONTEXT.md              ← this file
├── CLAUDE.md               ← operating rules, and the skeletons of a piece's pair and brief
└── NNN-kebab-title/        ← one piece, numbered from the register, with its own pair
    ├── CONTEXT.md          ← what this piece is for, and where it stands
    ├── CLAUDE.md           ← this piece's traps and its definition of done
    ├── brief.md            ← the plan: frontmatter with status and verified, eleven sections
    ├── script.md           ← a scripted piece's words (transcript.md for a recorded piece)
    ├── storyboard.md       ← a picture for every spoken line
    └── shot-list.md        ← a source for every shot
```

## What's here

- `NNN-kebab-title/` — **one folder per piece**, the number taken from
  `scripts/src/piece-register.md`, three digits, frozen once assigned and never reused.
- `brief.md` — **the one place the piece's plan and status live.** Its skeleton is fenced in
  this folder's `CLAUDE.md`: frontmatter `piece`, `title`, `kind`, `origin`, `picture`,
  `status`, `deliverables`, `source_media`, `target_seconds`, `words_per_minute`, `parent`,
  `source`, `synthetic_voice`, `ai_visuals`, `music`, `rights`, `verified`, `last_updated`,
  then the title and `## Purpose` · `## Audience` · `## Shape` · `## Metaphor` · `## Hook` · `## Key points` ·
  `## Call to action` · `## Disclosure plan` · `## Rights needs` · `## Draws on` · `## Notes`.
  `deliverables` lists full-length deliverables only, as keys of `toolkit/data/platforms.toml`;
  cut-downs live in the piece's cut-down plan. The gates its `status` and `verified` record are
  defined in `scripts/docs/reference/the-piece-ladder.md`.
- `script.md` or `transcript.md` — the words, in the format of
  `scripts/docs/reference/writing-for-the-ear.md`: one spoken sentence per line, beats as H2s.
  A piece has one or the other, never both.
- `storyboard.md` and `shot-list.md` — the format of
  `scripts/docs/reference/storyboards-and-shot-lists.md`. A piece with no picture, or a recorded
  one, has neither: its M3 is recorded `n/a` in the brief.

## Cross-references

- `scripts/docs/reference/the-piece-ladder.md` — the statuses and gates a brief records.
- `scripts/workflows/01-brief-a-piece/` — the procedure that opens a piece folder and writes its
  pair and brief.
- `scripts/src/piece-register.md` — where the number comes from.
