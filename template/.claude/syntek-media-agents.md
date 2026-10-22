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
5. Read every other `.claude/syntek-*-agents.md` present, such as the writing template's
   bridge where it is applied. Each governs its own template's layers and skills.

Existing AGENTS.md, GEMINI.md and project-specific instructions remain authoritative. The
canonical rules define the piece ladder, approval, rights, disclosures, captions, output
paths and paid-call discipline. Do not infer author approval from client permissions.

## Skills, models and capabilities

- .agents is a real folder. Its skills entry is a relative symbolic link to ../.claude/skills,
  so both paths expose one skill tree, with one copy of each SKILL.md and its mode files.
  Keep one copy of each skill. Never make .agents itself a link: Codex mounts it read-only,
  and its sandbox refuses a read-only link to a writable folder, so every command fails.
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

Fresh generation supplies root AGENTS.md and GEMINI.md, the .agents folder and
.codex/config.toml.
Codex uses CLAUDE.md as a fallback instruction filename after the user trusts the project.
Antigravity reads GEMINI.md and discovers skills through .agents/skills. This bridge explicitly
loads nested rules, whose native discovery formats differ between clients.

Before copying media into a project where .agents is a link, add --exclude /.agents to the
Copier copy command, then follow step 3 below. Where .agents/skills is a real directory,
preserve it and add --exclude /.agents/skills; a .agents/skills link of any target needs no
exclude, because Copier skips it and leaves it as it is. Copier fails before its skip check when
rendering a link onto a path that resolves to a directory. Integrate that existing skill tree
manually after the copy; never rename or remove it to make the copy succeed. Updates never
write under .agents.

Where .agents is a link to a folder outside the project, Copier refuses to render anything
beneath it, exclusions included, so the link alone is moved aside and put back. Updates do
this themselves: they rename it to .agents.syntek-held before the render and back
afterwards, never touching its target. If an update stops before it ends (a refused answer,
Ctrl-C at a question, or Copier failing as it cleans up after the render), the link stays
held as `.agents.syntek-held`, and the next update refuses the changed tree; where the link
is committed and the update stopped after its render, Copier has already put an identical
`.agents` link back. Put the link back from the project root, in a POSIX shell (Terminal on
macOS and Linux, Git Bash on Windows; never PowerShell's `rm`), before anything else, and
before discarding the stopped update with `git reset --hard` and `git clean -fd`, which
would delete a held link Git does not track. First check what stands at `.agents`:
`ls -ld .agents .agents.syntek-held`. Where it shows no `.agents.syntek-held`, nothing is
held: stop here and change nothing. Where `.agents` is a link (its line shows `->`), remove
that link alone with `rm .agents` (never `rm -r`, never a trailing slash); where it is a
folder or a file, move it aside to a name nothing holds yet (`ls -ld .agents.from-update`
finds nothing) with `mv .agents .agents.from-update` (no trailing slash), which holds what
the update wrote (check it, and delete nothing in it that is yours). Then, once
`ls -ld .agents` finds nothing, run `mv .agents.syntek-held .agents` (no trailing slash).
Never run that `mv` while `.agents` stands: it would put the held link inside it, and inside
the folder outside the project where `.agents` is a link. Then update again; where
`git status` still shows changes (a stop after the render), discard the stopped update
first: run `git clean -n -d`, a dry run, move out of the project anything of yours it lists,
then `git reset --hard && git clean -fd`. Where the held link was committed beside an
identical `.agents` link, the next update moves nothing, says so, and asks you to remove the
held link (`rm .agents.syntek-held`), commit, and update again. Before a copy, run
`mv .agents .agents.syntek-held`, copy with --exclude /.agents, then run
`mv .agents.syntek-held .agents`.

Where Git checks links out as text (core.symlinks=false, usually on Windows),
.agents/skills arrives as a small file holding its target. Enable symbolic links (Developer
Mode or an administrator shell, then git config core.symlinks true) and recreate it from the
project root: `ln -s ../.claude/skills .agents/skills`, or in PowerShell
`New-Item -ItemType SymbolicLink -Path .agents\skills -Target ..\.claude\skills`.

Claude Code's project MCP file is .mcp.json. Antigravity's workspace MCP file is
.agents/mcp_config.json. Both ship with an empty mcpServers object; Codex MCP servers belong
in .codex/config.toml using its TOML format. A .claude/mcp_config.json left by an older
release is no longer read; merge any server it holds into .agents/mcp_config.json.
Configure and authenticate servers locally using the chosen client's current documentation.
Remote server fields differ between formats: do not copy configuration blindly. Keep secrets
out of Git, preserve existing server entries, and keep ElevenLabs's base path covering the
project. A configured server does not approve a credit-spending call.

## Enabling an existing project

These entrypoints and client settings are copy-only shared files. Copier update delivers
this bridge and rules, but never creates new copy-only files in an existing project. Updating
across 0.4.2 runs one migration: where .agents is a link to .claude, it makes the real folder
and moves .claude/mcp_config.json into it where that path is free, and reports anything else.
An .agents link to a folder outside the project is held aside and restored by every update,
as Client setup says; it is never converted.

1. Read .copier-answers.syntek-media.yml for the recorded source, ref and answers. Generate a
   fresh project in a separate temporary folder using that source and ref and those answers
   as the data file. Keep the fresh answers record there; do not replace the real project's
   answers or run another copy over the real project.
2. Review the generated AGENTS.md, GEMINI.md, .codex/config.toml and its folder pair, and
   the .agents folder. Copy only missing files into the project. An existing file, folder or
   link must be preserved; ask the owner how to combine settings or route its existing
   entrypoint to this bridge.
3. Where .agents is absent, create the folder, then the relative link
   `ln -s ../.claude/skills .agents/skills`, and copy .agents/mcp_config.json. Where .agents
   is still a link to .claude, run the 0.4.2 migration again with the command it printed, or
   with the owner's agreement remove that link (never its target) and do the same. Do not
   replace a real folder or another link.
4. Add an agreed pointer to this bridge in an existing AGENTS.md or GEMINI.md, telling the
   client to read every `.claude/syntek-*-agents.md` present. Review any existing Codex
   configuration before adding the CLAUDE.md fallback. Restart the client and confirm that it
   reads this bridge, the active rules, memory and the intended skill tree.

Missing authentication or a preserved incompatible alias needs local setup before that
capability works. Template updates never overwrite the author's solution.
