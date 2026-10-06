@./CONTEXT.md

# CLAUDE.md — .codex/ development settings

Read order: root AGENTS.md → `.claude/CLAUDE.md` → DESIGN.md → this folder's CONTEXT.md
(imported above) → this file, before changing config.toml.

## Purpose (one line)

Keep product skills and manuals out of Codex template-development work.

## How to work here

- Read existing configuration and DESIGN.md D73 before changing a skill exclusion.
- Keep every product skill disabled using a path relative to this .codex folder.
- Add an exclusion when an approved new product skill is added; verify with
  `.github/scripts/dev-isolation.sh` and the relevant source audits.

## Guardrails

- No product instruction fallback, model selection, permission bypass, trust override or
  MCP credential belongs in this shared development configuration.
- Files under template/ remain source text; their production instructions never govern here.

## Output & naming

- config.toml holds the development skill exclusions; nothing here ships.
