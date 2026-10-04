# CONTEXT.md — .claude/

The Claude Code configuration for **developing** the template — not the configuration a generated project receives, which lives in `template/.claude/`.
Its job is the opposite of the product's: where `template/.claude/` loads skills and rules into a session in a generated project, this folder keeps them out of the maintainer's.
Nothing here ships (`_subdirectory: template`).

## Directory Tree

```text
.claude/
├── CONTEXT.md        ← this file
├── CLAUDE.md         ← the development manual: contract, dev isolation, token discipline, recipes
└── settings.json     ← dev isolation: a Skill(<name>) deny for every template skill, and claudeMdExcludes
```

## What's here

- `CLAUDE.md` — how to work on the template. It imports the root `CONTEXT.md` and this file, and routes every design question to `DESIGN.md`.
- `settings.json` — **two layers of isolation, both required** (DESIGN.md Section 7). `permissions.deny` lists `Skill(<name>)` for every skill under `template/.claude/skills/`, because Claude Code loads a nested skills folder as soon as a session reads a file beneath it; `claudeMdExcludes` keeps `template/**/CLAUDE.md` and `template/.claude/**` out of development sessions. Every new template skill needs its deny line here, added or approved by the maintainer.
- There is no `MEMORY.md`, no hook, no skills folder and no MCP configuration: the template's own decisions live in `DESIGN.md` and `CHANGELOG.md`, where a reviewer can see them, and nothing here calls ElevenLabs.

## Cross-references

- `template/.claude/` — the product's configuration, which this folder isolates.
- `.github/scripts/dev-isolation.sh` — proves every template skill is denied here and that `claudeMdExcludes` is present.
- `DESIGN.md` Section 7 — the dev-isolation decision; D5 and D11 — how the product's own `.claude/` is owned.
