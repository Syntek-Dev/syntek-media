# 05-model-allocation.md — which model does which media work

**Last Updated**: <%DATE%> **Version**: 0.1.0 **Maintained By**: <%OWNER_NAME%>
**Language**: British English (en_GB)

> **Template-owned.** Shipped by syntek-media and replaced by every `copier update`: never edit it here. Where syntek-author's project settings file (00-project.md) is present, it outranks this file and says where project rules go; otherwise they go in `.claude/CLAUDE.md`, under the heading 'Project-specific rules'.

The two model tiers for media work are defined here and nowhere else in syntek-media. Every other
media file names a tier, never a rule of its own, so a change of policy is one edit. Where
syntek-author is applied, its own table governs writing work; both name the tiers the same way.

---

## 1. The two tiers

No Haiku on this project.

Jev is a narrow external scoring service, used only through the approved option scorecard
(`publishing/docs/reference/scoring-options.md`). It does not replace the substantive tier
for creating options or author approval; its scores never pass a gate.

| Work | Model |
|---|---|
| Mechanical only: renders and encodes, probes, file moves and renames, `take add` and `footage add`, register and log rows already agreed, checklist ticks | **<%MODEL_MECHANICAL%>** |
| Everything substantive: anything a viewer or listener will read or hear (scripts, transcripts, caption text, titles, descriptions, thumbnail words, voice direction), edit decisions, rights and disclosure judgements, grilling, reviewing, any decision about meaning | **opus** |

If Opus usage is exhausted, substantive work falls back to **sonnet** until it returns, never
lower. **When in doubt, the work is substantive.** A caption break that changes what a line seems
to say, or a cut that drops a qualification, is a judgement, not a chore.

In the other coding agents (Codex, Gemini CLI, Antigravity, OpenCode), these aliases identify
work tiers: each client runs them on the model the project's answers name for it (Section 4,
where the project uses that client), or on the model the owner chooses there; nothing switches
provider automatically. Apply the same substantive review boundary and read
`.claude/syntek-media-agents.md` for client setup; to add a client,
`how-to/workflows/syntek-media/06-enable-a-coding-agent-client/`.

---

## 2. How the tiers are named in files

- **Checklist tags** are the literal `· _opus_` (the substantive tier) and `· _sonnet_` (the
  mechanical tier). They name the tier, not a model: the mechanical tier runs on the model in the
  table above.
- **Routing frontmatter** on guides, `STEPS.md` and `CHECKLIST.md` carries `model: opus` for
  substantive work and `model: sonnet` for mechanical work. As with the tags, `sonnet` there names
  the mechanical tier, which this project runs on **<%MODEL_MECHANICAL%>**.
- **Briefs, scripts, transcripts and registers carry no `model:` key.** The tier belongs to the
  task, not to the file being worked on.
- **Never write a version string.** Use the alias, `opus` or `sonnet`, so the project follows the
  current model without an edit.
- **Never put a template token inside an emphasised checklist tag.** A formatter that rewrites
  emphasis can corrupt it.

---

## 3. Why

Substantive work is where an error costs the author: a fabricated figure on screen, a flattened
argument in a clip, a voice directed out of character, a disclosure missed. The cheaper tier is
safe only where the result can be checked at a glance, which is why the line sits at mechanical
work and never higher, and why the fallback never drops below the tier the work needs.
<: if AGENT_CLIENTS | length > 0 :>

---

## 4. Other coding agents

Claude Code runs the tiers above. The other clients the answers name run them on these models,
the substantive tier first; the mechanical tier uses the same model unless the owner sets a
cheaper one in the client. A client's files exist only if the project was generated with it,
or it was added by the steps in `.claude/syntek-media-agents.md` or by
`how-to/workflows/syntek-media/06-enable-a-coding-agent-client/`. Over syntek-author, the client
and model answers default to syntek-author's record, so both templates' tables name the same
clients.

| Client | Model | Set in |
|---|---|---|
<: if 'codex' in AGENT_CLIENTS :>| Codex | <: if CODEX_MODEL :>`<%CODEX_MODEL%>`<: else :>Codex's own default<: endif :> | `config.toml` in `.codex` |
<: endif :><: if 'gemini-cli' in AGENT_CLIENTS :>| Gemini CLI | <: if GEMINI_MODEL :>`<%GEMINI_MODEL%>`<: else :>Gemini CLI's own default<: endif :> | `settings.json` in `.gemini` |
<: endif :><: if 'antigravity' in AGENT_CLIENTS :>| Antigravity | chosen in the app | Antigravity |
<: endif :><: if 'opencode' in AGENT_CLIENTS :>| OpenCode | <: if 'opencode' in AGENT_CLIENTS and OPENCODE_PROVIDER not in ['user', 'named'] :>`<%OPENCODE_MODEL%>` on <%OPENCODE_PROVIDER%> at <% OPENCODE_BASE_URL.rstrip('/') %>, <%OPENCODE_CONTEXT%> tokens of context<: elif 'opencode' in AGENT_CLIENTS and OPENCODE_PROVIDER == 'named' :>`<%OPENCODE_MODEL%>`<: else :>your own OpenCode settings<: endif :> | <: if 'opencode' in AGENT_CLIENTS and OPENCODE_PROVIDER == 'user' :>outside this project<: else :>`opencode.json`<: endif :> |
<: endif :>
This table follows the project's answers and is updated with this file. The client files are
written once and are the owner's: an update never creates or refreshes one, so after a change of
answer, change the client file to match. Since 0.6.0 an update adds the two MCP servers once to a
recorded client's existing MCP file; OpenCode's and Gemini CLI's settings get them only once the
permissions script's `--write` has run.
Elsewhere, `opus` and `sonnet` stay tier labels in every client. A local model must handle tool
calls reliably before it drafts: test it on a scratch copy first, and when in doubt keep
substantive work on the strongest model available. Client setup: `.claude/syntek-media-agents.md`.
<: endif :>