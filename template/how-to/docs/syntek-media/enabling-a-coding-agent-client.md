---
type: guide
skills: []
model: opus
---

# Enabling a coding agent client — adding Codex, Gemini CLI, Antigravity or OpenCode after the project was made

**Last Updated**: <%DATE%> **Version**: 0.1.0 **Maintained By**: <%OWNER_NAME%>
**Language**: British English (en_GB)

**What it is.** A coding agent, or client, is the program a session runs in. Claude Code always
comes with the project; Codex, Gemini CLI, Antigravity and OpenCode come only where the
`AGENT_CLIENTS` answer named them when the project was made. Every client reads the same rules,
skills and memory in `.claude/`, the others through an entrypoint, the bridge
`.claude/syntek-media-agents.md` and a settings file of their own. Enabling a client later means
recording it in the answers, then copying its files in by hand from a fresh render.

## Why an update never writes them

The entrypoints, the clients' settings files and the .agents folder are copy-only: Copier
writes them when the project is made and never again, so a file you have edited, deleted or
combined with your own stays as it is. Recording a new client with an update brings only its row
of the model table in `.claude/rules/syntek-media/05-model-allocation.md`; the update script
offers the two MCP servers once to that client's files where they already stand, and writes
none of them.

## The fresh-render route

- Render a fresh project into a temporary folder, from the source and version that
  `_src_path` and `_commit` in `.copier-answers.syntek-media.yml` record and with that file as
  the answers, the new client included. A copy is never run over the real project.
- Copy in only the client files the project lacks, from the list in the bridge's 'Enabling an
  existing project'; an existing file is combined by hand with the author, never overwritten.
- Settle the .agents folder: make it a real folder whose skills link leads to the one skill
  tree in `.claude/skills/`, as `how-to/src/TEMPLATE-GUIDE/agent-clients-and-mcp.md` explains.
- Route an existing entrypoint, AGENTS.md or GEMINI.md, to every `.claude/syntek-*-agents.md`
  with one agreed line.
- Run `python3 .claude/syntek-media-permissions.py --check`, then `--write` on the author's word,
  so the deny and ask rules reach the files the new client reads; then restart the client.

## A project that records no client

A project made standalone before 0.5.0, or updated into 0.5.0 over syntek-author, may record no
client in its answers while client files stand. No update offers those files a server until the
clients are recorded, so such a project records them first, with an update that names every
client it keeps.

## How we apply it here

- The bridge's list is the one list of client files: the procedure copies what it names, and
  nothing else.
- Recording the client is an update, run as `uvx --python '>=3.14' copier` with
  `-a .copier-answers.syntek-media.yml` and the five `GIT_CONFIG_*` variables, its report read
  like any other.
- The temporary folder is deleted once the files are in, and the client is recorded in
  `.claude/MEMORY.md`.

## Who implements it

- `how-to/workflows/syntek-media/06-enable-a-coding-agent-client/`: every step, with its
  commands.
- No skill runs it; follow it by hand, step by step with its checklist open.

## Governing standard

`.claude/rules/syntek-media/05-model-allocation.md` Section 4 owns which model each client runs;
the bridge, `.claude/syntek-media-agents.md`, owns the client files and the hand steps. The rules
own the requirement; this guide owns why the route runs through a fresh render.
