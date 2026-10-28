#!/usr/bin/env python3
"""agents-outside-link.py: let an update through where .agents links outside the project.

Why. Copier refuses to render any template path whose destination resolves outside the
project, and it checks that BEFORE it reads _exclude (Copier 9.17.1, copier/_main.py:810-812).
The template ships files under .agents/, so where .agents is a symbolic link to a folder
outside the project every update stops with ForbiddenPathError, although an update never
writes under .agents. A real .agents/ folder whose skills link points outside does not block.

What it does. Two stages of one unversioned migration pair, so it runs on every update: the
one pair of entries in copier.yml's _migrations that is not keyed to a release.
  hold     (_stage 'before', which Copier runs after its dirty check and before it renders
           into the project) renames that link to HELD, so the render sees no .agents, and
           prints the hand fix below. Where HELD already stands beside .agents, it moves
           nothing and prints the fix for what it finds.
  restore  (_stage 'after', declared before every other after-stage migration) puts it back:
           HELD is renamed to .agents where .agents is absent, or removed where .agents is
           already the identical link (the update's diff puts a committed link back). Anything
           else is left as it is, and the hand fix for what stands at .agents is printed.
The link's target is never followed, read, edited or deleted, and nothing else is touched.
Where .agents is not a link resolving outside the project, both stages do nothing. The link
alone is renamed aside and back, so the net change is zero; the one file it ever removes is
its own held link, and only where an identical .agents link already stands.

If the update stops between the stages (a refused answer, Ctrl-C at a question, or Copier
failing as it cleans up after the render), the link stays held and the next update refuses the
dirty tree. Where the link is committed, a stop after the render has already put .agents back,
as the identical link Copier's diff restores, and while anything stands at .agents, 'mv HELD
.agents' would put the held link inside it: inside the folder outside the project, where .agents
is that link. The hold stage prints the fix before the render starts; run it from the project
root in a POSIX shell (Terminal on macOS and Linux, Git Bash on Windows; never PowerShell's rm),
in order:
  1. ls -ld .agents .agents.syntek-held      what stands at .agents now
     where it shows no .agents.syntek-held, nothing is held: stop here and change nothing
  2. where .agents is a link (its line shows '->'): rm .agents
     the link alone: never rm -r, never a trailing slash
     where it is a folder or a file, to a name nothing holds yet: mv .agents .agents.from-update
     no trailing slash; it holds what the update wrote: check it, and delete nothing in it that
     is yours
  3. once ls -ld .agents finds nothing: mv .agents.syntek-held .agents   (no trailing slash)
Do it before discarding the stopped update (git reset --hard, git clean -fd): git clean deletes
a held link Git does not track, which is what a git-ignored .agents link becomes when held.
Where a stage fails before anything is held, it prints that nothing is held instead of the fix.

By hand. 'python3 agents-outside-link.py restore' from the project root does what the after
stage does: it renames HELD back where .agents is absent and removes HELD where .agents is the
identical link, which is the state a stop after the render leaves. A copy runs no migration:
the copy recipe is in the bridge (.claude/syntek-*-agents.md) and in README.md.

--self-test runs both stages in temporary folders: a normal update, a stop after the render
(with .agents put back as a link, as a folder and as a file), the printed fix run step by step,
a held link committed beside .agents, a held link the owner restores by hand, and a hold that
fails before it renames anything.

Python 3.14 or later (PYTHON_MIN, below), standard library only. Copier runs it on its own
Python, which uvx may choose from those it already holds, so every update command asks for
uvx --python '>=3.14'. On an older Python it does NOT run: hold prints a framed message on
stderr that it held nothing, naming the Python it found and the rerun, restore prints it only
where a link is held, and both exit 0, so where .agents links outside the project Copier then
stops the update; a --self-test there fails, and --help still prints this text. The check runs
before any other import, and the file parses as Python 3.8, so an old Python reaches the
message instead of a SyntaxError. Exit codes: 0 = always (--self-test: 0 passed, 1 a probe
failed). A non-zero exit from a stage would abort the update.
"""

import sys

# The one place the minimum is set: the move to a newer Python changes this line and the text
# above, nothing else.
PYTHON_MIN = (3, 14)


def too_old(stage, ver):
    """The framed message printed on stderr, in place of any run, where Python is older than
    PYTHON_MIN; stage is the subcommand, ver the running Python's version."""
    need, have = '%d.%d' % tuple(PYTHON_MIN), '%d.%d' % tuple(ver[:2])
    if stage == '--self-test':
        body = ['agents-outside-link did NOT run, because this is Python %s and it needs Python %s or later.'
                % (have, need),
                'The self-test did not run.',
                'Upgrade to Python %s or later, then run the self-test again.' % need]
    else:
        body = ['agents-outside-link did NOT run, because Copier runs on Python %s here'
                ' and it needs Python %s or later.' % (have, need),
                'It held and put back nothing: where .agents is a link outside the project, Copier stops',
                'this update, and a link an earlier update held as .agents.syntek-held stays held.',
                'Upgrade to Python %s or later, then run the same update again, starting' % need,
                "uvx --python '>=%s' copier update." % need]
    rule = '  ' + '=' * 76
    return '\n'.join([rule] + ['  ' + line for line in body] + [rule]) + '\n'


if __name__ == '__main__' and sys.version_info < PYTHON_MIN and sys.argv[1:2] not in (['--help'], ['-h']):
    if sys.argv[1:2] != ['restore'] or __import__('os').path.lexists('.agents.syntek-held'):
        sys.stderr.write('\n' + too_old(sys.argv[1] if len(sys.argv) > 1 else '', sys.version_info))
        sys.stderr.flush()
    sys.exit(1 if sys.argv[1:2] == ['--self-test'] else 0)

import os  # noqa: E402  (after the version check above)

ALIAS = '.agents'
HELD = '.agents.syntek-held'
ASIDE = ALIAS + '.from-update'
CHECK = 'ls -ld ' + ALIAS + ' ' + HELD
RM_LINK = 'rm ' + ALIAS
BY_HAND = 'mv ' + HELD + ' ' + ALIAS
LINK_ALONE = '(the link alone: never rm -r, never a trailing slash)'
SHELL = "in a POSIX shell (Terminal on macOS and Linux, Git Bash on Windows; never PowerShell's rm)"
NOT_HELD = 'nothing is held as ' + HELD + ': leave .agents as it stands, and change nothing.'


def say(line):
    print('  agents-outside-link: ' + line, flush=True)


def resolves_outside(path):
    root = os.path.realpath('.')
    return os.path.commonpath([root, os.path.realpath(path)]) != root


def what(path):
    """What stands at path: 'absent', 'a link to <target>', 'a folder' or 'a file'."""
    if os.path.islink(path):
        return 'a link to ' + os.readlink(path)
    if os.path.isdir(path):
        return 'a folder'
    return 'a file' if os.path.lexists(path) else 'absent'


def aside_name():
    """The first name to move .agents aside to that nothing holds yet."""
    name, n = ASIDE, 1
    while os.path.lexists(name):
        n += 1
        name = ASIDE + '-' + str(n)
    return name


def fix_lines():
    """The hand fix for a stop between the stages, safe whatever then stands at .agents."""
    return [
        'If the update stops before it ends, put the link back from the project root, ' + SHELL
        + ', in order:',
        '  1. check what stands at .agents: ' + CHECK,
        '     if it shows no ' + HELD + ', nothing is held: stop here and change nothing',
        "  2. if .agents is a link (its line shows '->'), remove that link alone: " + RM_LINK
        + ' (never rm -r, never a trailing slash)',
        '     if .agents is a folder or a file, move it aside to a name nothing holds yet (ls -ld ' + ASIDE
        + ' finds nothing): mv ' + ALIAS + ' ' + ASIDE + ' (no trailing slash; it holds what the update'
        ' wrote: check it, and delete nothing in it that is yours)',
        '  3. once ' + 'ls -ld ' + ALIAS + ' finds nothing, put the held link back: ' + BY_HAND
        + ' (no trailing slash)',
        'Never run step 3 while .agents stands: mv would put the held link inside it, and inside'
        ' the folder outside the project where .agents is a link.',
        'Do this before you discard a stopped update (git reset --hard, git clean -fd): git clean'
        ' deletes a held link that Git does not track.',
    ]


def hold():
    if not (os.path.islink(ALIAS) and resolves_outside(ALIAS)):
        return
    if os.path.lexists(HELD):
        found_held()
        return
    os.rename(ALIAS, HELD)  # the link only; its target is never touched
    say('held     .agents -> ' + os.readlink(HELD) + ' as ' + HELD + ' for this update.')
    for line in fix_lines():
        say(line)


def found_held():
    """HELD stands beside an outside .agents link: say what to do, and move nothing."""
    stop = (' Both were left as they are, so Copier will refuse this update. From the project'
            ' root, ' + SHELL + ', check first: ' + CHECK + '.')
    if not os.path.islink(HELD):
        say('found    ' + HELD + ', which is ' + what(HELD) + ', beside .agents, a link to '
            + os.readlink(ALIAS) + '; nothing here makes it.' + stop + ' Rename ' + HELD
            + ' to a name of your own, commit, and update again.')
    elif os.readlink(HELD) == os.readlink(ALIAS):
        say('found    ' + HELD + ' beside an identical .agents link (both -> ' + os.readlink(ALIAS)
            + '): an earlier update stopped after Copier put .agents back.' + stop
            + ' Then remove the held link: rm ' + HELD + ' ' + LINK_ALONE
            + ', commit, and update again.')
    else:
        say('found    ' + HELD + ' -> ' + os.readlink(HELD) + ' beside .agents -> '
            + os.readlink(ALIAS) + '.' + stop + ' Keep the link you want as .agents: rm ' + HELD
            + ' keeps .agents; ' + RM_LINK + ', then ' + BY_HAND + ', keeps the held one (each rm'
            ' removes a link alone: never rm -r; no command takes a trailing slash). Then commit, and'
            ' update again.')


def stage_main(stage):
    """Run one stage; on an error, print the fix only where a link is held, and never abort."""
    try:
        {'hold': hold, 'restore': restore}[stage]()
    except Exception as error:  # report, never abort the update
        try:
            say('could not finish (' + str(error) + '); nothing more was moved.')
            if os.path.islink(HELD):
                for line in fix_lines():
                    say(line)
            else:
                say(NOT_HELD)
        except Exception:
            pass


def restore():
    if not os.path.islink(HELD):
        return
    if not os.path.lexists(ALIAS):
        os.rename(HELD, ALIAS)
        say('restored .agents -> ' + os.readlink(ALIAS))
    elif os.path.islink(ALIAS) and os.readlink(ALIAS) == os.readlink(HELD):
        os.unlink(HELD)  # an identical link: the update's diff already put .agents back
        say('restored .agents -> ' + os.readlink(ALIAS) + ' (the update put it back)')
    else:
        left()


def left():
    """.agents stands and is not the held link: say what to do for what stands, and move nothing."""
    held = os.readlink(HELD)
    say('left     .agents is ' + what(ALIAS) + ', not the held link, which stays as ' + HELD
        + ' -> ' + held + '. Put it back by hand from the project root, ' + SHELL + '; check first: '
        + CHECK + '.')
    if os.path.islink(ALIAS):
        say('         To keep the held link, the one you had before this update: ' + RM_LINK + ' '
            + LINK_ALONE + ', then ' + BY_HAND + ' (no trailing slash). To keep .agents as it is instead: rm '
            + HELD + '.')
    else:
        aside = aside_name()
        say('         Move it aside, then put the held link back: mv ' + ALIAS + ' ' + aside + ', then '
            + BY_HAND + ' (neither mv takes a trailing slash). ' + aside + ' holds what the update wrote:'
            ' check it, and delete nothing in it that is yours.')
    say('         Never run ' + BY_HAND + ' while .agents stands: mv would put the held link inside it.')


# ── Self-test (temporary folders only) ────────────────────────────────────────────────────


def self_test():
    import contextlib
    import io
    import shutil
    import subprocess
    import tempfile

    fails = probes = 0

    def check(label, ok):
        nonlocal fails, probes
        probes += 1
        print(('  ✓ ' if ok else '  ✗ ') + label)
        fails += 0 if ok else 1

    home = os.getcwd()
    sh = shutil.which('sh')
    print('▸ agents-outside-link --self-test\n')
    with tempfile.TemporaryDirectory(prefix='agents-outside-link-selftest-') as tmp:
        base = os.path.realpath(tmp)
        n = [0]

        def fresh(target='../outside-agents'):
            """A project whose .agents links to the owner's agent tree beside it."""
            n[0] += 1
            top = os.path.join(base, 'case-' + str(n[0]))
            outside = os.path.join(top, 'outside-agents')
            proj = os.path.join(top, 'proj')
            os.makedirs(os.path.join(outside, 'skills'))
            with open(os.path.join(outside, 'note.md'), 'w', encoding='utf-8') as f:
                f.write("The owner's own agent tree, outside the project.\n")
            os.makedirs(os.path.join(proj, '.claude', 'skills'))
            os.symlink(target, os.path.join(proj, ALIAS))
            return proj, outside

        def run(stage, proj, guarded=False):
            """One stage, called directly, or through stage_main as the update runs it (guarded)."""
            out = io.StringIO()
            os.chdir(proj)
            try:
                with contextlib.redirect_stdout(out):
                    if guarded:
                        stage_main(stage)
                    else:
                        {'hold': hold, 'restore': restore}[stage]()
            finally:
                os.chdir(home)
            return out.getvalue()

        def shell(cmd, proj):
            return subprocess.run([sh, '-c', cmd], cwd=proj, capture_output=True, text=True).returncode

        def at(proj, name):
            os.chdir(proj)
            try:
                return what(name)
            finally:
                os.chdir(home)

        def tree(path):
            """Every entry under path, with a link's target and a file's bytes."""
            found = []
            for here, dirs, files in os.walk(path):
                for name in sorted(dirs + files):
                    full = os.path.join(here, name)
                    rel = os.path.relpath(full, path)
                    if os.path.islink(full):
                        found.append((rel, 'link', os.readlink(full)))
                    elif os.path.isfile(full):
                        with open(full, 'rb') as f:
                            found.append((rel, 'file', f.read()))
                    else:
                        found.append((rel, 'folder', None))
            return sorted(found)

        def crash(put_back):
            """hold, then a stop after the render that left put_back at .agents ('link', 'folder', 'file')."""
            proj, outside = fresh()
            run('hold', proj)
            if put_back == 'link':
                os.symlink('../outside-agents', os.path.join(proj, ALIAS))   # as Copier's diff restores it
            elif put_back == 'folder':
                os.makedirs(os.path.join(proj, ALIAS, 'skills'))
                with open(os.path.join(proj, ALIAS, 'mcp_config.json'), 'w', encoding='utf-8') as f:
                    f.write('{}\n')
            elif put_back == 'file':
                with open(os.path.join(proj, ALIAS), 'w', encoding='utf-8') as f:
                    f.write('../outside-agents')                              # a link checked out as text
            return proj, outside

        # ── The normal update ──
        proj, outside = fresh()
        before = tree(outside)
        out = run('hold', proj)
        check('hold: an outside .agents link is renamed to ' + HELD + ', its target untouched',
              at(proj, ALIAS) == 'absent' and at(proj, HELD) == 'a link to ../outside-agents'
              and tree(outside) == before)
        check('hold: prints the fix in order: the check, the rm of a link alone, the move aside, then the mv',
              all(s in out for s in (CHECK, RM_LINK + ' (never rm -r', 'mv ' + ALIAS + ' ' + ASIDE, BY_HAND))
              and out.index(CHECK) < out.index(RM_LINK) < out.index(BY_HAND))
        check('hold: step 1 says to stop and change nothing where no held link stands, before any rm',
              'if it shows no ' + HELD + ', nothing is held: stop here and change nothing' in out
              and out.index('nothing is held: stop here') < out.index(RM_LINK))
        check('hold: the fix names a POSIX shell, and no mv in it takes a trailing slash',
              SHELL in out and out.count('(no trailing slash') == 2)
        out = run('restore', proj)
        check('restore: with .agents absent, the held link is renamed back',
              at(proj, ALIAS) == 'a link to ../outside-agents' and at(proj, HELD) == 'absent'
              and 'restored .agents -> ../outside-agents' in out and tree(outside) == before)
        check('restore: a second run does nothing and prints nothing', run('restore', proj) == '')
        if sh:
            check('after an update that ended, the fix stops at step 1: ls -ld finds no held link',
                  shell('ls -ld ' + HELD, proj) != 0 and at(proj, ALIAS) == 'a link to ../outside-agents')
        proj2, outside2 = fresh()
        os.unlink(os.path.join(proj2, ALIAS))
        os.makedirs(os.path.join(proj2, ALIAS))
        check('hold: a real .agents folder is left alone, silently',
              run('hold', proj2) == '' and at(proj2, ALIAS) == 'a folder' and at(proj2, HELD) == 'absent')
        proj3, _ = fresh(target='.claude')
        check('hold: an .agents link inside the project is left alone, silently',
              run('hold', proj3) == '' and at(proj3, ALIAS) == 'a link to .claude')

        # ── A stop after the render, as the update leaves it ──
        proj, outside = crash('link')
        before = tree(outside)
        out = run('restore', proj)
        check('restore by hand after a stop that left the identical link: the held link alone is removed',
              at(proj, ALIAS) == 'a link to ../outside-agents' and at(proj, HELD) == 'absent'
              and '(the update put it back)' in out and tree(outside) == before)
        if sh:
            proj, outside = crash('link')
            before = tree(outside)
            ok = shell(CHECK, proj) == 0 and shell(RM_LINK, proj) == 0 and shell('ls -ld ' + ALIAS, proj) != 0
            ok = ok and shell(BY_HAND, proj) == 0
            check('the printed fix, run step by step after a stop that left the link: .agents is the link again, '
                  'no held link, nothing written outside the project',
                  ok and at(proj, ALIAS) == 'a link to ../outside-agents' and at(proj, HELD) == 'absent'
                  and tree(outside) == before)
            proj, outside = crash('link')
            shell(BY_HAND, proj)
            check('why step 2 comes first: the bare mv while .agents is the link puts the held link inside the '
                  'folder outside the project', os.path.islink(os.path.join(outside, HELD)))
            proj, outside = crash('folder')
            before = tree(outside)
            ok = shell(CHECK, proj) == 0 and shell('mv ' + ALIAS + ' ' + ASIDE, proj) == 0
            ok = ok and shell('ls -ld ' + ALIAS, proj) != 0 and shell(BY_HAND, proj) == 0
            check('the printed fix after a stop that left a folder: the folder is kept aside whole, .agents is the '
                  'link again, nothing written outside the project',
                  ok and at(proj, ALIAS) == 'a link to ../outside-agents' and at(proj, HELD) == 'absent'
                  and os.path.isfile(os.path.join(proj, ASIDE, 'mcp_config.json')) and tree(outside) == before)
        else:
            check('the printed fix runs under sh (no sh on this machine: not run)', True)

        # ── restore finds something else at .agents: it says what to do, and moves nothing ──
        for put_back, says in (('folder', 'mv ' + ALIAS + ' ' + ASIDE + ', then ' + BY_HAND),
                               ('file', 'mv ' + ALIAS + ' ' + ASIDE + ', then ' + BY_HAND)):
            proj, outside = crash(put_back)
            before, inside = tree(outside), tree(proj)
            out = run('restore', proj)
            check('restore with .agents a ' + put_back + ': moves nothing, and prints the check, the move '
                  'aside, then the mv', tree(proj) == inside and tree(outside) == before and CHECK in out
                  and says in out and 'rm -r ' + ALIAS not in out.replace('never rm -r', ''))
        proj, outside = crash('folder')
        os.makedirs(os.path.join(proj, ASIDE))
        out = run('restore', proj)
        check('restore: where ' + ASIDE + ' is taken, the fix names a free name',
              'mv ' + ALIAS + ' ' + ASIDE + '-2, then ' + BY_HAND in out)
        proj, outside = fresh()
        run('hold', proj)
        os.symlink('../elsewhere', os.path.join(proj, ALIAS))
        inside = tree(proj)
        out = run('restore', proj)
        check('restore with .agents a different link: moves nothing, and offers to keep either, rm of a link alone',
              tree(proj) == inside and RM_LINK + ' ' + LINK_ALONE + ', then ' + BY_HAND in out
              and 'rm ' + HELD in out)

        # ── hold finds a held link beside .agents (the stopped state, committed) ──
        proj, outside = crash('link')
        inside = tree(proj)
        out = run('hold', proj)
        check('hold with the held link beside an identical .agents: moves nothing, and says to remove the held link',
              tree(proj) == inside and 'an earlier update stopped' in out and CHECK in out
              and 'rm ' + HELD + ' ' + LINK_ALONE in out and BY_HAND not in out)
        proj, outside = crash('link')
        os.unlink(os.path.join(proj, HELD))
        os.symlink('../elsewhere', os.path.join(proj, HELD))
        inside = tree(proj)
        out = run('hold', proj)
        check('hold with a different held link beside .agents: moves nothing, and offers to keep either',
              tree(proj) == inside and 'rm ' + HELD + ' keeps .agents' in out
              and RM_LINK + ', then ' + BY_HAND + ', keeps the held one' in out)
        proj, outside = fresh()
        os.makedirs(os.path.join(proj, HELD))
        inside = tree(proj)
        out = run('hold', proj)
        check('hold with a folder named ' + HELD + ': moves nothing, and says to rename it',
              tree(proj) == inside and 'to a name of your own' in out)

        # ── A stage that fails before it holds anything prints no fix ──
        proj, outside = fresh()
        os.chmod(proj, 0o555)
        try:
            if os.access(proj, os.W_OK):
                check('a hold that cannot rename prints no fix (the folder stays writable here: not run)', True)
            else:
                out = run('hold', proj, guarded=True)
                check('a hold that cannot rename: says nothing is held, prints no rm, and .agents is unchanged',
                      'could not finish' in out and NOT_HELD in out and RM_LINK not in out and BY_HAND not in out
                      and at(proj, ALIAS) == 'a link to ../outside-agents' and at(proj, HELD) == 'absent')
        finally:
            os.chmod(proj, 0o755)

        # ── An older Python: a framed message on stderr, nothing moved; read from PYTHON_MIN ──
        need = '%d.%d' % PYTHON_MIN
        older = (PYTHON_MIN[0], PYTHON_MIN[1] - 1)
        have = '%d.%d' % older
        old_h, old_t = too_old('hold', older), too_old('--self-test', older)
        framed = all(t.splitlines()[0] == t.splitlines()[-1] == '  ' + '=' * 76 and t.endswith('\n')
                     for t in (old_h, old_t))
        check('old Python: the framed message names the Python, the minimum, what it skipped and the quoted rerun',
              framed and old_h.splitlines()[1] == '  agents-outside-link did NOT run, because Copier runs on Python '
              '%s here and it needs Python %s or later.' % (have, need)
              and 'It held and put back nothing' in old_h and 'Upgrade to Python %s or later' % need in old_h
              and "uvx --python '>=%s' copier update." % need in old_h
              and old_t.splitlines()[1:3] == ['  agents-outside-link did NOT run, because this is Python %s'
                                              ' and it needs Python %s or later.' % (have, need),
                                              '  The self-test did not run.'])
        check('old Python: the docstring states the minimum PYTHON_MIN sets',
              ('Python %s or later (PYTHON_MIN, below)' % need) in ' '.join(__doc__.split())
              and ("uvx --python '>=%s'" % need) in __doc__)
        import ast
        with open(os.path.abspath(__file__), encoding='utf-8') as f:
            source = f.read()
        try:
            ast.parse(source, feature_version=(3, 8))
            parses = True
        except SyntaxError:
            parses = False
        check('old Python: the file parses as Python 3.8, so an old Python reaches the message', parses)
        check('old Python: the version check runs before any other import',
              source.index("sys.exit(1 if sys.argv[1:2] == ['--self-test'] else 0)") < source.index('\nimport os')
              and source.index('\nimport sys\n') < source.index('\nPYTHON_MIN = '))

        def aged(arg, proj):
            """This file run as __main__ with arg, on a Python faked one minor release below PYTHON_MIN."""
            return subprocess.run([sys.executable, '-I', '-c',
                                   'import runpy, sys; sys.version_info = %r; sys.argv = [%r, %r]; '
                                   'runpy.run_path(sys.argv[0], run_name="__main__")'
                                   % (older + (0, 'final', 0), os.path.abspath(__file__), arg)],
                                  cwd=proj, capture_output=True, text=True)

        proj, outside = fresh()
        inside, before = tree(proj), tree(outside)
        r = aged('hold', proj)
        ok = (r.returncode == 0 and r.stdout == '' and r.stderr == '\n' + old_h
              and tree(proj) == inside and tree(outside) == before)
        check('old Python: hold exits 0, with the framed message alone on stderr, and holds nothing'
              + ('' if ok else ' (%r)' % (r,)), ok)
        r = aged('restore', proj)
        ok = r.returncode == 0 and r.stdout == '' and r.stderr == '' and tree(proj) == inside
        check('old Python: restore with nothing held exits 0 and prints nothing'
              + ('' if ok else ' (%r)' % (r,)), ok)
        proj, outside = crash('link')
        inside = tree(proj)
        r = aged('restore', proj)
        ok = (r.returncode == 0 and r.stdout == '' and r.stderr == '\n' + too_old('restore', older)
              and tree(proj) == inside)
        check('old Python: restore with a link held exits 0, with the framed message, and moves nothing'
              + ('' if ok else ' (%r)' % (r,)), ok)
        r = aged('--self-test', proj)
        ok = r.returncode == 1 and r.stdout == '' and r.stderr == '\n' + old_t
        check('old Python: --self-test exits 1, with its framed message' + ('' if ok else ' (%r)' % (r,)), ok)
        r = aged('--help', proj)
        ok = r.returncode == 0 and 'PYTHON_MIN' in r.stdout and r.stderr == ''
        check('old Python: --help still prints the docstring' + ('' if ok else ' (%r)' % (r,)), ok)
    print()
    if fails:
        print('✗ Self-test failed: ' + str(fails) + ' of ' + str(probes) + ' probes.')
        return 1
    print('✓ Self-test passed — ' + str(probes) + ' probes.')
    return 0


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] in ('-h', '--help'):
        print(__doc__)
        sys.exit(0)
    if sys.argv[1:] == ['--self-test']:
        sys.exit(self_test())
    stage = sys.argv[1] if len(sys.argv) > 1 else ''
    if stage not in ('hold', 'restore'):
        print('usage: agents-outside-link.py hold|restore|--self-test|--help')
        sys.exit(0)
    stage_main(stage)
    sys.exit(0)
