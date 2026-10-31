# 07-session-boundaries.md — hand off, never compact

**Last Updated**: <%DATE%> **Version**: 0.1.0 **Maintained By**: <%OWNER_NAME%>
**Language**: British English (en_GB)

> **Template-owned.** Shipped by syntek-media and replaced by every `copier update`: never edit it here. Where syntek-author's project settings file (00-project.md) is present, it outranks this file and says where project rules go; otherwise they go in `.claude/CLAUDE.md`, under the heading 'Project-specific rules'.

The two session hooks, `.claude/hooks/context-threshold-handoff.sh` (`UserPromptSubmit`) and
`.claude/hooks/pre-compact-handoff.sh` (`PreCompact`, and `SessionStart` after a `/compact`),
cite the project's session-boundaries rule; for media work, this file is that rule. The hooks,
the `handoff` skill and the `handoffs/` pair are family-shared: media ships the same files as
syntek-author, a copy writes each one where it is absent, and every update that runs the family
update script replaces one the author never changed and keeps and reports one they edited
(`.claude/rules/syntek-media/02-skills.md` Section 4).

---

## 1. The rule

**Requirement.** When a session's context window nears full, or the work reaches a natural break
(the end of a day, a move to another piece), write a handoff and stop. Never let the session
compact; Section 4 says how Claude Code enforces it.

**Why this rule exists.** A piece in progress carries settled decisions: a take approved, a cut
point chosen, a claim verified, a line rejected and why. Compaction keeps the conclusions and
drops the reasons; a handoff carries the live thread into a fresh, full window.

---

## 2. The steps

1. **Record durable knowledge in its real home first**: `.claude/MEMORY.md` through the gate in
   `.claude/rules/syntek-media/08-naming-and-memory.md` Section 3, a piece decision in its brief,
   a narrator or pronunciation in `brand/src/voice/voice.md`, a folder rule in its `CLAUDE.md`.
2. **Write the handoff**: the `handoff` skill, where present, with its media mode file
   (`.claude/rules/syntek-media/02-skills.md` Section 2); otherwise by hand, in the folder and
   with the filename the Paths of syntek-author's 00-project.md give, where present, else
   `handoffs/HANDOFF-<DESCRIPTOR>-DD-MM-YYYY.md`, creating the folder on first use. The
   descriptor names the work. **Never write the handoffs folder's pair by hand**: it is
   family-shared, and a template's copy, or its update script, writes it where the project
   never had it (`.claude/rules/syntek-media/01-layout-and-routing.md` Section 6). **A media
   handoff's next action names `run-media-workflow` and the procedure by its full folder
   name** (for example `run-media-workflow` → `production/workflows/02-make-a-voiceover/`),
   because the writing router of syntek-author, where present, reads only its own layers and
   finds no media procedure.
3. **Print the handoff's path and stop the turn**: a handoff followed by more work is stale.
4. <%OWNER_FIRST_NAME%> runs `/clear` and resumes in a fresh window from the handoff file.
   A handoff whose next action is a media procedure resumes through `run-media-workflow`,
   whichever router is asked first.

A handoff references artefacts by path and confidential material by name and location, never
pasted (`.claude/rules/syntek-media/06-global-rules.md` Section 10), and is pruned once resumed.

---

## 3. What a media handoff never drops

The `handoff` skill's media mode file carries this list as the part its step 5 adds.

- **Credits spent or queued**: each call made or agreed, its tool, its characters or minutes.
- **Renders in progress**: the command, the piece and the output still to be probed.
- **Approved takes and audiobook masters not yet archived**, with their register rows: they cannot
  be made again.
- **Approved deliverables not yet published**, and the gate each piece stands at.
- **Scheduled posts**, with their dates, times and platforms.
- **Unsynced design changes** between Claude Design and `brand/src/design-system/`.

---

## 4. How it is enforced

- `.claude/settings.json` sets `"autoCompactEnabled": false` and `"idleCompaction": false`, so
  compaction starts neither as the window fills nor while a session sits idle. The seed
  registers the family's two hooks in four entries. To a settings file the project already had,
  the copy and every update add each key and entry once where it is absent, keep a value the
  author set, and never add back one counted as offered.
- The `UserPromptSubmit` hook measures the context window before every prompt: at **50%** it
  advises, once a session, to plan the stopping point; at **75%** it insists, on every prompt, on
  a handoff now. Below Python 3.14 it measures nothing and warns. It assumes a window of 200,000
  tokens; for a larger one, set `CLAUDE_CONTEXT_WINDOW` under `"env"` in
  `.claude/settings.local.json`.
- The `PreCompact` hook **blocks** automatic compaction and lets a deliberate `/compact` through;
  after one, the `SessionStart` `compact` entry says that a handoff gives a cleaner break.
- A hook cannot write a handoff or end a turn; only the model can. **At the 75% warning, the
  handoff is the next thing written.** Other coding agents run no hook: there the session watches
  its own window and follows the same thresholds (`.claude/syntek-media-agents.md`).
