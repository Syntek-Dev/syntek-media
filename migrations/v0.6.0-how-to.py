#!/usr/bin/env python3
"""v0.6.0-how-to.py: say where media's user guide starts and that it is read-only, and name
what already stood in how-to/; move nothing.

What moved and why the update cannot say it (DESIGN.md D84, on the model of syntek-author's
v0.6.0-how-to.sh, its D44 and D56).
  syntek-media 0.6.0 adds its user guide to every project under how-to/, a folder it shares
  with syntek-author file by file, and makes the folder read-only: Claude Code is denied edits
  there, a hook refuses them, and every full update puts the template's text back on any file
  of the guide that differs. The update that crosses 0.6.0 writes media's own guide files by
  Copier's merge, and the shared ones, with the deny and the guard, through the update script
  that ends every update (D81), on Python 3.14. It moves nothing. What it cannot say, because
  the owner's files were there first or the folder is not what the guide expects, this lists.

The map (report only; every brand kind).
  1. Where media's guide starts, how to update from now on, that the guide is read-only, and
     where a departure from it is recorded.
  2. Where syntek-author's answers file stands: syntek-author's own guide, where its first
     chapter exists; otherwise, that syntek-author must be v0.6.0 or later, updated now and
     before syntek-media from then on.
  3. how-to where it is a link, a root entry that differs from how-to only in letter case,
     and a guide Git ignores.
  4. The owner's files at the guide's paths: a shared file HEAD holds, or an untracked one,
     whose bytes differ from the template's, and a file of media's own syntek-media/ folders
     HEAD holds that the update merged or marked as a conflict. The update report that
     follows puts the template's text back on each (unless another template wrote it, or Git
     does not hold it); the owner's text stays in Git.
  5. Every file under how-to/ that Git does not ignore and no template ships: not in this
     release's template/how-to/, nor under how-to/{docs,src/TEMPLATE-GUIDE,workflows}/<name>/
     for any .copier-answers.<name>.yml at the project root.
  6. Where opencode.json exists, the permissions script's --check, then --write, for the
     guide's new deny rule.
  7. The command that runs it again.

When it acts.
  Never: it only reads and prints. It stays silent and exits 0 where
  .copier-answers.syntek-media.yml is absent (not a syntek-media project, or not its root).

What it never does.
  - change, move, copy, untrack or delete any file, or write Git's index;
  - read a git-ignored file (DESIGN.md D42, D50): it reads only the files
    git ls-files -co --exclude-standard lists, git check-ignore and Git's objects at HEAD;
  - read the data root, or SYNTEK_DATA_ROOT;
  - fail the update: every path exits 0, an unexpected error included, because a non-zero
    exit aborts every migration declared after it, the family 'update' entry among them.

How it runs.
  From `copier update`, once, on the update that crosses 0.6.0 (`_migrations`, version
  v0.6.0, `_stage == 'after'`), after v0.4.2's entry and before the family 'update' block,
  through the interpreter running Copier. Standard library only; it parses and runs on
  Python 3.10, the oldest Copier 9.12.0 supports. By hand: from the project root, with the
  command printed at the end of every run, which clones the release and runs it again. A
  second run prints the same report over the same tree; once the update is committed it
  lists no file of media's own.

Exit codes: 0 = always.
"""

import filecmp
import glob
import os
import shlex
import subprocess
import sys
import textwrap

ANSWERS = '.copier-answers.syntek-media.yml'
PEER_ANSWERS = '.copier-answers.syntek-author.yml'
RELEASE = 'v0.6.0'
SCRIPT = 'v0.6.0-how-to.py'
GUIDE = 'how-to'
OWN_FOLDER = 'syntek-media'
GUIDE_START = 'how-to/src/TEMPLATE-GUIDE/syntek-media/01-overview.md'
PROCEDURE = 'how-to/workflows/syntek-media/04-update-the-template/'
PEER_GUIDE_START = 'how-to/src/TEMPLATE-GUIDE/syntek-author/01-overview.md'
GUIDE_HOMES = ('how-to/docs/', 'how-to/src/TEMPLATE-GUIDE/', 'how-to/workflows/')
MAX_LIST = 40
# The template clone this runs from: the update's own copy, or the clone the rerun makes.
SRC = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# No optional lock: a read must never refresh Git's index.
GIT_ENV = dict(os.environ, GIT_OPTIONAL_LOCKS='0')


def say(line=''):
    print(line, flush=True)


def git(*args):
    """Run git; return (exit status, stdout bytes). A missing git is status 127."""
    try:
        done = subprocess.run(('git',) + args, stdout=subprocess.PIPE,
                              stderr=subprocess.DEVNULL, env=GIT_ENV)
    except OSError:
        return 127, b''
    return done.returncode, done.stdout


def git_paths(*args):
    """The NUL-separated paths a git command prints, in order, without repeats."""
    status, out = git(*args)
    if status != 0:
        return []
    seen, paths = set(), []
    for raw in out.split(b'\0'):
        if raw:
            path = os.fsdecode(raw)
            if path not in seen:
                seen.add(path)
                paths.append(path)
    return paths


def source_of_answers():
    try:
        with open(ANSWERS, encoding='utf-8') as handle:
            for line in handle:
                if line.startswith('_src_path:'):
                    value = line.split(':', 1)[1].strip().strip('\'"')
                    if value:
                        return value
    except (OSError, ValueError):
        pass
    return '<the _src_path in ' + ANSWERS + '>'


def clone_url(source):
    """Copier's gh: and gl: shorthands are not URLs git understands."""
    for prefix, base in (('gh:', 'https://github.com/'), ('gl:', 'https://gitlab.com/')):
        if source.startswith(prefix):
            return base + source[len(prefix):]
    return source


def rerun_command():
    clone = '"${TMPDIR:-/tmp}/syntek-media-' + RELEASE + '"'
    return ('{ test -d ' + clone + ' || git clone --depth 1 --branch ' + RELEASE + ' '
            + shlex.quote(clone_url(source_of_answers())) + ' ' + clone
            + '; } && python3 ' + clone + '/migrations/' + SCRIPT)


def shipped_files():
    """Every file of this release's template/how-to/, relative to template/, sorted."""
    root = os.path.join(SRC, 'template')
    found = []
    for folder, dirs, files in os.walk(os.path.join(root, GUIDE)):
        dirs.sort()
        for name in files:
            rel = os.path.relpath(os.path.join(folder, name), root)
            found.append(rel.replace(os.sep, '/'))
    return sorted(found)


def sibling_homes():
    """The folders another template's guide files sit in, for each answers file at the root."""
    homes = []
    for answers in sorted(glob.glob('.copier-answers.*.yml')):
        if answers == ANSWERS or not os.path.isfile(answers):
            continue
        name = answers[len('.copier-answers.'):-len('.yml')]
        if name and '/' not in name:
            homes.extend(home + name + '/' for home in GUIDE_HOMES)
    return homes


def para(text, blank=True):
    """One paragraph of the report, wrapped at 94 columns, after a blank line."""
    if blank:
        say()
    for line in textwrap.wrap(text, width=94, initial_indent='  ', subsequent_indent='  ',
                              break_long_words=False, break_on_hyphens=False):
        say(line)


def listing(paths, line):
    for index, path in enumerate(paths):
        if index == MAX_LIST:
            say('    … and %d more' % (len(paths) - MAX_LIST))
            break
        say('    ' + line(path))


def main():
    if len(sys.argv) > 1 and sys.argv[1] in ('-h', '--help'):
        say(__doc__)
        return
    if not os.path.isfile(ANSWERS):
        return

    in_git = git('rev-parse', '--is-inside-work-tree')[1].strip() == b'true'
    has_head = in_git and git('rev-parse', '-q', '--verify', 'HEAD')[0] == 0
    prefix = os.fsdecode(git('rev-parse', '--show-prefix')[1].strip()) if in_git else ''
    full = os.environ.get('SYNTEK_UPDATE_REPORT', '').strip().lower() != 'off'
    old_python = sys.version_info < (3, 14)

    # What may be read (D42): only what Git lists, and only regular files.
    listed = set(git_paths('ls-files', '-z', '-co', '--exclude-standard')) if in_git else set()
    untracked = set(git_paths('ls-files', '-z', '-o', '--exclude-standard')) if in_git else set()

    def readable(path):
        return path in listed and os.path.isfile(path) and not os.path.islink(path)

    def differs(path):
        # As cmp -s: a file it cannot read (or a template file it cannot) counts as differing,
        # so it is listed as the owner's and the report goes on.
        try:
            return not filecmp.cmp(path, os.path.join(SRC, 'template', path), shallow=False)
        except OSError:
            return True

    shipped = shipped_files()
    shipped_set = set(shipped)
    own_marker = '/' + OWN_FOLDER + '/'
    shared = [p for p in shipped if own_marker not in p]
    own = [p for p in shipped if own_marker in p]
    homes = sibling_homes()

    link = ''
    if os.path.islink(GUIDE):
        try:
            link = os.readlink(GUIDE)
        except OSError:
            link = '?'
    cases = sorted(e for e in os.listdir('.') if e != GUIDE and e.lower() == GUIDE)
    ignored = False
    if in_git:
        for path in (GUIDE + '/CONTEXT.md', GUIDE_START):
            if git('check-ignore', '-q', '--no-index', '--', path)[0] == 0:
                ignored = True

    # The owner's files at the guide's paths, in this order and never twice.
    yours, kind = [], {}

    def mine(path, how):
        if path not in kind:
            kind[path] = how
            yours.append(path)

    if in_git:
        at_head = set(git_paths('ls-tree', '-r', '-z', '--name-only', 'HEAD', '--', GUIDE)) \
            if has_head else set()
        for path in shared:
            # A shared file HEAD holds whose bytes differ from the template's (an update never
            # renders one, so this is the owner's, or another template's).
            if path in at_head and readable(path) and differs(path):
                mine(path, 'tracked')
        for path in shared:
            # One Git does not hold yet, not ignored, whose bytes differ from the template's.
            if path in untracked and readable(path) and differs(path):
                mine(path, 'untracked')
        # A file of media's own folders that HEAD holds and the work tree no longer matches:
        # the owner's committed file, which Copier has just merged or marked as a conflict.
        # Never compared byte for byte: media's guides and procedures carry header tokens. A
        # file Copier wrote new is untracked, and once the update is committed HEAD equals
        # the work tree, so neither is ever listed.
        if has_head:
            held = [p for p in own if p in at_head]
            # --relative: diff prints paths from the repository root, unlike ls-files and
            # ls-tree, so a project in a subfolder of its repository would never match.
            changed = set(git_paths('diff', '--no-ext-diff', '--relative', '--name-only', '-z',
                                    'HEAD', '--', GUIDE)) if held else set()
            for path in held:
                if path in changed:
                    mine(path, 'tracked')

    # Files under how-to/ that no template ships.
    stray = []
    if in_git:
        for path in sorted(git_paths('ls-files', '-z', '-co', '--exclude-standard', '--',
                                     GUIDE + '/')):
            if path in shipped_set:
                continue
            # A .rej beside a guide file is this update's own: the report that follows prints
            # its rm.
            if path.endswith('.rej') and path[:-len('.rej')] in shipped_set:
                continue
            if any(path.startswith(home) for home in homes):
                continue
            stray.append(path)

    # ── The report ──
    say()
    say('▸ v0.6.0 migration (syntek-media) — the user guide, how-to/ (DESIGN.md D84); report only')
    say('  This release adds the user guide. Start at')
    say('    ' + GUIDE_START)
    say('  and update this template from now on with the steps in')
    say('    ' + PROCEDURE)
    para('The guide is read-only: Claude Code is denied edits there and a hook refuses them, once '
         '.claude/settings.json holds the deny and the guard, and every full update puts the '
         'template\'s text back on any file of it that differs and lists each in its report (what '
         'you had stays in Git). To work differently from it, record the departure where project '
         'rules go, never in how-to/: a departure from a guide or chapter there in the Overrides '
         'of syntek-author\'s 00-project.md, where present (a redirect included), and one from a '
         'procedure there in its Workflow aliases, by full folder path; otherwise it is a project '
         'rule in .claude/CLAUDE.md, under the heading \'Project-specific rules\'.', blank=False)

    if os.path.isfile(PEER_ANSWERS):
        if os.path.isfile(PEER_GUIDE_START):
            para('syntek-author\'s answers file stands here, and its own guide starts at')
            say('    ' + PEER_GUIDE_START)
            say('  Update syntek-author before syntek-media from now on, each from a clean tree.')
        else:
            para(PEER_ANSWERS + ' stands here without ' + PEER_GUIDE_START + ', so this '
                 'syntek-author is older than v0.6.0, which a combined project must not keep: '
                 'update syntek-author to v0.6.0 or later now, from a clean, committed tree, and '
                 'update it before syntek-media from then on.')

    if link:
        para('how-to is a link to %s: this update wrote the guide\'s files through it, and the '
             'update report restores no file beyond it. Make how-to a real folder, then update '
             'again.' % link)
    for twin in cases:
        para('\'%s\' differs from how-to only in letter case: on a disk that ignores case the '
             'guide\'s files went into it. Rename it before the next update.' % twin)
    if ignored:
        para('Git ignores files under how-to/ in this project (git check-ignore -v --no-index '
             'how-to/CONTEXT.md names the rule): an update never reads, restores or reports an '
             'ignored file, so the guide may not match this template version. Remove the rule.')
    if not in_git:
        para('Not a git repository, so the files under how-to/ are not listed.')

    if yours:
        if old_python:
            who = ('This runs on Python %d.%d, older than 3.14: where Copier runs on it too, '
                   'family-update.py does not run after this report, so nothing is put back, '
                   'refreshed or reported. Upgrade to Python 3.14 and run the same update again, '
                   'as %s gives it; that update puts' % (sys.version_info[0], sys.version_info[1],
                                                         PROCEDURE))
        elif full:
            who = 'The update report that follows puts'
        else:
            who = ('SYNTEK_UPDATE_REPORT=off skips the update report\'s restore; the next full '
                   'update puts')
        para('%d file(s) of yours stand where the guide now has files. %s the template\'s text '
             'there, unless another template wrote the file (it stays that template\'s version) '
             'or Git does not hold yours (it is left, and named). Your text stays in Git:'
             % (len(yours), who))

        def entry(path):
            if kind[path] == 'untracked':
                return path + '    (not in Git: commit or move it first)'
            return path + '    git show ' + shlex.quote('HEAD:' + ('./' if prefix else '') + path)

        listing(yours, entry)

    if stray:
        para('%d file(s) under how-to/ belong to no template. how-to/ is the templates\' '
             'read-only guide, so no session may edit them there. Nothing moves them; move each '
             'yourself, with git mv (or mv, for a file Git does not track), to where your own '
             'work lives: a guide to a layer\'s docs/project/, a procedure to its '
             'workflows/local/.' % len(stray))
        listing(stray, lambda path: path)

    if os.path.lexists('opencode.json'):
        para('This release adds a deny rule for how-to/ to .claude/settings.json, which the '
             'update offers once (never where you removed it). Then run:')
        say('    python3 .claude/syntek-media-permissions.py --check')
        say('  and, where it reports opencode.json lacking it, the same with --write.')

    say()
    say('  This script changed nothing. To run it again from the project root:')
    say('    ' + rerun_command())
    say()


if __name__ == '__main__':
    try:
        sys.stdout.reconfigure(errors='replace')
    except (AttributeError, ValueError, OSError):
        pass
    try:
        main()
    except BaseException as error:  # always exit 0: report, never abort the update
        try:
            say('  ! the v0.6.0 how-to report stopped: ' + repr(error))
            say('    It changed nothing. Run it again from the project root:')
            say('    ' + rerun_command())
        except BaseException:
            pass
    try:
        sys.stdout.flush()
    except BaseException:
        # A closed pipe (the report piped into head, say): point stdout at the null device,
        # so the interpreter's own last flush cannot turn exit 0 into 120.
        try:
            os.dup2(os.open(os.devnull, os.O_WRONLY), sys.stdout.fileno())
        except BaseException:
            os._exit(0)
    sys.exit(0)
