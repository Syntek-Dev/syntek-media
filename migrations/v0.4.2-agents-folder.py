#!/usr/bin/env python3
"""v0.4.2-agents-folder.py: replace the shipped `.agents -> .claude` link with a real folder.

What moved and why the update strands it (DESIGN.md D76, amending D11 and D73).
  syntek-media 0.3.0 to 0.4.1 shipped `.agents` as a relative symbolic link to `.claude`.
  Codex mounts `.agents` read-only, and its bubblewrap sandbox refuses a read-only path that
  is a link to a writable folder, so every sandboxed Codex command fails in such a project
  (syntek-author's reply of 14/10/2026, verified in the Codex 0.160.1 source and by run).
  From 0.4.2 `.agents/` is a real folder holding one link, `skills -> ../.claude/skills`, and
  Antigravity's workspace MCP file, `mcp_config.json`. `.agents` is a copy-only shared path,
  so `copier update` never touches it: without this script the link survives every update.

The map.
  .agents -> .claude (link)    .agents/            (real folder)
                               .agents/skills      -> ../.claude/skills (relative link)
  .claude/mcp_config.json      .agents/mcp_config.json, moved only where that path is free

When it acts.
  Only where `.agents` is a symbolic link whose target is exactly `.claude` or `.claude/`.
  A real folder (this script's own result included), a link to anywhere else, a text file
  Git checked out in place of a link (core.symlinks=false), or no `.agents` at all is left
  exactly as it is and reported.

What it never does.
  It never deletes, overwrites or edits a file anyone wrote. It removes one thing: the link
  `.agents` itself, never its target, and only after the replacement folder is complete
  beside it. Anything it creates and cannot finish it removes again; nothing else. It reads
  no git-ignored file (D50): the stale-text report uses `git grep`, which reads tracked files.
  This is D11's one stated exception: media changes a shared path only here.

How it runs.
  From `copier update`, in the project root, after the update (`_migrations`, version v0.4.2,
  `_stage == 'after'`). By hand: run it from the project root with python3 (3.8 or later,
  standard library only); the command is printed at the end of every run. A second run finds
  a real folder and changes nothing.

Exit codes: 0 = always. A non-zero exit would abort every later migration and leave the
project half-upgraded, so every problem is printed instead.
"""

import os
import shlex
import subprocess
import sys

ANSWERS = '.copier-answers.syntek-media.yml'
ALIAS = '.agents'
OLD_TARGETS = ('.claude', '.claude/')
SKILLS_LINK = os.path.join(ALIAS, 'skills')
SKILLS_TARGET = '../.claude/skills'
OLD_MCP = os.path.join('.claude', 'mcp_config.json')
NEW_MCP = os.path.join(ALIAS, 'mcp_config.json')
STAGING = '.agents.syntek-media-v0.4.2'
# Text the 0.3.0 to 0.4.1 copy-only files wrote about the old layout. Those files are the
# author's, so a line is reported, never rewritten.
STALE = ('.agents -> .claude', '.agents aliases', 'link to .claude', 'through the alias',
         'through .agents', OLD_MCP)


def say(line=''):
    print(line, flush=True)


def source_of_answers():
    try:
        with open(ANSWERS, encoding='utf-8') as handle:
            for line in handle:
                if line.startswith('_src_path:'):
                    return line.split(':', 1)[1].strip().strip('\'"')
    except OSError:
        pass
    return '<the _src_path in ' + ANSWERS + '>'


def clone_url(source):
    """Copier's gh: and gl: shorthands are not URLs git understands."""
    for prefix, base in (('gh:', 'https://github.com/'), ('gl:', 'https://gitlab.com/')):
        if source.startswith(prefix):
            return base + source[len(prefix):]
    return source


def rerun_command():
    clone = '"${TMPDIR:-/tmp}/syntek-media-v0.4.2"'
    return ('{ test -d ' + clone + ' || git clone --depth 1 --branch v0.4.2 '
            + shlex.quote(clone_url(source_of_answers())) + ' ' + clone
            + '; } && python3 ' + clone + '/migrations/v0.4.2-agents-folder.py')


def describe(path):
    if os.path.islink(path):
        return 'a symbolic link to ' + repr(os.readlink(path))
    if os.path.isdir(path):
        return 'a real folder'
    if os.path.exists(path):
        return 'a file'
    return 'absent'


def report_folder():
    """Describe an existing real .agents folder without touching it."""
    skills = describe(SKILLS_LINK)
    mcp = describe(NEW_MCP)
    say('  left     .agents/ is a real folder; nothing changed')
    say('           .agents/skills is ' + skills
        + ('' if skills == "a symbolic link to '" + SKILLS_TARGET + "'" else
           '; the 0.4.2 layout links it to ' + SKILLS_TARGET + ' (see the bridge,'
           ' .claude/syntek-media-agents.md, Enabling an existing project)'))
    say('           .agents/mcp_config.json is ' + mcp)
    if os.path.lexists(OLD_MCP):
        say('           .claude/mcp_config.json is still there; Antigravity reads'
            ' .agents/mcp_config.json, so merge any server you need by hand')


def report_text_link():
    try:
        with open(ALIAS, encoding='utf-8', errors='replace') as handle:
            text = handle.read(64).strip()
    except OSError:
        text = ''
    say('  left     .agents is a file, not a link or a folder; nothing changed')
    if text in OLD_TARGETS:
        say('           it holds ' + repr(text) + ': Git checked the old link out as text'
            ' (core.symlinks=false, usually on Windows). Turn on Developer Mode or run as'
            ' an administrator, set git config core.symlinks true, then make the folder'
            ' by hand as the bridge says (.claude/syntek-media-agents.md, Enabling an'
            ' existing project).')


def remove_partial(created):
    """Undo only what this run created, newest first."""
    for path in reversed(created):
        try:
            if os.path.islink(path) or os.path.isfile(path):
                os.unlink(path)
            elif os.path.isdir(path):
                os.rmdir(path)  # empty by construction; never rmtree
        except OSError as error:
            say('  ! could not remove ' + path + ' that this run created: ' + str(error))


def replace_link():
    """Build the folder beside the link, then swap. Returns True when .agents was replaced."""
    if os.path.lexists(STAGING):
        say('  left     .agents is still a link to .claude: ' + STAGING + ' already exists'
            ' and is not this run\'s to remove. Move it aside and run the script again.')
        return False
    created = []
    try:
        os.mkdir(STAGING)
        created.append(STAGING)
        os.symlink(SKILLS_TARGET, os.path.join(STAGING, 'skills'))
        created.append(os.path.join(STAGING, 'skills'))
    except OSError as error:
        remove_partial(created)
        say('  left     .agents is still a link to .claude: the new folder could not be'
            ' made (' + str(error) + '). On Windows, symbolic links need Developer Mode'
            ' or an administrator.')
        return False
    # Re-check immediately before the one removal this script makes.
    if not (os.path.islink(ALIAS) and os.readlink(ALIAS) in OLD_TARGETS):
        remove_partial(created)
        say('  left     .agents changed while the script ran; nothing changed')
        return False
    os.unlink(ALIAS)  # the link only; its target, .claude, is untouched
    try:
        os.rename(STAGING, ALIAS)
    except OSError as error:
        try:
            os.symlink('.claude', ALIAS)
            remove_partial(created)
            say('  left     .agents is a link to .claude again: the new folder could not'
                ' be moved into place (' + str(error) + ')')
        except OSError as again:
            say('  ! .agents was removed and could not be restored (' + str(again) + ').'
                ' The new folder is at ' + STAGING + ': rename it to .agents by hand.')
        return False
    say('  removed  .agents -> .claude (the link only; .claude is untouched)')
    say('  created  .agents/')
    say('  linked   .agents/skills -> ' + SKILLS_TARGET)
    if not os.path.isdir(os.path.join('.claude', 'skills')):
        say('           .claude/skills is missing, so the link dangles until it exists')
    return True


def move_mcp():
    if os.path.lexists(NEW_MCP):
        if os.path.lexists(OLD_MCP):
            say('  left     .claude/mcp_config.json and .agents/mcp_config.json both exist;'
                ' Antigravity reads .agents/mcp_config.json, so merge any server you need'
                ' by hand')
        return False
    if not os.path.lexists(OLD_MCP):
        say('  absent   .claude/mcp_config.json (deleted before this update); no'
            ' .agents/mcp_config.json is written. Add one only if you use Antigravity.')
        return False
    if os.path.islink(OLD_MCP) or not os.path.isfile(OLD_MCP):
        say('  left     .claude/mcp_config.json is ' + describe(OLD_MCP)
            + ', not a plain file; move it to .agents/mcp_config.json by hand if you want'
            ' Antigravity to read it')
        return False
    os.rename(OLD_MCP, NEW_MCP)
    say('  moved    .claude/mcp_config.json -> .agents/mcp_config.json (contents unchanged)')
    return True


def report_stale_text():
    try:
        out = subprocess.run(
            ['git', 'grep', '-n', '-I', '-F'] + sum((['-e', s] for s in STALE), [])
            + ['--', '.', ':!.claude/syntek-media-agents.md', ':!.claude/rules/'],
            capture_output=True, text=True, check=False)
    except OSError:
        return
    lines = [l for l in out.stdout.splitlines() if l]
    if not lines:
        return
    say()
    say('  Tracked lines that still describe the old layout (yours to edit; nothing was'
        ' changed). The 0.4.2 layout: .agents/ is a real folder, .agents/skills links to'
        ' ../.claude/skills, and Antigravity reads .agents/mcp_config.json.')
    for line in lines:
        say('    ' + line)


def main():
    if len(sys.argv) > 1 and sys.argv[1] in ('-h', '--help'):
        say(__doc__)
        return
    say('▸ syntek-media v0.4.2: the .agents folder (DESIGN.md D76)')
    if not os.path.isfile(ANSWERS):
        say('  left     ' + ANSWERS + ' is not here: run this from the project root.'
            ' Nothing changed.')
        return
    changed = moved = False
    if os.path.islink(ALIAS):
        target = os.readlink(ALIAS)
        if target in OLD_TARGETS:
            changed = replace_link()
            if changed:
                moved = move_mcp()
        else:
            say('  left     .agents is a link to ' + repr(target)
                + ', not to .claude; nothing changed. If Codex runs here, make .agents a real'
                ' folder by hand as the bridge says.')
    elif os.path.isdir(ALIAS):
        report_folder()
    elif os.path.exists(ALIAS):
        report_text_link()
    else:
        say('  left     there is no .agents; nothing changed. To add one, follow the bridge,'
            ' .claude/syntek-media-agents.md, Enabling an existing project.')
    report_stale_text()
    say()
    if changed:
        say('  Review and commit: git add -A .agents' + (' ' + OLD_MCP if moved else '')
            + ' && git status')
    say('  Run again from the project root (a second run changes nothing):')
    say('    ' + rerun_command())


if __name__ == '__main__':
    try:
        main()
    except Exception as error:  # always exit 0: report, never abort the update
        try:
            say('  ! the v0.4.2 .agents migration stopped: ' + repr(error))
            say('    Nothing it had not yet reported was changed. Run it again from the'
                ' project root.')
        except OSError:
            pass
    sys.exit(0)
