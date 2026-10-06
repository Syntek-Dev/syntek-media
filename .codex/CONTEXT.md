# CONTEXT.md — .codex/

Codex settings for developing this Copier template. Nothing here ships.

## Directory Tree

```text
.codex/
├── CONTEXT.md    ← this map
├── CLAUDE.md     ← how to maintain development isolation
└── config.toml   ← disables the ten product skills
```

Root AGENTS.md provides the development instructions. No CLAUDE.md fallback is enabled:
product manuals under template/ must stay source text. All ten template skill folders are
disabled using Codex's skills.config settings. Paths are relative to this .codex folder.

See `.github/scripts/dev-isolation.sh`, `.claude/CLAUDE.md` Section 3 and DESIGN.md D73.
