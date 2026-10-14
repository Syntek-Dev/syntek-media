#!/usr/bin/env python3
"""agents-outside-link.py: let an update through where .agents links outside the project.

Why (DESIGN.md D76 and D11). Copier refuses to render any template path whose destination
resolves outside the project, and it checks that BEFORE it reads _exclude (Copier 9.17.1,
copier/_main.py:810-812). Since 0.4.2 the template ships files under .agents/, so where
.agents is a symbolic link to a folder outside the project every update stops with
ForbiddenPathError, although the update gate keeps every update out of /.agents (D11).

What it does. Two stages of one unversioned migration pair, so it runs on every update: the
one pair of entries in copier.yml's _migrations that is not keyed to a release.
  hold     (_stage 'before', which Copier runs after its dirty check and before it renders
           into the project) renames that link to HELD, so the render sees no .agents.
  restore  (_stage 'after', declared before every other after-stage migration) puts it back:
           HELD is renamed to .agents where .agents is absent, or removed where the update has
           already put the identical link back. Anything else is left and reported.
The link's target is never followed, read, edited or deleted, and nothing else is touched.
Where .agents is not a link resolving outside the project, both stages do nothing. This is
D11's second, transient exception to 'media never mutates a shared file': it renames a link
aside and back, and the net change is zero.

If the update stops between the stages (a refused answer, Ctrl-C at a question), the link
stays held and the next update refuses the dirty tree. The hold stage prints the fix before
the render starts; run it from the project root:
  mv .agents.syntek-media-held .agents

By hand. 'python3 agents-outside-link.py restore' from the project root does the same as the
mv line where .agents is absent. A copy runs no migration: the copy recipe is in the bridge,
.claude/syntek-media-agents.md, and in README.md.

Python standard library only. Exit codes: 0 = always. A non-zero exit would abort the update.
"""

import os
import sys

ALIAS = '.agents'
HELD = '.agents.syntek-media-held'
BY_HAND = 'mv ' + HELD + ' ' + ALIAS


def say(line):
    print('  agents-outside-link: ' + line, flush=True)


def resolves_outside(path):
    root = os.path.realpath('.')
    return os.path.commonpath([root, os.path.realpath(path)]) != root


def hold():
    if not (os.path.islink(ALIAS) and resolves_outside(ALIAS)):
        return
    if os.path.lexists(HELD):
        say(HELD + ' already exists, so .agents was left as it is and Copier will refuse'
            ' the update. Compare the two links, keep one as .agents, commit, and update again.')
        return
    os.rename(ALIAS, HELD)  # the link only; its target is never touched
    say('held     .agents -> ' + os.readlink(HELD) + ' as ' + HELD + ' for this update.'
        ' If the update stops before it ends, restore it from the project root: ' + BY_HAND)


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
        say('left     .agents exists and is not the held link, which is still ' + HELD
            + '. Compare them and keep one as .agents by hand.')


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] in ('-h', '--help'):
        print(__doc__)
        sys.exit(0)
    try:
        {'hold': hold, 'restore': restore}[sys.argv[1] if len(sys.argv) > 1 else '']()
    except Exception as error:  # report, never abort the update
        try:
            say('could not finish (' + str(error) + '); check .agents and ' + HELD
                + '. Where .agents is absent: ' + BY_HAND)
        except Exception:
            pass
    sys.exit(0)
