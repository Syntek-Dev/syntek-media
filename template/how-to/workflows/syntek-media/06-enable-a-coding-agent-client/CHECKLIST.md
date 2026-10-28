---
workflow: 06-enable-a-coding-agent-client
phase: plan
skills: []
model: opus
---

# CHECKLIST.md — enable a coding agent client

**Last Updated**: <%DATE%> **Version**: 0.1.0 **Maintained By**: <%OWNER_NAME%>
**Language**: British English (en_GB)

> **See** `how-to/docs/syntek-media/enabling-a-coding-agent-client.md`. No gate in `scripts/docs/reference/the-piece-ladder.md` applies to this procedure.

## Pre-Conditions

- [ ] Read `.claude/CLAUDE.md` and `.claude/MEMORY.md`, then this folder's `CONTEXT.md` and `CLAUDE.md`. · _sonnet_
- [ ] The author has named the client to add, and the full list of clients the project keeps, every client whose files already stand included. · _opus_
- [ ] The tree is clean and committed, as step 1 of `how-to/workflows/syntek-media/04-update-the-template/` asks. · _sonnet_

## Execution Checklist

**Record**

- [ ] The client recorded through an update, run as `how-to/workflows/syntek-media/04-update-the-template/` runs it, with `uvx --python '>=3.14'`, the whole `AGENT_CLIENTS` list and the five `GIT_CONFIG_*` variables; its report read and the update committed. · _sonnet_
- [ ] Over syntek-author, the same list of clients agreed for syntek-author's own record. · _opus_

**Fresh render**

- [ ] A fresh project rendered into a temporary folder from the recorded source and version, with the answers file as `--data-file`; never a copy over the real project. · _sonnet_

**Files**

- [ ] Only the missing client files the bridge's list names copied in, each on the author's word. · _opus_
- [ ] Every client file that already existed combined by hand with the author, never overwritten. · _opus_
- [ ] .agents settled: a real folder with its skills link where it was missing, and Antigravity's MCP file where Antigravity is the new client; every other case agreed with the author and left as the bridge says. · _opus_
- [ ] An existing entrypoint given the agreed line sending its client to every bridge. · _opus_

**Permissions and the client**

- [ ] The permissions script run with `--check`, with `--write` on the author's word, and `--check` again. · _sonnet_
- [ ] The client restarted from the project's top folder, trusted where it asks, and confirmed to read its entrypoint, the bridge, the rules, the memory and the skills. · _sonnet_

## Done When

- [ ] **No file the project already had was overwritten.** · _opus_
- [ ] The client recorded in `.claude/MEMORY.md`, the temporary folder deleted by the author, and everything committed. · _sonnet_
