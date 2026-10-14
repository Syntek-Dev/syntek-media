@./CONTEXT.md

# CLAUDE.md — .agents/ development folder

Read order: root AGENTS.md → `.claude/CLAUDE.md` → DESIGN.md → this folder's CONTEXT.md
(imported above) → this file, before changing anything here.

## Purpose (one line)

Give Codex and Antigravity a development agent folder that exposes no product skill.

## How to work here

- Keep `.agents` a real folder; never replace it with a link (D76).
- Add `skills -> ../.claude/skills` only if the development `.claude/skills/` exists.
- Verify with `.github/scripts/dev-isolation.sh`.

## Guardrails

- Never link or copy anything from template/ here; product skills are source text.
- No MCP file, rules, workflows or credentials belong here.

## Output & naming

- This folder holds its pair, and at most the development skills link.
