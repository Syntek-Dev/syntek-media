# CONTEXT.md — how-to/workflows/syntek-media/06-enable-a-coding-agent-client/

The procedure for adding a coding agent (Codex, Gemini CLI, Antigravity or OpenCode) to a
project that has none of its files. It records the client in the answers through an update,
renders a fresh project into a temporary folder from the same source, version and answers,
copies in only the client files the project lacks, settles .agents by hand, sends any existing
entrypoint to every bridge, carries the permission rules to the client, and restarts it.

## Directory Tree

```text
how-to/workflows/syntek-media/06-enable-a-coding-agent-client/
├── CONTEXT.md          ← this file (when to use, what it produces)
├── CLAUDE.md           ← operating rules for this procedure
├── STEPS.md            ← ordered steps to execute, with every command
└── CHECKLIST.md        ← verification checklist before marking complete
```

## When to use this

- The author wants to use a coding agent the project was not made with.
- A client's files were deleted, and the author wants them back.
- The project's answers record no client while client files stand, because it was made before
  0.5.0 or updated into 0.5.0 over syntek-author: step 1 records every client whose files stand.
- An update report said a client file exists but the recorded answers do not name its client.

Reach for a **different** procedure when: the client is already recorded and its files exist,
and only its rules are out of date (step 8 of
`how-to/workflows/syntek-media/04-update-the-template/`, the permissions script); or the client
belongs to syntek-author's set-up, which syntek-author's own procedure for enabling a client
covers, in its folder under `how-to/workflows/`, where it is present.

## What it produces, and where

- The client recorded in `AGENT_CLIENTS` in `.copier-answers.syntek-media.yml`, and its row in
  the model table of `.claude/rules/syntek-media/05-model-allocation.md` Section 4.
- The client's entrypoint and settings file copied in where the project lacked them, and
  .agents as a real folder with its skills link, where the client needs it.
- The deny and ask rules of `.claude/settings.json` carried into the client's file, on the
  author's word.
- A line in `.claude/MEMORY.md` recording the client, committed.

## The failure this procedure exists to prevent

A client added by guesswork. A client file copied from memory or another project names the wrong
model, misses the MCP servers or the permission rules; an existing entrypoint overwritten loses
the author's own instructions; a copy run over the real project treats every file in it as the
template's. A client that never reaches the bridge works without the production rules, the
spending approval and the model tiers at all.

## Cross-references

- `how-to/docs/syntek-media/enabling-a-coding-agent-client.md`: why the route runs through a
  fresh render.
- `.claude/syntek-media-agents.md`: 'Enabling an existing project', the one list of client
  files, and 'Client setup'.
- `how-to/src/TEMPLATE-GUIDE/agent-clients-and-mcp.md`: each client's files, every .agents case
  and the permissions script.
- `how-to/workflows/syntek-media/04-update-the-template/`: the update step 1 runs.
