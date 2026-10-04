# CONTEXT.md — production/src/audiobook/

One chapter register per audiobook, recording each chapter from its source to a mastered,
checked file: the route chosen for it, its takes or recording, its master, its duration and its
check. Chapter text chunks and their takes sit in `production/src/audiobook/generated/`, and the
mastered chapters in `production/src/audiobook/renders/`; both are git-ignored, and chapter text
is never copied into a tracked file.

## Directory Tree

```text
production/src/audiobook/
├── CONTEXT.md          ← this file
├── CLAUDE.md           ← operating rules and the register skeleton
├── <piece>.md          ← one audiobook's chapter register, named for its piece folder
├── <piece>.ch00.md     ← its opening credits' spoken words (ch99: the closing credits)
├── generated/          ← chapter text chunks and their takes (git-ignored; README only)
└── renders/            ← mastered chapters, <piece>.chNN.mp3 (git-ignored; README only)
```

## What's here

- `<piece>.md` — frontmatter `piece`, `approved`, `route`, `channels`, `voice_use`, `model_id`
  and `output_format`, then one row per chapter, with the credit rows `ch00` and `ch99`. It is
  the audiobook's plan: an audiobook has no script, and the register approved is its M2.
  **`production/docs/reference/audiobook-narration.md` explains the three routes**, where each
  channel stands, and the ACX targets.
- `<piece>.ch00.md` and `<piece>.ch99.md` — the opening and closing credits' spoken words, the
  Source of their rows: the only text this folder holds.
- `production/src/audiobook/generated/` — chunks and each chapter's chunk sidecar written by
  `python3 toolkit/media.py audiobook text`, and their takes, renamed by `take add`.
- `production/src/audiobook/renders/` — chapters mastered by `audiobook master` and measured by
  `audiobook check`.
- A human narrator's recordings are source media, logged in the footage manifest; so is each
  approved master, because none can be made again for nothing. A chunk take is archived too only
  where the author wants it kept.

## Cross-references

- `production/workflows/05-narrate-an-audiobook/` — voicing or recording the chapters.
- `production/workflows/06-master-an-audiobook/` — mastering, checking and packaging them.
- `.claude/skills/narrate-audiobook/SKILL.md` — the skill both procedures use.
- `production/src/footage/manifest.toml` — where recordings and approved masters (and any take
  the author keeps) are archived.
