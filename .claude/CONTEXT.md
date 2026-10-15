# CONTEXT.md — .claude/

The Claude Code configuration for **developing** the template — not the configuration a generated project receives, which lives in `template/.claude/`.
Its job is the opposite of the product's: where `template/.claude/` loads skills and rules into a session in a generated project, this folder keeps them out of the maintainer's.
Nothing here ships (`_subdirectory: template`).

## Directory Tree

```text
.claude/
├── CONTEXT.md        ← this file
├── CLAUDE.md         ← the development manual: contract, dev isolation, token discipline, recipes
└── settings.json     ← dev isolation (Skill denies, skillOverrides "off", claudeMdExcludes) and the house session settings
```

## What's here

- `CLAUDE.md` — how to work on the template. It imports the root `CONTEXT.md` and this file, and routes every design question to `DESIGN.md`.
- `settings.json` — **three layers of isolation, all required** (DESIGN.md Section 7). `permissions.deny` lists `Skill(<name>)` for every skill under `template/.claude/skills/`, because Claude Code loads a nested skills folder as soon as a session reads a file beneath it; `skillOverrides` sets each of them `"off"`, because a deny refuses a skill but leaves it listed; `claudeMdExcludes` keeps `template/**/CLAUDE.md` and `template/.claude/**` out of development sessions. Every new template skill needs its deny line and its `skillOverrides` entry here, added or approved by the maintainer.
- `settings.json` also carries the house development settings, matched to syntek-base's own (maintainer, 15/10/2026): an allow list of read-only commands (`ls`, `grep`, `jq`, read-only `git` and `gh` and the like); denies on reading any `.env` file other than an example, by `Read` and by `Bash`; denies on `AskUserQuestion`, plan mode, `ReportFindings`, `DesignSync`, `NotebookEdit`, `PushNotification`, `RemoteTrigger`, `ScheduleWakeup` and the cron tools, so a session asks its questions in plain text; and `model`, `outputStyle`, `effortLevel`, `ultracode`, the workflow and auto-permission prompts, `autoCompactEnabled: false`, the disabled bundled skills, artifacts, claude.ai connectors, Remote Control and prompt suggestions, and the Syntek plugins off. `SendMessage` stays allowed, for messaging the syntek-author session. syntek-base's hooks and its ClickUp edit deny are not taken: media has neither the hook scripts nor that folder.
- There is no `MEMORY.md`, no hook and no skills folder. The one MCP server is the root `.mcp.json`'s `code-review-graph` (a local graph of this repository's code for reviews; `/.code-review-graph/` is ignored), launched with `--tools` naming every tool but `embed_graph_tool`, so no client is offered it, and with the cloud-embedding keys (`GOOGLE_API_KEY`, `VOYAGE_API_KEY`, `MINIMAX_API_KEY`, `CRG_OPENAI_API_KEY`, `CRG_OPENAI_BASE_URL`, `CRG_ACCEPT_CLOUD_EMBEDDINGS`) set empty in its `env`, so it cannot send code text out; `settings.json` also denies `embed_graph_tool` and asks before `apply_refactor_tool` and `generate_wiki_tool`. When the server's tools change, update the `--tools` list in both files. Never run `code-review-graph install` here: it writes hooks, skills and rules-file text the dev isolation refuses. The template's own decisions live in `DESIGN.md` and `CHANGELOG.md`, where a reviewer can see them, and nothing here calls ElevenLabs.

## Cross-references

- `template/.claude/` — the product's configuration, which this folder isolates.
- `.github/scripts/dev-isolation.sh` — proves every template skill is denied here, that `claudeMdExcludes` is present, and that the root `.agents/` is a real folder exposing nothing (check 6).
- `DESIGN.md` Section 7 — the dev-isolation decision; D5 and D11 — how the product's own `.claude/` is owned.
