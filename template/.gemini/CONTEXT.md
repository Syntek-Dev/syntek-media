# CONTEXT.md — .gemini/

Gemini CLI's project settings. Written once when the project was generated and the author's
from then on: `copier update` never renders, recreates or re-renders anything here. Its update
script only adds each MCP server a syntek template ships, once, to `settings.json` where it is
missing and the file already asks before that server's tools (`--write`, below), and never
adds back one you removed. The rules, skills and memory Gemini CLI follows live in `.claude/`,
which every client shares; it finds the skills through `.agents/skills`.

## Directory Tree

```text
.gemini/
├── CONTEXT.md       ← this file (yours)
├── CLAUDE.md        ← how to change these settings (yours)
└── settings.json    ← the model if one was chosen, excluded tools and MCP servers (yours)
```

## What's here

- `settings.json` — Gemini CLI's workspace settings: `model.name` when a model was chosen at
  generation, `tools.exclude` (the tools the project's `.claude/settings.json` denies, such as
  `ask_user`), `tools.confirmationRequired` (the MCP tools it asks before using, named
  `mcp_<server>_<tool>`), and `mcpServers`, which holds the two servers every project ships,
  `code-review-graph` and `scrapling`, beside any you add. It holds no key or credential:
  `code-review-graph`'s cloud keys are blank. Workspace settings override your user settings
  for this project only, and load only once you trust the folder; folder trust is on by default.
- Any `.claude/syntek-*-permissions.py` (they are the same script) adds a denied or confirmed
  tool here with `--write` when the project's `.claude/settings.json` gains one; the author may
  also edit these keys by hand.
- Skills are not copied here: `.agents/skills` is the one skill tree every client reads.

## Cross-references

- Every `.claude/syntek-*-agents.md` — the read order and setup every client shares, and the
  model each client uses.
- `GEMINI.md` — Gemini CLI's entrypoint at the project root.
