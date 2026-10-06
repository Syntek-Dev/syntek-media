# Shared media instructions for coding agents

> **Template-owned.** Updated by syntek-media. Keep project rules in the project's own
> instructions and local overrides, never in this file.

## Read order and precedence

1. Read `.claude/CLAUDE.md` and its referenced CONTEXT.md files explicitly. An import line in
   a Claude manual is a pointer to read, even when this client does not expand it.
2. Read every active Markdown rule recursively under .claude/rules, including each template's
   subfolder. Apply a path-scoped rule when its paths match the task. Read project settings
   and overrides first when a rule refers to them; syntek-author's project settings, where
   present, outrank template rules. Do not rely on automatic discovery of nested rules.
3. Read `.claude/MEMORY.md`, then the CONTEXT.md and CLAUDE.md of the folder being worked in.
   Follow the folder's routing to project guides and local workflows before template ones.
4. Read the chosen skill's SKILL.md and its selected brand-kind mode file before following
   it. Discover only skills present in this project; platform and media-kind gates still apply.

Existing AGENTS.md, GEMINI.md and project-specific instructions remain authoritative. The
canonical rules define the piece ladder, approval, rights, disclosures, captions, output
paths and paid-call discipline. Do not infer author approval from client permissions.

## Skills, models and capabilities

- .agents is a relative symbolic link to .claude. Both paths expose one skill tree, with one
  copy of each SKILL.md and its mode files. Keep one copy of each skill.
- Rules 05 defines substantive and mechanical tiers. On Codex and Antigravity, opus and
  sonnet are tier labels: use suitable models chosen by the owner in that client. No automatic
  provider switch or pinned version is required. Keep the substantive review boundaries.
- Client tool names may differ. Map an available tool by capability, then follow the same
  input checks and spending approval. If a required capability is unavailable, report that
  limit and use the documented manual or offline route; never pretend a call succeeded.
- Claude Design exports and ElevenLabs calls require an installed, authenticated capability
  in the chosen client. Local binaries and the toolkit remain available independently.
- Claude settings govern Claude Code. They do not configure Codex or Antigravity permissions,
  model selection or compaction. Preserve durable decisions and progress in project memory
  and a handoff before the client loses context.

## Client setup

Fresh generation supplies root AGENTS.md and GEMINI.md, .agents and .codex/config.toml.
Codex uses CLAUDE.md as a fallback instruction filename after the user trusts the project.
Antigravity reads GEMINI.md and discovers skills through .agents/skills. This bridge explicitly
loads nested rules, whose native discovery formats differ between clients.

Before copying media into a project with a real .agents directory, preserve that directory
and add --exclude /.agents to the Copier copy command. Copier can fail before its skip check
when rendering a link onto a directory. Integrate that existing skill tree manually after the
copy; never rename or remove it to make the copy succeed. Updates already exclude the alias.

Claude Code's project MCP file is .mcp.json. Antigravity's workspace MCP file is
.claude/mcp_config.json, also visible as .agents/mcp_config.json. Both ship with an empty
mcpServers object; Codex MCP servers belong in .codex/config.toml using its TOML format.
Configure and authenticate servers locally using the chosen client's current documentation.
Remote server fields differ between formats: do not copy configuration blindly. Keep secrets
out of Git, preserve existing server entries, and keep ElevenLabs's base path covering the
project. A configured server does not approve a credit-spending call.

## Enabling an existing project

These entrypoints and client settings are copy-only shared files. Copier update delivers
this bridge and rules, but never creates new copy-only files in an existing project.

1. Read .copier-answers.syntek-media.yml for the recorded source, ref and answers. Generate a
   fresh project in a separate temporary folder using that source and ref and those answers
   as the data file. Keep the fresh answers record there; do not replace the real project's
   answers or run another copy over the real project.
2. Review the generated AGENTS.md, GEMINI.md, .codex/config.toml and its folder pair,
   .claude/mcp_config.json and .agents link. Copy only missing files into the project. An
   existing file, real directory or differently targeted link must be preserved; ask the owner
   how to combine settings or route its existing entrypoint to this bridge.
3. Where .agents is absent, create the relative link .agents -> .claude. Do not replace an
   existing alias or directory. Where it already targets .claude, no change is needed.
4. Add an agreed pointer to this bridge in an existing AGENTS.md or GEMINI.md. Review any
   existing Codex configuration before adding the CLAUDE.md fallback. Restart the client and
   confirm that it reads this bridge, the active rules, memory and the intended skill tree.

Missing authentication or a preserved incompatible alias needs local setup before that
capability works. Template updates never overwrite the author's solution.
