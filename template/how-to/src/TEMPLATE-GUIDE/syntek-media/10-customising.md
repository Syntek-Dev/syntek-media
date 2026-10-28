# Customising — making the project work your way without breaking updates

The project is yours to shape, but some of its files belong to the template, and every update merges the template's changes into an edit you make to one of those.
This chapter shows which files are yours, which are the template's, and where your own way of working goes so that every update keeps it.

## What is yours

Everything you write is yours, and no update ever touches it.

- Your pieces, under `scripts/src/pieces/`, and the edit lists, cards, cut-down plans, captions, thumbnails and post packages you make for them are yours.
- The seeds are yours: the registers and logs, the footage manifest, the schedule, `brand/src/design-system/tokens.css`, `brand/src/voice/voice.md`, the platform profiles and `brand/src/platforms/overrides.toml`.
- A seed you delete comes back empty at the next update, because the skills read it by its path.
- Each layer's `docs/project/` and `workflows/local/` are yours, for guides and procedures of your own.
- A skill of your own goes in a new folder under `.claude/skills/`, with a name that collides with no skill of either template, and no update touches it.
- The shared files a copy writes only where they are missing, such as `README.md`, `CONTEXT.md`, `.claude/CLAUDE.md` and `.claude/MEMORY.md`, are yours to edit too.

## What is the template's

- The rules in `.claude/rules/syntek-media/`, the media skills with their mode files, and the bridge `.claude/syntek-media-agents.md` are the template's.
- So are every layer's `docs/reference/` guides and numbered workflows, all of `toolkit/`, and this template's folders in the guide.
- Never edit one of them.
- Every update merges the template's changes with your edit, and where you both changed the same lines it leaves a conflict, with both versions in the file for you to sort out.
- If a rule looks wrong to you, ask Claude to report it with a proposed wording.
- Claude keeps working under the rule as written until you decide, and never rewrites a rule, a skill or a guide without your instruction for that change.

## Overriding a template-owned file

Change how the project behaves instead, and the template's file stays as it shipped.

- A guide you write in a layer's `docs/project/`, with the same name as a guide in its `docs/reference/`, is read instead of the template's.
- A project guide for the piece ladder may add a check to a gate, but it never removes or weakens one.
- A procedure you write in a layer's `workflows/local/`, with the same folder name as one of the template's workflows, replaces it.
- A new guide or procedure of your own needs no matching name, and your procedures take their own numbering.
- Add a row for each one to the `CONTEXT.md` and `CLAUDE.md` of its folder, which are seeds and yours to edit.
- Where syntek-author's project settings file, 00-project.md, is present, a row under its Workflow aliases can name a media workflow by its full folder path and the procedure to run instead.
- A bullet under its Overrides can name a media rules file and section, or a media skill and step, and what you do instead.
- Where that file is absent, a rule of your own goes in `.claude/CLAUDE.md`, under the heading 'Project-specific rules', as a dated bullet, led in bold, with its reason.
- A project rule applies on top of the template's rules and wins where the two conflict, and only syntek-author's project settings file outranks it.
- Never refer to a numbered section of `.claude/CLAUDE.md` from another file, because its numbering is yours to change.

## Departing from the guide

- `how-to/` explains the template version this project runs, so it stays exactly as the template wrote it.
- Claude Code's deny in `.claude/settings.json` and the guide guard `.claude/hooks/how-to-read-only.sh` refuse edits there, even when you ask.
- Every full update puts the template's text back on any file of the guide that differs, a deleted one included, and lists each one in its report.
- What you had stays in Git, so nothing you wrote there is lost.
- To work differently from a chapter, a guide or a procedure, record the difference in syntek-author's project settings file, 00-project.md, under Overrides or Workflow aliases, where that file is present.
- Otherwise record it in `.claude/CLAUDE.md` under the heading 'Project-specific rules'.
- Never record it in `how-to/`.
- The guide's procedures have no `workflows/local/`, so a procedure of yours that replaces one is named in an alias row or a project rule.
- Keep your own notes in a layer's `docs/project/` or `workflows/local/`, never in the guide.

## `.claude/settings.json` is shared

- `.claude/settings.json` is written once, by whichever template was applied first, and no update renders it again.
- An update may add an entry the template lists that the file lacks, once only, and never again once it has been offered.
- You may add allows of your own, but never remove or weaken an ask or a deny.
- The asks stop Claude Code before every call that spends ElevenLabs credits, and an allow never overrides them.
- The denies keep hand edits out of every generated and renders folder and out of `how-to/`.
- After you change an ask or a deny, carry it to the other coding agents' files the project has with `python3 .claude/syntek-media-permissions.py --write`.

## What never to edit

- Never edit `.copier-answers.syntek-media.yml` by hand.
- A changed answer goes through an update, as `how-to/workflows/syntek-media/02-change-the-answers/` says.
- Never edit a rendered rules file, the brand brief in `.claude/rules/syntek-media/01-layout-and-routing.md` Section 1 included.
- The brand brief is rendered from your answers, so a changed answer arrives there on its own.
- Never edit a file in a generated or renders folder: the toolkit and ElevenLabs write those files, and an approved take is archived as source media.

## Where the rules live

- `.claude/rules/syntek-media/01-layout-and-routing.md` Section 8: who owns which files.
- `.claude/rules/syntek-media/01-layout-and-routing.md` Section 10: project settings, precedence and where a departure is recorded.
- `.claude/rules/syntek-media/03-production-ethics.md` Section 3: a project guide may add a check to a gate, never remove one.
- `.claude/rules/syntek-media/06-global-rules.md` Section 3: never self-edit, and the read-only guide.
- `.claude/rules/syntek-media/06-global-rules.md` Section 4: never overwrite what you wrote.

## Next

- What a copy and an update do to each kind of file → `how-to/src/TEMPLATE-GUIDE/syntek-media/06-what-copier-writes.md`
- Sharing the project with syntek-author → `how-to/src/TEMPLATE-GUIDE/syntek-media/12-beside-syntek-author.md`
- Adding or removing a platform or a media kind → `how-to/src/TEMPLATE-GUIDE/syntek-media/11-platforms-and-media-kinds.md`
