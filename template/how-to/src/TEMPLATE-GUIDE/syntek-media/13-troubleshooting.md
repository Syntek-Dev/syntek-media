# Troubleshooting — what to do, grouped by when it breaks

Find the moment it went wrong, then the symptom.
Each entry says what is happening and what to do, and names the chapter or procedure that owns the fix.
Where a step changes a settings file or the template's files, a session waits for your word before it acts.

## When copying

**A copy stops with 'Interactive session required'.**
Read the rest of the line, because Copier stops this way whenever it must ask something and has no terminal to ask in.
Where it ends 'Consider using `--overwrite`', Copier found a file of its own already standing at a path that is not one of the shared files.
That is a collision, and a collision is a fault in the template, never in your project.
Where it ends 'Use `--defaults` and/or `--data`/`--data-file`' instead, Copier needed an answer: run the copy in a terminal, or give it the answers.
A copy run in a terminal asks 'Overwrite …?' instead, even with `--defaults`, and yes is the default, so answer no.
After a collision, `git status` shows anything the copy wrote before it stopped.
Remove what it wrote, and report the collision with `how-to/workflows/syntek-media/03-report-a-template-problem/`.
Never run the copy again with `--overwrite`, because that replaces files that are not the template's.

**The copy lists shared files as 'conflict' then 'skip', or as 'identical'.**
That pair is expected, and it is not a collision.
A shared file that already stands is left exactly as it was, so the other template's copy stays.

**The copy prints a line starting `syntek-media: .copier-answers.syntek-author.yml stands here without`.**
The project's syntek-author is older than v0.6.0, because its own user guide is missing.
A project that holds both templates must not keep that older syntek-author.
Update syntek-author to v0.6.0 or later now, from a clean tree, by its own update procedure, and update it before syntek-media from then on.
`how-to/src/TEMPLATE-GUIDE/syntek-media/03-applying-over-syntek-author.md` explains why.

**The copy prints a message framed in lines of `=` that says `family-update did NOT run`.**
`uvx` ran Copier on a Python older than 3.14 that it already had, because the command did not ask for a newer one.
Every file was written, but the copy's last step recorded nothing for the first update's report.
It also added none of the settings entries and servers to a settings file or server file you already had.
Add those entries by hand, as `how-to/workflows/syntek-media/01-finish-a-copy/` says.
A copy run with `--skip-tasks` skips that step and every other task of the copy; the same procedure finishes the settings part.
Run every later command as `uvx --python '>=3.14' copier`, as this guide gives it.

**Codex fails on every command, or a client cannot see the project's skills.**
The .agents folder is not a plain folder: it may be a link to `.claude`, a link outside the project or a folder of your own.
A copy never changes an .agents folder or link you already had.
`how-to/src/TEMPLATE-GUIDE/agent-clients-and-mcp.md` explains each case and how to settle it by hand.

## In the first session

**Every toolkit call asks for permission.**
The settings file lacks the allow entries for the toolkit and ffmpeg, which no copy or update ever adds.
That happens when the copy kept a `.claude/settings.json` that was already there.
Add these to its `"allow"` list by hand, beside the entries already there:

```json
"Bash(python3 toolkit/*.py *)",
"Bash(uv run toolkit/*.py *)",
"Bash(ffmpeg *)",
"Bash(ffprobe *)",
"WebSearch",
"WebFetch"
```

`how-to/workflows/syntek-media/01-finish-a-copy/` gives the rest of what a kept settings file may lack.

**`python3 toolkit/media.py check --setup` reports findings.**
That is what it is for: run it before the first call that spends credits, and clear what it reports.
Each finding names what is missing, what it blocks and its fix.
A missing optional tool is only a note, and it names the commands it blocks.
A missing ask entry for `voice remix run` is a finding, because without it a remix would spend credits without a prompt.
`brand/workflows/06-check-the-setup/` takes you through every finding, one fix at a time.

**ElevenLabs answers 'outside of allowed directory'.**
The ElevenLabs server's base path does not contain this project, and speech-to-text refuses any file outside it.
A link to the project from inside the base path does not help.
Export your key in your shell first, then remove the server and add it again at user scope with a base path that contains the project:

```bash
claude mcp remove elevenlabs --scope user
```

```bash
claude mcp add --env ELEVENLABS_API_KEY="$ELEVENLABS_API_KEY" --env ELEVENLABS_MCP_BASE_PATH="$HOME" --transport stdio --scope user elevenlabs -- uvx elevenlabs-mcp
```

Use your home folder where every project lives under it, and otherwise the nearest folder that holds them all.
Never type the key itself on a command line, and never commit it.
`production/docs/reference/elevenlabs.md` explains the server and the rule.

**`git add` fails with `clean filter 'lfs' failed`.**
The tripwire is working: a large design export would otherwise have been committed whole, as a plain file.
Install Git LFS, then run this once:

```bash
git lfs install
```

Add the file again afterwards, and it is stored through Git LFS.
The setting the copy wrote into this repository's own Git settings is then harmless, because Git LFS sets the same value.

**An edit under `how-to/` is refused.**
That is by design: the user guide is read-only.
Claude Code's deny in `.claude/settings.json`, the rule `Edit(/how-to/**)`, refuses the edit, and the guide guard `.claude/hooks/how-to-read-only.sh` refuses it too.
Where an edit got through by another route, the next update puts the file back (`.claude/rules/syntek-media/06-global-rules.md` Section 3).
To work differently from the guide, record the difference in syntek-author's project settings file, 00-project.md, under Overrides or Workflow aliases, where that file is present.
Otherwise record it in `.claude/CLAUDE.md` under the heading 'Project-specific rules' (`.claude/rules/syntek-media/01-layout-and-routing.md` Section 10).

**An edit in a generated or renders folder is refused.**
That is also by design: the toolkit and ElevenLabs write those files, and nobody edits them by hand.
Change the source the file is made from, and make it again.

## When producing

**A toolkit command stops with exit code 2 and names a tool.**
Exit code 2 means the command could not run, because of a bad argument, a missing input or a missing tool.
The message names the tool and how to install it.
Install it, then run `python3 toolkit/media.py check --setup` again to confirm.
`how-to/src/TEMPLATE-GUIDE/syntek-media/02-prerequisites.md` lists every tool and what it is for.

**Transcribing stops, or names `MEDIA_TRANSCRIBE_PYTHON`.**
`toolkit/transcribe.py` needs a Python from 3.10 to 3.13, kept beside the 3.14 the rest of the toolkit runs on.
Where no Python in that range is found, the command stops with exit code 2 and names the fix.
Fetch what it needs once, yourself, with this command, because no session downloads models:

```bash
python3 toolkit/media.py transcribe fetch
```

Or set `MEDIA_TRANSCRIBE_PYTHON` at user scope to the path of a Python from 3.10 to 3.13 whose environment holds WhisperX.
Never activate that environment where Claude Code or the toolkit runs.

**A card or thumbnail command says the browser is missing.**
The card and scene renderers draw through Playwright's Chromium, and the command stops with exit code 2 when it is missing.
It prints the command that installs the browser, which you run yourself:

```bash
uv run --with playwright==1.63.0 playwright install chromium
```

**The setup check says ffmpeg lacks a library.**
Every render, caption burn and audio master needs an ffmpeg built with libass, libx264 and libmp3lame.
Install the full build your system offers, as the setup check's fix line says, then check again.
Encoding images to WebP or AVIF needs further libraries, which are optional: JPEG and PNG need none.

## When updating

**Copier refuses to start.**
Copier refuses to update a project with uncommitted changes, and it finds this template's answers file only when the command names it with `-a`.
Commit everything first, then run the command exactly as `how-to/workflows/syntek-media/04-update-the-template/` gives it.

**The update stopped part way with an error.**
These errors mean the update stopped after Copier had written the new version, and before the steps that follow it had run:

- `OSError: [Errno 39] Directory not empty`;
- `FileExistsError` or `NotADirectoryError` naming `how-to`;
- `ForbiddenPathError` naming a path in `how-to` or in the .agents folder.

Never commit what it left.
`how-to/src/TEMPLATE-GUIDE/updating-and-recovery.md` explains each error, under 'When an update stops'.
`how-to/workflows/syntek-media/05-recover-a-stopped-update/` undoes the stopped update and runs it again, with every command.

**The update printed a message framed in lines of `=` that says `family-update did NOT run`.**
`uvx` ran Copier on a Python older than 3.14, so nothing was reported, refreshed or put back in `how-to/`.
Look for conflict markers and `.rej` files yourself, and commit the update once they are settled.
Then run the same update again, on Python 3.14 or later:

```bash
GIT_CONFIG_COUNT=2 GIT_CONFIG_KEY_0=gc.auto GIT_CONFIG_VALUE_0=0 GIT_CONFIG_KEY_1=maintenance.auto GIT_CONFIG_VALUE_1=false \
  uvx --python '>=3.14' copier update --trust -a .copier-answers.syntek-media.yml
```

The five `GIT_CONFIG_*` settings in front turn Git's background housekeeping off for that one run.
The second report says the template did not change, because the first run already moved the answers file on.
Upgrade the Python your terminal runs as well, because the toolkit and the hooks need 3.14 too.

**No update report appeared at all.**
Copier skipped every step after it wrote, as it does when it cannot read a template version.
Run `git status`, and look for conflict markers and `.rej` files yourself.
`how-to/src/TEMPLATE-GUIDE/updating-and-recovery.md` explains the other cases, under 'When no report appears'.

**The report lists files under `RESTORED`.**
The user guide is read-only, so the update put the template's text back on each file of it that differed.
What you had stays in Git, and the report gives the command that shows it.
To keep a different way of working, record it as `how-to/src/TEMPLATE-GUIDE/syntek-media/10-customising.md` explains.

**The report lists a file under `LEFT AS IT IS`.**
The update could not safely put that guide file back, and the entry gives the reason.
Act on the reason: commit or move a file Git does not hold, make `how-to` a real folder where a link is the reason, move out a folder standing where a guide file belongs, or wait for the other template's update.

**Copier warns `MissingFileWarning`.**
This is expected, and harmless.
The template reads its own earlier answers, so that it can refuse a changed `BRAND_KIND`.
It also reads syntek-author's answers file for the answers both templates share, and in a project without syntek-author there is none to read.

**The update refuses a new `BRAND_KIND`.**
The message says `BRAND_KIND cannot change on update`, and the update touches nothing.
The mode files, the worked example and the brand seeds were written for one kind of brand.
A different kind of brand is a new project: make one, and copy your work across.

**Removing a platform or a media kind deleted files you had filled in.**
They remain in your Git history, so you can bring each one back from your last commit.
Next time, copy out what you need first, from the list the update prints before it asks its questions.
`how-to/src/TEMPLATE-GUIDE/syntek-media/11-platforms-and-media-kinds.md` explains what each removal deletes.

**A settings entry you removed came back.**
An update you have not committed counts as not made, so running it again offers everything again.
Remove the entry once more after you commit the update, and later updates leave it out.

## With syntek-author

**syntek-author is older than v0.6.0.**
An older syntek-author treats every src folder as yours, checks the user guide's chapters as your writing and puts nothing back in `how-to/`.
Update syntek-author first, by its own update procedure, to v0.6.0 or later.
From then on, update syntek-author before syntek-media, one template at a time, committing between them.

**syntek-author's `make lint` or `make flags` reports a file of media's.**
syntek-author's checks read media's src folders too, so media's scripts, registers and plans are written one sentence per line.
A finding in a file you wrote is yours to fix.
A finding in one of these chapters is a fault in the template, so report it.

**The two templates record different coding agents.**
Each template keeps its own answers, so each has its own table of which model each coding agent runs.
Make the answers agree through an update of the template that differs, giving every client you keep, as `how-to/workflows/syntek-media/02-change-the-answers/` says.
An update records a client, but never writes its files: `how-to/workflows/syntek-media/06-enable-a-coding-agent-client/` adds them.

**After an update, a message says the data-root answers differ.**
One project keeps one data-root store and one layout, so the data-root commands refuse to act until both templates agree.
Text work goes on meanwhile, and media itself files nothing under a data root.
Make the answers agree through an update of one template, as the message says and `how-to/src/TEMPLATE-GUIDE/the-data-root.md` explains.

**The report says a file holds the other template's version.**
That file waits for the other template's own update, which replaces it once that template ships a newer version.
Leave it as it is, because this template's version may be the older one.

## Still stuck

The `_src_path` line of `.copier-answers.syntek-media.yml` names the template's source, where its README and its issue tracker live.
The `_commit` line of the same file says which version of the template you run.
These commands print the Copier and Python versions a report needs:

```bash
uvx --python '>=3.14' copier --version
```

```bash
python3 --version
```

Add the command you ran, its full output and what `python3 toolkit/media.py check --setup` reports.
Never include a key, a voice ID, an account ID, a real name or a path inside your home folder.
Report a security problem privately, through the private vulnerability reporting at the source, never in a public issue.
`how-to/workflows/syntek-media/03-report-a-template-problem/` drafts the report for you to file.

## Where the rules live

- `.claude/rules/syntek-media/06-global-rules.md` Section 3 keeps the guide as the template wrote it, Section 10 says what a report never holds, and Section 11 says how an answer changes.
- `.claude/rules/syntek-media/03-production-ethics.md` Section 4 says why the setup check comes before the first credit-spending call.
- `.claude/rules/syntek-media/04-toolkit-pipeline.md` Section 4 says what each toolkit command needs.
- `.claude/rules/syntek-media/01-layout-and-routing.md` Section 10 says where a departure from the guide is recorded.
- `how-to/docs/syntek-media/updating-the-template.md` explains what an update changes and why a stopped one is never committed.
- `how-to/workflows/syntek-media/05-recover-a-stopped-update/` gives every step for an update that stopped.

## Next

- What an update does, and its report section by section → `how-to/src/TEMPLATE-GUIDE/updating-and-recovery.md`
- The tools to install → `how-to/src/TEMPLATE-GUIDE/syntek-media/02-prerequisites.md`
- Sharing the project with syntek-author → `how-to/src/TEMPLATE-GUIDE/syntek-media/12-beside-syntek-author.md`
- Reporting a fault in the template → `how-to/workflows/syntek-media/03-report-a-template-problem/`
