# CONTEXT.md — .codex/

Codex settings for developing this Copier template. Nothing here ships.

## Directory Tree

```text
.codex/
├── CONTEXT.md    ← this map
├── CLAUDE.md     ← how to maintain development isolation
└── config.toml   ← no instruction fallback; no skill rules (Codex ignores them here)
```

Root AGENTS.md provides the development instructions. No CLAUDE.md fallback is enabled:
product manuals under template/ must stay source text. Codex 0.160.1 honours skills.config only in the user's
config.toml and -c flags, so this file cannot disable a product skill. From the repository root Codex
finds none; under template/ it finds all seventeen and reads the product's AGENTS.md: never start it there.

See `.github/scripts/dev-isolation.sh`, `.claude/CLAUDE.md` Section 3 and DESIGN.md D73.
