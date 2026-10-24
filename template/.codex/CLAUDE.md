@./CONTEXT.md

# CLAUDE.md — .codex/

Read order: every `.claude/syntek-*-agents.md` → `.claude/CLAUDE.md` → `.claude/MEMORY.md` →
this folder's `CONTEXT.md` (imported above) → this file, before changing `config.toml`.

## Purpose (one line)

Keep Codex's project settings working, without overriding the author's choices.

## How to work here

- **Routing:** the shared read order, client setup and model tiers → every
  `.claude/syntek-*-agents.md` and the rules it names; Codex's settings → `config.toml`.
- **Model:** the mechanical tier for an agreed setting; the substantive tier for a permission or
  a decision about what Codex may do.
- **Concrete steps:** read `config.toml` → agree the change with the author → edit only the
  agreed keys → check the file still parses as TOML → restart Codex and confirm it still reads
  `AGENTS.md`, the rules and the folder manuals.
- **Definition of done:** the file parses, the `CLAUDE.md` fallback is still there, and the
  change is recorded in `.claude/MEMORY.md` when it is a decision.

## Guardrails

- **Never remove the `CLAUDE.md` fallback.** Without it Codex reads no folder manual.
- **Never add a trust level, a permission bypass or a credential.** Keys stay in Codex's own
  credential store or the environment.
- **Client permission is not the author's approval**, and a configured server is not approval
  to spend credits: the rules still decide.
- This pair and `config.toml` are the author's. `copier update` never re-renders them; its
  update script only adds a shipped MCP server to `config.toml` once (see `CONTEXT.md`).

## Output & naming

- `config.toml` — Codex's project settings. Nothing here is generated after the first copy.
