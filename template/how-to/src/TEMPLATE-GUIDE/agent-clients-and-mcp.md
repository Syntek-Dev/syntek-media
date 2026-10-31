# Agent clients and MCP servers — Claude Code, the other coding agents and the two servers

Every coding agent you use in this project reads one set of instructions, kept in the `.claude/` folder.
The other agents reach it through a short bridge file that each template ships.
Two servers that give a session extra tools come with every project, each fixed to one version, needing no key and asking you before its riskier tools.

## One tree for every client

A coding agent, also called a client, is the program you talk to in a session: Claude Code, Codex, Gemini CLI, Antigravity or OpenCode.
Claude Code always comes with the project, and the others only where you chose them when the project was made.
The `.claude/` folder holds the project's rules, its skills, its memory and the top manual, and each folder keeps its own manual.
There is one copy of each, and every client reads it.
Claude Code reads it by itself.
The other clients start from an entrypoint file at the top of the project: `AGENTS.md` for Codex and OpenCode, and `GEMINI.md` for Gemini CLI and Antigravity.
Each entrypoint sends its client to every `.claude/syntek-*-agents.md` file present.
That file is a bridge: it tells a client that is not Claude Code how to find the rules and in what order to read them.
Each template applied to the project ships its own bridge, and every entrypoint reads every bridge it finds.
So a project with two templates has two bridges, and each client reads both.

## Which files each client reads

Each client also has a settings file of its own, which names its model, the MCP servers it starts and the tools it must ask you about.

- Claude Code reads `.claude/settings.json`, and `.mcp.json` for its servers.
- Codex reads `config.toml` in `.codex`.
- Gemini CLI reads `settings.json` in `.gemini`.
- Antigravity reads `mcp_config.json` in `.agents`, and you choose its model in the app.
- OpenCode reads `opencode.json`, at the top of the project.

The skills, the written procedures a session follows for each kind of job, live in one place: `.claude/skills/`.
Some clients look for skills in `.agents` instead, so in a project made for any client besides Claude Code, `.agents` is a real folder, and the `skills` inside it is a link to `.claude/skills`.
A link, or symbolic link, is a small file that points at another folder, so every client sees one copy of each skill.
The entrypoints and the other clients' settings files are written when a template is copied into the project, and only where they are missing.
An update never adds or recreates one, and changes one only by adding the two MCP servers once to a file that lacks them.
So a file you delete stays deleted, and a client you stop using keeps its files until you delete them.
The one exception is a later copy, such as another template's first copy into the project, which writes each missing file of the clients its answers name.
Codex and Gemini CLI read their settings files in the project only once you trust the project, so trust it when they ask.
OpenCode reads no `CLAUDE.md` file at all, so the bridge is its only route to the rules.

## Adding a client later

A client you choose after the project was made needs its files copied in by hand, because an update never writes them.
The route has four parts.
First, you record the new client through the update of each template applied to the project, one at a time, in its `AGENT_CLIENTS` answer, listing every client you keep as well as the new one.
That changes the model table in each template's rules, and creates none of the client's files.
Next, you make a fresh project from the same template source and version into a temporary folder, with your answers.
Then you copy into your project only the client files it is missing.
Where a file already exists, you combine the two by hand and never overwrite yours; a session agrees each one with you first.
Last, you run the permissions script (below) and restart the client.
Your template's own procedure for enabling a client, in its folder under `how-to/workflows/`, gives every command.

## When .agents is not a plain folder

In a new project made for any client besides Claude Code, `.agents` is a real folder, and the `skills` inside it is a link to `.claude/skills`; a project made for Claude Code alone has no `.agents`.
Four other cases need care.

- An older layout made `.agents` a link to `.claude`, which Codex on Linux refuses: make it a real folder before a copy or a new client.
- A real `skills` folder inside `.agents`, one you made yourself, is never replaced: combine its skills with the project's by hand.
- A `skills` link inside `.agents` that points anywhere else also stays as it is, and its skills are combined by hand.
- An `.agents` link to a folder outside the project is kept as a link, and its target is never read or changed.

Copier, the tool that applies a template, refuses to write anything beneath a link that leads outside the project.
So every update renames such a link to `.agents.syntek-held` before it writes, and back afterwards.
That step runs on the Python that runs Copier and needs Python 3.14 or later; on an older one it holds nothing and says so in a message framed in lines of `=`, and Copier stops the update with `ForbiddenPathError`, which `how-to/src/TEMPLATE-GUIDE/updating-and-recovery.md` explains.
A copy does not do this for you, so hold the link by hand when you copy a template into such a project.
Run `mv .agents .agents.syntek-held` first, copy with `--exclude /.agents`, and afterwards run `mv .agents.syntek-held .agents`, even if the copy stopped.
An update can stop before it ends: at a refused answer, at Ctrl-C during a question, or when Copier fails as it cleans up after writing.
The link then stays held as `.agents.syntek-held`, and the next update refuses the changed tree.
By then `.agents` may stand again, because the update or a discard can put it back.
Put the link back before anything else, and before you discard the stopped update, because `git clean -fd` would delete a held link that Git does not track.
Work from the top folder of the project, in a POSIX shell: Terminal on macOS and Linux, or Git Bash on Windows, never PowerShell's `rm`.
First, see what stands at `.agents`:

```bash
ls -ld .agents .agents.syntek-held
```

Where it shows no `.agents.syntek-held`, nothing is held: stop here and change nothing.
Where `.agents` is a link (its line shows `->`), remove that link alone, never with `rm -r` and never with a trailing slash:

```bash
rm .agents
```

Where `.agents` is a folder or a file instead, move it aside to a name nothing holds yet, once `ls -ld .agents.from-update` finds nothing:

```bash
mv .agents .agents.from-update
```

`.agents.from-update` now holds what the update wrote: check it, and delete nothing in it that is yours.
Then, once `ls -ld .agents` finds nothing, put the held link back:

```bash
mv .agents.syntek-held .agents
```

Never run that `mv` while `.agents` stands: it would put the held link inside it, or inside the outside folder that `.agents` links to.
Then update again.
Where `git status` still shows changes, discard the stopped update first, as `how-to/src/TEMPLATE-GUIDE/updating-and-recovery.md` explains.
Where the held link was committed beside an identical `.agents` link, the next update moves nothing and says so.
It asks you to remove the held link with `rm .agents.syntek-held`, commit, and update again.
A `copier update --pretend` run still refuses such a project, because a pretend run skips the steps that hold the link.

## Carrying the settings to each client

`.claude/settings.json` holds Claude Code's deny rules, for what a session may never do, and its ask rules, for the tools it must ask you about first.
The other clients never read that file.
The permissions script, `.claude/syntek-*-permissions.py`, reads those rules and writes each one a client can hold into that client's own settings file.
Each template ships its own copy under its own name, and the copies are the same bytes, so either gives the same result.
It needs Python 3.14 or later: on an older Python it says in a framed message that it did NOT run, and changes nothing.
It reports every rule a client cannot hold, and why.
Of the other clients, only OpenCode can hold, in its own file, the deny that stops sessions editing the user guide.
Antigravity keeps its permissions in the app, so for it the script lists what to set there, the guide's deny included.
In Codex and Gemini CLI, which cannot hold the deny, the project's rules alone keep a session from editing the guide.
The `for` loop in these commands runs the first copy of the script it finds, whichever template wrote it.
This command shows the plan and any rule a client file is missing, and changes nothing:

```bash
for f in .claude/syntek-*-permissions.py; do python3 "$f" --check; break; done
```

It reports a problem where a client file that exists lacks a rule that client could hold.
When nothing is missing, it ends by saying that every rule it can express is in place.
With your agreement, this command adds the missing rules, changing only the permission settings of client files that already exist:

```bash
for f in .claude/syntek-*-permissions.py; do python3 "$f" --write; break; done
```

It never creates a client file.
Run it after each template is first copied into the project, after an update adds deny or ask rules to `.claude/settings.json`, and after you add a client.
What it writes for Codex and Gemini CLI works only once you trust the project.
Its OpenCode rules assume you start OpenCode at the top of the project.

## The two MCP servers

An MCP server is a small program that gives a session extra tools; MCP stands for Model Context Protocol.
Every project comes with two, listed in `.mcp.json` and in the settings file of each client its answers name.
Scrapling fetches web pages, either as a plain web request or through a browser it drives.
code-review-graph builds a map of the code in the project, kept on your machine.
Both are pinned, which means each is fixed to one version the template has checked, and neither needs a key or an account.
Claude Code asks you before each Scrapling tool that opens a browser, and before the two code-review-graph tools that write files.
It never offers code-review-graph's embedding tool, which can send your code to an online service.
The first start may be slow, because the servers are downloaded then, and a client may give up waiting once.
Every `.claude/syntek-*-agents.md` gives the commands that download them in advance: run them yourself, in your own terminal.
Never run code-review-graph's `install`, `init` or `uninstall`, or `scrapling install`: they add unpinned entries and change files across the project and your home folder.
An interactive Claude Code session asks you once before it starts a project's servers.
Codex and Gemini CLI start them only in a trusted project.
OpenCode starts them when it opens the project, and runs without a prompt every tool the project does not ask about.
So in OpenCode the rules are the only safeguard.
The project's rules in `.claude/rules/` say how a session may use the servers, under 'Web and code tools'.
An update adds the two servers once to `.mcp.json` and to the settings file of each client your answers name, wherever one lacks them (OpenCode's and Gemini CLI's once they hold the ask rules the permissions script writes), and never adds back one you removed.
A client file your answers do not name gets one line in the report instead; once you record its client, as 'Adding a client later' says, an update adds them.

## A skill of your own with the same name

A personal skill, kept in `~/.claude/skills/` in your home folder, replaces the project's skill of the same name in Claude Code, because personal skills come first.
So with a personal `handoff` skill, `/handoff` and the hooks that ask for the `handoff` skill run yours instead, and no update ever refreshes it.
The same holds for the project's other shared working-practice skills: `grill-me`, `grill-with-docs`, `grilling`, `to-questionnaire`, `wait-what` and `wayfinder`.
Rename or remove the personal one to use the project's.
OpenCode works the same way: a global skill with a project skill's name wins over it.

## Where the rules live

- The project's rules, in `.claude/rules/`, decide what a session may do with each client and server; where they differ from this chapter, the rules win.
- Every `.claude/syntek-*-agents.md` gives its template's read order, model tiers and client set-up.
- Your template's procedures, in its folder under `how-to/workflows/`, give the steps for enabling a client.

## Next

- Updating a project, and getting back from an update that stopped → `how-to/src/TEMPLATE-GUIDE/updating-and-recovery.md`
- Keeping binary files under a data root → `how-to/src/TEMPLATE-GUIDE/the-data-root.md`
