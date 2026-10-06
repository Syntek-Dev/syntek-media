# CONTEXT.md — .codex/

Codex's project configuration. These files are copy-only shared files: an update never
changes them, and an existing configuration stays the author's.

## Directory Tree

```text
.codex/
├── CONTEXT.md    ← this map
├── CLAUDE.md     ← how to maintain this configuration
└── config.toml   ← folder instruction fallback; local MCP settings belong here
```

## What's here

- `config.toml` — enables CLAUDE.md as a fallback instruction filename after the project is
  trusted in Codex. It ships without model selection, credentials or MCP servers.
- The production rules and skills live in the canonical .claude tree. The root AGENTS.md
  routes to `.claude/syntek-media-agents.md`; .agents aliases that same tree.

## Cross-references

- `.claude/syntek-media-agents.md` — shared read order, capabilities and setup.
- `AGENTS.md` — Codex's project entrypoint.
