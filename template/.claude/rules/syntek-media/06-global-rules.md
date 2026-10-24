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
`grill-with-docs` skill, where present, with its media mode file
(`.claude/rules/syntek-media/02-skills.md` Section 2); otherwise the same questions in chat prose,
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
environment, and exported in the user's shell for `media.py voice remix run`, never in `.mcp.json`
or a committed file, never typed on a command line, and never printed or echoed. Voice
IDs go only in `brand/src/voice/voice.md`, Claude Design links only in
`brand/src/design-register.md`. Never paste credentials, a release form's personal details or
private correspondence into a handoff, a brief or a plan; name and locate them instead.

**Why this rule exists.** These files are committed and pushed: a key in a hurried handoff is
published with the next push, and spent by whoever finds it.

---

## 11. Answers change through Copier

**Requirement.** The answers are recorded in `.copier-answers.syntek-media.yml`; never edit it by
hand. A changed answer goes through an update with Git's automatic housekeeping off for the run,
and Section 1 of `.claude/rules/syntek-media/01-layout-and-routing.md` follows on its own:

```bash
GIT_CONFIG_COUNT=2 GIT_CONFIG_KEY_0=gc.auto GIT_CONFIG_VALUE_0=0 GIT_CONFIG_KEY_1=maintenance.auto GIT_CONFIG_VALUE_1=false \
  uvx copier update --trust -a .copier-answers.syntek-media.yml
```

- **`BRAND_KIND` never changes**: the update refuses it. A different brand kind is a new project.
- **Removing a platform or a media kind deletes every file it generated**, filled seeds included,
  such as the platform's profile: list them for the author, have them copied out and committed,
  then run the update.
- **After such a change**, the shared files that describe the options (`README.md`, `CONTEXT.md`
  and `.claude/CLAUDE.md`, where media wrote them) and any rows for a removed platform in
  `brand/src/platforms/overrides.toml` are edited by hand.
- **A coding client ticked on an update** adds its row to the model table
  (`.claude/rules/syntek-media/05-model-allocation.md` Section 4) and nothing else: its files
  arrive only through the steps in `.claude/syntek-media-agents.md`.

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
the command that wrote it printed what it found, so read that output instead. A still
`scene.py stills` has just written may be opened by its printed path to review its picture and mouths;
never list the folder to find it.

**The data root is off-limits too, whatever the store.** A data root is a folder outside every
repository that holds a `.syntek-data-root` marker; this machine's is the one `SYNTEK_DATA_ROOT`
names. Never search, list, edit or write anything under one, by any tool or shell command. Media
files nothing there: its map, `.claude/syntek-media-dataroot.json`, names no folder, so footage
stays listed in `production/src/footage/manifest.toml` and the resolver's `add` refuses a media
file. The resolver, `python3 .claude/syntek-media-dataroot.py` (Python 3.11 or later), ships for
the family's shared records: `store` prints the store each template's answers record, and `root`
the root and its layout; where syntek-author is applied, its own data-root rules say when its
files are filed. The data-root answers are kept in step with every other template's: while two
disagree, every data command refuses (exit 2) until they agree, and the update that leaves them
apart says so. Change them through an update (Section 11), never by hand. The guard hook in
`.claude/settings.json` stops edits and writes under a root, and searches only where the client
offers `Grep` and `Glob`; elsewhere this rule alone keeps a search out of the root.

**Why this rule exists.** Ignored files hold credentials, local settings and private recordings. A
search that reads them prints them into the session, and from there into a handoff or a commit.
The data root holds records themselves: a search there prints them too, and an edit in place
breaks the checksum that proves a record unchanged.

---

## 13. Web and code tools

<!-- BEGIN family-shared rules: web and code tools -->
**Requirement.** Every project ships two MCP servers, pinned and keyless: `scrapling`, which
fetches web pages, and `code-review-graph`, a local map of a repository's code. Use them only
as this section says.

- **Give every `scrapling` tool only an `http://` or `https://` address**: never `file://` or
  any other scheme (ftp, gopher, dict, smb, telnet, tftp), which reads this machine's files or
  reaches local services. In OpenCode and Codex the plain tools and `screenshot` run without
  asking.
- **Ask the author before each of `scrapling`'s six asked browser tools**: `stealthy_fetch`,
  `bulk_stealthy_fetch`, `open_session`, `session_fetch`, `fetch` and `bulk_fetch`. Say which
  site, why, and which tool. Claude Code asks before each of them by itself; in a client that
  does not, ask in the conversation and wait. A configured server, or a tool the client lets you
  run, is not the author's approval. `screenshot` loads a page in a browser session already
  open: use it only on the site the author approved for that session, and ask before taking it
  to any other site.
- **Use the plainest tool that does the job**: the client's own web search or fetch first, then
  `make_request` or `bulk_get`. Even these present a browser's fingerprint and headers to the
  site, and no `scrapling` tool reads `robots.txt` or limits how fast it asks.
- **`make_request`, `bulk_get` and `session_make_request` only read.** Send `make_request` and
  `session_make_request` as a GET with no request body unless the author agrees to that request.
  Never send any of the three to a loopback, private or link-local address (localhost,
  127.0.0.0/8, 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16, 169.254.0.0/16, or a browser's
  DevTools port), and never set `follow_redirects` to true, `verify` to false, or a `proxy`.
  Codex runs these three without asking, because the server marks them read-only. OpenCode
  runs, without a prompt, every tool it is not told to ask before: these three, `screenshot`,
  `open_request_session` and every `code-review-graph` tool but the two that write, so there
  these rules are the only gate.
- **Never set `real_chrome`, `cdp_url` or `executable_path` without the author's word for that
  call**, and never use a stealth tool to get past a sign-in, a paywall, a challenge page or a
  site that refuses automated access: whether that is allowed is the author's decision, not the
  session's.
- **Respect each site's terms of use, its `robots.txt` and the law**, including data protection
  and copyright. This rule is not legal advice: where the position is unclear, stop and ask the
  author. Record what was fetched, from where and when, in the project's record of provenance
  where its rules name one.
- **`code-review-graph`** maps the code of the repository a call names: by default this project,
  whose graph it keeps in a `.code-review-graph` folder at the project root, which Git ignores.
  It indexes the files Git tracks; while Git tracks nothing (a new project before its first
  `git add`) it scans every file on disk, ignored ones included, so never build its graph before
  the project's first commit. Never pass `repo_root`, and never call `list_repos_tool` or
  `cross_repo_search_tool`, without the author's word: they reach other repositories on this
  machine and a registry in the home folder. `apply_refactor_tool` rewrites files and
  `generate_wiki_tool` writes pages, so both ask first; its cloud-embedding tool is never
  offered, and its cloud keys stay blank.
- **Never run `code-review-graph install`, `init` or `uninstall`, or `scrapling install`.** The
  first three rewrite the agent files every template shares, the project's settings, skills and
  Git hooks, and configuration outside the project; `scrapling install` installs system packages
  with administrator rights. The author runs the commands that fetch the servers and their
  browser, in their own terminal.

**Why this rule exists.** `scrapling`'s stealth tools are built to look like a person's browser
and to get through anti-bot protection, so a site cannot tell them from a visitor. Its
`real_chrome` option launches the Chrome installed on this machine, with a fresh profile;
`cdp_url` hands the session control of any browser that exposes DevTools at that address, on
this machine or another; `executable_path` launches whatever program it names. Every request
comes from the machine and network address of the browser that sends it, the author's or the
one `cdp_url` names: what a session fetches is the author's act, not the tool's.
`code-review-graph`'s installer adds an unpinned entry that offers the cloud-embedding tool
beside the pinned ones, and writes the agent files and the home folder's configuration.
<!-- END family-shared rules: web and code tools -->
