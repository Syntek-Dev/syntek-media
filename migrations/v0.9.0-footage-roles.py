#!/usr/bin/env python3
"""v0.9.0-footage-roles.py: say that media's footage folder now binds its two roles and leaves a
whole pull, what that asks of the project's syntek-author, and how to find rows filed there
earlier under another role; move nothing.

What changed and why the update cannot say it (DESIGN.md D89).
  syntek-media 0.9.0 vendors syntek-author v0.11.0's data-root resolver (syntek-author D61), and
  media's map, .claude/syntek-media-dataroot.json, now binds the footage folder,
  production/src/footage, to its two roles, footage and approved-take, and marks it
  "pull": "named". Media's copy of the resolver therefore refuses an add of any other role
  there, and a whole pull leaves the folder out. The map and the resolver are template-owned,
  no author file moves and no seed's required content changes, so no migration is required
  (D11); what an owner must do, or should know, an update's merge cannot say, so this prints
  it once.

The report (every brand kind; unconditional).
  1. What media's copy now refuses, from this release, on Python 3.14 or later: add of any
     other role in the footage folder (exit 2), --force and plan --copy included, and
     --role generated under DATA_STORE repo; and that a whole pull leaves the folder out,
     while pull 'production/src/footage/*' still pulls it.
  2. syntek-author, where the project holds one: its commands run its own copy, which refuses
     only from syntek-author v0.11.0; media's floor for combined projects is unchanged.
  3. Rows filed there earlier under another role stay as they are: no command changes or
     flags them, and status and verify print no role. The command that finds them, in the
     committed storage manifest.
  4. The command that runs it again.

When it acts.
  Never: it only prints. It stays silent and exits 0 where .copier-answers.syntek-media.yml
  is absent (not a syntek-media project, or not its root).

What it never does.
  - read any file but media's own answers file, and of that only the _src_path line, for the
    command that runs it again (as v0.6.0's and v0.7.0's reports do): it never reads
    syntek-author's record or its _commit (D14), nor the storage manifest it names;
  - name a path in the lessons' folder, or look there;
  - read, write, change, move, copy or delete any file, run Git or the resolver, or read the
    data root or SYNTEK_DATA_ROOT;
  - fail the update: every path exits 0, an unexpected error included, because a non-zero
    exit aborts every migration declared after it, the family 'update' entry among them.

How it runs.
  From `copier update`, once, on the update that crosses 0.9.0 (`_migrations`, version
  v0.9.0, `_stage == 'after'`), after v0.7.0's entry and before the family 'update' block,
  through the interpreter running Copier. Standard library only; it parses and runs on
  Python 3.10, the oldest Copier 9.12.0 supports (D85). By hand: from the project root, with
  the command printed at the end of every run, which clones the release and runs it again.
  Every run prints the same report.

Exit codes: 0 = always.
"""

import os
import shlex
import sys
import textwrap

ANSWERS = '.copier-answers.syntek-media.yml'
RELEASE = 'v0.9.0'
SCRIPT = 'v0.9.0-footage-roles.py'
# The syntek-author release whose resolver media 0.9.0 vendors (D89; syntek-author D61).
AUTHOR_RELEASE = 'v0.11.0'
FOOTAGE = 'production/src/footage'
RESOLVER = 'python3 .claude/syntek-media-dataroot.py'
# The re-run command clones from the source media's own answers file names (its _src_path line
# only, as v0.6.0's and v0.7.0's reports do; D89, D14), so a fork re-runs its own copy.


def say(line=''):
    print(line, flush=True)


def para(text, blank=True):
    """One paragraph of the report, wrapped at 94 columns, after a blank line."""
    if blank:
        say()
    for line in textwrap.wrap(text, width=94, initial_indent='  ', subsequent_indent='  ',
                              break_long_words=False, break_on_hyphens=False):
        say(line)


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


def main():
    if len(sys.argv) > 1 and sys.argv[1] in ('-h', '--help'):
        say(__doc__)
        return
    if not os.path.isfile(ANSWERS):
        return

    say()
    say('▸ v0.9.0 migration (syntek-media) — the footage folder\'s roles (DESIGN.md D89); '
        'report only')

    # 1. Media's own copy: what it refuses from this release (syntek-author D61).
    para('Media\'s map, .claude/syntek-media-dataroot.json, now binds its footage folder, '
         + FOOTAGE + ', to its two roles, footage and approved-take, and keeps it out of a '
         'whole pull. From this release media\'s copy of the data-root tool, ' + RESOLVER
         + ' (syntek-author ' + AUTHOR_RELEASE + '\'s bytes, on Python 3.14 or later), '
         'refuses add of any other role there (exit 2), naming the two; --force does not get '
         'past it, plan --copy never files another role there, and under DATA_STORE repo '
         '--role generated is refused too. A pull with no pattern, or with one such as *, '
         '*.mp4 or production/src/*, leaves the folder out and says so in one line; this '
         'still pulls it:')
    say('    ' + RESOLVER + " pull '" + FOOTAGE + "/*'")

    # 2. syntek-author: unconditional, because the report never reads syntek-author's record (D14).
    para('Where this project holds syntek-author, its make files-add and make files-pull run '
         'its own copy of the tool, which refuses another role in the footage folder, and '
         'leaves it out of a whole pull, only from syntek-author ' + AUTHOR_RELEASE + ' or '
         'later. Update it to ' + AUTHOR_RELEASE + ' or later for its tools to refuse too; '
         'until then, file media\'s footage only as footage or approved-take, as media\'s '
         'rules say. Media\'s floor for combined projects is unchanged: v0.6.0, and v0.8.0 '
         'where lessons come from both templates.')

    # 3. Rows filed earlier under another role.
    para('Rows already filed in the footage folder under another role stay as they are: no '
         'command changes or flags them, and status and verify print no role. To find any, '
         'look in the storage manifest for a role other than footage or approved-take:')
    say("    git grep -n --untracked 'role = ' -- " + FOOTAGE + '/external.toml')
    para('Under DATA_STORE repo the file does not exist, and nothing was filed.', blank=False)

    say()
    say('  This script changed nothing. To run it again, from the project root:')
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
            say('  ! the v0.9.0 report stopped: ' + repr(error))
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
