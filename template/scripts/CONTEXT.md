# CONTEXT.md — scripts/

The scripts layer: every piece from idea to an agreed plan. Each piece has a folder of its own
under `scripts/src/pieces/`, holding its brief, its script (or, for a recorded piece, its
transcript), its storyboard and its shot list. Nothing in this layer is rendered, recorded or
posted: footage, voice, cards and the edit live in `production/`, and cut-downs, captions,
thumbnails and posts in `publishing/`. The name means spoken scripts, never code: the toolkit's
code is in `toolkit/`.

## Directory Tree

```text
scripts/
├── CONTEXT.md        ← this file
├── CLAUDE.md         ← operating rules
├── docs/             ← guides: reference/ (template-owned) and project/ (yours)
├── src/              ← the pieces: the register, and one folder per piece
└── workflows/        ← numbered procedures, plus local/ for your own
```

## What's here

- `docs/` — **how a piece is planned and written here.** `docs/reference/` ships with the
  template and is updated by `copier update`; `docs/project/` is yours, and a same-named guide
  there overrides the reference one (the ladder guide excepted: a project guide may only add to
  its gates).
- `src/` — **the pieces themselves.** `src/piece-register.md` assigns every piece its number;
  `src/pieces/` holds one folder per piece, each with its own pair.
- `workflows/` — **the procedures.** Template procedures sit at `workflows/NN-name/`; your own
  sit at `workflows/local/NN-name/` and win over a template procedure with the same slug.

A *piece* is one deliverable work: a short, an explainer, a talk, a trailer, a podcast episode,
an audiobook or a standalone voiceover. It is `scripted` (written first, then voiced or filmed)
or `recorded` (a talk, interview or conversation that already exists as a recording). Its brief
records where it stands on one ladder, from `idea` to `published`, and the gates M1 to M7 between
the rungs are defined in `scripts/docs/reference/the-piece-ladder.md`. This layer carries a
piece to `storyboarded`; the production and publishing layers carry it the rest of the way.

## Cross-references

- `.claude/rules/syntek-media/01-layout-and-routing.md` — the layer table, the piece (Section 5)
  and the pair rule.
- `.claude/rules/syntek-media/03-production-ethics.md` — who decides what, and the ladder's
  requirement (Section 3).
- `scripts/src/CONTEXT.md` — the register and the files a piece carries.
- `scripts/workflows/CLAUDE.md` — 'You want to… | Procedure'.
- `scripts/docs/reference/the-piece-ladder.md` — the gates a piece passes on its way to
  published.
