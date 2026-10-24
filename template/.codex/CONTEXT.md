# CONTEXT.md — .codex/

Codex's project settings. Written once when the project was generated and the author's from
then on: `copier update` never renders, recreates or re-renders anything here. Its update
script only adds each MCP server a syntek template ships, once, to `config.toml` where it is
missing, and never adds back one you removed. The rules, skills and memory Codex follows live
in `.claude/`, which every client shares.

## Directory Tree

```text
.codex/
├── CONTEXT.md     ← this file (yours)
├── CLAUDE.md      ← how to change these settings (yours)
└── config.toml    ← the CLAUDE.md fallback, the model if one was chosen, local MCP servers (yours)
```

## What's here

- `config.toml` — `project_doc_fallback_filenames = ['CLAUDE.md']`, so a Codex session started
  inside a folder reads its `CLAUDE.md` and its parents' where there is no `AGENTS.md`, and
  `model` when one was chosen at generation. Codex loads it only after you trust the project.
  It sets no trust level, permission bypass or credential. Codex ignores a model provider set in
  a project file (with a warning): a local model for Codex belongs in your user-level settings.
- MCP servers for Codex go here as `[mcp_servers.<name>]` tables, in Codex's TOML format. Two
  ship in every project, `code-review-graph` and `scrapling`, each with a
  `[mcp_servers.<name>.tools.<tool>]` table setting `approval_mode = "prompt"` for every tool
  the project's `.claude/settings.json` asks before using: Codex runs a tool its server marks
  read-only without asking, so these tables are what make it ask. `code-review-graph`'s cloud
  keys are blank. Add other servers beside them and authenticate them locally; never commit a
  key. When `.claude/settings.json` gains an ask for a server declared here, `--write` from any
  `.claude/syntek-*-permissions.py` (they are the same script) adds its table; you may also
  add one by hand.

## Cross-references

- Every `.claude/syntek-*-agents.md` — the read order and setup every client shares, and the
  model each client uses.
- `AGENTS.md` — Codex's entrypoint at the project root.
