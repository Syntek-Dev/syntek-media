@./CONTEXT.md

# CLAUDE.md — how-to/workflows/syntek-media/

Read order: `.claude/CLAUDE.md` → `.claude/MEMORY.md` → `how-to/CONTEXT.md` →
`how-to/CLAUDE.md` → `how-to/workflows/CONTEXT.md` → `how-to/workflows/CLAUDE.md` → this
folder's `CONTEXT.md` (imported above) → this file → the chosen procedure's own files.

## Purpose (one line)

Hold syntek-media's procedures for keeping the project in step with the template, so each of
these jobs is done the same safe way every time, whoever runs it.

## How to work here

- **Routing:** pick by what you want. Check first for a Workflow aliases row in syntek-author's
  project settings file, where it is present, or a project rule in `.claude/CLAUDE.md` under the
  heading 'Project-specific rules'; a recorded alias wins.

| You want to… | Procedure |
|---|---|
| Finish a fresh copy before the first session spends anything | `how-to/workflows/syntek-media/01-finish-a-copy/` |
| Change an answer, add or remove a platform or a media kind | `how-to/workflows/syntek-media/02-change-the-answers/` |
| Report a fault in the template | `how-to/workflows/syntek-media/03-report-a-template-problem/` |
| Take the template's latest changes | `how-to/workflows/syntek-media/04-update-the-template/` |
| Get back from an update that stopped | `how-to/workflows/syntek-media/05-recover-a-stopped-update/` |
| Add Codex, Gemini CLI, Antigravity or OpenCode to this project | `how-to/workflows/syntek-media/06-enable-a-coding-agent-client/` |

- **Model:** the `_opus_` / `_sonnet_` tags in each `CHECKLIST.md` are authoritative: Opus for
  every judgement and every step that changes the template's files or the project's settings;
  the mechanical tier only for running a command the author has agreed and ticking items
  (`.claude/rules/syntek-media/05-model-allocation.md`).
- **Concrete steps (running one):** read the procedure's `CONTEXT.md` → `CLAUDE.md` →
  `STEPS.md`, then work `STEPS.md` in order with `CHECKLIST.md` open. `run-media-workflow` never
  routes these.
- **Definition of done (running):** every checklist item ticked or waived with the author's
  reason; the project committed as the procedure's last step says; nothing under `how-to/`
  changed except through the template's update, its recovery and the commands its report
  prints.

## Guardrails

- **Never edit these folders**, even when asked: no session edits, writes, moves or deletes a
  file under `how-to/` (`.claude/rules/syntek-media/06-global-rules.md` Section 3), and every
  full update puts the procedures back.
- **The project's own way is recorded where the rules say**
  (`.claude/rules/syntek-media/01-layout-and-routing.md` Section 10): a Workflow aliases row in
  syntek-author's project settings file, naming the procedure by its full folder path, where
  that file is present, and otherwise a project rule in `.claude/CLAUDE.md` under the heading
  'Project-specific rules'. It wins over the procedure it names.
- **Never renumber or reuse a number.** Numbering is frozen and append-only.
- **The author decides.** A step that discards changes, changes an answer or copies files in
  waits for the author's word; a session never runs it on its own judgement.
- **Commands run exactly as written**, from the project's top folder. A command that fails stops
  the procedure, and the author hears the command's own words.
- **Only this template's jobs.** syntek-author's update, recovery or set-up follows its own
  procedure, in its own folder under `how-to/workflows/`, never one of these.

## Output & naming

- **Folders:** `NN-verb-first-name/`, numbered from 01 here, each holding `CONTEXT.md`,
  `CLAUDE.md`, `STEPS.md` and `CHECKLIST.md`.
- **Procedures produce nothing here.** They change the project as their steps say: the
  template's files, the answers file, the client files, the settings and the commit.
