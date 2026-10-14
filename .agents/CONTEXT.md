# CONTEXT.md — .agents/

The agent folder Codex and Antigravity read when developing this Copier template. Nothing here
ships (`_subdirectory: template`); the product's own `.agents/` is `template/.agents/`.

## Directory Tree

```text
.agents/
├── CONTEXT.md    ← this map
└── CLAUDE.md     ← how to keep this folder safe
```

It is a real folder, never a link: Codex mounts `.agents` read-only, and its sandbox refuses a
read-only path that is a link to a writable folder (D76). The development `.claude/` has no
skills folder, so there is no `skills` link and no MCP file: nothing here is a tool.

See `.github/scripts/dev-isolation.sh` check 6, `.claude/CLAUDE.md` Section 3 and DESIGN.md D73
and D76.
