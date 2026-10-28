# Prerequisites — the tools and accounts to have first, and checking them

The audio and video side of the project needs a few free tools on your computer, and two accounts if you use a voice service or a design project.
This chapter lists them, says what each one is for, and shows how to check which ones you already have.

## The tools

| Tool | What it is for | Do you need it? |
|---|---|---|
| ffmpeg and ffprobe, built with libass, x264 and mp3lame | Every render, cut, encode, loudness pass and caption burn, and every check of a file | Yes |
| Python 3.14 or later | `toolkit/media.py`, the scripts in `.claude/` and the update script that ends every update | Yes |
| uv | Running Copier, the thumbnail and card renderer, and the two MCP servers | Yes |
| git | Recording every version of the project; every update relies on it | Yes |
| Playwright's Chromium | Rendering thumbnails, cards and scenes to images | Yes, for any card or thumbnail |
| git-lfs | Large design exports in `brand/src/exports/large/`, and nothing else | Only for large design exports |
| espeak-ng | A rough offline voice for timing a script, labelled approximate | Optional |
| Rhubarb Lip Sync | Mouth shapes for an animated scene, from a voice track | Optional |
| WhisperX, on its own older Python | Word-by-word timing of a voice track, offline | Optional |
| pandoc | Cleaner chapter text for an audiobook, where the project makes audiobooks | Optional |
| Claude Code | Running the skills, the rules and the procedures | Yes |

A missing optional tool blocks only the commands that need it, and the toolkit's check names them.
Install Playwright's Chromium once, with the pinned version the toolkit uses:

```bash
uv run --with playwright==1.63.0 playwright install chromium
```

Where your system supplies its own browser bundle instead, as NixOS does, it must be the same revision.

## Python 3.14, and the older Python transcription needs

Everything in the project runs on Python 3.14 or later, with one exception.
`toolkit/transcribe.py`, which lines up each spoken word with its time, uses WhisperX, and WhisperX does not run on Python 3.14.
So word timing needs a second Python, from 3.10 to 3.13, kept beside 3.14 and never in its place.
Set `MEDIA_TRANSCRIBE_PYTHON` to the path of that older interpreter, the one WhisperX is installed in.
Set it at user scope, such as in your shell's start-up file, and never in a project file.
`media.py` then runs that interpreter directly, by its path, whenever it needs WhisperX.
Never activate the WhisperX environment in the shell where Claude Code or `media.py` runs.
An activated environment puts its older `python3` first, and the hooks and the family's scripts need `python3` at 3.14.
Without `MEDIA_TRANSCRIBE_PYTHON`, `media.py` asks uv for a Python in that range, offline.
A user-scope `UV_PYTHON` that names a Python outside the range is never used for it.
Where no interpreter qualifies, the transcribe command stops with exit code 2, and its message names `MEDIA_TRANSCRIBE_PYTHON`.
Once the interpreter is in place, run this command yourself, once, to download the models word timing uses:

```bash
python3 toolkit/media.py transcribe fetch
```

After that, word timing works offline, and no skill ever downloads a model for you.

## Running Copier

Copier is the tool that applied this template and brings in its later versions.
It needs no installing, because uv's `uvx` command runs it for you.
This template needs Copier 9.12.0 or later.
The copy's last task and the update script that ends every update run on the Python that runs Copier, and they need Python 3.14 or later.
Left to itself, `uvx` may run Copier on an older Python it already has.
Then those scripts do nothing, and each prints a framed message saying it did NOT run.
So every Copier command in this guide starts `uvx --python '>=3.14' copier`, which asks uv for Python 3.14 or later and fetches it the first time if your computer has none.
Keep the quotes round `>=3.14`: without them, the shell reads `>` as an instruction to write the output to a file.
This command prints the version of Copier that `uvx` runs:

```bash
uvx --python '>=3.14' copier --version
```

## Accounts

The voice service is ElevenLabs, which Claude reaches through an MCP server, a small helper program that gives Claude its tools.
Add that server once, at user scope, named `elevenlabs`, with a base path that contains this project, or it refuses every project file.
Keep its key, `ELEVENLABS_API_KEY`, in your shell, and never type it on a command line or commit it.
`production/docs/reference/elevenlabs.md` gives the exact commands and the rule for choosing the base path.
Claude Design is where the brand's layouts are explored visually, in one design project kept in step with `brand/src/design-system/`.
`brand/docs/reference/claude-design.md` says how the two are kept in step, and what a sync must never do.

## Checking what you have

Every command in this guide runs in a terminal, from the project's top folder, in bash, zsh or another POSIX shell.
This command checks every tool the toolkit uses, and changes nothing:

```bash
python3 toolkit/media.py check --setup
```

It also checks the permission entries in `.claude/settings.json` that the toolkit relies on, whether the ElevenLabs key is set in your shell, and whether the server's base path contains the project.
It checks the word-timing interpreter's own Python against the range WhisperX needs.
Exit code 0 means every line is clean, 1 means it found something to fix, and 2 means it could not run.
A missing optional tool is a note naming the commands it blocks, and a broken tool is a finding with its fix.
`brand/workflows/06-check-the-setup/` walks through each finding with you, one at a time.
Clear what it reports before the first call that spends credits.
If `python3 --version` prints a version older than 3.14, nothing in the toolkit runs: install Python 3.14 or later first.

## Coding agents and the two MCP servers

Claude Code is the client this project is built around, and other coding agents can do the same work from the same rules.
The project also declares two MCP servers, one for reading web pages and one for mapping the project's code, which uv starts on demand.
`how-to/src/TEMPLATE-GUIDE/agent-clients-and-mcp.md` explains the other clients, the files each one reads, and the two servers.

## Where the rules live

- `.claude/rules/syntek-media/04-toolkit-pipeline.md` Section 3: the toolkit's own rules, transcription on its older Python among them.
- `.claude/rules/syntek-media/04-toolkit-pipeline.md` Section 4: what the toolkit needs, and what `check --setup` reports.
- `.claude/rules/syntek-media/05-model-allocation.md` Section 4: the other coding agents and their models.
- `.claude/rules/syntek-media/03-production-ethics.md` Section 4: no credit-spending batch before the check is clean.
- `brand/workflows/06-check-the-setup/`: the procedure for checking the setup.

## Next

- Checking the setup, step by step → `brand/workflows/06-check-the-setup/`
- What syntek-media adds, if you have not read it → `how-to/src/TEMPLATE-GUIDE/syntek-media/01-overview.md`
- Adding syntek-media to a syntek-author project → `how-to/src/TEMPLATE-GUIDE/syntek-media/03-applying-over-syntek-author.md`
- Making a project with syntek-media alone → `how-to/src/TEMPLATE-GUIDE/syntek-media/04-a-standalone-project.md`
