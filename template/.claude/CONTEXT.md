# CONTEXT.md — .claude/

Claude Code's configuration for <%BRAND_NAME%>: the project manual, the template's rules, the
project memory, the settings, the hooks and the skills. Nothing here is the work itself; it is
how the work is done. Some of it belongs to the project and some to the template, and the tree
marks which is which.

## Directory Tree

```text
.claude/
├── syntek-media-agents.md       ← the bridge for Codex, Gemini CLI, Antigravity and OpenCode (template-owned)
├── syntek-media-permissions.py  ← passes settings.json's denies and asks to the other clients' files (template-owned)
├── syntek-media-dataroot.py     ← the data-root resolver and the guard the PreToolUse hook runs (template-owned)
├── syntek-media-dataroot.json   ← media's filing folders on the data root: none (template-owned)
├── CLAUDE.md               ← the project brief, where the rules live, project rules (read first; yours)
├── CONTEXT.md              ← this file (yours)
├── MEMORY.md               ← project memory: facts, decisions, feedback, status (read second; yours)
├── settings.json           ← model, permissions, the ask rules, the session hooks and the data-root guard (yours)
├── settings.local.json     ← your machine-only overrides, if any (git-ignored; never committed)
├── hooks/                  ← context-threshold-handoff.sh, pre-compact-handoff.sh and the pair (all shared)
├── rules/                  ← rules loaded at launch, one folder per template (no pair here)
│   └── syntek-media/       ← the template's rules, loaded at launch (template-owned; never edit)
│       ├── 01-layout-and-routing.md   ← the brand brief (Section 1), layers, the piece, ownership
│       ├── 02-skills.md               ← the media skills, the family-shared skills and the companions
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
  toolkit, ffmpeg and ffprobe, an ask list that makes every credit-spending ElevenLabs tool and
  the shipped MCP servers' browser and writing tools prompt, a deny list that keeps hand edits
  out of generated and renders folders, and the `UserPromptSubmit` window hook, the
  `PreCompact` hook and the `PreToolUse` data-root guard. It is committed and shared; personal
  overrides (such as `CLAUDE_CONTEXT_WINDOW` under `"env"`, for a larger window) belong in
  `settings.local.json`.
- `hooks/` and `skills/` — see each folder's own `CONTEXT.md`.
- `syntek-media-agents.md` — how the other coding agents reach this folder: the read order they
  follow by hand, the model tiers, each client's setup and how to add a client later.
- `syntek-media-permissions.py` — run with `python3` (3.11 or later): `--check` reports which of
  `settings.json`'s denies and asks each other client's file carries, and `--write` adds the
  missing ones to client files that already exist. It never creates a file.
- `syntek-media-dataroot.py` and its map `syntek-media-dataroot.json` — the data-root resolver
  every Syntek template ships and the guard the `PreToolUse` hook runs; media's map names no
  folder (`.claude/rules/syntek-media/06-global-rules.md` Section 12).

## Cross-references

- `.claude/rules/syntek-media/01-layout-and-routing.md` — the brand brief, the layers, the folder
  pair, who owns which files, and which rule wins (Section 10).
- `.claude/rules/syntek-media/02-skills.md` — the media skill roster, and the family-shared
  skills' roles.
- `.claude/hooks/CONTEXT.md` — the hook registry and the window threshold.
- `.claude/rules/syntek-media/03-production-ethics.md` — credits, disclosure, rights and consent.
- `.claude/skills/CONTEXT.md` — how skills are laid out.
- `../CONTEXT.md` — the repository overview, imported by `CLAUDE.md`.
