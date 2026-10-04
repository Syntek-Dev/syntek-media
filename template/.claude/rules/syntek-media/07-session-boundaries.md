# 07-session-boundaries.md — hand off, never compact

**Last Updated**: <%DATE%> **Version**: 0.1.0 **Maintained By**: <%OWNER_NAME%>
**Language**: British English (en_GB)

> **Template-owned.** Shipped by syntek-media and replaced by every `copier update`: never edit it here. Where syntek-author's project settings file (00-project.md) is present, it outranks this file and says where project rules go; otherwise they go in `.claude/CLAUDE.md`, under the heading 'Project-specific rules'.

syntek-media ships no hook, no handoff skill and no handoffs folder: those are syntek-author's,
where it is applied. This is the rule media work follows either way.

---

## 1. The rule

**Requirement.** When a session's context window nears full, or the work reaches a natural break
(the end of a day, a move to another piece), write a handoff and stop. Never let the session
compact. The settings set `"autoCompactEnabled": false`; syntek-author's PreCompact hook, where
present, is the backstop.

**Why this rule exists.** A piece in progress carries settled decisions: a take approved, a cut
point chosen, a claim verified, a line rejected and why. Compaction keeps the conclusions and
drops the reasons; a handoff carries the live thread into a fresh, full window.

---

## 2. The steps

1. **Record durable knowledge in its real home first**: `.claude/MEMORY.md` through the gate in
   `.claude/rules/syntek-media/08-naming-and-memory.md` Section 3, a piece decision in its brief,
   a narrator or pronunciation in `brand/src/voice/voice.md`, a folder rule in its `CLAUDE.md`.
2. **Write the handoff**: the handoff skill (syntek-author), where present; otherwise by hand, in
   the folder and with the filename the Paths of syntek-author's 00-project.md give, where
   present, else `handoffs/HANDOFF-<DESCRIPTOR>-DD-MM-YYYY.md`, creating the folder on first use.
   The descriptor names the work. **Never write a pair in the handoffs folder**
   (`.claude/rules/syntek-media/01-layout-and-routing.md` Section 6). **A media handoff's next
   action names `run-media-workflow` and the procedure by its full folder name** (for example
   `run-media-workflow` → `production/workflows/02-make-a-voiceover/`), because the writing
   router of syntek-author, where present, reads only its own layers and finds no media procedure.
3. **Print the handoff's path and stop the turn**: a handoff followed by more work is stale.
4. <%OWNER_FIRST_NAME%> runs `/clear` and resumes in a fresh window from the handoff file.
   A handoff whose next action is a media procedure resumes through `run-media-workflow`,
   whichever router is asked first.

A handoff references artefacts by path and confidential material by name and location, never
pasted (`.claude/rules/syntek-media/06-global-rules.md` Section 10), and is pruned once resumed.

---

## 3. What a media handoff never drops

- **Credits spent or queued**: each call made or agreed, its tool, its characters or minutes.
- **Renders in progress**: the command, the piece and the output still to be probed.
- **Approved takes and audiobook masters not yet archived**, with their register rows: they cannot
  be made again.
- **Approved deliverables not yet published**, and the gate each piece stands at.
- **Scheduled posts**, with their dates, times and platforms.
- **Unsynced design changes** between Claude Design and `brand/src/design-system/`.
