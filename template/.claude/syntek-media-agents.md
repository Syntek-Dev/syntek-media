# Shared media instructions for coding agents

> **Template-owned.** Updated by syntek-media. Keep project rules in the project's own
> instructions and local overrides, never in this file.

Codex, Gemini CLI, Antigravity and OpenCode reach this file through the root AGENTS.md or
GEMINI.md, which send them to every `.claude/syntek-*-agents.md` present. Claude Code needs
none of it: it loads the same files natively. Nothing here adds a rule; it says how to reach
the rules that already exist.

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
   it; for a family-shared skill, media work reads its `MEDIA-` mode file only
   (`.claude/rules/syntek-media/02-skills.md` Section 2). Discover only skills present in this
   project; platform and media-kind gates still apply.
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
- Rules 05 defines substantive and mechanical tiers and, in its Section 4, the model each
  client the answers name runs here. Elsewhere opus and sonnet are tier labels, not model
  names: use the substantive model for anything that decides meaning; when in doubt, the
  work is substantive.
- Client tool names may differ. Map an available tool by capability, then follow the same
  input checks and spending approval. If a required capability is unavailable, report that
  limit and use the documented manual or offline route; never pretend a call succeeded.
- Claude Design exports and ElevenLabs calls require an installed, authenticated capability
  in the chosen client. Local binaries and the toolkit remain available independently.
- Seven skills are family-shared (`grilling`, `grill-me`, `grill-with-docs`, `wayfinder`,
  `handoff`, `to-questionnaire`, `wait-what`): every Syntek template ships the same SKILL.md,
  and `.claude/rules/syntek-media/02-skills.md` Section 4 gives each role they name its media
  path.

## What Claude Code enforces and other clients must follow

- **Hand off, never compact.** Claude Code's session hooks warn as the window fills and block
  automatic compaction; no other client runs them. Follow
  `.claude/rules/syntek-media/07-session-boundaries.md` by hand: write a handoff with the
  `handoff` skill before the context runs low, and start a new session from it. Turn off
  automatic compaction or summarising where the client allows it (OpenCode's opencode.json does).
- **The settings file's denies and asks are rules.** `.claude/settings.json` denies some edits
  and tools in Claude Code (hand edits in every generated and renders folder and in the user
  guide, the dialog tool, the cloud-embedding tool) and asks before every credit-spending
  ElevenLabs tool, the voice remix, and the browser and writing tools of the two shipped MCP
  servers. Treat every deny there as a rule in this client too, and every ask as a question to
  the author before the call. Where it denies asking the author through a dialog, ask in the
  conversation instead.
- **Passing the settings to each client.** `python3 .claude/syntek-media-permissions.py --check`
  (Python 3.14 or later) prints which of those denies and asks each client's file already
  carries, which it cannot express and why, and exits 1 if one it can express is missing.
  `--write` adds the missing ones to the client files that already exist, changing only their
  permission keys; it never creates a file. Run it once after the first copy, because the
  ElevenLabs asks reach Gemini CLI and OpenCode only this way (and Codex only where its own
  settings declare the server), and again after changing `.claude/settings.json` or adding a
  client, with the author's agreement. Run `--write` too when an update report gives it: the two
  MCP servers reach opencode.json and Gemini CLI's settings only once each holds every ask form.
  Allow rules stay with each client. Every `.claude/syntek-*-permissions.py` present is the same
  script.
- **The data root stays out of the session.** A data root is a folder outside every
  repository that holds a `.syntek-data-root` marker; this machine's is the one
  `SYNTEK_DATA_ROOT` names. Claude Code's `PreToolUse` hook (where `.claude/settings.json`
  wires it) blocks its file tools' edits and writes there, and its searches where it offers
  `Grep` and `Glob`; no other client runs it. Never browse, search, list or edit anything under
  a data root, by any tool or shell command. Media files nothing there:
  `python3 .claude/syntek-media-dataroot.py store` and `root` (Python 3.14 or later) report the
  store and the root, and `.claude/rules/syntek-media/06-global-rules.md` Section 12 says the
  rest; never work round a refusal. Where one of these scripts warns that it did not run because
  Python is older than 3.14, tell the author at once, in its words, and ask them to upgrade.
- **The user guide is read-only.** Claude Code denies edits under `how-to/`, and its guide
  guard (`.claude/hooks/how-to-read-only.sh`, a `PreToolUse` hook) refuses them; no other
  client runs the guard, and OpenCode holds the `how-to/*` deny only where its file carries it
  (a new copy's does; `--write` adds it to an older one). Never edit, write, move or delete
  anything under `how-to/`, except through a template's update, its recovery and the commands
  an update report prints for a file there: every full update puts the guide's files back. A
  departure goes where `.claude/rules/syntek-media/01-layout-and-routing.md` Section 10 says.
- **Permission is not approval.** A client that lets you edit or run a command has not given
  the author's approval. Approving a script, a take, a cut or a post, and anything else the
  rules reserve to the author, still needs the author's explicit word.
- **Paid calls.** A skill that spends credits states the cost and waits for the author, in
  every client. A configured server is not approval to call it.

## Client setup

| Client | Entrypoint | Project settings | Skills |
|---|---|---|---|
| Codex | AGENTS.md | `config.toml` in .codex: the CLAUDE.md fallback, the model, the MCP servers and their prompts | `skills` in .agents |
| Gemini CLI | GEMINI.md | `settings.json` in .gemini: model, MCP servers, excluded tools, confirmations | `skills` in .agents |
| Antigravity | GEMINI.md (and AGENTS.md where present) | `mcp_config.json` in .agents: MCP servers; model chosen in the app | `skills` in .agents |
| OpenCode 2 or later | AGENTS.md | opencode.json (OpenCode 2's format): model, local server, the MCP servers and their asks, permissions, no auto-compaction | `.claude/skills` and `skills` in .agents |

Each client's files ship only for the clients chosen when the project was generated; this bridge
and the rules ship always.

- **Codex** loads this project's settings and its CLAUDE.md fallback only once you trust the
  project; a project marked untrusted loads no AGENTS.md at all. Codex reads instruction files
  once, at the start, and at most 32 KiB of them by default, far less than the rules: read the
  rules files and each folder's manuals directly. It never reads GEMINI.md.
- **Gemini CLI** loads this project's settings, its MCP servers and the .agents skills only
  once the folder is trusted: trust the project when asked. It warns at every start that
  `tools.exclude` is deprecated; that key is the only project-level way to hide `ask_user`
  while workspace policies are disabled, so leave it.
- **Antigravity** reads both entrypoints where both exist; they carry the same pointer. Its
  remote MCP servers take `serverUrl`, not `url`.
- **OpenCode reads no CLAUDE.md at all.** Step 3 of the read order is not optional there: open
  each folder's CONTEXT.md and CLAUDE.md yourself. Start it at the project root: its permission
  paths are relative to the folder it starts in, and the last matching rule wins. OpenCode
  also lists CONTEXT.md and CLAUDE.md in `.claude/skills` as two skills, `CONTEXT` and
  `CLAUDE`: they are the folder's map, not procedures, so never run them. Of the four edit
  denies opencode.json ships, three name another template's paths and are inert here, and the
  fourth, `how-to/*`, is the guide's.
- **Local models** run through OpenCode: opencode.json names the server and its context,
  which must not exceed what the server loads. Test tool calling on a scratch repository
  before trusting a local model with a script. Codex can use a local model only through your
  user-level Codex settings, never this project's.
- **MCP servers.** Every project ships two, pinned and keyless, in `.mcp.json` and in each
  client's own file: `scrapling` (web pages) and `code-review-graph` (a local map of the code).
  Use them as `.claude/rules/syntek-media/06-global-rules.md` Section 13 says: ask the author
  before each of the six asked browser tools, and never run `code-review-graph install` or
  `scrapling install`. Codex and Gemini CLI start them only in a trusted project; OpenCode
  starts them when it opens the project, and runs every tool the project does not ask for
  without a prompt, so there the rules of Section 13 are the only gate. The first start
  downloads them through `uvx`, and a client may give up waiting once. The author runs these
  in their own terminal; a session never runs them. They warm the cache and download the
  Chromium that Scrapling drives, without administrator rights:

  ```bash
  uvx --from 'scrapling[ai]==0.4.15' --with 'playwright==1.64.0' --with 'patchright==1.64.3' scrapling --version
  uvx code-review-graph==2.3.9 --version
  uvx --from 'playwright==1.64.0' playwright install chromium
  ```

  Where that Chromium then fails to start for missing system libraries, Playwright's
  `install-deps chromium` installs them with administrator rights: the author runs it, never a
  session. ElevenLabs is not among the project's servers: it is configured once at user scope,
  as `production/docs/reference/elevenlabs.md` says, and its key never enters a project file.
  An update offers the two servers once to each recorded client's MCP file that lacks them, and
  never adds back one counted as offered (OpenCode's and Gemini CLI's only after `--write`). Add
  any other server from that client's current documentation, preserve existing entries and keep
  credentials out of Git.

Before copying media into a project where .agents is a link, add --exclude /.agents to the
Copier copy command, then follow step 3 below. Where .agents/skills is a real directory,
preserve it and add --exclude /.agents/skills; a .agents/skills link of any target needs no
exclude, because Copier skips it and leaves it as it is. Copier fails before its skip check when
rendering a link onto a path that resolves to a directory. Integrate that existing skill tree
manually after the copy; never rename or remove it to make the copy succeed. Copier's update
never renders under .agents; the update script only adds the two servers once to an existing
mcp_config.json there, and never writes through a link.

Where .agents is a link to a folder outside the project, Copier refuses to render anything
beneath it, exclusions included, so the link alone is moved aside and put back. Updates do
this themselves on Python 3.14 or later: they rename it to .agents.syntek-held before the
render and back afterwards, never touching its target. Below 3.14 the update stops with
`ForbiddenPathError`: run it again as `uvx --python '>=3.14' copier`. If an update stops
before it ends (a refused answer, Ctrl-C at a question, or Copier failing as it cleans up after
the render), the link stays held as `.agents.syntek-held`, and the next update refuses the
changed tree; where the link is committed and the update stopped after its render, Copier has
already put an identical `.agents` link back. Put the link back from the project root, in a
POSIX shell (Terminal on macOS and Linux, Git Bash on Windows; never PowerShell's `rm`), before
anything else, and before discarding the stopped update with `git reset --hard` and
`git clean -fd`, which would delete a held link Git does not track. First check what stands at `.agents`:
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

Claude Code's project MCP file is .mcp.json, and Antigravity's is .agents/mcp_config.json:
both hold the same two servers. Codex declares them in its TOML format, Gemini CLI and
OpenCode in their own settings files. A .claude/mcp_config.json left by an older release is no
longer read; merge any server it holds into .agents/mcp_config.json. Remote server fields
differ between formats: do not copy configuration blindly. Keep secrets out of Git, preserve
existing server entries, and keep ElevenLabs's base path covering the project. A configured
server does not approve a credit-spending call.

## The user guide

Media's guide lies in `how-to/src/TEMPLATE-GUIDE/syntek-media/` (its chapters),
`how-to/docs/syntek-media/` (its guides) and `how-to/workflows/syntek-media/` (its procedures);
start at `how-to/src/TEMPLATE-GUIDE/syntek-media/01-overview.md`. Read it, never edit it. Run a
procedure there as its folder says, with its checklist open; `run-media-workflow` never routes one.
Another template's guide sits beside it, in folders named for that template.

## Enabling an existing project

The procedure that follows these steps:
`how-to/workflows/syntek-media/06-enable-a-coding-agent-client/`.

The entrypoints and the client settings are copy-only shared files, and never arrive by
update. Copier update delivers this bridge, the rules and the media skills. Since 0.6.0 the
listed family-shared files (the seven skills, the session hooks and the guide guard, the
handoffs folder's pair and the shared files of the guide) arrive through the update script, on
Python 3.14 or later, which also adds the two servers once to a recorded client's existing MCP
file. On the update that first asks which clients, the answer defaults to none, or to the
clients syntek-author's answers record. Updating across 0.4.2 runs one migration: where .agents
is a link to .claude, it makes the real folder and moves .claude/mcp_config.json into it where
that path is free, and reports anything else. An .agents link to a folder outside the project
is held aside and restored by every update, as Client setup says; it is never converted.

1. Read .copier-answers.syntek-media.yml for the recorded source, ref and answers. Generate a
   fresh project in a separate temporary folder using that source and ref and those answers
   as the data file. Keep the fresh answers record there; do not replace the real project's
   answers or run another copy over the real project. To add a client, first record it with
   an update, with Git's automatic housekeeping off for the run, listing every client you keep
   as well as the new one; that brings its row of the model table and nothing else:

   ```bash
   GIT_CONFIG_COUNT=2 GIT_CONFIG_KEY_0=gc.auto GIT_CONFIG_VALUE_0=0 GIT_CONFIG_KEY_1=maintenance.auto GIT_CONFIG_VALUE_1=false \
     uvx --python '>=3.14' copier update --trust -a .copier-answers.syntek-media.yml --data 'AGENT_CLIENTS=[…]'
   ```

   `--python '>=3.14'` runs Copier on Python 3.14, which the update report needs; keep the
   quotes, or the shell reads `>` as a redirection.

2. Review the generated AGENTS.md, GEMINI.md, .codex and .gemini with their pairs,
   opencode.json, the .agents folder, the seven family-shared skills' SKILL.md files, the
   scripts and pair in `.claude/hooks` and the handoffs folder's pair. Copy only missing client
   files into the project; copy a family-shared file by hand only where the update script did
   not run, keeping the three hook scripts executable. An existing file, folder or link
   must be preserved; ask the owner how to combine settings or route its existing entrypoint
   to this bridge.
3. Where .agents is absent, create the folder, then the relative link
   `ln -s ../.claude/skills .agents/skills`, and copy .agents/mcp_config.json. Where .agents
   is still a link to .claude, run the 0.4.2 migration again with the command it printed, or
   with the owner's agreement remove that link (never its target) and do the same. Do not
   replace a real folder or another link.
4. Compare the fresh project's `.claude/settings.json` with the real one and, with the owner's
   agreement, add by hand only the six allows and, where the file lacks it, the data-root guard.
   The asks, the denies, the compaction values, the output style, the four handoff-hook entries
   and the guide guard come from the copy or the update script; add them by hand only where it
   did not run. Never remove or weaken an entry the owner has.
5. Add an agreed pointer to this bridge in an existing AGENTS.md or GEMINI.md, telling the
   client to read every `.claude/syntek-*-agents.md` present. Review any existing Codex
   configuration before adding the CLAUDE.md fallback. Then run
   `python3 .claude/syntek-media-permissions.py --check`, and `--write` if the author agrees.
   Restart the client and confirm that it reads this bridge, the active rules, memory and the
   intended skill tree.

Missing authentication or a preserved incompatible alias needs local setup before that
capability works. Template updates never overwrite the author's solution.
