# 06-global-rules.md — the rules that apply in every media folder and every media task

**Last Updated**: <%DATE%> **Version**: 0.1.0 **Maintained By**: <%OWNER_NAME%>
**Language**: British English (en_GB)

> **Template-owned.** Shipped by syntek-media and replaced by every `copier update`: never edit it here. Where syntek-author's project settings file (00-project.md) is present, it outranks this file and says where project rules go; otherwise they go in `.claude/CLAUDE.md`, under the heading 'Project-specific rules'.

These hold wherever media works. They keep syntek-author's section numbers and, briefly, its
wording, so a project with both templates reads one set of global rules. A folder's `CLAUDE.md`
may add to them; it never relaxes them.

---

## 1. Locale

**Requirement.** Write and check in British English (en_GB) throughout, captions included.

| Setting | Rule |
|---|---|
| Spelling | colour, organise, behaviour, programme, recognise; licence (noun) and license (verb); practice (noun) and practise (verb) |
| Quotation marks | single, with double inside single: 'she said "now", and left' |
| Dates | DD/MM/YYYY in prose, such as 03/10/2026; DD-MM-YYYY in filenames |
| Time | 24-hour, in <%TIMEZONE%> |
| Timecodes and durations | `HH:MM:SS.mmm` (SRT's comma form only inside `.srt` files); decimal seconds in TOML |
| Caption files | tagged `en-GB` |
| Cross-references | 'Section 3.2', never the section sign |

Where syntek-author's style sheet and terminology are present, they win for any word or mark they
settle.

**Why this rule exists.** Pieces made out of order, across many sessions and platforms, read as one
brand only if their mechanics are fixed once and checked every time.

---

## 2. Route; do not restate

**Requirement.** Every rule has one owner file, and everything else cites it by path and section.
The brand brief lives only in `.claude/rules/syntek-media/01-layout-and-routing.md` Section 1,
platform numbers only in `toolkit/data/platforms.toml` and the brand's overrides, project state
only in `.claude/MEMORY.md`. Never copy them into a skill, a guide or a folder file, and never
cite a numbered section of `.claude/CLAUDE.md`: its numbers are the project's to change.

**Why this rule exists.** Two wordings of one rule drift apart, and the stale one is always the one
that gets read: a platform limit restated in seven files is wrong in six after its next change.

---

## 3. Never self-edit

**Requirement.** No skill rewrites a skill, a guide, a rules file or any `CLAUDE.md` without the
author's explicit instruction. When a rule looks wrong, report it with a proposed wording, and keep
working under the rule as written until the author decides.

**Why this rule exists.** A system that edits its own rules to fit the task in hand will, sooner or
later, edit away the rule that protected the work.

---

## 4. Never overwrite

**Requirement.** Never overwrite a script, a transcript, a plan, a register, a master, a source
recording, an exported design asset, an approved take or any file the author wrote without
confirming first. A new version goes beside the old one; `footage add` copies and never moves.
The D66 timing and scene exceptions in rules 04 Section 3 replace their named tracked copy only
through an accepted run's `-o`, while Git holds it committed and unchanged, through a temporary
file renamed over it. A dirty or untracked copy is refused; every other file keeps the rule above.

**Why this rule exists.** A take cannot be generated again and a recording cannot be made again;
an overwritten one is gone.

---

## 5. One sentence per line, in `src/` only

**Requirement.** Prose in `src/` artefacts keeps one sentence per line, and a script or transcript
one spoken sentence per line. Apply it only to a paragraph you are already editing; never reflow a
whole file. Governance and instructional files keep their hard wrap. Where syntek-author is
applied, its lint reads media's `src/` Markdown too.

**Why this rule exists.** A diff, a review or a caption check then points at one sentence, and a
spoken line is timed, voiced and captioned as one unit.

---

## 6. The 300-line cap

**Requirement.** Every instructional Markdown file (guides, workflows, every `CONTEXT.md` and
`CLAUDE.md`, skills, mode files, everything under `.claude/`) stays within 300 lines, splitting
into `SCREAMING-SNAKE-CASE.md` sub-documents behind a thin index. `src/` artefacts and `README.md`
are exempt.

**Why this rule exists.** A long instruction file is read selectively, and the rule that gets
skipped is the one near the end.

---

## 7. Proofreading is supportive, and a report

**Requirement.** A proofreading pass on a script, transcript, caption text or post copy is a
report, not a rewrite: what and where, the correction offered, recurring items grouped, applied
only once accepted, about the text and never the person. It comes through the companions
(`.claude/rules/syntek-media/02-skills.md` Section 4); where they are absent, say which skill is
missing, and offer a read-aloud check only if the author asks.

**Why this rule exists.** Kind proofreading makes it safe to hand over a rough draft; a pass that
silently rewrites a script changes what the brand says aloud.

---

## 8. Design work opens with a grilling pass

**Requirement.** A piece's brief, the brand kit and the spoken voice open with a grilling pass: the
grill-with-docs skill (syntek-author), where present; otherwise the same questions in chat prose,
in frontier rounds (every unblocked question in one message), each with a recommended answer,
unless the Overrides of syntek-author's 00-project.md, where present, set another style. Look
facts up rather than asking for them, and record the author's decision
(`.claude/rules/syntek-media/08-naming-and-memory.md` Section 3).

**Why this rule exists.** A decision made before the script costs a minute; the same decision
found after the voiceover costs the takes.

---

## 9. Internal notes for deliberate deviations

**Requirement.** When the author authorises a departure from a rule or a guide in one artefact,
record it there: in Markdown, an `<!-- INTERNAL NOTE: … -->` comment directly under the
frontmatter; in CSS or TOML, a comment of the same words at the top. It is not a flag.

**Why this rule exists.** A deviation that lives only in a conversation is undone by the next
session that has not seen it.

---

## 10. Confidentiality

**Requirement.** API keys live at user scope only: the ElevenLabs key in the user-scope server's
environment, never in `.mcp.json` or a committed file, and never typed on a command line. Voice
IDs go only in `brand/src/voice/voice.md`, Claude Design links only in
`brand/src/design-register.md`. Never paste credentials, a release form's personal details or
private correspondence into a handoff, a brief or a plan; name and locate them instead.

**Why this rule exists.** These files are committed and pushed: a key in a hurried handoff is
published with the next push, and spent by whoever finds it.

---

## 11. Answers change through Copier

**Requirement.** The answers are recorded in `.copier-answers.syntek-media.yml`; never edit it by
hand. A changed answer goes through `uvx copier update --trust -a .copier-answers.syntek-media.yml`,
and Section 1 of `.claude/rules/syntek-media/01-layout-and-routing.md` follows on its own.

- **`BRAND_KIND` never changes**: the update refuses it. A different brand kind is a new project.
- **Removing a platform or a media kind deletes every file it generated**, filled seeds included,
  such as the platform's profile: list them for the author, have them copied out and committed,
  then run the update.
- **After such a change**, the shared files that describe the options (`README.md`, `CONTEXT.md`
  and `.claude/CLAUDE.md`, where media wrote them) and any rows for a removed platform in
  `brand/src/platforms/overrides.toml` are edited by hand.

**Why this rule exists.** A hand edit in a rendered file and a stale answer diverge silently, and
a platform removed without warning takes the author's filled-in profile with it.

---

## 12. What Git ignores stays out of the session

**Requirement.** Never search, scan, list or quote a file Git ignores. A search covers only the
files Git tracks or would track (`git ls-files --cached --others --exclude-standard`, `git grep`,
or a list filtered through `git check-ignore`). An ignored file (a render, a take, the footage
mirror) is opened only by the path a manifest, a register or the author names, or as output a
skill has just made in order to check it, and only to probe or play it. **A piece's output
folders** (`production/src/renders/<piece>/`, `production/src/voiceover/generated/<piece>/`,
`publishing/src/renders/<piece>/`) are never listed: `python3 toolkit/media.py where <piece>`
lists the piece's tracked files and names those folders, saying whether each exists, never what
is inside them. A working copy the toolkit writes in a piece's `timing` folder is never opened:
the command that wrote it printed what it found, so read that output instead.

**Why this rule exists.** Ignored files hold credentials, local settings and private recordings. A
search that reads them prints them into the session, and from there into a handoff or a commit.
