#!/usr/bin/env python3
"""v0.7.0-report.py: say what syntek-media 0.7.0 asks of the project's syntek-author, what its
data-root map now claims, and where its three new skills are; move nothing.

What changed and why the update cannot say it (DESIGN.md D86).
  syntek-media 0.7.0 adds three skills of its own, media-research, media-tone and media-teach,
  which run beside syntek-author's research, tone and teach, where present. media-teach keeps
  media's lessons, placed each time it runs. Media's data-root map,
  .claude/syntek-media-dataroot.json, now claims the footage folder, production/src/footage,
  with two evidence roles, footage and approved-take. No author file moves and no seed's
  required content changes, so no migration is required (D11); what an owner must do, or
  should know, an update's merge cannot say, so this prints it once.

The report (every brand kind; unconditional).
  1. syntek-author, where the project holds one: update it to v0.9.1 or later, the release
     media 0.7.0 vendors (D81), now and before syntek-media from then on; lessons from both
     templates need syntek-author v0.8.0 or later (syntek-author D57). Every other combined
     project keeps the v0.6.0 floor (D84).
  2. The data root: where the project records DATA_STORE external, footage verify warns of
     each logged file not yet filed; the resolver's status, syntek-author's make files-status
     with it, lists every mirror file in the footage folder that no storage row holds and
     exits 1 until the footage is filed, so syntek-author's steps that run it report media's
     footage; a session files it with the resolver's add, on the author's word, as footage or
     approved-take only. Under DATA_STORE repo nothing is filed and footage stays out of Git.
  3. Where the three skills are.
  4. The command that runs it again.

When it acts.
  Never: it only prints. It stays silent and exits 0 where .copier-answers.syntek-media.yml
  is absent (not a syntek-media project, or not its root).

What it never does.
  - read any answers file but media's own, and of that only the _src_path line, for the
    command that runs it again (as v0.6.0's report does): it never reads syntek-author's
    record or its _commit (D14), nor this project's store;
  - name a path in the lessons' folder, or look there;
  - read, write, change, move, copy or delete any file, run Git, or read the data root or
    SYNTEK_DATA_ROOT;
  - fail the update: every path exits 0, an unexpected error included, because a non-zero
    exit aborts every migration declared after it, the family 'update' entry among them.

How it runs.
  From `copier update`, once, on the update that crosses 0.7.0 (`_migrations`, version
  v0.7.0, `_stage == 'after'`), after v0.6.0's entry and before the family 'update' block,
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
RELEASE = 'v0.7.0'
SCRIPT = 'v0.7.0-report.py'
# The release media 0.7.0 vendors from syntek-author (D81), and the floor for lessons from
# both templates (syntek-author D57).
AUTHOR_RELEASE = 'v0.9.1'
LESSON_FLOOR = 'v0.8.0'
FOOTAGE = 'production/src/footage'
RESOLVER = 'python3 .claude/syntek-media-dataroot.py'
SKILLS = (
    ('.claude/skills/media-research/', 'media\'s reading about making and publishing media, '
     'from primary sources, beside syntek-author\'s research skill, where present'),
    ('.claude/skills/media-tone/', 'a tone pass on the words a piece says or shows, run only '
     'when named or triggered, beside syntek-author\'s tone skill, where present'),
    ('.claude/skills/media-teach/', 'practice in a media craft, tool or platform, away from '
     'the real work, beside syntek-author\'s teach skill, where present'),
)
# The re-run command clones from the source media's own answers file names (its _src_path line
# only, as v0.6.0's report does; D86, D14), so a fork re-runs its own copy.


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
    say('▸ v0.7.0 migration (syntek-media) — syntek-author, the data root and three new skills '
        '(DESIGN.md D86); report only')

    # 1. syntek-author: unconditional, because the report never reads syntek-author's record (D14).
    say('  Where this project holds syntek-author, update it to')
    say('    ' + AUTHOR_RELEASE + ' or later (the release media 0.7.0 vendors; a later media '
        'release names its own)')
    para('now, from a clean, committed tree, and update it before syntek-media from then on. '
         'It must be ' + LESSON_FLOOR + ' or later where lessons come from both templates '
         '(syntek-author D57): an older one reads '
         'media\'s lessons as its own topics. Every other combined project keeps the v0.6.0 '
         'floor.', blank=False)

    # 2. The data root (D86, option a): the warning, status, and the session's add.
    para('The data root. Media\'s map, .claude/syntek-media-dataroot.json, now claims its '
         'footage folder, ' + FOOTAGE + ', with two evidence roles, footage and approved-take, '
         'so a copy filed there is never replaced. Where this project records DATA_STORE '
         'external: footage verify warns, and never fails, of each logged file not yet filed; '
         'and the resolver\'s status (syntek-author\'s make files-status with it) lists every '
         'mirror file in the footage folder that no storage row holds and exits 1 until the '
         'footage is filed, so syntek-author\'s ingest, review and build steps that '
         'run it will report media\'s footage. A session files it with the resolver\'s add, '
         'on your word, as footage or approved-take only, and tells you so:')
    say('    ' + RESOLVER + ' add <file> --role footage --label <where else it is kept>')
    say('    ' + RESOLVER + ' status')
    para('You may run the same commands yourself, as the shared chapter on the data root gives '
         'them, with media\'s two roles only. Media has no filing command of its own yet. Where '
         'the project records DATA_STORE repo, nothing is filed: footage stays on its mirror and '
         'location labels, never in Git.', blank=False)

    # 3. Where the three skills are.
    para('Three skills of media\'s own, moded for the brand kind:')
    for path, what in SKILLS:
        say('    ' + path)
        for line in textwrap.wrap(what, width=86, break_long_words=False,
                                  break_on_hyphens=False):
            say('      ' + line)

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
            say('  ! the v0.7.0 report stopped: ' + repr(error))
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
