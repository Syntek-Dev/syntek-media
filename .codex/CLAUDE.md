@./CONTEXT.md

# CLAUDE.md — .codex/ development settings

Read order: root AGENTS.md → `.claude/CLAUDE.md` → DESIGN.md → this folder's CONTEXT.md
(imported above) → this file, before changing config.toml.

## Purpose (one line)

Keep product skills and manuals out of Codex template-development work.

## How to work here

- Read existing configuration and DESIGN.md D73 before changing config.toml or the user-level recipe.
- Never add [[skills.config]] here: Codex reads it only from ~/.codex/config.toml and -c flags.
- Start Codex at the repository root. To hide product skills under template/ as well, add one
  user-level rule per skill, to its SKILL.md (a folder path never matches):
  [[skills.config]]
  path = '/ABSOLUTE/PATH/TO/syntek-media/template/.claude/skills/voiceover/SKILL.md'
  enabled = false
- One rule for each of the seventeen folders under template/.claude/skills/: the ten media
  skills of DESIGN.md Section 5.1 and the seven family skills of Section 5.3 (D80) — grilling,
  grill-with-docs, grill-me, handoff, wayfinder, to-questionnaire and wait-what — which Codex
  finds through template/.agents/skills like the others. A rule is matched on the path, so it
  never hides a user-level skill of the same name elsewhere.
- When an approved product skill is added, add its line to that recipe; verify with
  `.github/scripts/dev-isolation.sh` and the relevant source audits.

## Guardrails

- No product instruction fallback, model selection, permission bypass, trust override or
  MCP credential belongs in this shared development configuration. Its one MCP server is
  code-review-graph, the same entry as the root .mcp.json: --tools omits embed_graph_tool and its
  env blanks the cloud-embedding keys.
- Files under template/ remain source text; their production instructions never govern here.

## Output & naming

- config.toml holds no skill rule and no fallback; nothing here ships.
