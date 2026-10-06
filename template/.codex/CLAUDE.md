@./CONTEXT.md

# CLAUDE.md — .codex/

Read order: `.claude/syntek-media-agents.md` → `.claude/CLAUDE.md` → `.claude/MEMORY.md` →
this folder's `CONTEXT.md` (imported above) → this file, before changing config.toml.

## Purpose (one line)

Maintain Codex's project configuration while preserving the author's settings.

## How to work here

- **Routing:** shared read order and client setup → `.claude/syntek-media-agents.md`;
  project settings → `config.toml`; local capabilities → the chosen client's MCP setup.
- **Model:** the mechanical tier for an agreed setting; substantive review for permissions
  or a decision about tool capabilities.
- **Steps:** read existing configuration, agree any integration, edit only the agreed keys,
  parse TOML, then verify the client still reads the project entrypoint and folder manuals.

## Guardrails

- This pair and config.toml are copy-only shared files. Updates never overwrite them.
- Configure MCP servers in Codex TOML and authenticate locally. Claude Code and Antigravity
  use separate JSON formats; preserve existing entries and keep credentials out of Git.
- Client configuration does not approve paid calls. The canonical spending rules still apply.

## Output & naming

- `config.toml` — local project settings, with no template model or permission bypass.
- Machine credentials stay in the client's local authentication store.
