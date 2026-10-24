@./CONTEXT.md

# CLAUDE.md — .gemini/

Read order: every `.claude/syntek-*-agents.md` → `.claude/CLAUDE.md` → `.claude/MEMORY.md` →
this folder's `CONTEXT.md` (imported above) → this file, before changing `settings.json`.

## Purpose (one line)

Keep Gemini CLI's project settings working, without overriding the author's choices.

## How to work here

- **Routing:** the shared read order, client setup and model tiers → every
  `.claude/syntek-*-agents.md` and the rules it names; Gemini CLI's settings → `settings.json`.
- **Model:** the mechanical tier for an agreed setting; the substantive tier for a permission or
  a decision about what Gemini CLI may do.
- **Concrete steps:** read `settings.json` → agree the change with the author → edit only the
  agreed keys → check the file still parses as JSON → restart Gemini CLI and confirm it still
  reads `GEMINI.md`, the rules and the skills.
- **Definition of done:** the file parses, existing server entries and excluded tools are kept,
  and the change is recorded in `.claude/MEMORY.md` when it is a decision.

## Guardrails

- **Never add a key, a token or a permission bypass.** Credentials stay in Gemini CLI's own store
  or the environment.
- **Never remove a tool from `tools.exclude`** that the project's `.claude/settings.json` still
  denies.
- **Never copy skills into this folder.** A second copy drifts from `.claude/skills/`.
- **Client permission is not the author's approval**, and a configured server is not approval
  to spend credits: the rules still decide.
- This pair and `settings.json` are the author's. `copier update` never re-renders them; its
  update script only adds a shipped MCP server to `settings.json` once (see `CONTEXT.md`).

## Output & naming

- `settings.json` — Gemini CLI's workspace settings. Nothing here is generated after the first
  copy.
