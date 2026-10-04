# CONTEXT.md — brand/workflows/06-check-the-setup/

The procedure for checking, before the first credit is spent and whenever a tool may have
changed, that this machine and this project can do what the media layers ask of them. It runs
`python3 toolkit/media.py check --setup`, which changes nothing: ffmpeg and ffprobe with the
libraries the toolkit needs, Python, uv, the pinned Playwright's Chromium, git-lfs where large
exports exist, the permission entries in `.claude/settings.json`, and whether the user-scope
ElevenLabs server's base path contains this repository. Each finding is fixed with the author, or
recorded with the commands it blocks.

## Directory Tree

```text
brand/workflows/06-check-the-setup/
├── CHECKLIST.md        ← model-tagged checklist; tick it as you go
├── CLAUDE.md           ← operating rules for this procedure
├── CONTEXT.md          ← this file: when to use it, what it produces
└── STEPS.md            ← the ordered steps, each naming its skill and guide
```

## When to use this

- Straight after the project is generated, or after syntek-media is applied over a
  syntek-author project.
- Before the first credit-spending call to ElevenLabs, and after any change to the server.
- On a new machine, or after an operating-system or tool upgrade.
- When a toolkit command exits 2 naming a missing tool.

Reach for a **different** procedure when the toolkit runs but a check about the work fails: the
kit (`brand/workflows/01-set-up-the-brand-kit/`), a large export
(`brand/workflows/03-record-a-design-export/`).

## What it produces, and where

- **A report** to the author: each finding, its fix, and what it blocks until fixed.
- **Fixes made with the author**, one at a time; a permission entry added to
  `.claude/settings.json` only on the author's explicit word.
- **A dated line** in `.claude/MEMORY.md` under Status: the setup is clean, or what remains open.

## The failure this procedure exists to prevent

A missing tool found halfway through a piece: a render that cannot burn captions, a thumbnail
that cannot be drawn, a speech-to-text call that the server rejects as outside its allowed
folder, or a credit-spending call that never asked permission because its rule was missing. Each
costs time, and the last costs money. Checked once, before the first spend, every gap is named
with its fix while nothing depends on it.

## Cross-references

- `.claude/rules/syntek-media/04-toolkit-pipeline.md` — Section 4, what the toolkit needs.
- `production/docs/reference/elevenlabs.md` — the server's setup and its base path.
- `brand/docs/reference/design-exports.md` — git-lfs and the tripwire.
