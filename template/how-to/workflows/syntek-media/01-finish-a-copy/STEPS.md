---
workflow: 01-finish-a-copy
phase: review
skills: []
model: opus
---

# STEPS.md — finish a copy

**Last Updated**: <%DATE%> **Version**: 0.1.0 **Maintained By**: <%OWNER_NAME%>
**Language**: British English (en_GB)

The ordered procedure for finishing a fresh copy of syntek-media, from what Copier printed to
the first commit. Each step names the guide it uses. **Run in order**, from the top folder of
the project, and tick `CHECKLIST.md` as you go. Every command runs exactly as written, in bash,
zsh or another POSIX shell.

> Read the read-order files first (this folder's `CONTEXT.md` and `CLAUDE.md`). No skill runs
> this procedure. Every step that changes a settings file or reaches outside the project waits
> for the author's word.

## 1. Read what the copy printed

> **Skill:** none · **Guide:** `how-to/docs/syntek-media/finishing-a-copy.md`

Go through Copier's output with the author, from the first file line to the end of the message
after the copy. Each file the project already had is printed as `conflict` then `skip`, or as
`identical`: Copier left it exactly as it was, which is expected, and is not a collision. Any
other path that already existed is a collision, a fault in the template: a copy run without a
terminal stopped with `Interactive session required` before writing it, and an interactive one
asked `Overwrite` with yes as the default, which should have been answered no. Where either
happened, this command lists what the copy wrote before it stopped:

```bash
git status
```

Remove what it wrote with the author, stop this procedure, and report the collision with
`how-to/workflows/syntek-media/03-report-a-template-problem/`. Read, too, any line that starts
`syntek-media:` and says syntek-author is older than v0.6.0: update syntek-author by its own
procedure, from a clean tree, before going on. Note whether a message framed in lines of `=`
says `family-update did NOT run`, and whether the copy was run with `--skip-tasks`: step 2
needs both answers. _Substantive._

## 2. Add the settings entries the message gives

> **Skill:** none · **Guide:** `how-to/docs/syntek-media/finishing-a-copy.md`

Item 2 of the message after the copy lists what no copy adds to a `.claude/settings.json` the
project already had. Read it with the author, and add each entry only on their word, exactly as
the message prints it, changing nothing else in the file:

- **Where step 1 showed `.claude/settings.json` as `conflict` then `skip`:** the six entries
  the message lists under `allow`, which no copy or update offers.
- **Where the framed `family-update did NOT run` message appeared, or the copy took
  `--skip-tasks`:** every other entry item 2 lists too, at the top level, in `ask`, in `deny`
  and in `hooks`. Otherwise the copy's last task has already offered them, once each.
- **Either way, where the file lacks it:** the data-root guard, the seed's other `PreToolUse`
  entry, which no copy or update offers in either template.

Where the message has gone, `python3 toolkit/media.py check --setup` at step 7 reports the
missing entries the toolkit needs: its allows, the ElevenLabs and voice-remix asks, and the
denies on `generated/` and `renders/`. It never checks the others, so compare the file with
item 2 by hand. _Substantive._

## 3. Carry the asks and denies to the other coding agents

> **Skill:** none · **Guide:** `how-to/docs/syntek-media/finishing-a-copy.md`

The other coding agents do not see the rules in `.claude/settings.json` until the permissions
script copies them into their own files. This command shows the plan and any rule a client
file lacks, and changes nothing:

```bash
python3 .claude/syntek-media-permissions.py --check
```

It ends `Every expressible rule is in place.` where nothing is missing, or names each rule a
client file lacks. On the author's word, this command adds the missing rules to the client
files that exist, never creating one, and prints what a client cannot express:

```bash
python3 .claude/syntek-media-permissions.py --write
```

_Mechanical._

## 4. Name the media layers in the index files, if the author wants

> **Skill:** none · **Guide:** `how-to/docs/syntek-media/finishing-a-copy.md`

The media rules in `.claude/rules/syntek-media/` load at launch whatever the index files say, so
this step is optional. Where the author wants it, add a line naming the media layers (`brand/`,
`scripts/`, `production/` and `publishing/`) to `README.md` and `CONTEXT.md`, and one naming
`.claude/rules/syntek-media/` to `.claude/CLAUDE.md`, in the author's words. Nothing needs adding
to `.gitignore` or `.mcp.json`: media's ignore rules are nested, and the ElevenLabs server is
user-scoped. _Substantive._

## 5. Register the ElevenLabs server

> **Skill:** none · **Guide:** `production/docs/reference/elevenlabs.md`

The server is added once, at user scope, by the author in their own terminal. Its base path must
contain this project, because speech-to-text refuses any file outside it: `$HOME` where every
project lives under it, otherwise the nearest folder that holds them all, put in place of
`$HOME` in the second command. The author exports `ELEVENLABS_API_KEY` in their shell first,
and never types the key on the command line or commits it. The first command removes an earlier
registration; the second adds the server again:

```bash
claude mcp remove elevenlabs --scope user
claude mcp add --env ELEVENLABS_API_KEY="$ELEVENLABS_API_KEY" --env ELEVENLABS_MCP_BASE_PATH="$HOME" \
  --transport stdio --scope user elevenlabs -- uvx elevenlabs-mcp
```

Where the project will make no generated audio, the author may leave this step for later; the
set-up check at step 7 then reports the server. A session never calls an ElevenLabs tool to test
it. _Substantive._

## 6. Set up Git LFS, where large exports will be kept

> **Skill:** none · **Guide:** `how-to/docs/syntek-media/finishing-a-copy.md`

Large design exports go in `brand/src/exports/large/`, which Git LFS stores. Where no LFS filter
was configured, the copy set a tripwire in this repository's own Git settings, so that adding a
file there fails loudly instead of committing it whole. Before that folder is used, the author
runs this once, with Git LFS installed:

```bash
git lfs install
```

It sets the same value, and the tripwire is then harmless. Where the project will keep no large
export, skip this step. _Mechanical._

## 7. Check the set-up

> **Skill:** none · **Guide:** `how-to/docs/syntek-media/finishing-a-copy.md`

Run `brand/workflows/06-check-the-setup/` from its step 1, which starts with this command and
changes nothing:

```bash
python3 toolkit/media.py check --setup
```

Fix each finding with the author as that procedure says, or record what it blocks. No
credit-spending call is made while an ElevenLabs line is open. _Substantive._

## 8. Commit, with the answers file

> **Skill:** none · **Guide:** `how-to/docs/syntek-media/finishing-a-copy.md`

This command lists what the copy and the steps above changed:

```bash
git status
```

It should list `.copier-answers.syntek-media.yml` among the new files, and nothing the author
does not recognise. Once they have agreed every change, this command commits the copy whole,
with the answers file every later update works from:

```bash
git add -A && git commit -m 'Add syntek-media'
```

Afterwards `git status` should end `nothing to commit, working tree clean`. Where the copy was
made on a branch, merge it into the project's main line with the author, the way they usually
do. _Mechanical._
