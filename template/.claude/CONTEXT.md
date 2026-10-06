# CONTEXT.md — .claude/

Claude Code's configuration for <%BRAND_NAME%>: the project manual, the template's rules, the
project memory, the settings and the skills. Nothing here is the work itself; it is how the work
is done. Some of it belongs to the project and some to the template, and the tree marks which is
which.

## Directory Tree

```text
.claude/
├── syntek-media-agents.md  ← shared instructions for Codex and Antigravity (template-owned)
├── mcp_config.json         ← Antigravity workspace MCP servers through .agents (empty; yours)
├── CLAUDE.md               ← the project brief, where the rules live, project rules (read first; yours)
├── CONTEXT.md              ← this file (yours)
├── MEMORY.md               ← project memory: facts, decisions, feedback, status (read second; yours)
├── settings.json           ← model, permissions, the ask rules for credit-spending tools (yours)
├── settings.local.json     ← your machine-only overrides, if any (git-ignored; never committed)
├── rules/                  ← rules loaded at launch, one folder per template (no pair here)
│   └── syntek-media/       ← the template's rules, loaded at launch (template-owned; never edit)
│       ├── 01-layout-and-routing.md   ← the brand brief (Section 1), layers, the piece, ownership
│       ├── 02-skills.md               ← the media skills and the companions
│       ├── 03-production-ethics.md    ← who decides, the ladder, credits, disclosure, rights
│       ├── 04-toolkit-pipeline.md     ← the toolkit and its commands
│       ├── 05-model-allocation.md     ← which model does which work
│       ├── 06-global-rules.md         ← locale and the rules that hold everywhere
│       ├── 07-session-boundaries.md   ← hand off, never compact
│       └── 08-naming-and-memory.md    ← names, and what goes in MEMORY.md
└── skills/                 ← one folder per skill (template-owned) and the folder's pair (yours)
```

## What's here

- `CLAUDE.md` — the operating manual for this project: the project brief, a map of the rules,
  and the project's own rules under 'Project-specific rules'. **Those rules win over the
  template's rules files where the two conflict.**
- `rules/syntek-media/` — the template's rules, `01-…` to `08-…`; Section 1 of the first is the
  brand brief, rendered from the answers and kept current by every update. Claude Code loads
  every Markdown file under `rules/` at launch with the same weight as `CLAUDE.md`, which is why
  this folder holds no `CONTEXT.md` or `CLAUDE.md` of its own. Another template applied to this
  project would add its own folder beside it.
- `MEMORY.md` — the durable memory every session reads second. Template files name its six
  headings. It splits into `memory/<topic>.md` files once it passes 300 lines.
- `settings.json` — `"model": "opus"`, `"autoCompactEnabled": false`, an allow list for the
  toolkit, ffmpeg and ffprobe, an ask list that makes every credit-spending ElevenLabs tool
  prompt, and a deny list that keeps hand edits out of generated and renders folders. It is
  committed and shared; personal overrides belong in `settings.local.json`.
- `skills/` — see the folder's own `CONTEXT.md`.

## Cross-references

- `.claude/rules/syntek-media/01-layout-and-routing.md` — the brand brief, the layers, the folder
  pair, who owns which files, and which rule wins (Section 10).
- `.claude/rules/syntek-media/02-skills.md` — the media skill roster.
- `.claude/rules/syntek-media/03-production-ethics.md` — credits, disclosure, rights and consent.
- `.claude/skills/CONTEXT.md` — how skills are laid out.
- `../CONTEXT.md` — the repository overview, imported by `CLAUDE.md`.
