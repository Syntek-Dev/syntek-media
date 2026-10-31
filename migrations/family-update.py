#!/usr/bin/env python3
"""family-update.py: say what an update did not deliver, and keep the shared files current.

Why. Copier delivers a template's change only to the files it owns. A file the owner changed,
a seed, a seed-once example, a copy-only path and a file the owner deleted keep their old
text, with no word from Copier. This script ends every update with a report of each such
file, and one offline git command to compare it and one to take the template's version.
It also refreshes the shared working-practice files (each template's
migrations/family-refresh.json lists them): copy-only files that every template of the
family ships byte for byte, which no update would otherwise reach.

Records, per clone, inside .git (never pushed by default, never in the work tree or index):
  refs/<template>/template  a commit whose tree is this project's full render of the version
                            now recorded (copy semantics: seeds, copy-only paths, examples).
                            Its parent is the previous render, so the chain holds every
                            version this project has been rendered at. Its message is the
                            full report, then 'commit: <sha>', 'answers: <blob>' and, where
                            that file's pairs can be read, 'answers-key: <sha256>'.
  refs/<template>/yours     the owner's HEAD when the update ran (the pre-update state).
The template's name comes from the answers file: .copier-answers.<template>.yml.

Subcommands (run from the project root; Copier runs both through _copier_python):
  update   --src S --to SHA --answers F   the last after-stage migration of every update:
           refresh, report, record.
  baseline --src S --to SHA --answers F   the last task of a copy: record the render, and
           refresh shared files that equal an earlier recorded render.
  --self-test                             prove the classes, the refresh and the commands
                                          in temporary folders (exits 1 on a failure).
  --help                                  this text.

The refresh replaces a listed file only when it is a regular file the update left untouched
(the work tree equals HEAD), whose bytes equal a render this project recorded, and which
differs from the new render. A listed file that is absent and that the owner never had (no
commit of HEAD's history, every side of every merge read, and no render this template or a sibling recorded before the update
and the project committed, held it) is added, so one the owner deleted stays deleted and one a
skipped refresh never wrote arrives with the next full run. A hook written or refreshed under
.claude/hooks/ is left mode 755. A file that cannot be written is reported and the run goes on
to the report and the record.

Restore. Where the data file lists folders under "restore" (a template's read-only guide),
every update that runs in full puts the new render's bytes back, after the refresh, the
settings entries and the MCP servers, on each regular file the new render holds under a
listed folder whose project copy differs: an edit, a merge, conflict markers or a deletion.
A shared file (one the data lists under "refresh") is put back only where it is missing,
holds a version a render here held, or holds bytes no recorded render holds while every
other template whose answers file HEAD holds has a record here of the version that file
names; otherwise it holds, or may hold, another template's newer version, which is never
downgraded while it stands unchanged. Left, and listed with the reason: another template's
version, a shared file this clone cannot judge (updating that template here, to a release
that writes update records, settles it), a file HEAD lacks whose bytes no render here holds
(it would be lost), a link or a path beyond one, and a path that is not a regular file. A
git-ignored file is never read or written. It never touches a path the new render lacks, and
never writes the index: a restored file Copier had marked as a conflict still needs git add,
which the report says. The report lists each file restored, with the commands that show what
the project had, which HEAD and refs/<name>/yours keep. A copy (baseline) restores nothing;
SYNTEK_UPDATE_REPORT=off and a render that failed restore nothing, and the next full update
does. An error in the restore is one line; the report and the record still follow.

A record the project never committed counts as not made. Where the tip record's version and
answers are not the ones HEAD's answers file names (an update discarded with git reset --hard
and git clean, or git stash -u, and run again or followed by an update to a later release),
the tip's first-parent chain of render records is walked to the nearest record that names
them, and the offers, the written blobs and the render history are read from it; the run is
recorded afresh on it (a rerun at the tip's own version and answers, only if any lane writes),
so the result is what an update from the committed version gives. Where no record names them,
the nearest record whose answers HEAD's history held is read, and where none is, no record
(the tip only where there is no HEAD, or git ignores the answers file or cannot say whether it
does). A copy's baseline reads its base the same way, and each sibling template's render
history is read likewise from its own chain, by its own answers file in HEAD alone (that file
names the sibling's version); a sibling with no record its answers file's history held is left
out. A hand rerun before the update is committed reads the same committed record, so it offers
again what the first run offered: where the files still hold the first run's writes it adds
nothing and records nothing, and an entry the owner removed from the uncommitted tree is added
back.
A run that records nothing (SYNTEK_UPDATE_REPORT=off, or a copy whose render failed; an update
at the tip's version and answers reuses the tip's render) at the tip's own version and answers,
which HEAD does not name, reads the work tree: where it is back at HEAD where the tip wrote (a
file holding a blob the tip lists as written, beyond the committed record's list, holds HEAD's
bytes again, or a full run would refresh or add a listed shared file it can write), the update
or copy was discarded, so the tip is set back to the record HEAD committed (or removed where
there is none) and committing the run never makes it count. Over the tip's writes, or the
owner's later edits to them (a hand rerun before the commit), the tip is left. Where every file
the tip wrote was rewritten since (another template's run, a formatter, a hand edit) and no
listed shared file shows the discard, the tip is left too, and what it offered is added by hand.

A record's answers match an answers file whose blob is the record's, or which holds the same
key and value pairs, read as YAML: comments, quotes, indentation, line folding, key order, a
leading '---', a byte-order mark and line endings apart, but every key, every value, the type
PyYAML (Copier's reader) gives each value and the order of every list kept (a plain value that
opens with a digit, a sign, a dot, ~, = or <, or is spelt yes, no, on, off, true, false, y or n
in any letter case, matches only the same text, and null matches null however it is written).
So a formatter that rewrites the file before it is committed still leaves the record counted.
Each record keeps a versioned sha256 of those pairs ('answers-key: '), since git may never
store the file it read. A file the reader is not sure of (an anchor, a tag, a block scalar, a
nested value, a flow list over several lines, a tab) compares by its blob alone.

Settings. Each entry the template's family-refresh.json lists (hooks, permissions deny and
ask, and top-level values such as autoCompactEnabled) that the new render's
.claude/settings.json also holds is offered to the project's settings.json once, by baseline
(a copy, also over an existing settings.json) or by update: present, it is only recorded;
absent, it is added; a rule the owner allows is reported, never added; a top-level key the
owner set to another value is kept and reported, never changed; a hook entry whose script is
not in .claude/hooks/ is reported and offered again, and one that names no script there is
never offered (it is known by its scripts); a settings.json that is a link, or lies
beyond one, is never written, and a link to a file inside the project is read, so only the
entries it lacks are named for adding by hand; a git-ignored settings.json is never read: one
line names the entries to add by hand, and none is recorded, so they are offered again. An ask
counts as allowed where an allow rule is the same rule or, for mcp__S__T, is mcp__S,
mcp__S__* or a tool-name glob after mcp__S__ that matches T: Claude Code takes the first of
deny, ask and allow that matches, however specific, so the ask would override the owner's
allow. A deny counts as allowed only by the same rule. The render record lists every entry offered
('settings: ' lines), so an entry the owner removed after it was offered stays removed. Where there is no record (a project
older than the record, a fresh clone, a copy without tasks), an entry counts as offered when
any committed version of settings.json held it (every side of every merge, no bound), and so
does a top-level value where the record lists none; a record that lists one decides alone. Such
an entry is never added; where the file is read and lacks it, one line names it, once. Entries are inserted as text into the
owner's file, in its own indentation and line endings; the file is written only when
something is added; a file that is not plain JSON is reported and left alone; if the result
would not parse to exactly the planned settings, the file is rewritten as JSON in its own key
order and indentation, and the report line says so. Never removed, reordered or weakened.

MCP servers. Each server the data file's "mcp" lists is offered once to each listed file,
with the value the new render's file holds at that file's key path, by baseline and by
update. A file the new render lacks (its client is not recorded) or the project lacks is
never created or written; one the project holds although the answers do not name its client
gets one line. A file in conflict, a link, a path beyond a link and a file that is not
regular are never written: what can be read is read, so only the servers it lacks are named
for adding by hand, and they are offered again. A git-ignored file is never read: one line
names the servers to add by hand, and the offer is recorded. A file that does not parse is
reported, and its servers are offered again. A server already there by name is only
recorded; where its value differs, one line says so, once, naming the sibling template whose
recorded render holds that value. A missing server is added unless the record lists it as
offered or any commit of HEAD's history held it there (the owner removed it; one line names it,
once). JSON is
inserted into the owner's text as settings are, and must parse to the plan; TOML gets the new
render's [mcp_servers.<server>] tables appended (its env and tools tables included) and is
written only if the result parses to the owner's file plus exactly those servers, with no
rewrite fallback. Where the file's bytes equal a recorded render and the new render's file
parses to it plus exactly the servers offered, the new render's bytes are written instead.
opencode.json and .gemini/settings.json gain a server only once they hold, in the form the
permissions script writes there, every ask rule for its tools that the new render's or the
project's .claude/settings.json holds, so an allow written there before the server existed
never covers its tools (in opencode.json an ask counts only where no later allow, of the file
or of an agent's own rules, which OpenCode applies last, outweighs it; an agent whose rules
would still outweigh it once --write appends it is named in one more line, since --write cannot
outweigh it); otherwise nothing is added or recorded there. One line then gives the permissions script's --write command for the client files whose
plan still lacks a rule (a held server's ask form that the project's settings.json asks for),
promising the next update only the servers --write completes; where the missing forms are asks
the project's settings.json does not hold (the owner allows those tools there, or it cannot be
read), one line says so instead, once, in the run whose settings lane names those asks, with the
two ways in: add the asks to settings.json and run --write, or add the server by hand. Where
this run added an mcp__ rule to settings.json, the --write line names only the client files that
lack it in their form (a file equal to the new render holds every rule), and, on a clause of its
own, any it could not read (git-ignored, beyond a link, not plain JSON or TOML), which may.

The record lists every server offered ('mcp: <path> <server> <sha256 of the value offered,
as canonical JSON>' lines, after 'mcp-offered: <count>'; no such count means no record of MCP
offers) and every blob this script wrote to settings.json or an MCP file ('written-blob:
<path> <blob>' lines, carried from record to record, the last 50 kept; ' edited' at the end
where the file held the owner's edit before the write and does not parse equal to the new
render's after it; an older record's 'settings-blob: ' lines are read as settings.json's). A later update counts a file only the script changed as
written once, never as the owner's edit; a file the script changed in this run is classified
by its blob from before the change; and a JSON or TOML file it wrote that parses equal to the
new render's, list order apart, counts as delivered.
Nothing else of the owner's is ever written: not the index or a branch, and the work tree only
through the refresh, the settings entries, the MCP servers and the restore. It never commits
and needs no network. The record holds no path of this machine (the rendered answers file,
which names the template's source, is left out of it).

The data file, migrations/family-refresh.json, is per template (each lists its own files),
but its format is shared by every template of the family:
  {"format": 1, "template": "<name in .copier-answers.<name>.yml>",
   "refresh": ["<project path>", ...],
   "restore": ["<project folder, no . or .. part>", ...],
   "settings": {"<top-level key>": <true, false, a number or a string>, ...,
                "hooks": {"<event>": [<entry exactly as settings.json holds it>, ...]},
                "permissions": {"deny": ["<rule>", ...], "ask": ["<rule>", ...]}},
   "mcp": {"servers": ["<name, [A-Za-z0-9_-]+>", ...],
           "files": {"<project path, no ..>": ["<key>", ...], ...}}}
A hook entry counts as present when an entry of the same event and matcher already runs every
hook script it names; a rule, when the same list already holds it; a top-level key, when the
owner's file holds the key at all (any value: one other than the template's is reported, once).
A record that lists no top-level value (written by an older script) leaves it to the committed
history, as where there is no record.
Every key of "settings" but hooks and permissions is a top-level value (an object, a list or
null there is ignored); a script older than this format reads only hooks and permissions, so it
ignores the top-level values and offers nothing for them.
"mcp" sits beside "settings", never inside it, and is optional. Its "files" maps each path to
the key path that holds the servers there; a path ending .toml is TOML, every other is JSON.
The values are read from the new render, never from the data file. A malformed "mcp" gives one
line and no MCP offer, and the rest of the run goes on. A script older than "mcp" ignores it.
"restore" sits beside "refresh" and is optional; a malformed one gives one line and no
restore, and the rest of the run goes on. A script older than "restore" ignores it.

SYNTEK_UPDATE_REPORT=off skips every render and prints only conflicts and deletions; it also
skips the refresh, the settings entries and the MCP servers and the restore, which the next
update without it then delivers (as it does after a render that failed). It records nothing,
but sets back a discarded record, as above. A .rej file counts as a conflict only beside a
template path and only where it is new or changed since HEAD.
The project must be its own git repository (not a folder inside one); otherwise nothing is
recorded, refreshed or added, and one line says so. A record is a commit whose message ends
with its 'commit: ' and 'answers: ' lines; any other commit at refs/<name>/template, and any
ref in a namespace of Git's own (refs/heads/template, say), is never read as one.
SYNTEK_UPDATE_COPIER names the command that renders (default: copier on PATH, then this
Python's copier module).

Python 3.14 or later (PYTHON_MIN, below), standard library and git only. Copier runs it on
its own Python, which uvx may choose from those it already holds, so every update command
asks for uvx --python '>=3.14'. On an older Python it does NOT run: it changes nothing and
prints a framed message on stderr naming everything it skipped, asking for Python 3.14 and
giving the rerun (a --self-test there fails; --help still prints this text). The check runs
before any other import, and the file parses as Python 3.8, so an old Python reaches the
message instead of a SyntaxError. Exit status: always 0, except a failing --self-test. A
non-zero exit would abort the update.
"""

import sys

# The one place the minimum is set: the move to a newer Python changes this line and the text
# above, nothing else.
PYTHON_MIN = (3, 14)


def too_old(sub, ver):
    """The framed message printed on stderr, in place of any run, where Python is older than
    PYTHON_MIN; sub is the subcommand, ver the running Python's version."""
    need, have = '%d.%d' % tuple(PYTHON_MIN), '%d.%d' % tuple(ver[:2])
    rerun = "uvx --python '>=%s' copier update" % need
    if sub == '--self-test':
        body = ['family-update did NOT run, because this is Python %s and it needs Python %s or later.' % (have, need),
                'The self-test did not run.',
                'Upgrade to Python %s or later, then run the self-test again.' % need]
    elif sub == 'baseline':
        body = ['family-update did NOT run, because Copier runs on Python %s here and it needs Python %s or later.'
                % (have, need),
                'This copy recorded nothing, refreshed no shared file and added no settings entry or MCP server.',
                'Upgrade to Python %s or later, and start every update with %s;' % (need, rerun),
                'the first one renders this version again.']
    else:
        body = ['family-update did NOT run, because Copier runs on Python %s here and it needs Python %s or later.'
                % (have, need),
                'This update printed no report, refreshed no shared file, added no settings entry or MCP server,',
                'put back no guide file and kept no record.',
                'Upgrade to Python %s or later. Then look for conflict markers and .rej files yourself,' % need,
                'commit this update, and run the same update again, starting %s.' % rerun]
    rule = '  ' + '=' * 76
    return '\n'.join([rule] + ['  ' + line for line in body] + [rule]) + '\n'


if __name__ == '__main__' and sys.version_info < PYTHON_MIN and sys.argv[1:2] not in (['--help'], ['-h']):
    sys.stderr.write('\n' + too_old(sys.argv[1] if len(sys.argv) > 1 else '', sys.version_info))
    sys.stderr.flush()
    sys.exit(1 if sys.argv[1:2] == ['--self-test'] else 0)

import copy
import fnmatch
import hashlib
import json
import os
import re
import shlex
import shutil
import subprocess
import tempfile

MAX_LIST = 25
GITCFG = ['-c', 'gc.auto=0', '-c', 'maintenance.auto=false', '-c', 'commit.gpgsign=false',
          '-c', 'core.quotepath=false']
IDENT = {'GIT_AUTHOR_NAME': 'family-update', 'GIT_AUTHOR_EMAIL': 'family-update@invalid',
         'GIT_COMMITTER_NAME': 'family-update', 'GIT_COMMITTER_EMAIL': 'family-update@invalid'}
SAFE = re.compile(r'[A-Za-z0-9._/@+-]+')
HOOK_SCRIPT = re.compile(r'\.claude/hooks/([A-Za-z0-9._-]+)')
SETTINGS = '.claude/settings.json'
REFRESH_DATA = 'migrations/family-refresh.json'
# Who relies on a top-level value, for the line that reports an owner's other value: the
# subject, its verb and the pronoun that ends the line ('... to use them').
SETTING_USERS = {'autoCompactEnabled': ('the handoff hooks', 'assume', 'them'),
                 'idleCompaction': ('the handoff hooks', 'assume', 'them'),
                 'outputStyle': ("the template's output style", 'is', 'it')}
SETTING_USERS_DEFAULT = ('the shared files', 'assume', 'them')
# An MCP rule of .claude/settings.json, as the permissions script reads one: mcp__<server>__<tool>.
MCP_RULE = re.compile(r'mcp__([A-Za-z0-9_-]+?)__([A-Za-z0-9_-]+)')
MCP_NAME = re.compile(r'[A-Za-z0-9_-]+')
MCP_PATH = re.compile(r'[A-Za-z0-9._@+-]+(?:/[A-Za-z0-9._@+-]+)*')   # and no . or .. part
# The client files whose own permission rules the permissions script writes; a server reaches
# the first two only once they hold its ask rules (an earlier broad allow there would cover it).
PERMISSION_FILES = ('opencode.json', '.codex/config.toml', '.gemini/settings.json')
ASK_FORMS = ('opencode.json', '.gemini/settings.json')
RENDER = None   # replaced by the self-test


def off():
    return os.environ.get('SYNTEK_UPDATE_REPORT', '').strip().lower() == 'off'


def say(line):
    print('  family-update: ' + line, flush=True)


def git(*args, env=None, inp=None, check=True, binary=False, cwd=None):
    e = dict(os.environ)
    e.update(env or {})
    r = subprocess.run(['git', *GITCFG, *args], input=inp, capture_output=True, env=e,
                       text=not binary, cwd=cwd)
    if check and r.returncode != 0:
        err = r.stderr if not binary else r.stderr.decode('utf-8', 'replace')
        raise RuntimeError('git ' + ' '.join(args[:2]) + ': ' + err.strip())
    return r.stdout


def verify(rev, cwd=None):
    return git('rev-parse', '-q', '--verify', rev + '^{commit}', check=False, cwd=cwd).strip()


def q(p):
    return p if SAFE.fullmatch(p) else '"' + p.replace('\\', '\\\\').replace('"', '\\"') + '"'


# ── Rendering ────────────────────────────────────────────────────────────────

def copier_cmd():
    named = os.environ.get('SYNTEK_UPDATE_COPIER', '').strip()
    if named:
        return shlex.split(named)
    if shutil.which('copier'):
        return ['copier']
    return [sys.executable, '-m', 'copier']


def copier_render(src, ref, data, out):
    """copier copy at ref into out, copy semantics, no tasks. Returns '' or the reason."""
    env = dict(os.environ)
    n = int(env.get('GIT_CONFIG_COUNT', '0') or 0)
    env.update({'GIT_CONFIG_KEY_%d' % n: 'gc.auto', 'GIT_CONFIG_VALUE_%d' % n: '0',
                'GIT_CONFIG_KEY_%d' % (n + 1): 'maintenance.auto',
                'GIT_CONFIG_VALUE_%d' % (n + 1): 'false', 'GIT_CONFIG_COUNT': str(n + 2)})
    cmd = copier_cmd() + ['copy', '--trust', '--defaults', '--quiet', '--skip-tasks',
                          '--vcs-ref', ref, '--data-file', data, src, out]
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, stdin=subprocess.DEVNULL, env=env)
    except OSError as err:
        return 'copier could not be run (%s)' % err.strerror
    if r.returncode != 0:
        lines = [l for l in (r.stderr or r.stdout).strip().splitlines() if l.strip()]
        return 'copier could not render %s (%s)' % (ref[:12], lines[-1].strip() if lines else 'exit %d' % r.returncode)
    return ''


def data_file(text, path):
    """The answers as a data file: Copier's own keys dropped, a missing client list empty."""
    lines = [l for l in text.splitlines() if not re.match(r'_[A-Za-z0-9_]*:', l)]
    if not any(re.match(r'AGENT_CLIENTS:', l) for l in lines):
        lines.append('AGENT_CLIENTS: []')
    with open(path, 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(lines) + '\n')
    return path


def render_tree(src, ref, answers_text, gitdir, tmp, name):
    """Render ref with the answers, store it in the project's objects. Returns (tree, reason)."""
    out = os.path.join(tmp, name)
    data = data_file(answers_text, os.path.join(tmp, name + '.yml'))
    reason = (RENDER or copier_render)(src, ref, data, out)
    if reason:
        return None, reason
    # The rendered answers file holds the template's absolute source path; the record keeps
    # no path of this machine (the project's own answers file is the one that counts).
    for f in os.listdir(out):
        if f.startswith('.copier-answers.') and os.path.isfile(os.path.join(out, f)):
            os.remove(os.path.join(out, f))
    idx = os.path.join(tmp, name + '.index')
    env = {'GIT_DIR': gitdir, 'GIT_WORK_TREE': out, 'GIT_INDEX_FILE': idx}
    git('add', '-A', '--force', '.', env=env, cwd=out)
    return git('write-tree', env=env, cwd=out).strip(), ''


# ── The records ──────────────────────────────────────────────────────────────

def tree_map(treeish):
    out = {}
    if not treeish:
        return out
    for item in git('ls-tree', '-r', '-z', '--full-tree', treeish, check=False).split('\0'):
        if '\t' not in item:
            continue
        meta, path = item.split('\t', 1)
        mode, typ, sha = meta.split()
        if typ == 'blob':
            out[path] = (mode, sha)
    return out


RECORD_TAIL = re.compile(r'^commit: [0-9a-f]{7,64}\nanswers: [0-9a-f]{7,64}$', re.M)
# Git's own namespaces: a branch or tag called 'template' is never a template's record.
GIT_NAMESPACES = {'heads', 'tags', 'remotes', 'notes', 'stash', 'replace', 'bisect', 'worktree',
                  'rewritten', 'prefetch', 'original', 'changes', 'pull', 'merge-requests'}


def is_record(msg):
    """A render record's message ends with its 'commit: ' and 'answers: ' lines."""
    return bool(RECORD_TAIL.search(msg or ''))


def ref_info(ref):
    """The render record at ref, or None where ref is absent or not a render record."""
    sha = verify(ref)
    if not sha:
        return None
    msg = git('log', '-1', '--format=%B', sha)
    if not is_record(msg):
        return None
    info = dict(re.findall(r'^(commit|answers|answers-key): (\S+)$', msg, re.M))
    info.update(sha=sha, tree=git('rev-parse', sha + '^{tree}').strip(),
                parent=verify(sha + '^'), msg=msg)
    return info


def record_chain(ref):
    """The commits of a chain of renders, newest first, stopping at the first that is not one."""
    out = []
    if not ref or not verify(ref):
        return out
    for chunk in git('log', '--first-parent', '--format=%H%x00%B%x1e', ref).split('\x1e'):
        chunk = chunk.lstrip('\n')
        if '\0' not in chunk:
            continue
        sha, msg = chunk.split('\0', 1)
        if not is_record(msg):
            break
        out.append(sha)
    return out


# The answers file as key and value pairs. A formatter may rewrite it before it is committed
# (lists re-indented, other quotes, comments, a '---', lines folded), so a record also matches
# an answers file that holds the same pairs. The reader takes only the YAML such a file holds
# (plain keys, each with a scalar or a list of scalars) and reads each scalar as PyYAML (Copier's
# reader) does; anything else leaves it unsure, and then only the blob compares.
YAML_ODD = re.compile('[^\n -~\xa0-\ud7ff\ue000-\ufffd\U00010000-\U0010ffff]|[\u2028\u2029\ufeff]')
YAML_KEY = re.compile(r'([A-Za-z_][A-Za-z0-9_]*):(?: +|$)')
YAML_TAIL = re.compile(r'(?: +(?:#.*)?)?')
YAML_FLOW = re.compile(r'[A-Za-z0-9_][A-Za-z0-9_./+-]*(?: [A-Za-z0-9_./+-]+)*')
YAML_STARTS = '-?:,[]{}#&*!|>\'"%@`'
YAML_WORDS = {'y', 'n', 'yes', 'no', 'on', 'off', 'true', 'false', 'null'}
YAML_ESCAPES = {'0': '\0', 'a': '\a', 'b': '\b', 't': '\t', 'n': '\n', 'v': '\v', 'f': '\f',
                'r': '\r', 'e': '\x1b', ' ': ' ', '"': '"', '/': '/', '\\': '\\', 'N': '\x85',
                '_': '\xa0', 'L': '\u2028', 'P': '\u2029'}


class Unsure(ValueError):
    """The answers file holds YAML the reader is not sure of."""


def _indent(line):
    return len(line) - len(line.lstrip(' '))


def _string(text):
    """Whether a plain scalar is a string in YAML 1.1 and 1.2 alike: it opens with no character a
    null, bool, number, date, merge key or value can open with, and is no bool or null word."""
    return bool(text) and text[0] not in '-+.0123456789~=<' and text.lower() not in YAML_WORDS


def _token(text):
    """A plain scalar as a value: ['s', text] where it is a string, else ['p', text] as written
    (any of YAML's ways to write null as ['p', 'null'])."""
    if text in ('<<', '=') or re.match(r'[0-9]{4}-', text):
        raise Unsure   # a merge key, a value key or a date: never an answer here
    if text in ('', '~', 'null', 'Null', 'NULL'):
        return ['p', 'null']
    return ['s' if _string(text) else 'p', text]


def _next_line(L, i, least):
    """After a line break in a scalar: (next line with text, its indent, empty lines between)."""
    gap, i = 0, i + 1
    while i < len(L) and not L[i].strip(' '):
        gap, i = gap + 1, i + 1
    if i == len(L) or _indent(L[i]) < least:
        raise Unsure
    return i, _indent(L[i]), gap


def _quoted(L, i, j, least):
    """The quoted scalar opening at L[i][j], folded as YAML folds it: (text, its last line, the
    column after its closing quote)."""
    q, out, line, j = L[i][j], [], L[i], j + 1
    while True:
        if j == len(line):   # a line break: spaces before it dropped, one break a space
            i, j, gap = _next_line(L, i, least)
            line = L[i]
            out.append('\n' * gap or ' ')
            continue
        c = line[j]
        if c == q and not (q == "'" and line[j + 1:j + 2] == "'"):
            return ''.join(out), i, j + 1
        if c == ' ':
            k = j
            while k < len(line) and line[k] == ' ':
                k += 1
            out.append(line[j:k] if k < len(line) else '')
            j = k
        elif q == "'" or c != '\\':
            out.append(c)
            j += 2 if c == q else 1   # '' is one ' inside single quotes
        elif j + 1 == len(line):   # an escaped line break: no space
            i, j, gap = _next_line(L, i, least)
            line = L[i]
            out.append('\n' * gap)
        else:
            e = line[j + 1]
            n = {'x': 2, 'u': 4, 'U': 8}.get(e, 0)
            h = line[j + 2:j + 2 + n]
            if n:
                if not re.fullmatch('[0-9A-Fa-f]{' + str(n) + '}', h) or 0xd800 <= int(h, 16) <= 0xdfff \
                        or int(h, 16) > 0x10ffff:
                    raise Unsure   # no character, or half of one
                out.append(chr(int(h, 16)))
            elif e in YAML_ESCAPES:
                out.append(YAML_ESCAPES[e])
            else:
                raise Unsure
            j += 2 + n


def _plain(L, i, j, least):
    """The plain scalar starting at L[i][j], folded as YAML folds it: (text, next line)."""
    out, line = [], L[i]
    while True:
        k = j
        while k < len(line) and line[k] != ' ':
            if line[k] == ':' and line[k + 1:k + 2] in ('', ' '):
                raise Unsure   # a mapping inside the value
            k += 1
        out.append(line[j:k])
        j = k
        while j < len(line) and line[j] == ' ':
            j += 1
        if j < len(line):
            if line[j] == '#':
                return ''.join(out), i + 1
            out.append(line[k:j])
            continue
        n, gap = i + 1, 0
        while n < len(L) and not L[n].strip(' '):
            n, gap = n + 1, gap + 1
        if n == len(L) or _indent(L[n]) < least or L[n].lstrip(' ')[0] == '#':
            return ''.join(out), n
        out.append('\n' * gap or ' ')   # a line that goes on is text, whatever it opens with
        i, line, j = n, L[n], _indent(L[n])


def _scalar(L, i, j, least):
    """The scalar at L[i][j], continued only on lines indented least or more: (value, next line)."""
    c = L[i][j]
    if c in '\'"':
        text, i, j = _quoted(L, i, j, least)
        if not YAML_TAIL.fullmatch(L[i], j):
            raise Unsure
        return ['s', text], i + 1
    if c in YAML_STARTS and not (c in '-?:' and L[i][j + 1:j + 2] not in ('', ' ')):
        raise Unsure
    text, i = _plain(L, i, j, least)
    return _token(text), i


def _flow(line, j):
    """The one-line list of scalars opening at line[j] ('['): (value, the column after it)."""
    items, j = [], j + 1
    while True:
        while line[j:j + 1] == ' ':
            j += 1
        if not items and line[j:j + 1] == ']':
            return ['l', items], j + 1
        if line[j:j + 1] in ('"', "'"):
            text, _, j = _quoted([line], 0, j, 1)
            items.append(['s', text])
        else:
            m = YAML_FLOW.match(line, j)
            if not m:
                raise Unsure
            items.append(_token(m.group()))
            j = m.end()
        while line[j:j + 1] == ' ':
            j += 1
        if line[j:j + 1] == ']':
            return ['l', items], j + 1
        if line[j:j + 1] != ',':
            raise Unsure
        j += 1


def _items(L, i, col):
    """The block list whose items open '- ' at column col from line i: (value, next line)."""
    items = []
    while i < len(L):
        line = L[i]
        if not line.strip(' ') or line.lstrip(' ').startswith('#'):
            i += 1
            continue
        if _indent(line) != col or line[col:col + 2] != '- ':
            break
        j = col + 2
        while line[j:j + 1] == ' ':
            j += 1
        if j == len(line) or line[j] == '#':
            raise Unsure   # an empty item, or one that opens on a later line
        value, i = _scalar(L, i, j, col + 1)
        items.append(value)
    if not items:
        raise Unsure
    return ['l', items], i


def answers_pairs(text):
    """An answers file's key and value pairs as canonical JSON, or None where the text holds YAML
    the reader is not sure of. Each key maps to ['s', text] (a string, whatever its quotes or
    folding), ['p', text] (a plain scalar whose first character or spelling YAML may read as
    another type: kept as written, but null, however written, as null), or ['l', [...]] (a list
    of those, in order, block or flow); comments, a leading '---', a byte-order mark, line
    endings and key order are left out."""
    try:
        text = text[1:] if text.startswith('\ufeff') else text
        text = text.replace('\r\n', '\n')
        if YAML_ODD.search(text):
            raise Unsure
        L, out, i, begun = text.split('\n'), {}, 0, False
        while i < len(L):
            line = L[i]
            if not line.strip(' ') or line.lstrip(' ').startswith('#'):
                i += 1
                continue
            if not begun and re.fullmatch(r'---(?: +(?:#.*)?)?', line):
                begun, i = True, i + 1
                continue
            begun = True
            m = YAML_KEY.match(line)
            if not m or not _string(m.group(1)) or m.group(1) in out:
                raise Unsure
            key, j = m.group(1), m.end()
            if j < len(line) and line[j] == '[':
                out[key], j = _flow(line, j)
                if not YAML_TAIL.fullmatch(line, j):
                    raise Unsure
                i += 1
            elif j < len(line) and line[j] != '#':
                out[key], i = _scalar(L, i, j, 1)
            else:   # the value opens on a later line, or is empty
                n = i + 1
                while n < len(L) and (not L[n].strip(' ') or L[n].lstrip(' ').startswith('#')):
                    n += 1
                col = _indent(L[n]) if n < len(L) else 0
                if n < len(L) and (L[n][col:col + 2] == '- ' or L[n][col:] == '-'):
                    out[key], i = _items(L, n, col)
                elif col:
                    out[key], i = _scalar(L, n, col, 1)
                else:
                    out[key], i = _token(''), i + 1
        if not out:
            raise Unsure
        return json.dumps(out, sort_keys=True, ensure_ascii=False, separators=(',', ':'))
    except Unsure:
        return None


_ANSWERS = {}


def answers_key(blob, raw=None):
    """The sha256, behind a format tag, of answers_pairs of an answers file, the blob's bytes
    (raw where given: a file git has not stored), read once per blob, or again where raw is
    given and the blob read as None; None where it is absent or its pairs unread."""
    if blob not in _ANSWERS or (raw is not None and _ANSWERS[blob] is None):
        if raw is None:
            raw = git('cat-file', 'blob', blob, check=False, binary=True) \
                if re.fullmatch(r'[0-9a-f]{40,64}', blob or '') else b''
        try:
            pairs = answers_pairs(raw.decode('utf-8'))
        except UnicodeDecodeError:
            pairs = None
        _ANSWERS[blob] = hashlib.sha256(('answers-pairs/1\n' + pairs).encode('utf-8')).hexdigest() if pairs else None
    return _ANSWERS[blob]


def same_answers(info, blob):
    """Whether record info was made with the answers of blob (an answers file): the same blob,
    or the same key and value pairs (the record's 'answers-key: ' line, or where an older record
    has none, its own blob's pairs)."""
    if not info or not blob:
        return False
    if info.get('answers') == blob:
        return True
    key = answers_key(blob)
    return bool(key) and (info.get('answers-key') or answers_key(info.get('answers'))) == key


def answers_held(path):
    """Every blob HEAD's history held at path (history_blobs: the new blob of each commit that
    changed it, a merge's against each parent, so a blob a merge alone made or a side branch it
    set aside is seen too, whatever the owner's log settings), or None where that cannot tell which records the project committed: there is no
    HEAD, or git ignores path (so no commit holds it), or git cannot say whether it does."""
    if not verify('HEAD') or ignored(path) is not False:
        return None
    try:
        return set(history_blobs(path))
    except RuntimeError:   # git cannot walk the history (older than 2.31, say): it cannot say
        return None


def history_blobs(path):
    """Every blob a commit of HEAD's history held at path, newest first, each once: every parent of
    every merge followed (--full-history), each merge read against each parent and the root commit
    read too, whatever the owner's log settings, with no bound on depth."""
    if not verify('HEAD'):
        return []
    out = {}
    for line in git('log', '--full-history', '--diff-merges=separate', '--root', '--no-abbrev', '--format=',
                    '--raw', 'HEAD', '--', ':(literal)' + path).splitlines():   # an error raises: never an empty history
        parts = line.split()
        if line.startswith(':') and len(parts) >= 5 and parts[3].strip('0'):
            out.setdefault(parts[3], None)
    return list(out)


def committed_record(cur, commit, answers, held):
    """The record HEAD committed, read from the first-parent chain of render records at cur (a
    ref_info record): cur itself where it names answers (the blob of HEAD's answers file) and,
    unless commit is None, commit (the version that file names); else the nearest record below
    it that names both; else the nearest record, cur included, whose answers match a blob in
    held (answers_held of the answers path); else None. A record's answers match a blob that is
    its own or holds the same key and value pairs (same_answers). A record the project never
    committed (an update or a copy discarded, or one not yet committed) counts as not made.
    Where held is None (no HEAD, or git ignores the answers file or cannot say whether it
    does), cur stands in for both last steps. Returns (record or None, True where it is not cur)."""
    if not cur:
        return cur, False

    def names(info):
        return same_answers(info, answers) and (commit is None or info.get('commit') == commit)
    if names(cur):
        return cur, False
    chain = [cur]
    for sha in record_chain(cur['sha'])[1:]:
        info = ref_info(sha)
        if names(info):
            return info, True
        chain.append(info)
    if held is None:
        return cur, False
    for i, info in enumerate(chain):
        if any(same_answers(info, b) for b in held):
            return info, i > 0
    return None, True


def history(ref, into=None):
    """Every blob each path has held in a chain of renders: {path: {blob, ...}}. Each tree
    is read whole (no rename detection), and the walk stops at a commit that is no record."""
    seen = into if into is not None else {}
    for sha in record_chain(ref):
        for p, (_, blob) in tree_map(sha).items():
            seen.setdefault(p, set()).add(blob)
    return seen


def union_history(*maps):
    """Several {path: {blob, ...}} maps as one."""
    out = {}
    for m in maps:
        for p, blobs in m.items():
            out.setdefault(p, set()).update(blobs)
    return out


def owner_held(p, yours):
    """True where the owner's committed history, or the tree at the last update, held p."""
    if p in yours:
        return True
    return bool(git('log', '-1', '--full-history', '--format=%H', 'HEAD', '--', ':(literal)' + p, check=False).strip())


def written_blobs(msg):
    """Every blob this script wrote, as a render record lists them: [(path, blob, edited)].
    edited: the file held the owner's edit before the write, so the blob is never the
    template's. An older record's 'settings-blob: ' lines are settings.json's."""
    out = []
    for line in (msg or '').splitlines():
        m = re.fullmatch(r'written-blob: (\S+) ([0-9a-f]{7,64})( edited)?', line)
        if m:
            out.append((m.group(1), m.group(2), bool(m.group(3))))
            continue
        m = re.fullmatch(r'settings-blob: ([0-9a-f]{7,64})', line)
        if m:
            out.append((SETTINGS, m.group(1), False))
    return out


def commit(tree, msg, ref=None, parent=None):
    sha = git('commit-tree', tree, *(['-p', parent] if parent else []), '-m', msg, env=IDENT).strip()
    if ref:
        git('update-ref', ref, sha)
    return sha


def beyond_link(p):
    """True where a folder on the path is a link: such a path is never read or written."""
    parts = p.split('/')[:-1]
    return any(os.path.islink('/'.join(parts[:i + 1])) for i in range(len(parts)))


def worktree(paths):
    """Blob ids of the work-tree files, clean filters applied: {path: blob} (absent: missing)."""
    out, files = {}, []
    for p in paths:
        if beyond_link(p):
            continue
        if os.path.islink(p):
            out[p] = git('hash-object', '-t', 'blob', '--stdin', inp=os.readlink(p)).strip()
        elif os.path.isfile(p):
            files.append(p)
    for i in range(0, len(files), 500):
        chunk = files[i:i + 500]
        shas = git('hash-object', '--stdin-paths', inp='\n'.join(chunk) + '\n').split()
        out.update(zip(chunk, shas))
    return out


def ignored_paths(paths):
    """The paths among paths that exist and that git ignores: never read, so never hashed,
    classified or refreshed. A path git cannot judge counts as ignored, so it is never read."""
    paths = [p for p in paths if os.path.lexists(p) and not beyond_link(p)]
    if not paths:
        return set()
    r = subprocess.run(['git', *GITCFG, 'check-ignore', '-z', '--stdin'], input='\0'.join(paths) + '\0',
                       capture_output=True, text=True)
    if r.returncode in (0, 1):
        return {p for p in r.stdout.split('\0') if p}
    return {p for p in paths if ignored(p) is not False}


def conflicts():
    unmerged = sorted({l.split('\t', 1)[1] for l in git('ls-files', '-u', '-z').split('\0') if '\t' in l})
    rej = []
    for root, dirs, files in os.walk('.', followlinks=False):
        dirs[:] = [d for d in dirs if d != '.git' and not os.path.islink(os.path.join(root, d))]
        rej += [os.path.relpath(os.path.join(root, f)).replace(os.sep, '/') for f in files if f.endswith('.rej')]
    return unmerged, sorted(rej)


def this_update_rej(rej, H, paths):
    """The .rej files this update left: beside a template path (paths: the old and new renders;
    None where neither is known, when a git-ignored one is dropped instead), and new or changed
    since HEAD, so a stale one committed earlier is not reported again."""
    if not rej:
        return []
    now = worktree(rej)
    keep = [r for r in rej if (paths is None or r[:-4] in paths)
            and not (H.get(r) and now.get(r) == H[r][1])]
    if paths is None and keep:
        ignored = set(git('check-ignore', '-z', '--stdin', inp='\0'.join(keep) + '\0', check=False).split('\0'))
        keep = [r for r in keep if r not in ignored]
    return keep


# ── The refresh ──────────────────────────────────────────────────────────────

def refresh_data(src, t):
    """The template's family-refresh.json, or None (missing, unreadable or the wrong shape)."""
    try:
        with open(os.path.join(src, REFRESH_DATA), encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        return None
    except (OSError, ValueError) as err:
        say('%s could not be read (%s): nothing refreshed.' % (REFRESH_DATA, err))
        return None
    settings = data.get('settings', {}) if isinstance(data, dict) else None
    lists = [settings.get('hooks', {}), settings.get('permissions', {})] if isinstance(settings, dict) else []
    shaped = (isinstance(data, dict) and data.get('format') == 1 and data.get('template') == t
              and isinstance(data.get('refresh', []), list)
              and all(isinstance(p, str) for p in data.get('refresh', []))
              and isinstance(settings, dict) and len(lists) == 2
              and all(isinstance(v, dict) and all(isinstance(x, list) for x in v.values()) for v in lists))
    if not shaped:
        say('%s is not format 1 for %s: nothing refreshed.' % (REFRESH_DATA, t))
        return None
    return data


def inside(p, root):
    real = os.path.realpath(p)
    return real == root or real.startswith(root + os.sep)


def is_hook(p):
    return p.startswith('.claude/hooks/') and p.endswith('.sh')


def write_blob(p, mode, sha):
    """Write a blob; a hook (or a file the render made executable) is left mode 755."""
    os.makedirs(os.path.dirname(p) or '.', exist_ok=True)
    data = git('cat-file', 'blob', sha, binary=True)
    with open(p, 'wb') as f:
        f.write(data)
    if is_hook(p) or mode == '100755':
        os.chmod(p, 0o755)
    else:
        os.chmod(p, os.stat(p).st_mode & ~0o111)


def refresh(paths, N, P, H, own, recorded, others, arrive, root, held, write=True):
    """Replace each listed shared file the owner had not changed; add each one the owner never
    had. own: every blob a render here held (the refresh test); recorded: the renders this
    template recorded before this run; held(p): the owner's committed history or the tree at
    the last update held p. A file the owner deleted therefore stays deleted, and one an update
    never wrote (a report switched off, a render that failed) arrives with the next full run.
    write=False writes nothing and returns what it would write, skipping a file, or a new file's
    folder, it cannot write.
    Returns (refreshed, added, failed), failed as 'path (reason)'."""
    done, added, failed = [], [], []
    for p in paths:
        n = N.get(p)
        if not n or n[0] not in ('100644', '100755') or beyond_link(p) or not inside(os.path.dirname(p) or '.', root):
            continue
        w, h = P.get(p), H.get(p)
        try:
            if w is not None:
                if os.path.islink(p) or not os.path.isfile(p) or w != (h[1] if h else None):
                    continue
                if w != n[1] and w in own.get(p, ()):
                    if write:
                        write_blob(p, n[0], n[1])
                    elif not os.access(p, os.W_OK):
                        continue
                    done.append(p)
            elif arrive and h is None and not os.path.lexists(p) and not recorded.get(p) \
                    and not any(o.get(p) for o in others.values()) and not held(p):
                if write:
                    write_blob(p, n[0], n[1])
                else:
                    d = os.path.dirname(p) or '.'
                    while not os.path.lexists(d):
                        d = os.path.dirname(d) or '.'
                    if not os.access(d, os.W_OK | os.X_OK):
                        continue
                added.append(p)
        except OSError as err:
            failed.append('%s (%s)' % (p, err.strerror or err))
    return done, added, failed


def refresh_notes(t, done, added, failed):
    notes = []
    if done:
        notes.append('▸ %s: refreshed %d shared file%s you had not changed: %s' % (
            t, len(done), '' if len(done) == 1 else 's', ', '.join(done)))
    if added:
        notes.append('▸ %s: added %d shared file%s new in this version: %s' % (
            t, len(added), '' if len(added) == 1 else 's', ', '.join(added)))
    if failed:
        notes.append('▸ %s: could not write %d shared file%s, left as %s: %s' % (
            t, len(failed), '' if len(failed) == 1 else 's', 'it was' if len(failed) == 1 else 'they were',
            ', '.join(failed)))
    return notes


def restore_dirs(data):
    """The project folders the data lists under "restore" (a template's read-only guide): []
    where it lists none, None where the key is malformed."""
    dirs = data.get('restore', []) if isinstance(data, dict) else []
    ok = isinstance(dirs, list) and all(
        isinstance(d, str) and MCP_PATH.fullmatch(d) and not ({'.', '..'} & set(d.split('/')))
        for d in dirs)
    return dirs if ok else None


def answers_siblings(t):
    """The other templates whose answers file HEAD holds at the project's root."""
    if not verify('HEAD'):
        return []
    names = git('ls-tree', '--name-only', 'HEAD', check=False).splitlines()
    return sorted(m.group(1) for m in (re.fullmatch(r'\.copier-answers\.(.+)\.yml', n) for n in names)
                  if m and m.group(1) != t)


def unrecorded_siblings(t):
    """The other templates whose answers file HEAD holds but whose render record here does not
    name it (no record, or one of another version or answers: a plain clone has none, since
    records travel only with git push --mirror). Their shared files' current versions are not
    known in this clone, so the restore never judges a shared file against them."""
    out = []
    for s in answers_siblings(t):
        path = '.copier-answers.%s.yml' % s
        ans = git('rev-parse', '-q', '--verify', 'HEAD:' + path, check=False).strip()
        cur = ref_info('refs/%s/template' % s) if s not in GIT_NAMESPACES else None
        base = committed_record(cur, None, ans, answers_held(path))[0] if cur else None
        if not (base and same_answers(base, ans)):
            out.append(s)
    return out


def unread_reason(unread):
    """Why a shared file is left while siblings have no record here, and what settles it."""
    one = len(unread) == 1
    return ('this clone holds no record of %s, so this may be %s: updating %s here, to a release '
            'that writes update records, settles it (or work in a clone that holds %s records, '
            'which travel only with git push --mirror)' % (
                ', '.join(unread), 'its version' if one else 'the version of one of them',
                'that template' if one else 'each of them', 'its' if one else 'their'))


def restore(dirs, shared, N, H, own, others, unread, root, write=True):
    """Put the new render's bytes back on every regular file it holds under dirs whose project
    copy differs. shared: the paths the data lists under "refresh", which another template
    may ship too; own: every blob this template's renders here held; others: each sibling's
    render history; unread: the siblings unrecorded_siblings names.
    A file whose copy holds bytes no render here held, and which HEAD lacks, is left (its bytes
    are in no commit). A shared file whose copy holds bytes this template never rendered here
    is left where a sibling's render held them, or where any sibling is unread; otherwise it
    is the owner's edit and is put back. Left, with a reason: those, a link or a path beyond
    one, a path outside the project and a path that is not a regular file. Skipped silently: a
    git-ignored path (never read; the report lists one the template changed as not compared).
    Never a path N lacks; never the index.
    Returns (restored, missing, left, failed): missing, the restored paths that were absent;
    left as (path, reason); failed as 'path (reason)'."""
    under = lambda p: any(p == d or p.startswith(d + '/') for d in dirs)
    restored, missing, left, failed, plain = [], set(), [], [], []
    for p in sorted(p for p, (mode, _) in N.items() if under(p) and mode in ('100644', '100755')):
        if beyond_link(p) or os.path.islink(p) or not inside(os.path.dirname(p) or '.', root):
            left.append((p, 'a link, or a path beyond one: the template never writes through it'))
        else:
            plain.append(p)
    ign = ignored_paths(plain) | {p for p in plain if not os.path.lexists(p) and ignored(p) is not False}
    plain = [p for p in plain if p not in ign]
    now = worktree(plain)
    for p in plain:
        n, w = N[p], now.get(p)
        if w == n[1]:
            continue
        if os.path.lexists(p) and not os.path.isfile(p):
            left.append((p, 'not a regular file'))
            continue
        if w is not None and w not in own.get(p, ()):
            sib = next((s for s, hist in sorted(others.items()) if w in hist.get(p, ())), None)
            if p in shared and sib:
                left.append((p, "it holds %s's version of a shared file: that template's update brings its own" % sib))
                continue
            if p not in H:
                left.append((p, "Git does not hold your copy: commit or move it, and the next update restores the template's"))
                continue
            if p in shared and unread:
                left.append((p, unread_reason(unread)))
                continue
        try:
            if write:
                write_blob(p, n[0], n[1])
            restored.append(p)
            if w is None:
                missing.add(p)
        except (OSError, RuntimeError) as err:
            failed.append('%s (%s)' % (p, getattr(err, 'strerror', None) or err))
    return restored, missing, left, failed


def hook_scripts(entry):
    return {m for h in (entry.get('hooks') or []) if isinstance(h, dict)
            for m in HOOK_SCRIPT.findall(str(h.get('command', '')))}


def has_hook(settings, event, entry):
    want, matcher = hook_scripts(entry), entry.get('matcher', '')
    # An entry is known by its scripts in .claude/hooks/: one that names none would match every
    # entry of its event and matcher, so it matches none, and no render ever offers it.
    if not want:
        return False
    hooks = settings.get('hooks') if isinstance(settings, dict) else None
    for e in ((hooks if isinstance(hooks, dict) else {}).get(event) or []):
        if isinstance(e, dict) and e.get('matcher', '') == matcher and want <= hook_scripts(e):
            return True
    return False


def is_scalar(v):
    return isinstance(v, (bool, int, float, str))


def same(a, b):
    """JSON equality: false is never 0, and 1 never true (a TOML date compares as its text)."""
    return json.dumps(a, sort_keys=True, default=str) == json.dumps(b, sort_keys=True, default=str)


def has_rule(settings, kind, rule):
    perms = settings.get('permissions') if isinstance(settings, dict) else None
    rules = (perms if isinstance(perms, dict) else {}).get(kind)
    return isinstance(rules, list) and rule in rules


def allow_covers(settings, item):
    """True where an allow rule of the owner's covers a deny or ask entry, which is then
    reported, never added. A deny is covered by the same rule only. An ask is also covered,
    for mcp__S__T, by mcp__S, mcp__S__* or a tool-name glob after mcp__S__ that matches T (the
    server part literal): Claude Code takes the first of deny, ask and allow that matches,
    however specific, so the ask would override that allow."""
    if has_rule(settings, 'allow', item[1]):
        return True
    m = MCP_RULE.fullmatch(item[1]) if item[0] == 'ask' else None
    if not m:
        return False
    server, tool = m.groups()
    perms = settings.get('permissions') if isinstance(settings, dict) else None
    allows = (perms if isinstance(perms, dict) else {}).get('allow')
    prefix = 'mcp__%s__' % server
    for rule in (allows if isinstance(allows, list) else []):
        if not isinstance(rule, str):
            continue
        if rule == 'mcp__' + server or (rule.startswith(prefix) and fnmatch.fnmatchcase(tool, rule[len(prefix):])):
            return True
    return False


def entry_id(item):
    """One line naming a settings entry, as the render record's 'settings:' lines hold it."""
    if item[0] == 'hook':
        _, event, entry = item
        what = ','.join(sorted(hook_scripts(entry))) or json.dumps(entry.get('hooks'), sort_keys=True)
        return 'hook %s %s %s' % (event, json.dumps(entry.get('matcher', '')), what)
    return '%s %s' % (item[0], item[1])


def read_json_blob(tree, path):
    sha = tree.get(path)
    if not sha:
        return {}
    try:
        v = json.loads(git('cat-file', 'blob', sha[1]))
        return v if isinstance(v, dict) else {}
    except ValueError:
        return {}


def committed_ids(items):
    """The ids of the items that any committed .claude/settings.json of HEAD's history held (every
    side of every merge, no bound): entries the owner had, so one missing now was removed, not
    never added."""
    found, want = set(), {entry_id(i) for i in items}
    for blob in history_blobs(SETTINGS):
        st = blob_value(blob, SETTINGS)   # a byte-order mark ignored; one that does not parse, skipped
        if isinstance(st, dict):
            found |= {entry_id(i) for i in items if present(st, i)}
        if found >= want:
            break
    return found


def present(settings, item):
    if item[0] == 'setting':
        return isinstance(settings, dict) and item[1] in settings
    return has_hook(settings, item[1], item[2]) if item[0] == 'hook' else has_rule(settings, item[0], item[1])


# ── Adding to settings.json, the owner's text kept ──────────────────────────
# The file is parsed once more with every value's span, and each entry is inserted as text
# beside its neighbours, in the indentation and line ending the file already uses. The
# result must parse to exactly the planned settings; if it does not, the file is rewritten
# as JSON in its own key order and indentation, and the report line says so.

_WS = re.compile(r'[ \t\n\r]*')
_DEC = json.JSONDecoder()


def _span(s, i):
    i = _WS.match(s, i).end()
    c = s[i:i + 1]
    if c in ('{', '['):
        node, close = {'t': c, 's': i, 'items': []}, '}' if c == '{' else ']'
        i = _WS.match(s, i + 1).end()
        if s[i:i + 1] == close:
            node['e'] = i + 1
            return node, i + 1
        while True:
            i = _WS.match(s, i).end()
            if c == '{':
                if s[i:i + 1] != '"':
                    raise ValueError('a key expected at %d' % i)
                ks = i
                key, j = json.decoder.scanstring(s, i + 1)
                j = _WS.match(s, j).end()
                if s[j:j + 1] != ':':
                    raise ValueError('a colon expected at %d' % j)
                val, i = _span(s, j + 1)
                node['items'].append((key, val, ks))
            else:
                val, i = _span(s, i)
                node['items'].append(val)
            i = _WS.match(s, i).end()
            if s[i:i + 1] == ',':
                i += 1
                continue
            if s[i:i + 1] == close:
                node['e'] = i + 1
                return node, i + 1
            raise ValueError('a comma or %s expected at %d' % (close, i))
    val, j = _DEC.raw_decode(s, i)
    return {'t': 'v', 's': i, 'e': j}, j


def _member(node, key):
    for k, val, _ in reversed(node['items']):
        if k == key:
            return val
    return None


def _style(s):
    """(indent unit or None for a one-line file, line ending)."""
    nl = '\r\n' if '\r\n' in s else '\n'
    m = re.search(r'\n([ \t]+)\S', s)
    return (m.group(1) if m else None), nl


def _line_indent(s, pos):
    start = s.rfind('\n', 0, pos) + 1
    return re.match(r'[ \t]*', s[start:]).group(0)


def _dump(value, base, unit, nl):
    if unit is None:
        return json.dumps(value, ensure_ascii=False)
    return json.dumps(value, indent=unit, ensure_ascii=False).replace('\n', nl + base)


def _insert(s, node, piece, unit, nl):
    """piece(base) → the text of one new member or element; returns the new text."""
    first = node['items'][0] if node['items'] else None
    if first is not None:
        first_at = first[2] if node['t'] == '{' else first['s']
        lead = s[node['s'] + 1:first_at]
        last = node['items'][-1][1] if node['t'] == '{' else node['items'][-1]
        if '\n' in lead:
            base = lead[lead.rfind('\n') + 1:]
            return s[:last['e']] + ',' + nl + base + piece(base, unit) + s[last['e']:]
        return s[:last['e']] + ', ' + piece('', None) + s[last['e']:]
    if unit is None:
        return s[:node['s'] + 1] + piece('', None) + s[node['e'] - 1:]
    base = _line_indent(s, node['s'])
    return s[:node['s'] + 1] + nl + base + unit + piece(base + unit, unit) + nl + base + s[node['e'] - 1:]


def _add_text(s, path, value, unit, nl):
    """Add value at path (a list of keys; the last a key to create or a list to append to)."""
    root, end = _span(s, 0)
    if s[_WS.match(s, end).end():].strip():
        raise ValueError('text after the JSON value')
    node = root
    for depth, key in enumerate(path):
        if node['t'] != '{':
            raise ValueError('not an object at ' + '.'.join(path[:depth]))
        child = _member(node, key)
        if child is None:
            rest = value
            for k in reversed(path[depth + 1:]):
                rest = {k: rest}
            return _insert(s, node, lambda base, u, k=key, v=rest: json.dumps(k, ensure_ascii=False) + ': ' + _dump(v, base, u, nl), unit, nl)
        node = child
    if node['t'] != '[':
        raise ValueError('not a list at ' + '.'.join(path))
    item = value[0]
    return _insert(s, node, lambda base, u: _dump(item, base, u, nl), unit, nl)


def _add_obj(obj, path, value):
    """A null on the path counts as absent (the text insertion then fails, and the file is
    rewritten as JSON, reported)."""
    for key in path[:-1]:
        if obj.get(key) is None:
            obj[key] = {}
        obj = obj[key]
    if obj.get(path[-1]) is None:
        obj[path[-1]] = []
    obj[path[-1]].extend(json.loads(json.dumps(value)))


def settings_merge(data, N, offered, skip):
    """Add the settings entries the template offers and this project was never offered.

    data: the template's family-refresh.json; N: the new render; offered: the ids recorded as
    offered before (None: no record, so the committed history of settings.json decides; a record
    listing no top-level value leaves those to it). An entry the history alone counts as offered
    is never added, and is named once where the file is read and lacks it.
    Returns (report lines, the ids now offered)."""
    want = data.get('settings') or {}
    new = read_json_blob(N, SETTINGS) if SETTINGS in N else None
    if not want or new is None:
        return [], set(offered or ())
    items = [('hook', event, entry) for event, entries in sorted((want.get('hooks') or {}).items())
             for entry in (entries or []) if isinstance(entry, dict) and has_hook(new, event, entry)]
    items += [(kind, rule) for kind in ('deny', 'ask') for rule in ((want.get('permissions') or {}).get(kind) or [])
              if has_rule(new, kind, rule)]
    items += [('setting', key, value) for key, value in sorted(want.items()) if key not in ('hooks', 'permissions')
              and is_scalar(value) and isinstance(new, dict) and key in new and same(new[key], value)]
    seen = set(offered) if offered is not None else committed_ids(items)
    if offered is not None and not any(x.startswith('setting ') for x in offered):
        # A record written by a script older than top-level values never lists them: the
        # committed history then decides, so a key the owner deleted is not added back. A record
        # that lists one decides alone, as it does for hook entries and rules.
        late = [i for i in items if i[0] == 'setting' and entry_id(i) not in seen]
        seen |= committed_ids(late) if late else set()
    # Counted as offered only because a committed version held it: never added, and named once
    # where the file is read and lacks it. An owner's other top-level value is still reported, once.
    held = {entry_id(i) for i in items if entry_id(i) in seen and entry_id(i) not in (offered or ())}
    history_only = {x for x in held if x.startswith('setting ')}
    pending = [i for i in items if entry_id(i) not in seen or entry_id(i) in held]
    # An early return records no history-only top-level value: the first run that can read the
    # file judges it. A held hook entry or rule is recorded without a line.
    if not pending or SETTINGS in skip or not os.path.lexists(SETTINGS):
        # Nothing new; a conflict in the file (reported there); or the owner has none.
        return [], seen - history_only
    ig = ignored(SETTINGS) if not beyond_link(SETTINGS) else False
    if ig is not False:
        # Never read (its ignore rule may guard a credential): one line names the entries to add
        # by hand, and none is recorded, so they are offered again.
        hand = [i for i in pending if entry_id(i) not in held]
        return (['▸ %s %s, so it was not read and these entries were not added (add them by hand; they are '
                 'offered again by the next update): %s' % (
                     SETTINGS, 'is ignored by git' if ig else 'could not be checked against the ignore rules',
                     '; '.join(describe(i) for i in hand))] if hand else []), seen - history_only
    why = ('lies beyond a link' if beyond_link(SETTINGS) else 'is a link' if os.path.islink(SETTINGS)
           else 'is not a regular file' if not os.path.isfile(SETTINGS) else '')
    if why:
        # Never written through a link; offered again once it is a plain file. A link whose
        # target is a file inside the project is read, never written.
        raw = None
        if why == 'is a link' and os.path.isfile(SETTINGS) and inside_project(SETTINGS):
            with open(SETTINGS, 'rb') as f:
                raw = f.read()
        return settings_unwritable('%s %s' % (SETTINGS, why), pending, raw, seen - history_only, held)
    with open(SETTINGS, 'rb') as f:
        raw = f.read()
    bom = b'\xef\xbb\xbf' if raw.startswith(b'\xef\xbb\xbf') else b''
    try:
        text = raw[len(bom):].decode('utf-8')
        cur = json.loads(text)
    except ValueError:
        cur = None
    if not isinstance(cur, dict):
        return settings_unwritable('%s is not plain JSON' % SETTINGS, pending, raw, seen - history_only, held)
    # A hook entry is added only beside its script: one the owner removed, or that could not be
    # written, is reported and offered again by the next update; one the history holds aside is
    # named by the history line instead.
    missing = [i for i in pending if i[0] == 'hook' and entry_id(i) not in held and not present(cur, i)
               and any(not os.path.isfile('.claude/hooks/' + s) for s in hook_scripts(i[2]))]
    pending = [i for i in pending if i not in missing]
    unwired = ['▸ not added to %s, because its script is not in .claude/hooks/ (it is offered again by the next update): %s' % (
        SETTINGS, '; '.join(describe(i) for i in missing))] if missing else []
    plan, added, allowed, refused, kept, gone = json.loads(text), [], [], [], [], []
    ops = []
    for i in pending:
        seen.add(entry_id(i))
        if i[0] == 'setting':
            if i[1] in plan:
                if not same(plan[i[1]], i[2]):
                    kept.append(i)
                continue
            if entry_id(i) in held:
                gone.append(i)
                continue
            plan[i[1]] = i[2]
            ops.append(([i[1]], i[2]))
            added.append(describe(i))
            continue
        if present(plan, i):
            continue
        if entry_id(i) in held:
            gone.append(i)   # before allow_covers: a removed ask is the owner's removal, not their allow
            continue
        if i[0] == 'hook':
            path, value = ['hooks', i[1]], [i[2]]
        elif allow_covers(plan, i):
            allowed.append(describe(i))
            continue
        else:
            path, value = ['permissions', i[0]], [i[1]]
        holder = plan
        ok = True
        for key in path[:-1]:
            holder = holder.get(key) if isinstance(holder, dict) else None
            ok = ok and (holder is None or isinstance(holder, dict))
        last = holder.get(path[-1]) if isinstance(holder, dict) else None
        if not ok or (last is not None and not isinstance(last, list)):
            refused.append(describe(i) + ' (its place in the file is not a list)')
            continue
        _add_obj(plan, path, value)
        ops.append((path, value))
        added.append(describe(i))
    lines = []
    if ops:
        unit, nl = _style(text)
        if unit is None and not cur:
            unit = '  '
        out, how = text, ''
        try:
            for path, value in ops:
                out = _add_text(out, path, value, unit, nl)
            if json.loads(out) != plan:
                raise ValueError('the text did not parse to the plan')
        except (ValueError, IndexError, KeyError):
            out = json.dumps(plan, indent=unit if unit is not None else 2, ensure_ascii=False).replace('\n', nl)
            out += nl if text.endswith(('\n', '\r')) else ''
            how = ' (the file was rewritten as JSON, its key order and indentation kept, because the entries could not be inserted into its text)'
        with open(SETTINGS, 'wb') as f:
            f.write(bom + out.encode('utf-8'))
        lines.append('▸ added to %s%s: %s' % (SETTINGS, how, '; '.join(added)))
    if allowed:
        lines.append('▸ not added to %s, because you allow it: %s' % (SETTINGS, '; '.join(allowed)))
    if refused:
        lines.append('▸ not added to %s: %s' % (SETTINGS, '; '.join(refused)))
    if gone:
        lines.append(history_line(SETTINGS, [held_name(i) for i in gone]))
    lines += [kept_line(i, plan[i[1]]) for i in kept]
    return lines + unwired, seen


def kept_line(item, value):
    """The one line for an owner's top-level value other than the one offered."""
    who, verb, them = SETTING_USERS.get(item[1], SETTING_USERS_DEFAULT)
    offered = json.dumps(item[2], ensure_ascii=False)
    return '▸ kept your %s in %s: %s %s %s; set it to %s in %s to use %s.' % (
        describe((item[0], item[1], value)), SETTINGS, who, verb, offered, offered, SETTINGS, them)


HELD_WHY = 'because a committed version of the file held it (you removed it)'


def history_line(path, names, sep='; '):
    """The one line for entries not added because a committed version of the file held them."""
    return '▸ not added to %s, %s: %s' % (path, HELD_WHY, sep.join(names))


def held_name(item):
    """An entry as the history line names it: a top-level value by its key alone, since the
    value the history held may not be the one offered."""
    return 'the key %s' % json.dumps(item[1]) if item[0] == 'setting' else describe(item)


def inside_project(p):
    """True where the path resolves to a place inside the project (the working folder)."""
    root = os.path.realpath('.')
    return os.path.realpath(p).startswith(root + os.sep)


def settings_unwritable(what, pending, raw, seen, held):
    """settings.json cannot be written (a link, or not plain JSON). What it holds is read where
    it can be, so the 'add by hand' line names only entries really missing, an owner's other
    top-level value is reported once instead, and an entry the history counts as offered (held)
    is never named for adding: it is recorded, and named once where the file parses and lacks it.
    raw: the file's bytes, or None where it is not read. Returns (report lines, ids offered)."""
    try:
        text = raw.decode('utf-8-sig') if raw is not None else None
    except ValueError:
        text = None
    try:
        cur = json.loads(text) if text is not None else None
    except ValueError:
        cur = None
    seen, lines, hand, gone = set(seen), [], [], []
    for i in pending:
        if isinstance(cur, dict) and present(cur, i):
            seen.add(entry_id(i))
            if i[0] == 'setting' and not same(cur[i[1]], i[2]):
                lines.append(kept_line(i, cur[i[1]]))
            continue
        if i[0] == 'setting' and not isinstance(cur, dict) and text is not None:
            # Not plain JSON (comments, say): the key's own value, where one can be found.
            m = re.search(r'"%s"\s*:\s*(true|false|null|-?[0-9][0-9.eE+-]*|"(?:[^"\\]|\\.)*")' % re.escape(i[1]), text)
            if m:
                seen.add(entry_id(i))
                try:
                    v = json.loads(m.group(1))
                except ValueError:
                    v = m.group(1)
                if not same(v, i[2]):
                    lines.append(kept_line(i, v))
                continue
        if entry_id(i) in held:
            # Counted as offered by the history: recorded, never added; named only where the file
            # parses, so whether it lacks the entry can be told.
            seen.add(entry_id(i))
            if isinstance(cur, dict):
                gone.append(i)
            continue
        hand.append(i)
    if gone:
        lines.append(history_line(SETTINGS, [held_name(i) for i in gone]))
    if hand:
        lines.append('▸ %s, so these entries were not added (add them by hand): %s' % (
            what, '; '.join(describe(i) for i in hand)))
    return lines, seen


def describe(item):
    if item[0] == 'setting':
        return '%s: %s' % (json.dumps(item[1]), json.dumps(item[2], ensure_ascii=False))
    if item[0] == 'hook':
        m = item[2].get('matcher')
        return 'the %s%s hook for %s' % (item[1], ' (%s)' % m if m else '', ', '.join(sorted(hook_scripts(item[2]))) or '?')
    return '%s %s' % item


def offered_ids(msg):
    """The ids a render record's message lists as offered, or None when it lists none."""
    if not msg or not re.search(r'^settings-offered: ', msg, re.M):
        return None
    return {l[len('settings: '):] for l in msg.splitlines() if l.startswith('settings: ')}


def record_tail(to, answers_blob, ids, blobs=(), mcp=None):
    """The record's tail: what it renders, with the answers_key of the answers file (a formatter
    may rewrite that file before it is committed, so git may never store this blob), the
    settings entries and MCP servers offered (mcp: {(path, server): hash}, or None where no
    record of MCP offers exists yet), and every blob this script wrote here (carried from
    record to record): one the owner had not edited before the write counts as the template's
    on a later update, never as the owner's."""
    kept = list(dict.fromkeys((p, b, bool(e)) for p, b, e in blobs))[-50:]
    key = answers_key(answers_blob)
    tail = '\n\ncommit: %s\nanswers: %s\n%ssettings-offered: %d\n%s' % (
        to, answers_blob, ('answers-key: %s\n' % key) if key else '', len(ids),
        ''.join('settings: %s\n' % i for i in sorted(ids)))
    if mcp is not None:
        tail += 'mcp-offered: %d\n%s' % (len(mcp), ''.join(
            'mcp: %s %s %s\n' % (p, s, h) for (p, s), h in sorted(mcp.items())))
    return tail + ''.join('written-blob: %s %s%s\n' % (p, b, ' edited' if e else '') for p, b, e in kept)


def canon(v):
    """JSON (or parsed TOML) compared by meaning: list order ignored."""
    if isinstance(v, dict):
        return {k: canon(x) for k, x in v.items()}
    if isinstance(v, list):
        return sorted((canon(x) for x in v), key=lambda x: json.dumps(x, sort_keys=True, default=str))
    return v


def settings_wrote(lines):
    """The blob of settings.json where the merge just wrote it, else None."""
    if not any(re.match(r'▸ added to ', l) for l in lines):
        return None
    return worktree([SETTINGS]).get(SETTINGS)


# ── MCP servers, added to the owner's own files ─────────────────────────────
# family-refresh.json's "mcp" names the servers and, for each file, the key path that holds
# them. Each server is offered once to each listed file that the new render holds and the
# project already has, with the value the new render holds there; nothing is ever created,
# replaced or removed. JSON is inserted as settings entries are; TOML has the new render's
# tables appended, and is written only where the result parses to exactly the plan.

def _toml():
    import tomllib   # imported here, after the version check at the top of this file
    return tomllib


def mcp_data(data):
    """((servers, {path: key path}), '') from the data file's "mcp"; (None, '') where it has
    none; (None, one line) where it cannot be read, so the lane is skipped, never the run."""
    m = data.get('mcp') if isinstance(data, dict) else None
    if m is None:
        return None, ''
    servers = m.get('servers') if isinstance(m, dict) else None
    files = m.get('files') if isinstance(m, dict) else None
    ok = (isinstance(servers, list) and isinstance(files, dict) and len(set(map(str, servers))) == len(servers)
          and all(isinstance(s, str) and MCP_NAME.fullmatch(s) for s in servers)
          and all(isinstance(p, str) and MCP_PATH.fullmatch(p) and not set(p.split('/')) & {'.', '..'}
                  and isinstance(k, list) and k and all(isinstance(x, str) and x for x in k)
                  for p, k in files.items()))
    if not ok:
        return None, '▸ the "mcp" key of %s is not in the shape this script reads, so no MCP server was offered.' % REFRESH_DATA
    return (list(servers), dict(files)), ''


def offered_mcp(msg):
    """{(path, server): hash} a render record lists as offered, or None where it lists none."""
    if not msg or not re.search(r'^mcp-offered: \d+$', msg, re.M):
        return None
    return {(p, s): h for p, s, h in re.findall(r'^mcp: (\S+) (\S+) ([0-9a-f]{64})$', msg, re.M)}


def value_hash(v):
    return hashlib.sha256(json.dumps(v, sort_keys=True, separators=(',', ':'), ensure_ascii=False,
                                     default=str).encode('utf-8')).hexdigest()


def parse_bytes(path, raw):
    """A JSON or TOML file's value (TOML where the path ends .toml), or None where it does not
    parse. A byte-order mark is ignored."""
    if raw is None:
        return None
    try:
        text = raw.decode('utf-8-sig')
        return _toml().loads(text) if path.endswith('.toml') else json.loads(text)
    except ValueError:   # a decoding, JSON or TOML error
        return None


_PARSED = {}


def blob_value(sha, path):
    """parse_bytes of a blob, read once per run."""
    if (sha, path) not in _PARSED:
        _PARSED[(sha, path)] = parse_bytes(path, git('cat-file', 'blob', sha, check=False, binary=True))
    return _PARSED[(sha, path)]


def servers_at(value, keys):
    """('ok', the object at the key path), ('missing', None) where a key on it is absent (it
    can be created), or ('bad', None) where a node on it is not an object."""
    node = value
    for k in keys:
        if not isinstance(node, dict):
            return 'bad', None
        if k not in node:
            return 'missing', None
        node = node[k]
    return ('ok', node) if isinstance(node, dict) else ('bad', None)


def ignored(p):
    """True where git ignores p (such a file is never read), False where it does not, None
    where git cannot tell."""
    r = subprocess.run(['git', *GITCFG, 'check-ignore', '-q', '--', p], capture_output=True)
    return True if r.returncode == 0 else False if r.returncode == 1 else None


def committed_servers(path, keys, servers):
    """The servers any commit of HEAD's history held at the key path of path (every side of every
    merge, no bound): ones the owner had, so one missing now was removed, never to be added back."""
    found = set()
    for blob in history_blobs(path):
        st, node = servers_at(blob_value(blob, path), keys)
        if st == 'ok':
            found |= {s for s in servers if s in node}
        if found >= set(servers):
            break
    return found


def project_settings():
    """The project's .claude/settings.json as it stands now, parsed, or None where it is absent,
    beyond a link, a link out of the project, git-ignored (never read) or not plain JSON."""
    if beyond_link(SETTINGS) or not os.path.isfile(SETTINGS) or (os.path.islink(SETTINGS) and not inside_project(SETTINGS)) \
            or ignored(SETTINGS) is not False:
        return None
    try:
        with open(SETTINGS, 'rb') as f:
            mine = json.loads(f.read().decode('utf-8-sig'))
    except (OSError, ValueError):
        return None
    return mine if isinstance(mine, dict) else None


def rule_list(settings, kind):
    perms = settings.get('permissions') if isinstance(settings, dict) else None
    rules = perms.get(kind) if isinstance(perms, dict) else None
    return [r.strip() for r in rules if isinstance(r, str)] if isinstance(rules, list) else []


def project_asks(N, mine=None):
    """The ask rules a client file must hold, in its own form, before a server is added there:
    every ask of the new render's settings.json and of the project's as it stands now (which
    the permissions script maps), so a broad allow written in that file before the server
    existed never covers a tool the update brings in, whatever the project's settings.json
    allows or has lost. mine: project_settings()."""
    return list(dict.fromkeys(rule_list(read_json_blob(N, SETTINGS), 'ask') + rule_list(mine, 'ask')))


def oc_glob(value, pattern):
    """OpenCode's wildcard match, as the permissions script reads it: '*' is any run of
    characters, '?' one, and a trailing ' *' is optional."""
    rx = re.sub(r'[.+^${}()|\[\]\\]', lambda m: '\\' + m.group(0), pattern.replace('\\', '/'))
    rx = rx.replace('*', '.*').replace('?', '.')
    if rx.endswith(' .*'):
        rx = rx[:-3] + '( .*)?'
    return re.fullmatch(rx, value.replace('\\', '/'), re.S) is not None


OC_STRICT = {'allow': 0, 'ask': 1, 'deny': 2}


def oc_holds(rules, action, effect):
    """True where an OpenCode permissions array holds effect ('ask' or 'deny') for action on every
    resource at its end, as the permissions script judges it: a rule as strict or stricter is
    there, and no later, less strict rule that matches outweighs it (the last match wins)."""
    level = OC_STRICT[effect]
    last = max((i for i, r in enumerate(rules) if isinstance(r, dict) and r.get('action') == action
                and r.get('resource') == '*' and OC_STRICT.get(r.get('effect'), -1) >= level), default=-1)
    return last >= 0 and not any(
        isinstance(r, dict) and isinstance(r.get('action'), str) and isinstance(r.get('resource'), str)
        and OC_STRICT.get(r.get('effect'), 3) < level and oc_glob(action, r['action']) and oc_glob('*', r['resource'])
        for r in rules[last + 1:])


def oc_asks(rules, action):
    """True where an OpenCode permissions array still asks (or denies) before action at its end:
    the ask is there and no later allow that matches outweighs it (the last match wins)."""
    return oc_holds(rules, action, 'ask')


def oc_agents(cur, rules, action):
    """The agents of opencode.json whose own rules, which OpenCode appends after the file's,
    let action run without its ask: an owner's earlier allow there outweighs any ask above it."""
    agents = cur.get('agents') if isinstance(cur, dict) else None
    if not isinstance(agents, dict):
        return []
    return sorted(str(n) for n, a in agents.items() if isinstance(a, dict) and isinstance(a.get('permissions'), list)
                  and not oc_asks(rules + a['permissions'], action))


def oc_rules(cur):
    rules = cur.get('permissions') if isinstance(cur, dict) else None
    return rules if isinstance(rules, list) else []


def missing_forms(path, cur, server, asks):
    """The tools of server whose ask rule, in the form the permissions script writes into
    opencode.json or .gemini/settings.json, the file does not hold yet, or (opencode.json) holds
    but a later allow, its own or an agent's, outweighs."""
    tools = [m.group(2) for m in (MCP_RULE.fullmatch(a) for a in asks) if m and m.group(1) == server]
    if path == 'opencode.json':
        rules = oc_rules(cur)
        return [t for t in tools if not oc_asks(rules, '%s_%s' % (server, t))
                or oc_agents(cur, rules, '%s_%s' % (server, t))]
    if path == '.gemini/settings.json':
        if '_' in server:   # not expressible there, so the permissions script writes nothing
            return []
        tools_key = cur.get('tools') if isinstance(cur, dict) else None
        listed = tools_key.get('confirmationRequired') if isinstance(tools_key, dict) else None
        listed = listed if isinstance(listed, list) else []
        return [t for t in tools if 'mcp_%s_%s' % (server, t) not in listed]
    return []


def oc_agents_after_write(cur, action):
    """The agents of opencode.json whose own rules would still let action run unasked once the
    file's own rules hold its ask, appended at their end as the permissions script's --write
    appends it: an agent's rules come after the file's, so --write cannot outweigh them."""
    rules = oc_rules(cur)
    if not oc_asks(rules, action):
        rules = rules + [{'action': action, 'resource': '*', 'effect': 'ask'}]
    return oc_agents(cur, rules, action)


def hold_kinds(path, cur, server, tools, mine):
    """Why each tool's ask form is missing from a client file, as [(tool, kind)]: 'agent' where
    an agent's own rule in opencode.json outweighs it, even once --write appends the form (--write
    cannot); 'write' where the project's settings.json asks before the tool, so the permissions
    script's plan holds the form and --write adds it; 'allowed' where settings.json allows the
    tool instead of asking; 'absent' where it does neither, or cannot be read (mine:
    project_settings())."""
    asks, out = rule_list(mine, 'ask'), []
    for t in tools:
        rule = 'mcp__%s__%s' % (server, t)
        if path == 'opencode.json' and oc_agents_after_write(cur, '%s_%s' % (server, t)):
            out.append((t, 'agent'))
        elif rule in asks:
            out.append((t, 'write'))
        elif isinstance(mine, dict) and allow_covers(mine, ('ask', rule)):
            out.append((t, 'allowed'))
        else:
            out.append((t, 'absent'))
    return out


def client_lacks(path, rules):
    """True where the client file at path lacks, in the form the permissions script writes there,
    one of rules ((kind, 'mcp__S__T') pairs, deny or ask): a form missing, or (opencode.json) one
    a later, less strict rule of the file outweighs. A file equal to the new render holds every
    rule. False where it holds them all, or is absent (--write writes nothing there). None where
    it exists but is not read here (git-ignored or git cannot tell, beyond a link, a link out of
    the project, not plain JSON or TOML): whether it lacks one is unknown."""
    if not os.path.isfile(path):
        return False
    if beyond_link(path) or (os.path.islink(path) and not inside_project(path)) or ignored(path) is not False:
        return None
    try:
        with open(path, 'rb') as f:
            cur = parse_bytes(path, f.read())
    except OSError:
        return None
    if not isinstance(cur, dict):
        return None
    for kind, rule in rules:
        m = MCP_RULE.fullmatch(rule)
        if not m or kind not in OC_STRICT:
            continue
        server, tool = m.groups()
        if path == 'opencode.json' and not oc_holds(oc_rules(cur), '%s_%s' % (server, tool), kind):
            return True
        if path == '.gemini/settings.json' and kind == 'ask' and missing_forms(path, cur, server, [rule]):
            return True
        if path == '.codex/config.toml' and kind == 'ask':
            servers = cur.get('mcp_servers')
            declared = servers.get(server) if isinstance(servers, dict) else None
            if isinstance(declared, dict):   # the script writes a tool's table only under a declared server
                tables = declared.get('tools')
                table = tables.get(tool) if isinstance(tables, dict) else None
                if not (isinstance(table, dict) and table.get('approval_mode') == 'prompt'):
                    return True
    return False


def settings_named(lines, added=False):
    """The (kind, mcp__ rule) pairs the settings lane's lines name: those it added (added=True),
    or every one it named, added, allowed or left to add by hand."""
    out = []
    for l in lines:
        if added and not l.startswith('▸ added to %s' % SETTINGS):
            continue
        out += [(k, r) for k, r in re.findall(r'\b(ask|deny) (mcp__[A-Za-z0-9_-]+)', l) if MCP_RULE.fullmatch(r)]
    return list(dict.fromkeys(out))


_TOML_HEADER = re.compile(r'[ \t]*(\[\[?)([^\[\]#]+)\]\]?[ \t]*(?:#.*)?')


def _toml_blocks(text, server):
    """The new render's tables of one server: [mcp_servers.<server>] and every table under
    it, each from its header to the line before the next header, trailing blank lines and
    comments dropped. Returns a list of line lists."""
    tl, out, cur = _toml(), [], None
    for line in text.splitlines():
        m = _TOML_HEADER.fullmatch(line)
        if not m:
            if cur is not None:
                cur.append(line)
            continue
        cur, path = None, []
        if m.group(1) == '[':
            try:
                node = tl.loads('[%s]\n' % m.group(2))
            except ValueError:
                node = None
            while isinstance(node, dict) and len(node) == 1:
                k = next(iter(node))
                path.append(k)
                node = node[k]
        if path[:2] == ['mcp_servers', server]:
            cur = [line]
            out.append(cur)
    for b in out:
        while len(b) > 1 and (not b[-1].strip() or b[-1].lstrip().startswith('#')):
            b.pop()
    return out


def _toml_append(text, blocks, nl):
    """The owner's text, a final line ending added where missing and one blank line, then the
    tables, in the owner's line ending."""
    body = (nl + nl).join(nl.join(b) for b in blocks) + nl
    if not text.strip():
        return text + body
    head = text if text.endswith(('\n', '\r')) else text + nl
    blank = head.splitlines()[-1].strip() == ''
    return head + ('' if blank else nl) + body


def mcp_differs(path, keys, server, value, others, t):
    """The one line for a server the owner holds with another value than the one offered."""
    cmp = 'compare: git diff %s/template -- %s' % (t, q(path))
    for name in sorted(others):
        for b in sorted(others[name].get(path, ())):
            st, node = servers_at(blob_value(b, path), keys)
            if st == 'ok' and server in node and same(node[server], value):
                return "▸ %s holds %s's version of the %s MCP server, which is kept (%s)" % (
                    path, name, json.dumps(server), cmp)
    return "▸ kept your %s MCP server in %s, which differs from the template's (%s)" % (json.dumps(server), path, cmp)


def mcp_merge(spec, N, offered, skip, rendered, others, t):
    """Offer each MCP server to each file, once. spec: (servers, {path: key path}); N: the new
    render; offered: {(path, server): hash} recorded before, or None; skip: paths in conflict;
    rendered: every blob a render here held, by path (where the file still equals one, the
    new render's bytes may be taken); others: the sibling templates' render histories.
    Returns (lines, {(path, server): hash} now offered, [(path, blob before, blob after)]
    written, {path: {server: [(tool, why), ...]}} held back for their ask rules, why as
    hold_kinds gives it)."""
    servers, files = spec
    seen, lines, writes, held, asks, mine = dict(offered or {}), [], [], {}, None, None
    for path, keys in files.items():
        n = N.get(path)
        if not n:
            if os.path.lexists(path):
                lines.append('▸ %s exists but the recorded answers do not name its client, so no MCP server was offered to it' % path)
            continue
        if not os.path.lexists(path) or path in skip:
            continue   # never created; a conflict is in the report and offered again
        st, node = servers_at(blob_value(n[1], path), keys)
        offers = {s: node[s] for s in servers if st == 'ok' and s in node}
        todo = [s for s in servers if s in offers and (path, s) not in seen]
        if not todo:
            continue
        hashes = {s: value_hash(offers[s]) for s in todo}
        hand = 'add them by hand; git show %s/template:%s shows them' % (t, q(path))
        if beyond_link(path):
            lines.append('▸ %s lies beyond a link, so these MCP servers were not added (%s): %s' % (path, hand, ', '.join(todo)))
            continue
        ig = ignored(path)
        if ig is not False:
            if ig:   # never read: the servers are named once, and recorded as offered
                seen.update({(path, s): hashes[s] for s in todo})
            lines.append('▸ %s %s, so it was not read and no MCP server was added to it (%s): %s' % (
                path, 'is ignored by git' if ig else 'could not be checked against the ignore rules', hand, ', '.join(todo)))
            continue
        why, raw = '', None
        if os.path.islink(path):
            why = 'is a link'
            if os.path.isfile(path) and inside_project(path):
                with open(path, 'rb') as f:
                    raw = f.read()
        elif not os.path.isfile(path):
            why = 'is not a regular file'
        else:
            with open(path, 'rb') as f:
                raw = f.read()
        toml = path.endswith('.toml')
        cur = parse_bytes(path, raw)
        if why or not isinstance(cur, dict):
            # Read only (a link inside the project), or not plain JSON or TOML: the servers it
            # plainly holds are recorded; the rest are named, and offered again.
            have = []
            if isinstance(cur, dict):
                cst, cnode = servers_at(cur, keys)
                have = [s for s in todo if cst == 'ok' and s in cnode]
                lines += [mcp_differs(path, keys, s, cnode[s], others, t) for s in have if not same(cnode[s], offers[s])]
            elif raw is not None:
                text = raw.decode('utf-8', 'replace')
                have = [s for s in todo if re.search(
                    r'(^|[{,\s.\[])["\']?%s["\']?\s*(:|=|\]|\.)' % re.escape(s), text, re.M)]
            seen.update({(path, s): hashes[s] for s in have})
            rest = [s for s in todo if s not in have]
            if rest:
                lines.append('▸ %s %s, so these MCP servers were not added (%s): %s' % (
                    path, why or ('is not plain TOML' if toml else 'is not plain JSON'), hand, ', '.join(rest)))
            continue
        cst, cnode = servers_at(cur, keys)
        if cst == 'bad':
            seen.update({(path, s): hashes[s] for s in todo})
            lines.append('▸ not added to %s, because its %s is not an object (%s): %s' % (
                path, '.'.join(keys), hand, ', '.join(todo)))
            continue
        present = [s for s in todo if cst == 'ok' and s in cnode]
        for s in present:
            seen[(path, s)] = hashes[s]
            if not same(cnode[s], offers[s]):
                lines.append(mcp_differs(path, keys, s, cnode[s], others, t))
        absent = [s for s in todo if s not in present]
        gone = committed_servers(path, keys, absent) if absent else set()
        seen.update({(path, s): hashes[s] for s in gone})   # removed by the owner: never re-added
        if gone:
            lines.append(history_line(path, [s for s in absent if s in gone], ', '))
        add = [s for s in absent if s not in gone]
        if add and path in ASK_FORMS:
            if asks is None:
                mine = project_settings()
                asks = project_asks(N, mine)
            lacking = [s for s in add if missing_forms(path, cur, s, asks)]
            if lacking:
                # Not recorded: offered again once the file holds them. Each tool says why its
                # form is missing, so the line after the lane promises only what --write does.
                held[path] = {s: hold_kinds(path, cur, s, missing_forms(path, cur, s, asks), mine) for s in lacking}
                # Only the agents whose rules would still outweigh the asks once --write appends
                # them, and only the servers they hold back.
                by_agent = [s for s in lacking if any(k == 'agent' for _, k in held[path][s])]
                by = sorted({n for s in by_agent for tool, k in held[path][s] if k == 'agent'
                             for n in oc_agents_after_write(cur, '%s_%s' % (s, tool))})
                if by:
                    lines.append("▸ %s: %s let%s these servers' tools run unasked after the file's own rules (OpenCode "
                                 "applies an agent's rules last, so --write cannot outweigh them): they wait until that rule "
                                 "asks, changed by hand: %s" % (path, ', '.join('agents.%s.permissions' % n for n in by),
                                                                 's' if len(by) == 1 else '', ', '.join(by_agent)))
                add = [s for s in add if s not in lacking]
        if not add:
            continue
        plan = copy.deepcopy(cur)
        holder = plan
        for k in keys:
            holder = holder.setdefault(k, {})
        for s in add:
            holder[s] = copy.deepcopy(offers[s])
        before = worktree([path]).get(path)
        bom = b'\xef\xbb\xbf' if raw.startswith(b'\xef\xbb\xbf') else b''
        text = raw[len(bom):].decode('utf-8')
        how = ''
        if before in rendered.get(path, ()) and same(blob_value(n[1], path), plan):
            out = git('cat-file', 'blob', n[1], binary=True)   # unedited: the new render's own bytes
        elif toml:
            nl = '\r\n' if '\r\n' in text else '\n'
            new_text = git('cat-file', 'blob', n[1], binary=True).decode('utf-8-sig')
            blocks = [b for s in add for b in _toml_blocks(new_text, s)]
            result = _toml_append(text, blocks, nl)
            if parse_bytes(path, result.encode('utf-8')) is None or not same(_toml().loads(result), plan):
                seen.update({(path, s): hashes[s] for s in add})
                lines.append('▸ not added to %s, because appending their tables would not leave exactly your file '
                             'plus the servers (an inline or dotted mcp_servers, say; %s): %s' % (path, hand, ', '.join(add)))
                continue
            out = bom + result.encode('utf-8')
        else:
            unit, nl = _style(text)
            if unit is None and not cur:
                unit = '  '
            result = text
            try:
                for s in add:
                    result = _add_text(result, keys + [s], offers[s], unit, nl)
                if json.loads(result) != plan:
                    raise ValueError('the text did not parse to the plan')
            except (ValueError, IndexError, KeyError):
                result = json.dumps(plan, indent=unit if unit is not None else 2, ensure_ascii=False).replace('\n', nl)
                result += nl if text.endswith(('\n', '\r')) else ''
                how = ' (the file was rewritten as JSON, its key order and indentation kept, because the servers could not be inserted into its text)'
            out = bom + result.encode('utf-8')
        try:
            with open(path, 'wb') as f:
                f.write(out)
        except OSError as err:
            lines.append('▸ could not write %s (%s), so these MCP servers were not added: %s' % (
                path, err.strerror or err, ', '.join(add)))
            continue
        writes.append((path, before, worktree([path]).get(path)))
        seen.update({(path, s): hashes[s] for s in add})
        lines.append('▸ added %d MCP server%s to %s%s: %s' % (len(add), '' if len(add) == 1 else 's', path, how, ', '.join(add)))
    return lines, seen, writes, held


def mcp_lane(data, N, offered, skip, rendered, others, t, settings_lines):
    """The MCP lane of one run, with its one line for the permissions script. Returns (lines,
    the offers to record, the writes); without an "mcp" key, the offers recorded before."""
    spec, bad = mcp_data(data)
    if spec is None:
        return ([bad] if bad else []), offered, []
    lines, seen, writes, held = mcp_merge(spec, N, offered, skip, rendered, others, t)
    added = settings_named(settings_lines, added=True)
    named = set(settings_named(settings_lines))
    join = lambda xs: ' and '.join([', '.join(xs[:-1]), xs[-1]]) if len(xs) > 1 else xs[0]
    cmd = 'python3 .claude/%s-permissions.py --write' % t
    # The --write line names only the client files whose plan still lacks a rule: a held server's
    # form that the project's settings.json asks for, or an MCP rule this run added there.
    lacks = {p: client_lacks(p, added) for p in PERMISSION_FILES if p not in skip} if added else {}
    files = [p for p in PERMISSION_FILES if p not in skip and (
        any(k == 'write' for kinds in held.get(p, {}).values() for _, k in kinds) or lacks.get(p))]
    # A client file this run could not read may lack the added rule: it is named on its own clause.
    unread = [p for p in PERMISSION_FILES if p not in files and p in lacks and lacks[p] is None]
    # Only a server whose every missing form --write adds is promised to the next update.
    soon = [(p, [s for s, kinds in held[p].items() if all(k == 'write' for _, k in kinds)]) for p in held]
    soon = [(p, ss) for p, ss in soon if ss]
    if files or unread:
        into = [join(files)] if files else []
        if unread:
            one = len(unread) == 1
            into.append('%s where %s them (%s not read here)' % (
                join(unread), 'it lacks' if one else 'they lack', 'it was' if one else 'they were'))
        line = '▸ to carry the %s into %s, run: %s' % (
            'new ask and deny rules' if added else 'ask rules these MCP servers wait for', ' and into '.join(into), cmd)
        if soon:
            line += ('; the next update then adds the MCP servers to each file that holds their ask rules '
                     '(held back now: %s)') % '; '.join('%s %s' % (p, ', '.join(ss)) for p, ss in soon)
        lines.append(line)
    # A server whose forms wait for asks the project's settings.json does not hold (the owner
    # allows those tools there, or it cannot be read) never gains them by --write: that is said
    # instead, once, in the run whose settings lane names those asks, with the two ways in.
    wait = [(p, s, ['mcp__%s__%s' % (s, tool) for tool, k in kinds if k in ('allowed', 'absent')],
             {k for _, k in kinds}) for p in held for s, kinds in held[p].items()]
    wait = [w for w in wait if w[2]]
    asks = list(dict.fromkeys(a for w in wait for a in w[2]))
    if any(('ask', a) in named for a in asks):
        kinds = set().union(*(w[3] for w in wait))
        where = list(dict.fromkeys(w[0] for w in wait))
        lines.append(
            "▸ these MCP servers wait for ask rules --write cannot carry, because %s does not ask before "
            "their tools%s: %s. To add them, either add those asks to %s (%s) and run %s, after which the next "
            "update adds them; or add the servers to those files by hand (%s)." % (
                SETTINGS, ' (you allow them there)' if 'absent' not in kinds else
                ' (you allow some of them there)' if 'allowed' in kinds else '',
                '; '.join('%s %s' % (p, ', '.join(dict.fromkeys(w[1] for w in wait if w[0] == p))) for p in where),
                SETTINGS, ', '.join(asks), cmd, '; '.join('git show %s/template:%s' % (t, q(p)) for p in where)))
    return lines, seen, writes


def delivered(N, path):
    """True where the project's file, parsed (JSON, or TOML for .toml), equals the new
    render's, list order apart."""
    if path not in N or os.path.islink(path) or not os.path.isfile(path) or beyond_link(path):
        return False
    try:
        with open(path, 'rb') as f:
            mine = parse_bytes(path, f.read())
    except OSError:
        return False
    theirs = blob_value(N[path][1], path)
    return mine is not None and theirs is not None and same(canon(mine), canon(theirs))


# ── The report ───────────────────────────────────────────────────────────────

def classify(N, O, P, H, own, others, skip, ign=()):
    g = {k: [] for k in ('edit', 'sibling', 'once', 'new_here', 'not_restored', 'new_absent', 'lost', 'ignored')}
    counts = {'changed': 0, 'delivered': 0, 'merged': 0}
    for p in sorted(set(N) | set(O)):
        if os.path.basename(p).startswith('.copier-answers.') or p.endswith('.rej'):
            continue
        n, o, w, h = N.get(p), O.get(p), P.get(p), H.get(p)
        if (n and o and n[1] == o[1]) or (not n and not o):
            continue
        counts['changed'] += 1
        if p in ign:
            g['ignored'].append(p)
            continue
        if p in skip:
            continue
        if n:
            if w == n[1]:
                counts['delivered'] += 1
            elif w is None:
                if h is None:
                    g['not_restored' if o else 'new_absent'].append(p)
            elif h and w != h[1]:
                counts['merged'] += 1
            elif o is None:
                sib = next((name for name, hist in sorted(others.items()) if w in hist.get(p, ())), None)
                if sib:
                    g['sibling'].append((p, sib))
                else:
                    g['new_here'].append(p)
            elif w == o[1] or w in own.get(p, ()):
                g['once'].append(p)
            else:
                sib = next((name for name, hist in sorted(others.items()) if w in hist.get(p, ())), None)
                if sib:
                    g['sibling'].append((p, sib))
                else:
                    g['edit'].append(p)
        elif w is None and h and h[1] != o[1]:
            g['lost'].append(p)
        else:
            counts['delivered'] += 1
    return g, counts


def section(lines, cap, title, entries, cmds):
    if not entries:
        return
    lines += ['', '  %s (%d):' % (title, len(entries))]
    for e in entries[:cap]:
        p = e[0] if isinstance(e, tuple) else e
        lines.append('    ' + p)
        lines += ['        ' + c for c in cmds(p)]
    if len(entries) > cap:
        lines.append('    … and %d more (this report again: see the last line)' % (len(entries) - cap))


def body(t, g, unmerged, rej, deleted_unknown, cap):
    T, Y = t + '/template', t + '/yours'
    L = []
    section(L, cap, 'CONFLICT: both versions are in the file between <<<<<<< and >>>>>>>; resolve it, then git add',
            unmerged, lambda p: ['compare: git diff %s %s -- %s' % (T, Y, q(p)),
                                 'take:    git checkout %s -- %s' % (T, q(p))])
    rej_here = [r[:-4] for r in rej if os.path.lexists(r[:-4])]
    rej_gone = [r[:-4] for r in rej if not os.path.lexists(r[:-4])]
    ro = lambda p: any(p == d or p.startswith(d + '/') for d in g.get('restore_dirs', []))
    section(L, cap, "REJECTED HUNKS: the file holds the template's version; your lines are in <file>.rej",
            rej_here, lambda p: ['compare: git diff %s %s -- %s' % (T, Y, q(p))] + (
                ['then:    rm -- %s' % q(p + '.rej')]
                if ro(p) else ['yours:   git restore --source=%s -- %s' % (Y, q(p))]))
    restore = lambda p: ['see:     git show %s:%s' % (Y, q(p)), 'restore: git restore --source=%s -- %s' % (Y, q(p))]
    section(L, cap, 'DELETED by this update although you had changed them (retired by the template, or by an answer that no longer ships them)',
            g['lost'] + rej_gone, restore)
    section(L, cap, 'DELETED by this update (retired by the template, or by an option you turned off)',
            deleted_unknown, restore)
    where = g.get('restore_where', '')
    held, missing, marks = g.get('restore_held', set()), g.get('restore_missing', set()), g.get('restore_marks', set())

    def was(p):
        if p in missing:
            out = ['was:     missing before this update']
        elif p in held:
            out = ['compare: git diff %s %s -- %s' % (T, Y, q(p)), 'yours:   git show %s:%s' % (Y, q(p))]
        else:
            out = ['was:     not in Git, holding a version a template rendered here']
        if p in marks:
            out.append('then:    git add -- %s' % q(p))
        return out
    section(L, cap, "RESTORED to the template's text, because %s is read-only (what you had is in Git)" % where,
            g.get('restored', []), was)
    left = dict(g.get('restore_left', []))
    section(L, cap, 'LEFT AS IT IS in %s, which is read-only' % where, sorted(left),
            lambda p: ['why:     %s' % left[p], 'see:     git show %s:%s' % (T, q(p))])
    take = lambda p: ['compare: git diff %s -- %s' % (T, q(p)), 'take:    git restore --source=%s -- %s' % (T, q(p))]
    section(L, cap, 'NOT UPDATED because you had changed them', g['edit'], take)
    sibs = {}
    for p, s in g['sibling']:
        sibs.setdefault(s, []).append(p)
    for s in sorted(sibs):
        section(L, cap, "NOT UPDATED because the file holds %s's version (a shared file)" % s, sibs[s], take)
    section(L, cap, 'NOT UPDATED because files of this kind are written once: seeds, examples, copy-only',
            g['once'], take)
    section(L, cap, 'NOT UPDATED because it is new in this version and you already had a file there',
            g['new_here'], take)
    show = lambda p: ['see:     git show %s:%s' % (T, q(p)), 'take:    git restore --source=%s -- %s' % (T, q(p))]
    section(L, cap, 'NOT RESTORED because you had deleted them', g['not_restored'], show)
    section(L, cap, 'NOT ADDED: new in this version, and an update never adds files of this kind',
            g['new_absent'], show)
    section(L, cap, 'NOT COMPARED because git ignores them, so they were not read',
            g.get('ignored', []), lambda p: ['see:     git show %s:%s' % (T, q(p))])
    return L


def build_report(t, frm, to, g, counts, unmerged, rej, notes, extra, cap, full):
    """notes: the refresh lines; extra: (deleted_unknown, headline_override)."""
    deleted_unknown, override = extra
    lines = list(notes)
    head = '▸ %s update report, %s → %s' % (t, frm, to)
    B = body(t, g, unmerged, rej, deleted_unknown, cap)
    if override:
        lines.append(head + ': ' + override)
        lines += B
        return lines + (['', '  These commands work offline until the next update.'] if B else [])
    refreshed, added = counts.get('refreshed', 0), counts.get('added', 0)
    kept = sum(len(g[k]) for k in ('edit', 'sibling', 'once', 'new_here', 'not_restored', 'new_absent'))
    unread = len(g.get('ignored', []))
    if counts['changed'] == 0 and not B:
        return lines + [head + ': the template did not change.']
    if not B:
        return lines + [head + ': every change was delivered (%d file%s).' % (
            counts['changed'], '' if counts['changed'] == 1 else 's')]
    parts = [('delivered', counts['delivered']), ('merged with your edits', counts['merged']),
             ('refreshed', refreshed), ('added', added), ('restored', counts.get('restored', 0)),
             ('left in a read-only folder', counts.get('left', 0)), ('kept back', kept),
             ('conflict' + ('' if len(unmerged) + len(rej) == 1 else 's'), len(unmerged) + len(rej)),
             ('deleted although you had changed them', len(g['lost'])),
             ('not compared because git ignores them', unread)]
    lines.append(head)
    if counts['changed']:
        lines.append('  The template changed %d file%s here: %s.' % (
            counts['changed'], '' if counts['changed'] == 1 else 's',
            ', '.join('%d %s' % (n, w) for w, n in parts if n)))
    else:
        lines.append('  The template changed no file here.')
    restored = len(g.get('restored', []))
    if restored:
        lines.append("  %d file%s of %s, which is read-only, %s put back to the template's text (RESTORED below)." % (
            restored, '' if restored == 1 else 's', g.get('restore_where', ''), 'was' if restored == 1 else 'were'))
    lines.append("  %s changed none of your files. In every compare, '-' lines are the template's and '+' lines are yours." % (
        ('Apart from the refresh above%s, this report' % (' and the files restored below' if restored else '')) if notes
        else ('Apart from the files restored below, this report' if restored else 'This report')))
    lines += B
    lines += ['', "  These commands work offline until the next update. To see the template's whole change to a file:",
              '  git diff %s/template^ %s/template -- <path>' % (t, t),
              '  This report again, with every entry: git log -1 --format=%%B %s/template' % t]
    return lines


# ── The subcommands ──────────────────────────────────────────────────────────

def template_name(answers):
    m = re.fullmatch(r'\.copier-answers\.(.+)\.yml', os.path.basename(answers))
    return m.group(1) if m else 'template'


def setup(args):
    if git('rev-parse', '--is-inside-work-tree', check=False).strip() != 'true':
        say('not a git repository: nothing recorded.')
        return None
    src, to, answers = args.get('--src'), args.get('--to'), args.get('--answers')
    if git('rev-parse', '--show-prefix').strip():
        data = refresh_data(os.path.abspath(src), template_name(answers)) if src and answers else None
        missing = [p for p in (data or {}).get('refresh', []) if not os.path.lexists(p)]
        say('the project is not at its repository root, so nothing was recorded, no shared file was '
            'refreshed or added and no settings entry or MCP server was offered%s. Run the update in a '
            'project that is its own git repository.' % ((' (missing here: %s)' % ', '.join(missing)) if missing else ''))
        return None
    if not (src and answers and to and re.fullmatch(r'[0-9a-f]{7,64}', to)):
        say('needs --src, --to <commit> and --answers (is the template a git repository?).')
        return None
    rel = os.path.relpath(os.path.abspath(answers)).replace(os.sep, '/')
    return {'src': os.path.abspath(src), 'to': to, 'answers': rel, 't': template_name(rel),
            'gitdir': os.path.abspath(git('rev-parse', '--git-dir').strip()),
            'root': os.path.realpath('.')}


def others_history(t):
    """The render records of every other template here: refs/<name>/template, where <name> is
    no namespace of Git's own and the commit is a render record. Each is read from the record
    the sibling's answers file in HEAD names (committed_record, by its own answers file in HEAD
    alone, which names the sibling's version), so a sibling's update or copy the project never
    committed counts as not made; where no record names it, from the nearest record whose
    answers HEAD's history held, and where none is, that sibling is left out (from the tip only
    where there is no HEAD or git ignores the sibling's answers file)."""
    out = {}
    head = verify('HEAD')
    for ref in git('for-each-ref', '--format=%(refname)', 'refs/').split():
        m = re.fullmatch(r'refs/([^/]+)/template', ref)
        if not m or m.group(1) == t or m.group(1) in GIT_NAMESPACES:
            continue
        cur = ref_info(ref)
        if not cur:
            continue
        path = '.copier-answers.%s.yml' % m.group(1)
        ans = git('rev-parse', '-q', '--verify', 'HEAD:' + path, check=False).strip() if head else ''
        base, _ = committed_record(cur, None, ans, answers_held(path))
        if base:
            out[m.group(1)] = history(base['sha'])
    return out


def set_back(c, T, tip, base, arrive):
    """A run that records nothing (the report off, a render that failed) at the version and
    answers of tip, a record HEAD never committed; base is the record HEAD committed (or None).
    Where the work tree is back at HEAD where tip wrote (a file holding a blob tip lists as
    written beyond base's list holds HEAD's bytes again, or a full run at tip's version and
    answers would refresh or, where arrive, add a listed shared file it can write), tip was
    discarded: it is set back to base, or removed, so committing this run never makes it count.
    A hand rerun over tip's writes, or over the owner's later edits to them, leaves it; so does
    a run where every file tip wrote was rewritten since (another template's run, a formatter, a
    hand edit) and no listed shared file shows the discard."""
    H = tree_map('HEAD')
    known = {(p, b) for p, b, _ in written_blobs(base['msg'])} if base else set()
    mine = {}
    for p, b, _ in written_blobs(tip['msg']):
        if (p, b) not in known:
            mine.setdefault(p, set()).add(b)
    unread = ignored_paths(sorted(mine))
    now = worktree(sorted(set(mine) - unread))
    def at_head(p):
        h = H[p][1] if p in H else None
        return now.get(p) == h and h not in mine[p]
    gone = any(at_head(p) for p in mine if p not in unread)
    data = None if gone else refresh_data(c['src'], c['t'])
    if data:
        N = tree_map(tip['tree'])
        paths = [p for p in data.get('refresh', []) if isinstance(p, str) and p in N]
        paths = [p for p in paths if p not in ignored_paths(paths)]
        own = history(base['sha']) if base else {}
        Y = 'refs/%s/yours' % c['t']
        yours = tree_map(Y) if verify(Y) else {}
        done, added, _ = refresh(paths, N, worktree(paths), H, own, own,
                                 others_history(c['t']) if arrive else {}, arrive, c['root'],
                                 lambda p: owner_held(p, yours), write=False)
        gone = bool(done or added)
    if gone and base:
        git('update-ref', T, base['sha'], tip['sha'])
    elif gone:
        git('update-ref', '-d', T, tip['sha'])


def answers_commits(path, limit):
    """The distinct _commit values in the answers file's history, newest first."""
    out = []
    for sha in git('log', '--format=%H', 'HEAD', '--', path, check=False).split():
        text = git('show', '%s:%s' % (sha, path), check=False)
        m = re.search(r'^_commit:\s*(\S+)', text, re.M)
        if m and m.group(1) not in [v for v, _ in out]:
            out.append((m.group(1), text))
        if len(out) > limit:
            break
    return out


def seed_list(answers, src, from_sha):
    """Up to three earlier versions the answers file's history names, other than from_sha."""
    out = []
    for v, txt in answers_commits(answers, 3):
        sha = verify(v, cwd=src)
        if sha and sha != from_sha and sha not in [s for s, _ in out]:
            out.append((sha, txt))
    return out[:3]


def seed_history(c, tmp, from_sha, old_text, old_ans, chain, seeds):
    """Where no record matches: render the earlier versions (oldest first) and the old one,
    chained as records under chain. Returns (chain, O tree or None, O commit or None)."""
    t, src = c['t'], c['src']
    for i, (sha, txt) in enumerate(reversed(seeds)):
        tree, _ = render_tree(src, sha, txt, c['gitdir'], tmp, 'h%d' % i)
        if tree:
            chain = commit(tree, '%s render, history\n\ncommit: %s\nanswers: %s\n' % (
                t, sha, git('hash-object', '--stdin', inp=txt).strip()), None, chain)
    O_tree, _ = render_tree(src, from_sha, old_text, c['gitdir'], tmp, 'o')
    if not O_tree:
        return chain, None, None
    chain = commit(O_tree, '%s render\n\ncommit: %s\nanswers: %s\n' % (t, from_sha, old_ans), None, chain)
    return chain, O_tree, chain


def cmd_baseline(args):
    c = setup(args)
    if not c:
        return
    t, T, src = c['t'], 'refs/%s/template' % c['t'], c['src']
    with open(c['answers'], encoding='utf-8') as f:
        answers_text = f.read()
    tip = ref_info(T)
    head = verify('HEAD')
    head_text = git('show', 'HEAD:' + c['answers'], check=False) if head else ''
    m = re.search(r'^_commit:\s*(\S+)', head_text, re.M)
    from_sha = verify(m.group(1), cwd=src) if m else ''
    head_ans = git('rev-parse', '-q', '--verify', 'HEAD:' + c['answers'], check=False).strip() if head_text else ''
    # A record the project never committed counts as not made (a copy discarded, then run
    # again): the base is the record HEAD's answers file names, else the nearest whose answers
    # HEAD's history held, else none (a moving adoption discarded: HEAD never held an answers
    # file), and the offers then fall back to the committed history of settings.json.
    cur, uncommitted = committed_record(tip, from_sha or None, head_ans, answers_held(c['answers']))
    ab = git('hash-object', c['answers']).strip()
    with open(c['answers'], 'rb') as f:
        answers_key(ab, f.read())
    # A copy that records nothing (the report off, a render that failed) at the version and
    # answers of a record HEAD never committed (a copy discarded, then made again) sets that
    # record back where the work tree no longer holds what it wrote.
    again = bool(tip) and uncommitted and tip.get('commit') == c['to'] and same_answers(tip, ab)
    if off():
        if again:
            set_back(c, T, tip, cur, False)
        return
    with tempfile.TemporaryDirectory() as tmp:
        tree, reason = render_tree(src, c['to'], answers_text, c['gitdir'], tmp, 'n')
        if not tree:
            say('no render recorded (%s); the first update will render it.' % reason)
            if again:
                set_back(c, T, tip, cur, False)
            return
        chain = cur['sha'] if cur else None
        if not cur and head:
            # A copy over a project an earlier version of this template made (copier recopy, a
            # moving re-adoption) and that has no record: its renders are seeded as an update
            # seeds them, so the shared files the copy kept are refreshed now and later updates
            # know their history.
            if from_sha and from_sha != verify(c['to'], cwd=src):
                chain, _, _ = seed_history(c, tmp, from_sha, head_text, head_ans, None,
                                           seed_list(c['answers'], src, from_sha))
    notes = []
    data = refresh_data(src, t)
    N = tree_map(tree)
    offered = offered_ids(cur['msg']) if cur else None
    mcp_offered = offered_mcp(cur['msg']) if cur else None
    blobs = written_blobs(cur['msg']) if cur else []
    own = history(chain) if chain else {}
    for p, b, edited in blobs:
        if not edited:
            own.setdefault(p, set()).add(b)
    others = others_history(t)
    rendered = union_history(own, *others.values())
    lines = []
    if data:
        try:
            if chain and head:
                paths = [p for p in data.get('refresh', []) if p in N]
                unread = ignored_paths(paths)
                paths = [p for p in paths if p not in unread]
                done, _, failed = refresh(paths, N, worktree(paths), tree_map('HEAD'), own, own, {},
                                          False, c['root'], lambda p: True)
                notes += refresh_notes(t, done, [], failed)
            # A copy over an existing settings.json keeps the owner's file (a seed): the entries
            # this template offers are added to it, once, as an update would. One git ignores is
            # never read, so never hashed.
            before = worktree([SETTINGS]).get(SETTINGS) if not ignored_paths([SETTINGS]) else None
            lines, offered = settings_merge(data, N, offered, set())
            notes += [l.replace('▸ ', '▸ %s: ' % t, 1) for l in lines]
            wrote = settings_wrote(lines)
            if wrote:
                blobs.append((SETTINGS, wrote, not delivered(N, SETTINGS) and before not in rendered.get(SETTINGS, ())))
        except Exception as err:   # report what was done; the record is still written
            notes.append('▸ %s: the refresh stopped (%s).' % (t, err))
        try:
            # A copy keeps an existing .mcp.json and client file (seed, copy-only): the servers
            # this template offers are added to them, once, as an update would.
            ml, mcp_offered, writes = mcp_lane(data, N, mcp_offered, set(), rendered, others, t, lines)
            notes += [l.replace('▸ ', '▸ %s: ' % t, 1) for l in ml]
            blobs += [(p, after, not delivered(N, p) and before not in rendered.get(p, ())) for p, before, after in writes]
        except Exception as err:
            notes.append('▸ %s: the MCP servers stopped (%s).' % (t, err))
    if notes:
        print('\n'.join(notes), flush=True)
    commit(tree, '\n'.join(notes + ['%s render, copied' % t]) + record_tail(c['to'], ab, offered or set(), blobs, mcp_offered),
           T, chain)


def cmd_update(args):
    c = setup(args)
    if not c:
        return
    t, src, to, answers = c['t'], c['src'], c['to'], c['answers']
    T, Y = 'refs/%s/template' % t, 'refs/%s/yours' % t
    frm_raw = os.environ.get('VERSION_FROM', '')
    head = verify('HEAD')
    head_text = git('show', 'HEAD:' + answers, check=False) if head else ''
    if not frm_raw:
        m = re.search(r'^_commit:\s*(\S+)', head_text, re.M)
        frm_raw = m.group(1) if m else ''
    from_sha = verify(frm_raw, cwd=src) if frm_raw else ''
    frm = os.environ.get('VERSION_PEP440_FROM') or frm_raw or '?'
    vto = os.environ.get('VERSION_PEP440_TO') or os.environ.get('VERSION_TO') or to[:10]
    head_ans = git('rev-parse', '-q', '--verify', 'HEAD:' + answers, check=False).strip() if head else ''
    ans_now = git('hash-object', answers).strip()
    with open(answers, 'rb') as f:
        answers_key(ans_now, f.read())   # read now: git may never store this file
    with open(answers, encoding='utf-8') as f:
        answers_text = f.read()
    unmerged, rej_all = conflicts()
    H = tree_map('HEAD') if head else {}
    cur = ref_info(T)
    empty = lambda: {k: [] for k in ('edit', 'sibling', 'once', 'new_here', 'not_restored', 'new_absent', 'lost')}

    # A record the project never committed counts as not made: where the tip does not name the
    # version and answers HEAD's answers file names (an update discarded with git reset --hard and
    # git clean, or git stash -u, then run again or followed by an update to a later release; or
    # a hand rerun over the uncommitted tree), the offers, the written blobs and the render
    # history are read from the nearest record of the tip's first-parent chain that names them;
    # where none does, from the nearest whose answers HEAD's history held; and where none is,
    # from no record: the committed version is rendered afresh, as for a project with no record.
    base, uncommitted = committed_record(cur, from_sha or None, head_ans, answers_held(answers))

    O_tree = O_commit = N_tree = None
    rerun = False
    if cur and cur.get('commit') == to and same_answers(cur, ans_now):
        rerun, N_tree = True, cur['tree']
        if uncommitted:
            # Only a record that names the committed version is the old render; one HEAD's
            # history merely held, or none, leaves it to be rendered, as below.
            if base and base.get('commit') == from_sha and same_answers(base, head_ans):
                O_tree, O_commit = base['tree'], base['sha']
        elif from_sha == to:
            O_tree, O_commit = cur['tree'], cur['sha']
    elif base and from_sha and base.get('commit') == from_sha and same_answers(base, head_ans):
        O_tree, O_commit = base['tree'], base['sha']

    if off():
        O = tree_map(O_tree)
        rej = this_update_rej(rej_all, H, set(O) if O_tree else None)
        skip = set(unmerged) | {r[:-4] for r in rej}
        if O_tree:
            ign = ignored_paths(sorted(set(O) - skip))
            g, _ = classify({}, O, worktree(sorted(set(O) - ign)), H, {}, {}, skip | ign)
            gone = []
        else:
            g = empty()
            gone = [p for p in sorted(H) if not os.path.lexists(p) and p not in skip]
        g = {k: (v if k == 'lost' else []) for k, v in g.items()}
        if head:
            git('update-ref', Y, head)
        r_off = restore_dirs(refresh_data(src, t) or {}) or []
        also = (', and no file of %s is restored' % ', '.join(d + '/' for d in r_off)) if r_off else ''
        print('\n'.join(build_report(t, frm, vto, g, {}, unmerged, rej, [], (gone, 'SYNTEK_UPDATE_REPORT=off, so conflicts and deletions only; no shared file is refreshed or added%s until an update runs without it.' % also), MAX_LIST, False)), flush=True)
        # At the tip's own version and answers, which HEAD does not name (an update discarded and
        # run again with the report off, or a hand rerun before the commit), the tip is set back
        # where its writes are gone, so committing this run never makes a discarded record count.
        if rerun and uncommitted:
            set_back(c, T, cur, base, True)
        return

    with tempfile.TemporaryDirectory() as tmp:
        if N_tree is None:
            N_tree, reason = render_tree(src, to, answers_text, c['gitdir'], tmp, 'n')
            if not N_tree:
                rej = this_update_rej(rej_all, H, None)
                skip = set(unmerged) | {r[:-4] for r in rej}
                gone = [p for p in sorted(H) if not os.path.lexists(p) and p not in skip]
                if head:
                    git('update-ref', Y, head)
                r_off = restore_dirs(refresh_data(src, t) or {}) or []
                also = (', and no file of %s is restored' % ', '.join(d + '/' for d in r_off)) if r_off else ''
                print('\n'.join(build_report(t, frm, vto, empty(), {}, unmerged, rej, [], (gone, 'no report, because %s; no shared file was refreshed or added%s, so the next update does it.' % (reason, also.replace('is restored', 'was restored'))), MAX_LIST, False)), flush=True)
                return
        chain = base['sha'] if base else None
        if O_tree is None and from_sha:
            seeds = seed_list(answers, src, from_sha) if not base else []
            chain, O_tree, O_commit = seed_history(c, tmp, from_sha, head_text or answers_text,
                                                   head_ans or ans_now, chain, seeds)
            if not O_tree:
                chain = base['sha'] if base else chain
        elif O_commit:
            chain = O_commit

    N, O = tree_map(N_tree), tree_map(O_tree)
    rej = this_update_rej(rej_all, H, set(N) | set(O))
    skip = set(unmerged) | {r[:-4] for r in rej}
    skip |= {p for p in set(N) | set(O) if beyond_link(p)}
    # A file git ignores is never read (its ignore rule may guard a credential): it is left out
    # of the comparison, the refresh and the report's commands, and listed once on its own. The
    # MCP lane judges it itself (one line, the offer recorded), so it is not in skip.
    ign = ignored_paths(sorted((set(N) | set(O)) - skip))
    P = worktree(sorted((set(N) | set(O)) - ign))
    recorded = history(base['sha']) if base else {}
    own = history(O_commit or (base['sha'] if base else None))
    for p, (_, sha) in O.items():
        own.setdefault(p, set()).add(sha)
    # Every blob this script wrote over a file the owner had not edited counts as the template's.
    blobs = written_blobs(base['msg']) if base else []
    for p, b, edited in blobs:
        if not edited:
            own.setdefault(p, set()).add(b)
    others = others_history(t)
    rendered = union_history(own, recorded, *others.values())
    yours = tree_map(Y) if verify(Y) else {}
    notes, counts = [], {}
    offered = offered_ids(base['msg']) if base else None
    mcp_offered = offered_mcp(base['msg']) if base else None
    data = refresh_data(src, t)
    touched = set()
    lines = []
    wrote_any = False   # whether any lane wrote a file in this run
    if data:
        try:
            paths = [p for p in data.get('refresh', []) if isinstance(p, str)]
            done, added, failed = refresh(paths, N, P, H, own, recorded, others, bool(head), c['root'],
                                          lambda p: owner_held(p, yours))
            touched |= set(done) | set(added)
            wrote_any = bool(touched)
            counts['refreshed'], counts['added'] = len(done), len(added)
            notes += refresh_notes(t, done, added, failed)
            lines, offered = settings_merge(data, N, offered, skip)
            notes += [l.replace('▸ ', '▸ %s: ' % t, 1) for l in lines]
            wrote = settings_wrote(lines)
            wrote_any = wrote_any or bool(wrote)
            # A settings.json git ignores is never read, so never judged delivered.
            done_settings = SETTINGS not in skip and SETTINGS not in ign and delivered(N, SETTINGS)
            if wrote:
                # P holds every file as it was before this run wrote it: that is what is classified.
                blobs.append((SETTINGS, wrote, not done_settings and P.get(SETTINGS) not in rendered.get(SETTINGS, ())))
            if done_settings:
                P[SETTINGS] = N[SETTINGS][1]   # the release's settings, its entries added: delivered
        except Exception as err:   # report what was done; the report and the record still follow
            notes.append('▸ %s: the refresh stopped (%s); the report below covers every other file.' % (t, err))
        try:
            ml, mcp_offered, writes = mcp_lane(data, N, mcp_offered, skip, rendered, others, t, lines)
            notes += [l.replace('▸ ', '▸ %s: ' % t, 1) for l in ml]
            wrote_any = wrote_any or bool(writes)
            for p, before, after in writes:
                done_file = delivered(N, p)
                blobs.append((p, after, not done_file and before not in rendered.get(p, ())))
                if done_file:
                    P[p] = N[p][1]   # the release's file, the servers added: delivered
        except Exception as err:
            notes.append('▸ %s: the MCP servers stopped (%s); the report below covers every other file.' % (t, err))
    r_dirs, r_done, r_missing, r_left = [], [], set(), []
    if data:
        r_dirs = restore_dirs(data)
        if r_dirs is None:
            r_dirs = []
            notes.append('▸ %s: %s lists "restore" in a form this script does not read, so no file was restored.' % (t, REFRESH_DATA))
        elif r_dirs:
            try:
                shared = {p for p in data.get('refresh', []) if isinstance(p, str)}
                r_done, r_missing, r_left, r_failed = restore(
                    r_dirs, shared, N, H, own, others, unrecorded_siblings(t), c['root'])
                if r_failed:
                    notes.append('▸ %s: could not restore %d file%s of %s, left as %s: %s' % (
                        t, len(r_failed), '' if len(r_failed) == 1 else 's',
                        ', '.join(d + '/' for d in r_dirs), 'it was' if len(r_failed) == 1 else 'they were',
                        ', '.join(r_failed)))
            except Exception as err:   # nothing was written; the report and the record still follow
                notes.append('▸ %s: the restore stopped (%s); the report below covers every other file.' % (t, err))
            touched |= set(r_done) | {p for p, _ in r_left}
            wrote_any = wrote_any or bool(r_done)
    g, cnt = classify(N, O, P, H, own, others, skip | touched, ign)
    cnt.update(counts)
    cnt['restored'] = sum(1 for p in r_done if N.get(p) != O.get(p))
    cnt['left'] = sum(1 for p, _ in r_left if N.get(p) != O.get(p))
    if O_tree:
        override = ''
        deleted_unknown = []
    else:
        g = {k: [] for k in g}
        deleted_unknown = [p for p in sorted(H) if not os.path.lexists(p) and p not in skip]
        override = ('the full report needs version %s, which could not be rendered.' % frm_raw) if not rerun else ''
    g['restore_dirs'] = r_dirs
    if r_done or r_left:
        g['restored'], g['restore_left'] = r_done, r_left
        g['restore_where'] = ', '.join(d + '/' for d in r_dirs)
        g['restore_held'] = {p for p in r_done if p in H}
        g['restore_missing'] = r_missing
        g['restore_marks'] = {p for p in r_done if p in unmerged}
    shown = [u for u in unmerged if u not in set(r_done)]
    printed = build_report(t, frm, vto, g, cnt, shown, rej, notes, (deleted_unknown, override), MAX_LIST, False)
    print('\n'.join(printed), flush=True)
    # A rerun records nothing: a hand rerun over the uncommitted tree finds the first run's writes
    # and adds nothing. Where the tip was never committed and a lane wrote (the update was
    # discarded, or the owner removed an entry it offered before committing it), the run is
    # recorded afresh on the record HEAD committed. Every other run records on its base.
    if rerun and not (uncommitted and wrote_any):
        return
    full = build_report(t, frm, vto, g, cnt, shown, rej, notes, (deleted_unknown, override), 10 ** 9, True)
    commit(N_tree, '\n'.join(full) + record_tail(to, ans_now, offered or set(), blobs, mcp_offered), T, chain)
    if head:
        git('update-ref', Y, head)


# ── Self-test ────────────────────────────────────────────────────────────────

def tree_map_in(cwd, ref):
    old = os.getcwd()
    try:
        os.chdir(cwd)
        return tree_map(ref)
    finally:
        os.chdir(old)


def settings_probe(base, check):
    """settings_merge on real files: the owner's text kept, nothing written when nothing is new."""
    hook = {'hooks': [{'type': 'command', 'command': 'bash .claude/hooks/probe-hook.sh', 'timeout': 10}]}
    pre = {'matcher': 'auto', 'hooks': [{'type': 'command', 'command': 'bash .claude/hooks/pre.sh auto'}]}
    data = {'settings': {'autoCompactEnabled': False, 'hooks': {'UserPromptSubmit': [hook], 'PreCompact': [pre]},
                         'permissions': {'deny': ['Edit(build/**)', 'Bash(rm *)'], 'ask': ['Bash(git push *)']}}}
    rendered = {'autoCompactEnabled': False, 'hooks': {'PreCompact': [pre], 'UserPromptSubmit': [hook]},
                'permissions': {'deny': ['Edit(build/**)', 'Bash(rm *)'], 'ask': ['Bash(git push *)']}}
    cases = {
        'tabs': '{\n\t"model": "opus",\n\t"permissions": {\n\t\t"allow": [\n\t\t\t"Bash(rm *)"\n\t\t]\n\t}\n}\n',
        'four': '{\r\n    "permissions": {\r\n        "deny": [\r\n            "Read(.env)"\r\n        ]\r\n    },\r\n    "model": "opus"\r\n}',
        'two': '{\n  "hooks": {\n    "PreCompact": [\n      {\n        "matcher": "manual",\n        "hooks": []\n      }\n    ]\n  },\n  "permissions": {"deny": ["Read(.env)"]}\n}\n',
        'compact': '{"model":"opus"}',
        'empty': '{}\n',
        'bom': '﻿{\n  "model": "opus"\n}\n',
        'jsonc': '{\n  // my settings\n  "model": "opus"\n}\n',
        'odd': '{\n  "permissions": {\n    "deny": "Edit(build/**)"\n  }\n}\n',
        'done': json.dumps(rendered, indent=3) + '\n',
        'null': '{\n  "permissions": null,\n  "hooks": {"PreCompact": null}\n}\n',
    }
    old = os.getcwd()
    for name, text in cases.items():
        d = os.path.join(base, name)
        os.makedirs(os.path.join(d, '.claude'))
        try:
            os.chdir(d)
            git('init', '-q')
            os.makedirs('.claude/hooks')
            for script in ('probe-hook.sh', 'pre.sh'):
                with open('.claude/hooks/' + script, 'w', encoding='utf-8') as f:
                    f.write('exit 0\n')
            with open(SETTINGS, 'w', encoding='utf-8', newline='') as f:
                f.write(text)
            before = open(SETTINGS, 'rb').read()
            st = os.stat(SETTINGS)
            sha = git('hash-object', '-w', '--stdin', inp=json.dumps(rendered, indent=2) + '\n').strip()
            N = {SETTINGS: ('100644', sha)}
            lines, seen = settings_merge(data, N, None, set())
            after = open(SETTINGS, 'rb').read()
            out = '\n'.join(lines)
            if name in ('jsonc',):
                check(after == before and 'not plain JSON' in out, '%s: a file that is not plain JSON is reported and left alone (%r)' % (name, out))
                continue
            if name == 'done':
                check(after == before and os.stat(SETTINGS).st_mtime_ns == st.st_mtime_ns and not lines,
                      '%s: nothing new, so the file is not written (%r)' % (name, out))
                check(len(seen) == 6, '%s: every entry present is recorded as offered (%d)' % (name, len(seen)))
                continue
            if name == 'odd':
                check(b'"deny": "Edit(build/**)"' in after and 'is not a list' in out,
                      '%s: a rule list that is not a list is reported, never replaced (%r)' % (name, out))
                continue
            cur = json.loads(after.decode('utf-8-sig'))
            check(all(present(cur, i) for i in [('hook', 'UserPromptSubmit', hook), ('hook', 'PreCompact', pre),
                                                 ('deny', 'Edit(build/**)'), ('ask', 'Bash(git push *)')])
                  and cur.get('autoCompactEnabled') is False,
                  '%s: every new entry is added (%r)' % (name, out))
            check(('rewritten' in out) == (name == 'null'),
                  '%s: the entries were inserted into the owner\'s text, or a null rewritten and reported (%r)' % (name, out))
            again, _ = settings_merge(data, N, seen, set())
            check(not again and open(SETTINGS, 'rb').read() == after, '%s: a second merge adds nothing' % name)
            check(after.endswith(b'\n') == before.endswith(b'\n'), '%s: the final newline is kept as it was' % name)
            check(after.startswith(b'\xef\xbb\xbf') == before.startswith(b'\xef\xbb\xbf'), '%s: the byte-order mark is kept as it was' % name)
            if name == 'tabs':
                body = after.decode()
                check(all(not re.match(r' ', l) for l in body.splitlines()), 'tabs: every added line is indented with tabs')
                check(body.startswith('{\n\t"model": "opus",\n\t"permissions": {\n\t\t"allow": [\n\t\t\t"Bash(rm *)"\n\t\t]'),
                      'tabs: the owner\'s lines are kept')
                check(not has_rule(cur, 'deny', 'Bash(rm *)') and 'because you allow it: deny Bash(rm *)' in out,
                      'tabs: a rule the owner allows is reported, never added')
                check(list(cur) == ['model', 'permissions', 'hooks', 'autoCompactEnabled'], 'tabs: the owner\'s key order is kept (%r)' % list(cur))
            if name == 'four':
                body = after.decode()
                check('\r\n' in body and '\n' not in body.replace('\r\n', ''), 'four: CRLF line endings are kept')
                check(all(len(re.match(r' *', l).group(0)) % 4 == 0 for l in body.split('\r\n')), 'four: four-space indentation is kept')
                check(list(cur) == ['permissions', 'model', 'hooks', 'autoCompactEnabled'] and cur['permissions']['deny'][0] == 'Read(.env)',
                      'four: the owner\'s order and rules are kept (%r)' % list(cur))
            if name == 'two':
                check(len(cur['hooks']['PreCompact']) == 2 and cur['hooks']['PreCompact'][0]['matcher'] == 'manual',
                      'two: the hook is appended after the owner\'s entry')
                check('"permissions": {"deny": ["Read(.env)", "Edit(build/**)"' in after.decode(),
                      'two: a one-line list stays on one line (%r)' % after.decode())
            if name == 'compact':
                check('\n' not in after.decode(), 'compact: a one-line file stays one line')
        finally:
            os.chdir(old)
    # Never written: a file in conflict, a link, one beyond a linked folder. A hook entry whose
    # script is missing is reported and offered again, its rules still added.
    for name in ('conflict', 'link', 'beyond', 'noscript'):
        d = os.path.join(base, name)
        os.makedirs(d)
        try:
            os.chdir(d)
            git('init', '-q')
            plain = '{\n  "model": "opus"\n}\n'
            if name == 'beyond':
                os.makedirs('real-claude/hooks')
                os.symlink('real-claude', '.claude')
                target = 'real-claude/settings.json'
            else:
                os.makedirs('.claude/hooks')
                target = '.claude/shared.json' if name == 'link' else SETTINGS
            if name != 'noscript':
                for script in ('probe-hook.sh', 'pre.sh'):
                    with open(os.path.join(os.path.dirname(target), 'hooks', script), 'w') as f:
                        f.write('exit 0\n')
            with open(target, 'w', encoding='utf-8') as f:
                f.write(plain)
            if name == 'link':
                os.symlink('shared.json', SETTINGS)
            sha = git('hash-object', '-w', '--stdin', inp=json.dumps(rendered, indent=2) + '\n').strip()
            N = {SETTINGS: ('100644', sha)}
            lines, seen = settings_merge(data, N, None, {SETTINGS} if name == 'conflict' else set())
            out = '\n'.join(lines)
            now = open(target, encoding='utf-8').read()
            if name == 'conflict':
                check(now == plain and not lines, 'conflict: a settings.json in conflict is left alone (%r)' % out)
            elif name in ('link', 'beyond'):
                check(now == plain and ('is a link' if name == 'link' else 'lies beyond a link') in out
                      and 'add them by hand' in out and 'probe-hook.sh' in out,
                      '%s: never written through a link, and the entries are reported (%r)' % (name, out))
                check(not seen, '%s: the entries stay to be offered again (%r)' % (name, seen))
            else:
                cur = json.loads(now)
                check(not cur.get('hooks') and has_rule(cur, 'deny', 'Edit(build/**)')
                      and 'its script is not in .claude/hooks/' in out,
                      'noscript: a hook entry is never added without its script; the rules are (%r)' % out)
                check(not any(x.startswith('hook ') for x in seen), 'noscript: the hook entries are offered again')
        finally:
            os.chdir(old)
    # A settings.json git ignores is never read (mode 000 proves it) or written: one line names
    # the entries to add by hand, none is recorded, and the next run names them again.
    d = os.path.join(base, 'ignored')
    os.makedirs(os.path.join(d, '.claude', 'hooks'))
    try:
        os.chdir(d)
        git('init', '-q')
        for script in ('probe-hook.sh', 'pre.sh'):
            with open('.claude/hooks/' + script, 'w') as f:
                f.write('exit 0\n')
        with open('.gitignore', 'w') as f:
            f.write('/.claude/settings.json\n')
        plain = '{\n  "model": "opus"\n}\n'
        with open(SETTINGS, 'w', encoding='utf-8') as f:
            f.write(plain)
        sha = git('hash-object', '-w', '--stdin', inp=json.dumps(rendered, indent=2) + '\n').strip()
        N = {SETTINGS: ('100644', sha)}
        st = os.stat(SETTINGS)
        os.chmod(SETTINGS, 0)
        try:
            lines, seen = settings_merge(data, N, None, set())
            again, seen2 = settings_merge(data, N, seen, set())
        except OSError as err:
            lines, seen, again, seen2 = ['read: %s' % err], {'read'}, [], set()
        finally:
            os.chmod(SETTINGS, 0o644)
        st2 = os.stat(SETTINGS)
        check(open(SETTINGS).read() == plain and (st.st_size, st.st_mtime_ns) == (st2.st_size, st2.st_mtime_ns)
              and len(lines) == 1 and 'is ignored by git, so it was not read' in lines[0] and 'add them by hand' in lines[0]
              and 'probe-hook.sh' in lines[0] and 'deny Edit(build/**)' in lines[0] and '"autoCompactEnabled": false' in lines[0],
              'ignored: settings.json is never read or written, one line names the entries (%r)' % lines)
        check(not seen and not seen2 and again == lines, 'ignored: nothing is recorded, so the entries are offered again (%r)' % again)
    finally:
        os.chdir(old)
    # The rule for an entry missing now: offered before (recorded, or in a committed settings.json)
    # means the owner removed it, so it stays removed; never offered means it is added.
    d = os.path.join(base, 'removed')
    os.makedirs(os.path.join(d, '.claude', 'hooks'))
    try:
        os.chdir(d)
        git('init', '-q')
        for script in ('probe-hook.sh', 'pre.sh'):
            with open('.claude/hooks/' + script, 'w') as f:
                f.write('exit 0\n')
        with open(SETTINGS, 'w', encoding='utf-8') as f:
            f.write(json.dumps({'hooks': {'UserPromptSubmit': [hook]}}, indent=2) + '\n')
        git('add', '-A')
        git('commit', '-q', '-m', 'had it', env=IDENT)
        with open(SETTINGS, 'w', encoding='utf-8') as f:
            f.write('{\n  "model": "opus"\n}\n')
        git('commit', '-q', '-am', 'removed it', env=IDENT)
        sha = git('hash-object', '-w', '--stdin', inp=json.dumps(rendered, indent=2) + '\n').strip()
        N = {SETTINGS: ('100644', sha)}
        lines, seen = settings_merge(data, N, None, set())
        cur = json.loads(open(SETTINGS).read())
        check(not has_hook(cur, 'UserPromptSubmit', hook) and has_hook(cur, 'PreCompact', pre)
              and ['▸ not added to %s, %s: the UserPromptSubmit hook for probe-hook.sh' % (SETTINGS, HELD_WHY)]
              == [l for l in lines if HELD_WHY in l],
              'no record: a hook a committed settings.json held is not re-added, and named once; one it never held is (%r)' % lines)
        with open(SETTINGS, 'w', encoding='utf-8') as f:
            f.write('{\n  "model": "opus"\n}\n')
        lines, _ = settings_merge(data, N, seen, set())
        check(not lines and open(SETTINGS).read() == '{\n  "model": "opus"\n}\n',
              'recorded: entries the owner removed after they were offered are not re-added')
        write_blob('.claude/hooks/probe-hook.sh', '100644', sha)
        check(os.stat('.claude/hooks/probe-hook.sh').st_mode & 0o777 == 0o755, 'a hook the refresh writes is mode 755')
    finally:
        os.chdir(old)
    # An entry an earlier release wired in another command form (the same event, matcher and
    # script) is that entry: never rewritten, no second added, and recorded as offered.
    d = os.path.join(base, 'old-form')
    os.makedirs(os.path.join(d, '.claude', 'hooks'))
    try:
        os.chdir(d)
        git('init', '-q')
        for script in ('probe-hook.sh', 'pre.sh'):
            with open('.claude/hooks/' + script, 'w') as f:
                f.write('exit 0\n')
        older = {'matcher': 'auto', 'hooks': [{'type': 'command',
                                                'command': '[ -f .claude/hooks/pre.sh ] && exec bash .claude/hooks/pre.sh auto'}]}
        text = json.dumps({'hooks': {'PreCompact': [older]}}, indent=2) + '\n'
        with open(SETTINGS, 'w', encoding='utf-8') as f:
            f.write(text)
        sha = git('hash-object', '-w', '--stdin', inp=json.dumps(rendered, indent=2) + '\n').strip()
        N = {SETTINGS: ('100644', sha)}
        lines, seen = settings_merge(data, N, None, set())
        cur = json.loads(open(SETTINGS).read())
        check(cur['hooks']['PreCompact'] == [older] and 'hook PreCompact "auto" pre.sh' in seen
              and has_hook(cur, 'UserPromptSubmit', hook) and 'pre.sh' not in '\n'.join(lines),
              'old form: an entry wired in another command form is kept byte for byte, no second is added, '
              'and it is recorded as offered (%r)' % lines)
        again, _ = settings_merge(data, N, seen, set())
        check(not again and json.loads(open(SETTINGS).read()) == cur, 'old form: a second merge adds nothing (%r)' % again)
    finally:
        os.chdir(old)
    # A hook entry that names no script in .claude/hooks/ (a guard for new projects only) is
    # never offered, recorded or reported, though the data lists it and the render wires it.
    d = os.path.join(base, 'scriptless')
    os.makedirs(os.path.join(d, '.claude', 'hooks'))
    try:
        os.chdir(d)
        git('init', '-q')
        with open('.claude/hooks/probe-hook.sh', 'w') as f:
            f.write('exit 0\n')
        guard = {'matcher': 'Edit|Write', 'hooks': [{'type': 'command', 'command': 'python3 .claude/guard.py guard'}]}
        listed = {'settings': {'hooks': {'PreToolUse': [guard], 'UserPromptSubmit': [hook]}}}
        wired = {'hooks': {'PreToolUse': [guard], 'UserPromptSubmit': [hook]}}
        with open(SETTINGS, 'w', encoding='utf-8') as f:
            f.write('{\n  "model": "opus"\n}\n')
        sha = git('hash-object', '-w', '--stdin', inp=json.dumps(wired, indent=2) + '\n').strip()
        N = {SETTINGS: ('100644', sha)}
        lines, seen = settings_merge(listed, N, None, set())
        cur = json.loads(open(SETTINGS).read())
        check(not has_hook(wired, 'PreToolUse', guard) and 'PreToolUse' not in cur.get('hooks', {})
              and has_hook(cur, 'UserPromptSubmit', hook) and not any(x.startswith('hook PreToolUse') for x in seen)
              and 'guard.py' not in '\n'.join(lines),
              'scriptless: a hook entry that names no script in .claude/hooks/ is never offered, recorded or '
              'reported, while the rest are added (%r)' % lines)
    finally:
        os.chdir(old)
    setting_probe(os.path.join(base, 'top-level'), check)


def setting_probe(base, check):
    """A top-level value (autoCompactEnabled): added only where the key is absent, as text in
    the owner's own format; an owner's other value kept and reported once; offered once."""
    data = {'settings': {'autoCompactEnabled': False}}
    line = 'the handoff hooks assume false; set it to false in .claude/settings.json to use them.'
    added = {
        'two': ('{\n  "model": "opus"\n}\n', '{\n  "model": "opus",\n  "autoCompactEnabled": false\n}\n'),
        'tabs': ('{\n\t"model": "opus"\n}\n', '{\n\t"model": "opus",\n\t"autoCompactEnabled": false\n}\n'),
        'bom-crlf': ('\ufeff{\r\n    "model": "opus"\r\n}',
                     '\ufeff{\r\n    "model": "opus",\r\n    "autoCompactEnabled": false\r\n}'),
        'one-line': ('{"model":"opus"}', '{"model":"opus", "autoCompactEnabled": false}'),
        'empty': ('{}\n', '{\n  "autoCompactEnabled": false\n}\n'),
    }
    kept = {'false': '{\n  "autoCompactEnabled": false\n}\n', 'true': '{\n  "autoCompactEnabled": true\n}\n',
            'zero': '{"autoCompactEnabled": 0}', 'null': '{"model": "opus", "autoCompactEnabled": null}\n'}
    old = os.getcwd()

    def case(name, text, rendered=None, history=()):
        d = os.path.join(base, name)
        os.makedirs(os.path.join(d, '.claude'))
        os.chdir(d)
        git('init', '-q')
        for i, h in enumerate(history):
            with open(SETTINGS, 'w', encoding='utf-8', newline='') as f:
                f.write(h)
            git('add', '-A')
            git('commit', '-q', '-m', 'h%d' % i, env=IDENT)
        with open(SETTINGS, 'w', encoding='utf-8', newline='') as f:
            f.write(text)
        sha = git('hash-object', '-w', '--stdin',
                  inp=json.dumps(rendered or {'model': 'opus', 'autoCompactEnabled': False}, indent=2) + '\n').strip()
        return {SETTINGS: ('100644', sha)}, os.stat(SETTINGS).st_mtime_ns

    try:
        for name, (text, want) in added.items():
            N, _ = case(name, text)
            lines, seen = settings_merge(data, N, None, set())
            got = open(SETTINGS, 'rb').read().decode('utf-8')
            check(got == want, 'top-level %s: the key is inserted in the owner\'s format (%r)' % (name, got))
            check(len(lines) == 1 and lines[0].startswith('▸ added to') and '"autoCompactEnabled": false' in lines[0],
                  'top-level %s: one added line (%r)' % (name, lines))
            check(seen == {'setting autoCompactEnabled'}, 'top-level %s: recorded as offered (%r)' % (name, seen))
            again, _ = settings_merge(data, N, seen, set())
            check(not again and open(SETTINGS, 'rb').read().decode('utf-8') == want, 'top-level %s: added once' % name)
            with open(SETTINGS, 'w', encoding='utf-8', newline='') as f:
                f.write(text)
            again, _ = settings_merge(data, N, seen, set())
            check(not again and open(SETTINGS, 'rb').read().decode('utf-8') == text,
                  'top-level %s: a key the owner deleted after the offer is not re-added' % name)
            os.chdir(old)
        for name, text in kept.items():
            N, mtime = case(name, text)
            lines, seen = settings_merge(data, N, None, set())
            check(open(SETTINGS, 'rb').read().decode('utf-8') == text and os.stat(SETTINGS).st_mtime_ns == mtime,
                  'top-level %s: the owner\'s value is never written' % name)
            if name == 'false':
                check(not lines, 'top-level false: nothing to say (%r)' % lines)
            else:
                check(len(lines) == 1 and lines[0].startswith('▸ kept your "autoCompactEnabled": ') and lines[0].endswith(line),
                      'top-level %s: one line says the hooks assume false (%r)' % (name, lines))
            check(seen == {'setting autoCompactEnabled'}, 'top-level %s: recorded as offered' % name)
            again, _ = settings_merge(data, N, seen, set())
            check(not again, 'top-level %s: reported once, never again (%r)' % (name, again))
            os.chdir(old)
        # idleCompaction, the other value the handoff hooks rely on, reads the same line.
        N, mtime = case('idle-true', '{\n  "idleCompaction": true\n}\n', {'idleCompaction': False})
        lines, seen = settings_merge({'settings': {'idleCompaction': False}}, N, None, set())
        check(len(lines) == 1 and lines[0].startswith('▸ kept your "idleCompaction": true') and lines[0].endswith(line)
              and seen == {'setting idleCompaction'} and os.stat(SETTINGS).st_mtime_ns == mtime,
              'top-level idle-true: an owner\'s idleCompaction true is kept and the line names the handoff hooks (%r)' % lines)
        again, _ = settings_merge({'settings': {'idleCompaction': False}}, N, seen, set())
        check(not again, 'top-level idle-true: reported once, never again (%r)' % again)
        os.chdir(old)
        # A string value (outputStyle): added where absent, an owner's other string kept and
        # reported once in its own words, never added back once removed.
        style = {'settings': {'outputStyle': 'Concise'}}
        sline = ("the template's output style is \"Concise\"; set it to \"Concise\" in .claude/settings.json "
                 'to use it.')
        N, _ = case('style-add', '{\n  "model": "opus"\n}\n', {'model': 'opus', 'outputStyle': 'Concise'})
        lines, seen = settings_merge(style, N, None, set())
        want = '{\n  "model": "opus",\n  "outputStyle": "Concise"\n}\n'
        check(open(SETTINGS).read() == want and len(lines) == 1 and '"outputStyle": "Concise"' in lines[0]
              and seen == {'setting outputStyle'},
              'top-level style-add: a string value is added where the key is absent (%r)' % lines)
        with open(SETTINGS, 'w', encoding='utf-8', newline='') as f:
            f.write('{\n  "model": "opus"\n}\n')
        again, _ = settings_merge(style, N, seen, set())
        check(not again and 'outputStyle' not in open(SETTINGS).read(),
              'top-level style-add: a string value the owner removed is never added back (%r)' % again)
        os.chdir(old)
        N, mtime = case('style-other', '{\n  "outputStyle": "Explanatory"\n}\n', {'outputStyle': 'Concise'})
        lines, seen = settings_merge(style, N, None, set())
        check(lines == ['▸ kept your "outputStyle": "Explanatory" in %s: %s' % (SETTINGS, sline)]
              and seen == {'setting outputStyle'} and os.stat(SETTINGS).st_mtime_ns == mtime,
              'top-level style-other: an owner\'s other style is kept and named in its own words (%r)' % lines)
        again, _ = settings_merge(style, N, seen, set())
        check(not again, 'top-level style-other: reported once, never again (%r)' % again)
        os.chdir(old)
        N, _ = case('style-history', '{\n  "model": "opus"\n}\n', {'outputStyle': 'Concise'},
                    history=('{\n  "outputStyle": "Concise"\n}\n',))
        lines, seen = settings_merge(style, N, None, set())
        check(lines == ['▸ not added to %s, %s: the key "outputStyle"' % (SETTINGS, HELD_WHY)]
              and 'outputStyle' not in open(SETTINGS).read() and 'setting outputStyle' in seen,
              'top-level style-history: a style a committed settings.json held is not re-added (%r)' % lines)
        os.chdir(old)
        N, mtime = case('style-jsonc', '{\n  // mine\n  "outputStyle": "Learning"\n}\n', {'outputStyle': 'Concise'})
        lines, seen = settings_merge(style, N, None, set())
        check(len(lines) == 1 and lines[0].startswith('▸ kept your "outputStyle": "Learning"') and lines[0].endswith(sline)
              and os.stat(SETTINGS).st_mtime_ns == mtime,
              'top-level style-jsonc: a string the text holds is read and reported once (%r)' % lines)
        os.chdir(old)
        # No record: a committed settings.json that held the key means the owner removed it.
        N, _ = case('history', '{\n  "model": "opus"\n}\n', history=('{\n  "autoCompactEnabled": false\n}\n',))
        lines, seen = settings_merge(data, N, None, set())
        check(lines == ['▸ not added to %s, %s: the key "autoCompactEnabled"' % (SETTINGS, HELD_WHY)]
              and 'autoCompactEnabled' not in open(SETTINGS).read() and 'setting autoCompactEnabled' in seen,
              'top-level history: a key a committed settings.json held is not re-added, and named once (%r)' % lines)
        again, _ = settings_merge(data, N, seen, set())
        check(not again, 'top-level history: the record then keeps it quiet (%r)' % again)
        os.chdir(old)
        N, mtime = case('history-true', '{\n  "autoCompactEnabled": true\n}\n', history=('{\n  "autoCompactEnabled": true\n}\n',))
        lines, seen = settings_merge(data, N, None, set())
        check(len(lines) == 1 and lines[0].endswith(line) and os.stat(SETTINGS).st_mtime_ns == mtime,
              'top-level history-true: an owner\'s committed true is kept and reported once (%r)' % lines)
        again, _ = settings_merge(data, N, seen, set())
        check(not again, 'top-level history-true: the record then keeps it quiet (%r)' % again)
        os.chdir(old)
        N, _ = case('old-record', '{\n  "model": "opus"\n}\n', history=('{\n  "autoCompactEnabled": false\n}\n',))
        lines, seen = settings_merge(data, N, {'deny Edit(build/**)'}, set())
        check(lines == ['▸ not added to %s, %s: the key "autoCompactEnabled"' % (SETTINGS, HELD_WHY)]
              and 'autoCompactEnabled' not in open(SETTINGS).read() and 'setting autoCompactEnabled' in seen,
              'top-level old-record: a record that lists no top-level value leaves it to the history (%r)' % lines)
        again, _ = settings_merge(data, N, seen, set())
        check(not again, 'top-level old-record: the record then keeps it quiet (%r)' % again)
        os.chdir(old)
        N, _ = case('old-record-new', '{\n  "model": "opus"\n}\n', history=('{\n  "model": "opus"\n}\n',))
        lines, seen = settings_merge(data, N, {'deny Edit(build/**)'}, set())
        check('autoCompactEnabled": false' in open(SETTINGS).read() and 'setting autoCompactEnabled' in seen,
              'top-level old-record-new: a key no record and no commit held is added (%r)' % lines)
        os.chdir(old)
        # No record and a conflict in settings.json: the committed true is not recorded until a
        # run can read the file, which then reports it exactly once.
        N, _ = case('history-skip', '{\n  "autoCompactEnabled": true\n}\n', history=('{\n  "autoCompactEnabled": true\n}\n',))
        lines, seen = settings_merge(data, N, None, {SETTINGS})
        check(not lines and 'setting autoCompactEnabled' not in seen,
              'top-level history-skip: a conflict records no unreported value (%r, %r)' % (lines, seen))
        lines, seen = settings_merge(data, N, seen, set())
        again, _ = settings_merge(data, N, seen, set())
        check(len(lines) == 1 and lines[0].endswith(line) and not again,
              'top-level history-skip: the next clean run reports it exactly once (%r, %r)' % (lines, again))
        os.chdir(old)
        # A link to a file inside the project is read, never written: a key it holds is never
        # named for adding by hand, an owner's true is reported once, and the next run is quiet.
        N, _ = case('link', '')
        os.remove(SETTINGS)
        with open('.claude/real.json', 'w') as f:
            f.write('{\n  "autoCompactEnabled": true\n}\n')
        os.symlink('real.json', SETTINGS)
        lines, seen = settings_merge(data, N, None, set())
        again, _ = settings_merge(data, N, seen, set())
        check(len(lines) == 1 and lines[0].endswith(line) and 'by hand' not in lines[0] and not again
              and open('.claude/real.json').read() == '{\n  "autoCompactEnabled": true\n}\n',
              'top-level link: a linked true is reported once, never named for adding by hand (%r, %r)' % (lines, again))
        os.remove('.claude/real.json')
        with open('.claude/real.json', 'w') as f:
            f.write('{\n  "model": "opus"\n}\n')
        lines, seen = settings_merge(data, N, None, set())
        again, _ = settings_merge(data, N, seen, set())
        check(len(lines) == 1 and 'by hand' in lines[0] and again == lines,
              'top-level link: a key the linked file lacks is named for adding by hand on every run (%r, %r)' % (lines, again))
        os.chdir(old)
        # Not plain JSON (a comment): a key the text holds is never named for adding by hand.
        N, mtime = case('jsonc', '{\n  // mine\n  "autoCompactEnabled": false\n}\n')
        lines, seen = settings_merge(data, N, None, set())
        check(not lines and 'setting autoCompactEnabled' in seen and os.stat(SETTINGS).st_mtime_ns == mtime,
              'top-level jsonc: a key the text holds is not named for adding by hand (%r)' % lines)
        os.chdir(old)
        # Offered only where the new render holds the same value.
        for name, rendered in (('unrendered', {'model': 'opus'}), ('other-value', {'autoCompactEnabled': True})):
            N, mtime = case(name, '{\n  "model": "opus"\n}\n', rendered)
            lines, seen = settings_merge(data, N, None, set())
            check(not lines and not seen and os.stat(SETTINGS).st_mtime_ns == mtime,
                  'top-level %s: a value the new render does not hold is never offered (%r)' % (name, lines))
            os.chdir(old)
        # A shape this script does not know is ignored, never fatal.
        N, mtime = case('unknown', '{\n  "model": "opus"\n}\n', {'model': 'opus', 'env': {'A': '1'}})
        lines, seen = settings_merge({'settings': {'env': {'A': '1'}, 'nothing': None}}, N, None, set())
        check(not lines and not seen, 'top-level unknown: an object or null value is ignored (%r)' % lines)
    finally:
        os.chdir(old)



def history_probe(base, check):
    """An entry the history alone keeps out: never added, named once where the file is read and
    lacks it, and recorded; a record that lists a top-level value decides alone; every side of
    every merge, every depth and every version is read, whatever the owner's log settings."""
    HELD = HELD_WHY
    hook = {'hooks': [{'type': 'command', 'command': 'bash .claude/hooks/probe-hook.sh', 'timeout': 10}]}
    pre = {'matcher': 'auto', 'hooks': [{'type': 'command', 'command': 'bash .claude/hooks/pre.sh auto'}]}
    full = {'settings': {'autoCompactEnabled': False, 'hooks': {'UserPromptSubmit': [hook], 'PreCompact': [pre]},
                         'permissions': {'deny': ['Edit(build/**)', 'Bash(rm *)'], 'ask': ['Bash(git push *)']}}}
    rendered = {'autoCompactEnabled': False, 'hooks': {'PreCompact': [pre], 'UserPromptSubmit': [hook]},
                'permissions': {'deny': ['Edit(build/**)', 'Bash(rm *)'], 'ask': ['Bash(git push *)']}}
    js = lambda v: json.dumps(v, indent=2) + '\n'
    old = os.getcwd()

    def put(rel, text):
        os.makedirs(os.path.dirname(rel) or '.', exist_ok=True)
        with open(rel, 'w', encoding='utf-8', newline='') as f:
            f.write(text)

    def repo(name, history=(), current=None, scripts=('probe-hook.sh', 'pre.sh'), render=rendered):
        d = os.path.join(base, name); os.makedirs(os.path.join(d, '.claude', 'hooks'))
        os.chdir(d); git('init', '-q')
        for s in scripts:
            put('.claude/hooks/' + s, 'exit 0\n')
        for i, h in enumerate(history):
            put(SETTINGS, h); git('add', '-A'); git('commit', '-q', '-m', 'h%d' % i, env=IDENT)
        if current is not None:
            put(SETTINGS, current)
        sha = git('hash-object', '-w', '--stdin', inp=js(render)).strip()
        return {SETTINGS: ('100644', sha)}

    def side(path, base_text, side_text, other='other'):
        """base on the default branch; on side: side_text then base_text; merge --no-ff."""
        put(path, base_text); git('add', '-A'); git('commit', '-q', '-m', 'base', env=IDENT)
        git('checkout', '-q', '-b', 'side')
        put(path, side_text); git('commit', '-q', '-am', 'held', env=IDENT)
        put(path, base_text); git('commit', '-q', '-am', 'removed', env=IDENT)
        git('checkout', '-q', '-')
        put(other, 'x\n'); git('add', '-A'); git('commit', '-q', '-m', 'other', env=IDENT)
        git('merge', '-q', '--no-ff', 'side', '-m', 'merge', env=IDENT)

    try:
        two = {'settings': {'autoCompactEnabled': False, 'idleCompaction': False}}
        r2 = {'model': 'opus', 'autoCompactEnabled': False, 'idleCompaction': False}
        # record-decides (fix 1)
        N = repo('record-decides', history=('{\n  "idleCompaction": true\n}\n',), current='{\n  "model": "opus"\n}\n', render=r2)
        lines, seen = settings_merge(two, N, {'setting autoCompactEnabled', 'deny Edit(build/**)'}, set())
        cur = json.loads(open(SETTINGS).read())
        check(cur.get('idleCompaction') is False and 'autoCompactEnabled' not in cur and len(lines) == 1
              and lines[0].startswith('▸ added to') and '"idleCompaction": false' in lines[0] and 'setting idleCompaction' in seen,
              'record-decides: a record listing a top-level value decides alone (%r)' % lines)
        os.chdir(old)
        # jsonc-held (contract F1)
        N = repo('jsonc-held', history=('{\n  "idleCompaction": false\n}\n',), current='{\n  // mine\n  "autoCompactEnabled": true\n}\n', render=r2)
        lines, seen = settings_merge(two, N, None, set())
        check(len(lines) == 1 and lines[0].startswith('▸ kept your "autoCompactEnabled": true') and HELD not in lines[0]
              and seen == {'setting autoCompactEnabled', 'setting idleCompaction'},
              'jsonc-held run 1: kept line once, both recorded, no history line (%r, %r)' % (lines, seen))
        put(SETTINGS, '{\n  "autoCompactEnabled": true\n}\n')
        again, _ = settings_merge(two, N, seen, set())
        check(not again and 'idleCompaction' not in open(SETTINGS).read(), 'jsonc-held run 2: quiet, not added (%r)' % again)
        os.chdir(old)
        # held-present: fresh clone of a healthy project is silent
        N = repo('held-present', history=(js(rendered),))
        mt = os.stat(SETTINGS).st_mtime_ns
        lines, seen = settings_merge(full, N, None, set())
        check(not lines and os.stat(SETTINGS).st_mtime_ns == mt and len(seen) == 6, 'held-present: silent, all six recorded (%r %d)' % (lines, len(seen)))
        os.chdir(old)
        # held-rules: a held deny and a held ask the owner allows: the history line, not 'because you allow it'
        rules = {'settings': {'permissions': {'deny': ['Edit(build/**)'], 'ask': ['Bash(git push *)']}}}
        rr = {'permissions': {'deny': ['Edit(build/**)'], 'ask': ['Bash(git push *)']}}
        cur_text = js({'permissions': {'allow': ['Bash(git push *)']}})
        N = repo('held-rules', history=(js(rr),), current=cur_text, render=rr)
        lines, seen = settings_merge(rules, N, None, set())
        check(lines == ['▸ not added to %s, %s: deny Edit(build/**); ask Bash(git push *)' % (SETTINGS, HELD)]
              and open(SETTINGS).read() == cur_text and seen == {'deny Edit(build/**)', 'ask Bash(git push *)'},
              'held-rules: one history line, nothing written, no allow line (%r)' % lines)
        again, _ = settings_merge(rules, N, seen, set())
        check(not again, 'held-rules: quiet next (%r)' % again)
        os.chdir(old)
        # held-noscript
        hk = {'settings': {'hooks': {'UserPromptSubmit': [hook]}}}
        hr = {'hooks': {'UserPromptSubmit': [hook]}}
        N = repo('held-noscript', history=(js(hr),), current='{\n  "model": "opus"\n}\n', scripts=(), render=hr)
        lines, seen = settings_merge(hk, N, None, set())
        check(lines == ['▸ not added to %s, %s: the UserPromptSubmit hook for probe-hook.sh' % (SETTINGS, HELD)]
              and seen == {'hook UserPromptSubmit "" probe-hook.sh'}, 'held-noscript: history line, not the script line (%r %r)' % (lines, seen))
        again, _ = settings_merge(hk, N, seen, set())
        check(not again, 'held-noscript: quiet next (%r)' % again)
        os.chdir(old)
        # held-unread
        N = repo('held-unread', history=(js(hr),), current='{\n  // mine\n  "model": "opus"\n}\n', render=hr)
        lines, seen = settings_merge(hk, N, None, set())
        check(not lines and seen == {'hook UserPromptSubmit "" probe-hook.sh'}, 'held-unread: no line, recorded (%r %r)' % (lines, seen))
        put(SETTINGS, '{\n  "model": "opus"\n}\n')
        again, _ = settings_merge(hk, N, seen, set())
        check(not again and 'hooks' not in open(SETTINGS).read(), 'held-unread run 2: quiet, not added (%r)' % again)
        os.chdir(old)
        # bom-history (impl F5): a committed settings.json with a byte-order mark is read
        N = repo('bom-history', history=('﻿' + js(hr),), current='{\n  "model": "opus"\n}\n', render=hr)
        lines, seen = settings_merge(hk, N, None, set())
        check('hooks' not in open(SETTINGS).read() and len(lines) == 1 and HELD in lines[0], 'bom-history: a BOM version is read (%r)' % lines)
        os.chdir(old)
        # side-settings (fix 3)
        N = repo('side-settings', render=hr)
        side(SETTINGS, '{"model":"opus"}\n', js({'model': 'opus', **hr}))
        ctrl = git('log', '--format=%H', 'HEAD', '--', SETTINGS).split()
        lines, seen = settings_merge(hk, N, None, set())
        check(len(ctrl) == 1, 'side-settings control: the default walk lists one commit (%d)' % len(ctrl))
        check('hooks' not in open(SETTINGS).read() and lines == ['▸ not added to %s, %s: the UserPromptSubmit hook for probe-hook.sh' % (SETTINGS, HELD)]
              and 'hook UserPromptSubmit "" probe-hook.sh' in seen, 'side-settings: not added, named, recorded (%r)' % lines)
        os.chdir(old)
        # log settings (hardening): root commit read under log.showRoot=false; evil merge under log.diffMerges=combined
        N = repo('log-root', history=(js(hr),), current='{\n  "model": "opus"\n}\n', render=hr)
        git('config', 'log.showRoot', 'false'); git('config', 'log.diffMerges', 'combined')
        lines, seen = settings_merge(hk, N, None, set())
        check('hooks' not in open(SETTINGS).read() and len(lines) == 1 and HELD in lines[0], 'log-root: root read whatever log.showRoot (%r)' % lines)
        os.chdir(old)
        N = repo('log-evil', render=hr)
        git('config', 'log.diffMerges', 'combined')
        put(SETTINGS, '{"model":"opus"}\n'); git('add', '-A'); git('commit', '-q', '-m', 'base', env=IDENT)
        git('checkout', '-q', '-b', 'side'); put(SETTINGS, '{"model":"opus","a":1}\n'); git('commit', '-q', '-am', 'a', env=IDENT)
        git('checkout', '-q', '-'); put(SETTINGS, '{"model":"opus","b":1}\n'); git('commit', '-q', '-am', 'b', env=IDENT)
        git('merge', '-q', 'side', '-m', 'm', env=IDENT, check=False)
        put(SETTINGS, js({'model': 'opus', 'a': 1, 'b': 1, **hr})); git('commit', '-q', '-am', 'resolved with the hook', env=IDENT)
        put(SETTINGS, '{"model":"opus","a":1,"b":1}\n'); git('commit', '-q', '-am', 'hook removed', env=IDENT)
        lines, seen = settings_merge(hk, N, None, set())
        check('hooks' not in open(SETTINGS).read() and len(lines) == 1 and HELD in lines[0], 'log-evil: a merge-only version read under log.diffMerges=combined (%r)' % lines)
        os.chdir(old)
        # deep (fix 4) settings + mcp
        d = os.path.join(base, 'deep'); os.makedirs(d); os.chdir(d); git('init', '-q')
        both = {'code-review-graph': PROBE_CRG, 'scrapling': PROBE_SCR}
        stream = []
        def blobcmd(path, text):
            b = text.encode()
            stream.append(b'M 100644 inline ' + path.encode() + b'\ndata %d\n' % len(b) + b + b'\n')
        for k in range(206):
            stream.append(b'commit refs/heads/probe-deep\nmark :%d\ncommitter p <p@x> %d +0000\ndata 2\nc\n' % (k + 1, 1700000000 + k))
            if k:
                stream.append(b'from :%d\n' % k)
            blobcmd(SETTINGS, js({'n': k, **(hr if k == 0 else {})}))
            blobcmd('.mcp.json', js({'n': k, 'mcpServers': {'scrapling': PROBE_SCR} if k == 0 else {}}))
        git('fast-import', '--quiet', inp=b''.join(stream).decode())
        git('checkout', '-q', '-f', 'probe-deep')
        os.makedirs('.claude/hooks', exist_ok=True); put('.claude/hooks/probe-hook.sh', 'exit 0\n')
        sha = git('hash-object', '-w', '--stdin', inp=js(hr)).strip()
        N = {SETTINGS: ('100644', sha), '.mcp.json': ('100644', git('hash-object', '-w', '--stdin', inp=js({'mcpServers': both})).strip())}
        lines, seen = settings_merge(hk, N, None, set())
        check(len(git('log', '--format=%H', 'HEAD', '--', SETTINGS).split()) == 206, 'deep: 206 commits')
        check('hooks' not in open(SETTINGS).read() and len(lines) == 1 and HELD in lines[0], 'deep settings: held beyond 200 (%r)' % lines)
        data = {'mcp': {'servers': ['code-review-graph', 'scrapling'], 'files': {'.mcp.json': ['mcpServers']}}}
        ml, mseen, _ = mcp_lane(data, N, None, set(), {}, {}, 'probe', [])
        check('scrapling' not in json.loads(open('.mcp.json').read())['mcpServers'] and ('.mcp.json', 'scrapling') in mseen
              and any(HELD in l and l.endswith(': scrapling') for l in ml), 'deep mcp: held beyond 200 (%r)' % ml)
        os.chdir(old)
        # side-mcp
        d = os.path.join(base, 'side-mcp'); os.makedirs(d); os.chdir(d); git('init', '-q')
        side('.mcp.json', '{"mcpServers": {}}\n', js({'mcpServers': {'scrapling': PROBE_SCR}}))
        N = {'.mcp.json': ('100644', git('hash-object', '-w', '--stdin', inp=js({'mcpServers': both})).strip())}
        ml, mseen, _ = mcp_lane(data, N, None, set(), {}, {}, 'probe', [])
        check(ml == ['▸ not added to .mcp.json, %s: scrapling' % HELD, '▸ added 1 MCP server to .mcp.json: code-review-graph']
              and ('.mcp.json', 'scrapling') in mseen, 'side-mcp: (%r)' % ml)
        again, _, _ = mcp_lane(data, N, mseen, set(), {}, {}, 'probe', [])
        check(not again, 'side-mcp: quiet next (%r)' % again)
        os.chdir(old)
        # side-shared (fix 5)
        d = os.path.join(base, 'side-shared'); os.makedirs(d); os.chdir(d); git('init', '-q')
        put('a', 'a\n'); git('add', '-A'); git('commit', '-q', '-m', 'base', env=IDENT)
        git('checkout', '-q', '-b', 'side'); put('.claude/skills/x/SKILL.md', 's\n'); git('add', '-A'); git('commit', '-q', '-m', 'add', env=IDENT)
        git('rm', '-q', '.claude/skills/x/SKILL.md'); git('commit', '-q', '-m', 'del', env=IDENT)
        git('checkout', '-q', '-'); put('b', 'b\n'); git('add', '-A'); git('commit', '-q', '-m', 'other', env=IDENT)
        git('merge', '-q', '--no-ff', 'side', '-m', 'merge', env=IDENT)
        check(owner_held('.claude/skills/x/SKILL.md', {}), 'side-shared: owner_held sees a side branch')
        check(not owner_held('.claude/skills/y/SKILL.md', {}), 'side-shared: a file never held is not')
        os.chdir(old)
        # wait: the history line names a removed MCP ask; the wait line follows once
        crg_ask, scr_ask = 'mcp__code-review-graph__apply_refactor_tool', 'mcp__scrapling__fetch'
        d = os.path.join(base, 'wait'); os.makedirs(os.path.join(d, '.claude')); os.chdir(d); git('init', '-q')
        put(SETTINGS, js({'permissions': {'ask': [crg_ask, scr_ask]}})); git('add', '-A'); git('commit', '-q', '-m', 'asks', env=IDENT)
        put(SETTINGS, js({'permissions': {'ask': [crg_ask]}})); git('commit', '-q', '-am', 'no scrapling ask', env=IDENT)
        catch = js({'permissions': [{'action': '*', 'resource': '*', 'effect': 'allow'}]})
        put('opencode.json', catch); git('add', '-A'); git('commit', '-q', '-m', 'oc', env=IDENT)
        srend = {'permissions': {'ask': [crg_ask, scr_ask]}}
        oc_new = js({'$schema': 'x', 'mcp': {'servers': {k: {'type': 'local', 'command': [v['command']] + v['args']} for k, v in both.items()}},
                     'permissions': [{'action': 'scrapling_fetch', 'resource': '*', 'effect': 'ask'},
                                     {'action': 'code-review-graph_apply_refactor_tool', 'resource': '*', 'effect': 'ask'}]})
        N = {SETTINGS: ('100644', git('hash-object', '-w', '--stdin', inp=js(srend)).strip()),
             'opencode.json': ('100644', git('hash-object', '-w', '--stdin', inp=oc_new).strip())}
        sd = {'settings': {'permissions': {'ask': [crg_ask, scr_ask]}}}
        slines, sseen = settings_merge(sd, N, None, set())
        odata = {'mcp': {'servers': ['code-review-graph', 'scrapling'], 'files': {'opencode.json': ['mcp', 'servers']}}}
        ml, mseen, _ = mcp_lane(odata, N, None, set(), {}, {}, 'probe', slines)
        check(slines == ['▸ not added to %s, %s: ask %s' % (SETTINGS, HELD, scr_ask)], 'wait: settings history line (%r)' % slines)
        check(sum('wait for ask rules --write cannot carry' in l for l in ml) == 1, 'wait: the wait line once (%r)' % ml)
        slines2, _ = settings_merge(sd, N, sseen, set())
        ml2, _, _ = mcp_lane(odata, N, mseen, set(), {}, {}, 'probe', slines2)
        check(not slines2 and not any('wait for ask rules' in l for l in ml2), 'wait: not again (%r %r)' % (slines2, ml2))
        os.chdir(old)
    finally:
        os.chdir(old)


PROBE_CRG = {'command': 'uvx', 'args': ['crg==1', 'serve', '--tools', 'a,b'], 'env': {'KEY': ''}}
PROBE_SCR = {'command': 'uvx', 'args': ['--from', 'scr==1', 'scr', 'mcp']}
PROBE_TOML_HEAD = "# The client's settings.\nproject_doc_fallback_filenames = ['CLAUDE.md']\n"
PROBE_TOML = PROBE_TOML_HEAD + (
    "\n[mcp_servers.code-review-graph]\ncommand = 'uvx'\nargs = ['crg==1', 'serve', '--tools', 'a,b']\n"
    "\n[mcp_servers.code-review-graph.env]\nKEY = ''\n"
    '\n[mcp_servers.code-review-graph.tools.apply_refactor_tool]\napproval_mode = "prompt"\n'
    "\n[mcp_servers.scrapling]\ncommand = 'uvx'\nargs = ['--from', 'scr==1', 'scr', 'mcp']\n"
    '\n[mcp_servers.scrapling.tools.fetch]\napproval_mode = "prompt"\n')
PROBE_MCP = {'servers': ['code-review-graph', 'scrapling'],
             'files': {'.agents/mcp_config.json': ['mcpServers'], '.codex/config.toml': ['mcp_servers'],
                       '.gemini/settings.json': ['mcpServers'], '.mcp.json': ['mcpServers'], 'opencode.json': ['mcp', 'servers']}}


def mcp_probe(base, check):
    """The MCP lane on real files: each server offered once, the owner's text kept, nothing
    created, nothing ignored read, nothing written through a link."""
    both = {'code-review-graph': PROBE_CRG, 'scrapling': PROBE_SCR}
    asks = ['mcp__scrapling__fetch', 'mcp__code-review-graph__apply_refactor_tool']
    oc_forms = [{'action': 'scrapling_fetch', 'resource': '*', 'effect': 'ask'},
                {'action': 'code-review-graph_apply_refactor_tool', 'resource': '*', 'effect': 'ask'}]
    gm_forms = ['mcp_scrapling_fetch', 'mcp_code-review-graph_apply_refactor_tool']
    js = lambda v: json.dumps(v, indent=2) + '\n'
    new = {'.mcp.json': js({'mcpServers': both}), '.agents/mcp_config.json': js({'mcpServers': both}),
           '.codex/config.toml': PROBE_TOML,
           '.gemini/settings.json': js({'tools': {'exclude': ['ask_user'], 'confirmationRequired': gm_forms}, 'mcpServers': both}),
           'opencode.json': js({'$schema': 'x', 'mcp': {'servers': {k: {'type': 'local', 'command': [v['command']] + v['args']}
                                                                 for k, v in both.items()}},
                                'permissions': oc_forms + [{'action': 'edit', 'resource': 'build/*', 'effect': 'deny'}]}),
           SETTINGS: js({'permissions': {'ask': asks}})}
    old_mcp, old_agents = '{"mcpServers": {}}\n', '{\n  "mcpServers": {}\n}\n'
    data = {'mcp': PROBE_MCP}
    old = os.getcwd()

    def blob(text):
        return git('hash-object', '-w', '--stdin', inp=text).strip()

    def put(rel, content, mode=None):
        os.makedirs(os.path.dirname(rel) or '.', exist_ok=True)
        with open(rel, 'wb') as f:
            f.write(content if isinstance(content, bytes) else content.encode('utf-8'))
        if mode is not None:
            os.chmod(rel, mode)

    def get(rel):
        with open(rel, 'rb') as f:
            return f.read()

    def project(name, files, commits=(), drop=()):
        d = os.path.join(base, name)
        os.makedirs(d)
        os.chdir(d)
        git('init', '-q')
        for i, snap in enumerate(commits):
            for rel, text in snap.items():
                put(rel, text)
            git('add', '-A')
            git('commit', '-q', '-m', 'c%d' % i, env=IDENT)
        put(SETTINGS, new[SETTINGS])
        for rel, text in files.items():
            put(rel, text)
        return {rel: ('100644', blob(text)) for rel, text in new.items() if rel not in drop}

    def lane(N, offered=None, skip=(), rendered=None, others=None, settings_lines=()):
        return mcp_lane(data, N, offered, set(skip), rendered or {}, others or {}, 'probe', list(settings_lines))

    try:
        # JSON: the unedited one-line seed takes the new render's bytes; a second run is a no-op.
        N = project('fast', {'.mcp.json': old_mcp})
        lines, seen, writes = lane(N, rendered={'.mcp.json': {blob(old_mcp)}})
        check(get('.mcp.json') == new['.mcp.json'].encode() and lines == ['▸ added 2 MCP servers to .mcp.json: code-review-graph, scrapling'],
              'mcp fast: an unedited seed takes the new render\'s bytes (%r)' % lines)
        check(set(seen) == {('.mcp.json', 'code-review-graph'), ('.mcp.json', 'scrapling')} and len(writes) == 1
              and all(re.fullmatch(r'[0-9a-f]{64}', h) for h in seen.values()), 'mcp fast: both offers recorded with their hash (%r)' % seen)
        mtime = os.stat('.mcp.json').st_mtime_ns
        again, seen2, writes2 = lane(N, offered=seen, rendered={'.mcp.json': {blob(old_mcp)}})
        check(not again and not writes2 and seen2 == seen and os.stat('.mcp.json').st_mtime_ns == mtime,
              'mcp fast: a second run changes nothing, mtime included (%r)' % again)
        os.chdir(old)
        # The 23-byte form of another template's copy gains exactly the shared bytes.
        N = project('agents23', {'.agents/mcp_config.json': old_agents})
        lane(N)
        check(get('.agents/mcp_config.json') == new['.agents/mcp_config.json'].encode(),
              'mcp agents23: inserting into the 23-byte file gives the shared bytes exactly')
        os.chdir(old)
        # An edited one-line file stays one line, the owner's server first.
        N = project('one-line', {'.mcp.json': '{"mcpServers": {"mine": {"command": "x"}}}\n'})
        lines, _, _ = lane(N, rendered={'.mcp.json': {blob(old_mcp)}})
        body = get('.mcp.json').decode()
        cur = json.loads(body)
        check(body.count('\n') == 1 and body.endswith('}\n') and list(cur['mcpServers']) == ['mine', 'code-review-graph', 'scrapling']
              and cur['mcpServers']['scrapling'] == PROBE_SCR, 'mcp one-line: stays one line, the owner\'s server first (%r)' % body)
        os.chdir(old)
        # Four spaces, CRLF, a byte-order mark, no final newline: all kept.
        raw = b'\xef\xbb\xbf' + '{\r\n    "mcpServers": {\r\n        "mine": {\r\n            "command": "x"\r\n        }\r\n    }\r\n}'.encode()
        N = project('crlf', {'.mcp.json': raw})
        lines, seen, _ = lane(N)
        after = get('.mcp.json')
        text = after[3:].decode()
        check(after.startswith(b'\xef\xbb\xbf') and '\n' not in text.replace('\r\n', '') and not text.endswith('\n')
              and all(len(re.match(r' *', l).group(0)) % 4 == 0 for l in text.split('\r\n'))
              and list(json.loads(text)['mcpServers']) == ['mine', 'code-review-graph', 'scrapling'] and 'rewritten' not in ''.join(lines),
              'mcp crlf: the mark, CRLF, four spaces, no final newline and the owner\'s order kept (%r)' % text[:120])
        mtime = os.stat('.mcp.json').st_mtime_ns
        again, _, _ = lane(N, offered=seen)
        check(not again and os.stat('.mcp.json').st_mtime_ns == mtime, 'mcp crlf: a second run changes nothing')
        os.chdir(old)
        # Tabs in .gemini/settings.json that already holds its ask rules.
        tabs = ('{\n\t"tools": {\n\t\t"confirmationRequired": [\n\t\t\t"mcp_scrapling_fetch",\n'
                '\t\t\t"mcp_code-review-graph_apply_refactor_tool"\n\t\t]\n\t},\n\t"mcpServers": {}\n}\n')
        N = project('tabs', {'.gemini/settings.json': tabs})
        lines, _, _ = lane(N)
        body = get('.gemini/settings.json').decode()
        check(not any(l.startswith(' ') for l in body.splitlines()) and set(json.loads(body)['mcpServers']) == set(both),
              'mcp tabs: added with tab indentation (%r)' % lines)
        os.chdir(old)
        # opencode.json with no "mcp": mcp.servers is created at its end.
        N = project('oc-new', {'opencode.json': js({'permissions': oc_forms})})
        lines, _, _ = lane(N)
        cur = json.loads(get('opencode.json'))
        check(list(cur) == ['permissions', 'mcp'] and set(cur['mcp']['servers']) == set(both),
              'mcp oc-new: mcp.servers created at the end (%r, %r)' % (list(cur), lines))
        os.chdir(old)
        # A key path that is not an object is refused, never replaced, and said once.
        text = js({'mcp': True, 'permissions': oc_forms})
        N = project('oc-bad', {'opencode.json': text})
        lines, seen, _ = lane(N)
        check(get('opencode.json') == text.encode() and any('mcp.servers is not an object' in l for l in lines)
              and ('opencode.json', 'scrapling') in seen, 'mcp oc-bad: a non-object refused, reported, recorded (%r)' % lines)
        os.chdir(old)
        # JSONC: reported, not written, offered again.
        text = '{\n  // mine\n  "permissions": []\n}\n'
        N = project('jsonc', {'opencode.json': text})
        lines, seen, _ = lane(N)
        again, _, _ = lane(N, offered=seen)
        check(get('opencode.json') == text.encode() and any('is not plain JSON' in l for l in lines)
              and not any(p == 'opencode.json' for p, _ in seen) and again == lines,
              'mcp jsonc: reported, never written, offered again (%r)' % lines)
        os.chdir(old)
        # TOML: an append parses to exactly the new render's servers; the unedited file takes
        # the new render's bytes; no final newline and CRLF are handled.
        for name, text in (('toml-append', PROBE_TOML_HEAD + "model = 'mine'\n"), ('toml-nonl', "model = 'mine'"),
                           ('toml-crlf', "model = 'mine'\r\n"), ('toml-fast', PROBE_TOML_HEAD)):
            N = project(name, {'.codex/config.toml': text})
            lines, seen, _ = lane(N, rendered={'.codex/config.toml': {blob(PROBE_TOML_HEAD)}})
            body = get('.codex/config.toml').decode()
            tree = _toml().loads(body)
            check(tree.get('mcp_servers') == _toml().loads(PROBE_TOML)['mcp_servers'] and body.startswith(text.rstrip('\r\n'))
                  and lines == ['▸ added 2 MCP servers to .codex/config.toml: code-review-graph, scrapling'],
                  'mcp %s: the tables, env and tools included, appended (%r)' % (name, lines))
            if name == 'toml-fast':
                check(body == PROBE_TOML, 'mcp toml-fast: an unedited file takes the new render\'s bytes')
            if name == 'toml-crlf':
                check('\n' not in body.replace('\r\n', ''), 'mcp toml-crlf: CRLF kept')
            if name == 'toml-nonl':
                check(body.startswith("model = 'mine'\n\n[mcp_servers.code-review-graph]\n"), 'mcp toml-nonl: a final newline added (%r)' % body[:60])
            again, _, _ = lane(N, offered=seen)
            check(not again, 'mcp %s: a second run is quiet' % name)
            os.chdir(old)
        # TOML that already declares a server (a table, dotted keys, an inline table) or that
        # cannot be extended: the owner's bytes kept, each said once.
        for name, text, want in (
                ('toml-table', PROBE_TOML_HEAD + "\n[mcp_servers.scrapling]\ncommand = 'mine'\n", 'kept your "scrapling"'),
                ('toml-dotted', "mcp_servers.scrapling.command = 'mine'\n", 'kept your "scrapling"'),
                ('toml-inline', "mcp_servers = { scrapling = { command = 'mine' } }\n", 'would not leave exactly your file'),
                ('toml-inline-other', "mcp_servers = { mine = { command = 'x' } }\n", 'would not leave exactly your file')):
            N = project(name, {'.codex/config.toml': text})
            lines, seen, _ = lane(N)
            body = get('.codex/config.toml').decode()
            check(body.startswith(text) and any(want in l for l in lines) and _toml().loads(body)['mcp_servers'].get('scrapling', {}).get('command') != 'uvx',
                  'mcp %s: the owner\'s server kept and reported (%r)' % (name, lines))
            if name.startswith('toml-inline'):
                check(body == text, 'mcp %s: an inline table is never written' % name)
            again, _, _ = lane(N, offered=seen)
            check(not again, 'mcp %s: said once (%r)' % (name, again))
            os.chdir(old)
        # Appended tables that would not parse to exactly the plan are never written (here the
        # extraction is made to lose a line).
        global _toml_blocks
        real = _toml_blocks
        _toml_blocks = lambda text, server: [b[:-1] if len(b) > 2 else b for b in real(text, server)]
        try:
            text = PROBE_TOML_HEAD + "model = 'mine'\n"
            N = project('toml-verify', {'.codex/config.toml': text})
            lines, seen, writes = lane(N)
        finally:
            _toml_blocks = real
        check(get('.codex/config.toml') == text.encode() and not writes and any('would not leave exactly your file' in l for l in lines),
              'mcp toml-verify: an append that does not parse to the plan is never written (%r)' % lines)
        os.chdir(old)
        # Offers: a server held with another value is kept, said once; a sibling's value is named.
        mine = js({'mcpServers': {'scrapling': {'command': 'mine'}}})
        sib_blob = None
        for name in ('differs', 'sibling'):
            N = project(name, {'.mcp.json': mine})
            others = {}
            if name == 'sibling':
                sib_blob = blob(js({'mcpServers': {'scrapling': {'command': 'mine'}}, 'x': 1}))
                others = {'sibling': {'.mcp.json': {sib_blob}}}
            lines, seen, _ = lane(N, others=others)
            body = get('.mcp.json').decode()
            want = "holds sibling's version of the \"scrapling\" MCP server" if name == 'sibling' else 'kept your "scrapling" MCP server'
            check('"scrapling": {\n      "command": "mine"\n    }' in body and any(want in l and 'compare: git diff probe/template -- .mcp.json' in l for l in lines)
                  and 'code-review-graph' in json.loads(body)['mcpServers'] and ('.mcp.json', 'scrapling') in seen,
                  'mcp %s: kept byte for byte, one line, recorded (%r)' % (name, lines))
            again, _, _ = lane(N, offered=seen, others=others)
            check(not again, 'mcp %s: quiet on the next run' % name)
            os.chdir(old)
        # Removed after the offer: never added back. Removed with no record, the history shows it:
        # never added back. An old record without MCP offers and a clean history: added.
        only = js({'mcpServers': {'code-review-graph': PROBE_CRG}})
        N = project('removed', {'.mcp.json': only})
        lines, seen, _ = lane(N, offered={('.mcp.json', 'scrapling'): '0' * 64})
        check(get('.mcp.json') == only.encode() and not lines and ('.mcp.json', 'code-review-graph') in seen,
              'mcp removed: a server removed after the offer is not re-added (%r)' % lines)
        os.chdir(old)
        N = project('history', {'.mcp.json': only}, commits=({'.mcp.json': new['.mcp.json']}, {'.mcp.json': only}))
        lines, seen, _ = lane(N)
        check(get('.mcp.json') == only.encode() and lines == ['▸ not added to .mcp.json, %s: scrapling' % HELD_WHY]
              and ('.mcp.json', 'scrapling') in seen,
              'mcp history: a server the committed history held is not re-added, and named once (%r)' % lines)
        again, _, _ = lane(N, offered=seen)
        check(not again, 'mcp history: quiet on the next run (%r)' % again)
        os.chdir(old)
        N = project('clean', {'.mcp.json': old_mcp}, commits=({'.mcp.json': old_mcp},))
        lines, _, _ = lane(N)
        check(set(json.loads(get('.mcp.json'))['mcpServers']) == set(both), 'mcp clean: no record, a clean history: added (%r)' % lines)
        os.chdir(old)
        # Guards: the client not named; the file absent; git-ignored at mode 000; a link and a
        # path beyond one; a file in conflict.
        text = js({'permissions': oc_forms})
        N = project('unnamed', {'opencode.json': text}, drop=('opencode.json',))
        lines, seen, _ = lane(N)
        check(get('opencode.json') == text.encode() and not any(p == 'opencode.json' for p, _ in seen)
              and lines == ['▸ opencode.json exists but the recorded answers do not name its client, so no MCP server was offered to it'],
              'mcp unnamed: nothing offered, nothing recorded, one line (%r)' % lines)
        os.chdir(old)
        N = project('absent', {})
        lines, seen, _ = lane(N)
        check(not lines and not seen and not any(os.path.lexists(p) for p in PROBE_MCP['files']),
              'mcp absent: no file is ever created (%r)' % lines)
        os.chdir(old)
        N = project('ignored', {'.gitignore': '.mcp.json\n', '.mcp.json': old_mcp})
        os.chmod('.mcp.json', 0)
        st = os.stat('.mcp.json')
        lines, seen, writes = lane(N, rendered={'.mcp.json': {blob(old_mcp)}})
        st2 = os.stat('.mcp.json')
        again, _, _ = lane(N, offered=seen)
        os.chmod('.mcp.json', 0o644)
        check((st.st_size, st.st_mtime_ns) == (st2.st_size, st2.st_mtime_ns) and not writes and len(lines) == 1
              and 'is ignored by git, so it was not read' in lines[0] and 'git show probe/template:.mcp.json' in lines[0]
              and ('.mcp.json', 'scrapling') in seen and not again, 'mcp ignored: never read or written, said once (%r)' % lines)
        os.chdir(old)
        N = project('link', {'shared/mcp.json': old_mcp, 'real-agents/mcp_config.json': old_agents})
        os.symlink('shared/mcp.json', '.mcp.json')
        os.symlink('real-agents', '.agents')
        lines, seen, writes = lane(N)
        check(get('shared/mcp.json') == old_mcp.encode() and get('real-agents/mcp_config.json') == old_agents.encode() and not writes
              and any(l.startswith('▸ .mcp.json is a link') for l in lines) and any(l.startswith('▸ .agents/mcp_config.json lies beyond a link') for l in lines)
              and not seen, 'mcp link: never written through a link, offered again (%r)' % lines)
        os.chdir(old)
        N = project('conflict', {'.mcp.json': old_mcp})
        lines, seen, writes = lane(N, skip={'.mcp.json'})
        check(get('.mcp.json') == old_mcp.encode() and not lines and not seen and not writes, 'mcp conflict: a file in conflict is untouched')
        os.chdir(old)
        # An owner's catch-all allow in opencode.json covers no tool the update brings in: the
        # servers wait, with the --write line, until the file holds their ask rules.
        catch = js({'permissions': [{'action': '*', 'resource': '*', 'effect': 'allow'}]})
        N = project('catch-all', {'opencode.json': catch})
        lines, seen, writes = lane(N)
        check(get('opencode.json') == catch.encode() and not writes and not any(p == 'opencode.json' for p, _ in seen)
              and len(lines) == 1 and 'python3 .claude/probe-permissions.py --write' in lines[0]
              and 'held back now: opencode.json code-review-graph, scrapling' in lines[0],
              'mcp catch-all: the servers held back with the --write line (%r)' % lines)
        put('opencode.json', js({'permissions': [{'action': '*', 'resource': '*', 'effect': 'allow'}] + oc_forms}))
        lines, seen, _ = lane(N, offered=seen)
        check(set(json.loads(get('opencode.json')).get('mcp', {}).get('servers', {})) == set(both)
              and lines == ['▸ added 2 MCP servers to opencode.json: code-review-graph, scrapling'],
              'mcp catch-all: after --write, the next run adds them (%r)' % lines)
        os.chdir(old)
        # An agent's own allow in opencode.json comes after the file's asks, so it outweighs them:
        # the server waits, and one line names the agent's rule; a later allow of the file's own
        # outweighs them the same way.
        N = project('agent-allow', {'opencode.json': js({'permissions': oc_forms, 'agents': {'build': {'permissions': [
            {'action': 'scrapling_*', 'resource': '*', 'effect': 'allow'}]}}})})
        lines, seen, writes = lane(N)
        servers = set(json.loads(get('opencode.json')).get('mcp', {}).get('servers', {}))
        check('scrapling' not in servers and not any(p == 'opencode.json' and s == 'scrapling' for p, s in seen)
              and any("agents.build.permissions lets these servers' tools run unasked" in l and l.endswith(': scrapling') for l in lines),
              'mcp agent allow: an agent allow holds the server back, named (%r)' % lines)
        put('opencode.json', js({'permissions': oc_forms + [{'action': 'scrapling_*', 'resource': '*', 'effect': 'allow'}]}))
        lines, seen, writes = lane(N)
        servers = set(json.loads(get('opencode.json')).get('mcp', {}).get('servers', {}))
        check('scrapling' not in servers and not any(p == 'opencode.json' and s == 'scrapling' for p, s in seen)
              and any('held back now: opencode.json scrapling' in l for l in lines)
              and not any('agents.' in l for l in lines),
              'mcp later allow: a later top-level allow outweighs the asks, so the server waits (%r)' % lines)
        os.chdir(old)
        # No ask in the file's own rules, and an agent's allow: --write would append the asks, but
        # that agent's rule still outweighs them, so the server is never promised to the next
        # update, and only that agent is named, never one whose rules leave the tools alone.
        N = project('agent-no-ask', {'opencode.json': js({'agents': {
            'build': {'permissions': [{'action': 'scrapling_*', 'resource': '*', 'effect': 'allow'}]},
            'plan': {'permissions': [{'action': 'edit', 'resource': '*', 'effect': 'deny'}]}}})})
        lines, seen, writes = lane(N)
        check(not writes and not any(p == 'opencode.json' for p, _ in seen)
              and any(l.startswith("▸ opencode.json: agents.build.permissions lets these servers' tools run unasked")
                      and l.endswith(': scrapling') for l in lines)
              and not any('agents.plan' in l for l in lines)
              and any('(held back now: opencode.json code-review-graph)' in l for l in lines)
              and not any('held back now' in l and 'scrapling' in l for l in lines),
              'mcp agent no-ask: an agent allow --write cannot outweigh is never promised; only that agent named (%r)' % lines)
        os.chdir(old)
        # The same where the project's settings.json allows Scrapling, so it holds no ask for it
        # (the settings lane said 'because you allow it') while this run added the other server's:
        # the new render's asks still decide, and both servers wait. The --write line promises
        # only the server --write completes; the allowed one is said instead, once, with the two
        # ways in; after --write the next run adds the first, and the second only once the owner
        # asks before its tools and runs --write again.
        crg_ask, scr_ask = 'mcp__code-review-graph__apply_refactor_tool', 'mcp__scrapling__fetch'
        allowed_settings = js({'permissions': {'allow': ['mcp__scrapling__*'], 'ask': [crg_ask]}})
        N = project('catch-all-allowed', {'opencode.json': catch, SETTINGS: allowed_settings})
        said = ['▸ added to %s: ask %s' % (SETTINGS, crg_ask), '▸ not added to %s, because you allow it: ask %s' % (SETTINGS, scr_ask)]
        lines, seen, writes = lane(N, settings_lines=said)
        write_line = ('▸ to carry the new ask and deny rules into opencode.json, run: python3 .claude/probe-permissions.py --write; '
                      'the next update then adds the MCP servers to each file that holds their ask rules '
                      '(held back now: opencode.json code-review-graph)')
        check(get('opencode.json') == catch.encode() and not writes and not any(p == 'opencode.json' for p, _ in seen)
              and len(lines) == 2 and lines[0] == write_line,
              'mcp catch-all-allowed: the --write line promises only the server --write completes (%r)' % lines)
        check(len(lines) == 2 and lines[1].startswith('▸ these MCP servers wait for ask rules --write cannot carry')
              and '(you allow them there): opencode.json scrapling.' in lines[1] and '(%s)' % scr_ask in lines[1]
              and 'and run python3 .claude/probe-permissions.py --write, after which' in lines[1]
              and 'by hand (git show probe/template:opencode.json)' in lines[1],
              'mcp catch-all-allowed: the allowed server is said instead, with the two ways in (%r)' % lines[1:])
        lines, seen, _ = lane(N, offered=seen)
        check(lines == [write_line.replace('new ask and deny rules', 'ask rules these MCP servers wait for')],
              'mcp catch-all-allowed: the next run says --write again, and the allowed server not again (%r)' % lines)
        put('opencode.json', js({'permissions': [{'action': '*', 'resource': '*', 'effect': 'allow'}, oc_forms[1]]}))
        lines, seen, _ = lane(N, offered=seen)
        check(set(json.loads(get('opencode.json')).get('mcp', {}).get('servers', {})) == {'code-review-graph'}
              and lines == ['▸ added 1 MCP server to opencode.json: code-review-graph'],
              'mcp catch-all-allowed: after --write, the next run adds the completed server, silent on the other (%r)' % lines)
        put(SETTINGS, js({'permissions': {'allow': ['mcp__scrapling__*'], 'ask': [crg_ask, scr_ask]}}))
        cur = json.loads(get('opencode.json'))
        cur['permissions'].append(oc_forms[0])
        put('opencode.json', js(cur))
        lines, seen, _ = lane(N, offered=seen)
        check(set(json.loads(get('opencode.json'))['mcp']['servers']) == set(both)
              and lines == ['▸ added 1 MCP server to opencode.json: scrapling'],
              'mcp catch-all-allowed: the asks added by hand and --write run, the next run adds it (%r)' % lines)
        os.chdir(old)
        # A settings.json git ignores is never read here either (mode 000): every form waits as
        # one settings.json does not ask for, said in the run whose settings lane names the asks.
        N = project('settings-ignored', {'opencode.json': catch, '.gitignore': '/.claude/settings.json\n'})
        os.chmod(SETTINGS, 0)
        try:
            said = ['▸ %s is ignored by git, so it was not read and these entries were not added (add them by hand; they '
                    'are offered again by the next update): ask %s; ask %s' % (SETTINGS, scr_ask, crg_ask)]
            lines, seen, writes = lane(N, settings_lines=said)
        finally:
            os.chmod(SETTINGS, 0o644)
        check(get('opencode.json') == catch.encode() and not writes and len(lines) == 1
              and ': opencode.json code-review-graph, scrapling.' in lines[0] and 'you allow' not in lines[0]
              and 'wait for ask rules --write cannot carry' in lines[0],
              'mcp settings-ignored: never read; the servers wait, said once with the two ways in (%r)' % lines)
        os.chdir(old)
        # The --write line where this run added an mcp__ rule names only the client files that
        # lack it in their form: none where each equals the new render; one that lost the form.
        N = project('rules', {'.codex/config.toml': PROBE_TOML, 'opencode.json': new['opencode.json'],
                              '.gemini/settings.json': new['.gemini/settings.json']})
        said = ['▸ added to %s: ask %s' % (SETTINGS, scr_ask)]
        lines, seen, _ = lane(N, settings_lines=said)
        check(not lines, 'mcp rules: no --write line where every client file equals the new render (%r)' % lines)
        cur = json.loads(new['opencode.json'])
        cur['permissions'] = [r for r in cur['permissions'] if r['action'] != 'scrapling_fetch']
        put('opencode.json', js(cur))
        put('.codex/config.toml', PROBE_TOML.replace('\n[mcp_servers.scrapling.tools.fetch]\napproval_mode = "prompt"\n', ''))
        lines, _, _ = lane(N, offered=seen, settings_lines=said)
        check(lines == ['▸ to carry the new ask and deny rules into opencode.json and .codex/config.toml, run: '
                        'python3 .claude/probe-permissions.py --write'],
              'mcp rules: the --write line names only the files that lack the rule (%r)' % lines)
        lines, _, _ = lane(N, offered=seen, settings_lines=['▸ added to %s: deny mcp__code-review-graph__embed_graph_tool' % SETTINGS])
        check(lines == ['▸ to carry the new ask and deny rules into opencode.json, run: python3 .claude/probe-permissions.py --write'],
              'mcp rules: a deny is judged in opencode.json alone, where it has a form (%r)' % lines)
        lines, _, _ = lane(N, offered=seen)
        check(not lines, 'mcp rules: no line where no rule was added and no server waits (%r)' % lines)
        os.chdir(old)
        # A client file this run cannot read (git-ignored, mode 000) may lack the added rule:
        # --write still reaches it, so the line names it on a clause of its own.
        N = project('rules-ignored', {'opencode.json': new['opencode.json'], '.gitignore': '/opencode.json\n'})
        os.chmod('opencode.json', 0)
        try:
            lines, _, writes = lane(N, settings_lines=['▸ added to %s: ask %s' % (SETTINGS, scr_ask)])
        finally:
            os.chmod('opencode.json', 0o644)
        check(not writes and '▸ to carry the new ask and deny rules into opencode.json where it lacks them (it was not read '
              'here), run: python3 .claude/probe-permissions.py --write' in lines,
              'mcp rules-ignored: an unread client file is named on its own clause (%r)' % lines)
        os.chdir(old)
        # A malformed "mcp": one line, nothing offered, the offers recorded before kept; none: as before.
        rec = {('.mcp.json', 'scrapling'): '1' * 64}
        for bad in ({'servers': 'scrapling', 'files': {}}, {'servers': ['a b'], 'files': {}},
                    {'servers': ['s'], 'files': {'../x.json': ['k']}}, {'servers': ['s'], 'files': {'x.json': []}}):
            got = mcp_lane({'mcp': bad}, {}, rec, set(), {}, {}, 'probe', [])
            check(len(got[0]) == 1 and 'not in the shape' in got[0][0] and got[1] == rec and got[2] == [],
                  'mcp malformed %r: one line, the lane skipped' % bad)
        check(mcp_lane({'settings': {}}, {}, None, set(), {}, {}, 'probe', []) == ([], None, []),
              'mcp none: a data file without "mcp" behaves as before')
    finally:
        os.chdir(old)


def answers_probe(check):
    """answers_pairs: a formatter's rewrite of the same answers reads the same; other answers, a
    value of another type and a list in another order never do; YAML it is unsure of is None."""
    copier = ("# Rendered by Copier.\n#   copier update -a .copier-answers.probe.yml\n"
              "AGENT_CLIENTS:\n- codex\n- opencode\nCODEX_MODEL: ''\nCOUNT: 32768\nFLAG: true\n"
              "GONE: null\nNOTE: A ferry pilot on a drowned coast must carry a stranger across\n"
              "    the salt marsh before the spring tide.\nSUBTITLE: 'yes'\n"
              "TEST: \"it's a tab\\tand a long\\\n    \\ tail\"\nTITLE: '007'\n_commit: v3\n"
              "_src_path: gh:Example/probe\n")
    prettier = ("---\nAGENT_CLIENTS:\n  - codex\n  - opencode\nCODEX_MODEL: \"\"\nCOUNT: 32768\n"
                "FLAG: true\nGONE: null\nNOTE:\n  A ferry pilot on a drowned coast must carry a\n"
                "  stranger across the salt marsh before the spring tide.\nSUBTITLE: \"yes\"\n"
                "TEST:\n  \"it's a tab\\tand a long\\\n  \\ tail\"\nTITLE: \"007\"\n_commit: v3\n"
                "_src_path: gh:Example/probe\n")
    flow = ("_src_path: gh:Example/probe # the source\r\n_commit: v3\r\nTITLE: \"007\"\r\n"
            "TEST: \"it's a tab\\tand a long tail\"\r\nSUBTITLE: 'yes'\r\nNOTE: A ferry pilot on a "
            "drowned coast must carry a stranger across the salt marsh before the spring tide.\r\n"
            "GONE:\r\nFLAG: true\r\nCOUNT: 32768\r\nCODEX_MODEL: ''\r\nAGENT_CLIENTS: [codex, 'opencode']")
    want = answers_pairs(copier)
    check(want is not None and json.loads(want)['TEST'] == ['s', "it's a tab\tand a long tail"],
          'answers: Copier\'s file reads as its pairs (%r)' % want)
    for label, text in (('re-indented lists, double quotes, values on the next line', prettier),
                        ('a flow list, unfolded text, another key order, comments, CRLF', flow),
                        ('a byte-order mark and no comments', '\ufeff' + copier.split('\n', 2)[2])):
        got = answers_pairs(text)
        check(got == want, 'answers: %s read as the same pairs (%r)' % (label, got))
    for label, old, new in (('a list in another order', '- codex\n- opencode', '- opencode\n- codex'),
                            ("'yes' unquoted (true)", "SUBTITLE: 'yes'", 'SUBTITLE: yes'),
                            ("'007' unquoted (7)", "TITLE: '007'", 'TITLE: 007'),
                            ('a number quoted', 'COUNT: 32768', "COUNT: '32768'"),
                            ("'' left empty (null)", "CODEX_MODEL: ''", 'CODEX_MODEL:'),
                            ('null quoted', 'GONE: null', "GONE: 'null'"),
                            ('a word changed', 'spring tide', 'neap tide'),
                            ('a list item added', '- opencode\n', '- opencode\n- gemini-cli\n'),
                            ('a list item dropped', '- opencode\n', ''),
                            ('a key dropped', 'FLAG: true\n', ''),
                            ('a key added', 'FLAG: true\n', 'FLAG: true\nMORE: x\n')):
        got = answers_pairs(copier.replace(old, new))
        check(old in copier and got is not None and got != want,
              'answers: %s reads as other pairs (%r)' % (label, got))
    for label, old, new in (('an anchor', "TITLE: '007'", "TITLE: &t '007'"),
                            ('a block scalar', 'FLAG: true', 'FLAG: |\n  true'),
                            ('a tab', 'COUNT: 32768', 'COUNT:\t32768'),
                            ('a nested mapping', 'FLAG: true', 'FLAG:\n  a: b'),
                            ('a key twice', 'FLAG: true', 'FLAG: true\nFLAG: true'),
                            ('a tag', 'FLAG: true', 'FLAG: !!str true'),
                            ('a flow list over two lines', 'AGENT_CLIENTS:\n- codex\n- opencode',
                             'AGENT_CLIENTS: [codex,\n  opencode]'),
                            ('a second document', '_commit: v3', '_commit: v3\n---\nX: y')):
        check(old in copier and answers_pairs(copier.replace(old, new)) is None,
              'answers: %s leaves the reader unsure' % label)


def allow_probe(check):
    """An ask the owner allows by server, wildcard or tool glob is reported, never added; a
    deny is covered only by the same rule."""
    deny = 'mcp__code-review-graph__embed_graph_tool'
    asks = ['mcp__scrapling__fetch', 'mcp__scrapling__bulk_fetch', 'mcp__scrapling__open_session',
            'mcp__code-review-graph__apply_refactor_tool']
    data = {'settings': {'permissions': {'deny': [deny], 'ask': asks}}}
    for allows, want_added in ((['mcp__scrapling__*', 'mcp__code-review-graph'], {deny}),
                               (['mcp__scrapling'], {deny, asks[3]}),
                               (['mcp__scrapling__*fetch'], {deny, asks[2], asks[3]}),
                               (['mcp__scrap*', 'mcp__scrapling__open'], set(asks) | {deny})):
        with tempfile.TemporaryDirectory() as d:
            old = os.getcwd()
            try:
                os.chdir(d)
                git('init', '-q')
                os.makedirs('.claude')
                with open(SETTINGS, 'w', encoding='utf-8') as f:
                    f.write(json.dumps({'permissions': {'allow': allows}}, indent=2) + '\n')
                sha = git('hash-object', '-w', '--stdin', inp=json.dumps(data['settings'], indent=2) + '\n').strip()
                lines, _ = settings_merge(data, {SETTINGS: ('100644', sha)}, None, set())
                perms = json.loads(open(SETTINGS).read())['permissions']
                got = set(perms.get('deny', [])) | set(perms.get('ask', []))
                check(got == want_added and (got == set(asks) | {deny} or any('because you allow it' in l for l in lines)),
                      'allow %r: added %r, want %r (%r)' % (allows, sorted(got), sorted(want_added), lines))
            finally:
                os.chdir(old)


def self_test():
    """Builds fake renders by hand (no Copier) and runs update and baseline against them."""
    global RENDER
    fails = []

    def check(cond, what):
        if not cond:
            fails.append(what)

    def write(base, rel, text, mode=None):
        p = os.path.join(base, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, 'w', encoding='utf-8', newline='\n') as f:
            f.write(text)
        if mode:
            os.chmod(p, mode)

    def read(base, rel):
        try:
            with open(os.path.join(base, rel), encoding='utf-8') as f:
                return f.read()
        except OSError:
            return None

    def run(cwd, *argv, env=None):
        import io
        import contextlib
        old, buf = os.getcwd(), io.StringIO()
        saved = dict(os.environ)
        os.environ.update(env or {})
        try:
            os.chdir(cwd)
            with contextlib.redirect_stdout(buf):
                main(['family-update.py', *argv])
        finally:
            os.chdir(old)
            os.environ.clear()
            os.environ.update(saved)
        return buf.getvalue()

    def sections(out):
        where, cur = {}, None
        for line in out.splitlines():
            m = re.match(r'  ([A-Z][A-Z ]+?)[:( ]', line)
            if m and not line.startswith('    '):
                cur = line.strip()
            elif re.match(r'    \S', line) and cur and not line.startswith('    …'):
                where[line.strip()] = cur
        return where

    G = ['.claude/skills/plain/SKILL.md', '.claude/skills/edited/SKILL.md',
         '.claude/skills/fresh/SKILL.md', '.claude/hooks/fresh-hook.sh']
    hook = {'hooks': [{'type': 'command', 'command': 'bash .claude/hooks/fresh-hook.sh', 'timeout': 10}]}
    releases = {
        'v1': {'README.md': 'readme 1\n', 'owned.md': 'owned 1\n', 'merged.md': 'a\nb\nc\nd\ne\n',
               'conflict.md': 'one\n', 'retired.md': 'retired 1\n', '.gitignore': 'build/\n',
               'example.md': 'example 1\n', 'CONTEXT.md': 'context 1\n',
               G[0]: 'plain 1\n', G[1]: 'edited 1\n',
               SETTINGS: '{\n  "model": "opus"\n}\n'},
    }
    v2 = dict(releases['v1'])
    v2.update({'README.md': 'readme 2\n', 'owned.md': 'owned 2\n', 'merged.md': 'a\nb\nc\nd\nE\n'})
    releases['v2'] = v2
    v3 = dict(v2)
    v3.update({'README.md': 'readme 3\n', 'owned.md': 'owned 3\n', 'merged.md': 'a\nb\nc\nd\nE3\n',
               'conflict.md': 'template three\n', '.gitignore': 'build/\n*.log\n',
               'example.md': 'example 3\n', 'CONTEXT.md': 'context 3\n', 'brand-new.md': 'new 3\n',
               'mine.md': 'template mine 3\n', G[0]: 'plain 3\n', G[1]: 'edited 3\n',
               G[2]: 'fresh 3\n', G[3]: '#!/bin/sh\nexit 0\n',
               SETTINGS: json.dumps({'model': 'opus', 'permissions': {'deny': ['Edit(build/**)', 'Bash(rm *)']},
                                     'hooks': {'UserPromptSubmit': [hook]}}, indent=2) + '\n'})
    del v3['retired.md']
    releases['v3'] = v3
    v4 = dict(v3)
    v4.update({'owned.md': 'owned 4\n', 'merged.md': 'a\nb\nc\nd\nE4\n',
               SETTINGS: json.dumps({'model': 'sonnet', 'hooks': {'UserPromptSubmit': [hook]},
                                     'permissions': {'deny': ['Edit(build/**)', 'Bash(rm *)'],
                                                     'ask': ['Bash(git push *)']}}, indent=2) + '\n'})
    releases['v4'] = v4

    with tempfile.TemporaryDirectory() as tmp:
        src, proj = os.path.join(tmp, 'tpl'), os.path.join(tmp, 'proj')
        os.makedirs(os.path.join(src, 'migrations'))
        write(src, REFRESH_DATA, json.dumps({'format': 1, 'template': 'probe', 'refresh': G, 'settings': {
            'hooks': {'UserPromptSubmit': [hook]},
            'permissions': {'deny': ['Edit(build/**)', 'Bash(rm *)'], 'ask': ['Bash(git push *)']}}}))
        git('init', '-q', src)
        shas = {}
        for v in ('v1', 'v2', 'v3', 'v4'):
            write(src, 'VERSION', v + '\n')
            git('-C', src, 'add', '-A')
            git('-C', src, 'commit', '-q', '-m', v, env=IDENT)
            git('-C', src, 'tag', v)
            shas[v] = verify(v, cwd=src)
        by_sha = {s: v for v, s in shas.items()}
        renders = []

        def fake(src_, ref, data, out):
            v = by_sha.get(verify(ref, cwd=src) or ref)
            if v is None or os.environ.get('PROBE_NO_COPIER'):
                return 'copier could not be run (probe)'
            renders.append(v)
            for rel, text in releases[v].items():
                write(out, rel, text, 0o755 if rel.endswith('.sh') else None)
            write(out, '.copier-answers.probe.yml', '_commit: %s\nNAME: probe\n' % v)
            return ''
        RENDER = fake
        A = '.copier-answers.probe.yml'
        common = ['--src', src, '--answers', A]

        # A copy at v1, its baseline, the owner at work.
        git('init', '-q', proj)
        for rel, text in releases['v1'].items():
            write(proj, rel, text)
        write(proj, A, '_commit: v1\nNAME: probe\n')
        run(proj, 'baseline', '--to', shas['v1'], *common)
        check(verify('refs/probe/template', cwd=proj), 'baseline records refs/probe/template')
        write(proj, '.gitignore', 'build/\nmine/\n')
        write(proj, 'merged.md', 'A\nb\nc\nd\ne\n')
        write(proj, 'conflict.md', 'mine one\n')
        write(proj, 'retired.md', 'retired, edited\n')
        write(proj, G[1], 'edited by the owner\n')
        write(proj, 'mine.md', 'my own file\n')
        write(proj, SETTINGS, '{\n  "model": "opus",\n  "permissions": {\n    "allow": ["Bash(rm *)"]\n  }\n}\n')
        os.remove(os.path.join(proj, 'example.md'))
        git('-C', proj, 'add', '-A')
        git('-C', proj, 'commit', '-q', '-m', 'copied and worked', env=IDENT)

        def copier_update(v_from, v_to, conflict_mode='inline'):
            """What Copier would do: deliver owned files, merge, conflict, delete, keep the rest."""
            new = releases[v_to]
            for rel in ('owned.md',):
                write(proj, rel, new[rel])
            if v_to == 'v2':
                write(proj, 'merged.md', 'A\nb\nc\nd\nE\n')
            else:
                write(proj, 'merged.md', 'A\nb\nc\nd\nE3\n')
                if conflict_mode == 'inline':
                    write(proj, 'conflict.md', '<<<<<<< before updating\nmine one\n=======\ntemplate three\n>>>>>>> after updating\n')
                    base = git('-C', proj, 'hash-object', '-w', '--stdin', inp='one\n').strip()
                    ours = git('-C', proj, 'hash-object', '-w', '--stdin', inp='mine one\n').strip()
                    theirs = git('-C', proj, 'hash-object', '-w', '--stdin', inp='template three\n').strip()
                    git('-C', proj, 'update-index', '--index-info',
                        inp='0 %s\tconflict.md\n100644 %s 1\tconflict.md\n100644 %s 2\tconflict.md\n100644 %s 3\tconflict.md\n'
                        % ('0' * 40, base, ours, theirs))
                else:
                    write(proj, 'conflict.md', 'template three\n')
                    write(proj, 'conflict.md.rej', '@@ -1 +1 @@\n-one\n+mine one\n')
                os.remove(os.path.join(proj, 'retired.md'))
            write(proj, A, '_commit: %s\nNAME: probe\n' % v_to)

        env2 = {'VERSION_FROM': 'v1', 'VERSION_PEP440_FROM': '1', 'VERSION_PEP440_TO': '2'}
        copier_update('v1', 'v2')
        out = run(proj, 'update', '--to', shas['v2'], *common, env=env2)
        s = sections(out)
        check(s.get('README.md', '').startswith('NOT UPDATED because files of this kind'), 'step 1: an unedited seed is written once (%r)' % s.get('README.md'))
        check(s.get('.gitignore') is None, 'step 1: a seed the template did not change is not listed')
        git('-C', proj, 'add', '-A')
        git('-C', proj, 'commit', '-q', '-m', 'updated to v2', env=IDENT)

        # A sibling template's record holds the bytes CONTEXT.md has here, and the project
        # committed the sibling's copy, its answers file with it (a record counts only where
        # HEAD's history held its answers).
        sib_tree_dir = os.path.join(tmp, 'sib')
        write(sib_tree_dir, 'CONTEXT.md', 'context of the sibling\n')
        env_sib = {'GIT_DIR': os.path.join(proj, '.git'), 'GIT_WORK_TREE': sib_tree_dir,
                   'GIT_INDEX_FILE': os.path.join(tmp, 'sib.index')}
        git('add', '-A', '--force', '.', env=env_sib, cwd=sib_tree_dir)
        stree = git('write-tree', env=env_sib, cwd=sib_tree_dir).strip()
        write(proj, '.copier-answers.sibling.yml', '_commit: s1\nNAME: sibling\n')
        os.chdir(proj)
        try:
            commit(stree, 'sibling render\n\ncommit: %s\nanswers: %s\n' % (
                'a' * 40, git('hash-object', '.copier-answers.sibling.yml').strip()), 'refs/sibling/template')
        finally:
            os.chdir(tmp)
        write(proj, 'CONTEXT.md', 'context of the sibling\n')
        git('-C', proj, 'add', '-A')
        git('-C', proj, 'commit', '-q', '-m', 'sibling copy', env=IDENT)

        before = git('-C', proj, 'rev-parse', 'refs/probe/template').strip()
        rej_proj = os.path.join(tmp, 'proj-rej')
        shutil.copytree(proj, rej_proj, symlinks=True)
        env3 = {'VERSION_FROM': 'v2', 'VERSION_PEP440_FROM': '2', 'VERSION_PEP440_TO': '3'}
        renders.clear()
        copier_update('v2', 'v3')
        out = run(proj, 'update', '--to', shas['v3'], *common, env=env3)
        s = sections(out)
        check(renders == ['v3'], 'B: an update with a matching record renders the new version only (%r)' % renders)
        want = {'conflict.md': 'CONFLICT', 'retired.md': 'DELETED by this update although',
                '.gitignore': 'NOT UPDATED because you had changed', G[1]: 'NOT UPDATED because you had changed',
                'README.md': 'NOT UPDATED because files of this kind', 'CONTEXT.md': "NOT UPDATED because the file holds sibling's",
                'mine.md': 'NOT UPDATED because it is new', 'example.md': 'NOT RESTORED',
                'brand-new.md': 'NOT ADDED'}
        for p, sec in want.items():
            check(s.get(p, '').startswith(sec), 'section of %s: want %r, got %r' % (p, sec, s.get(p)))
        for p in ('owned.md', 'merged.md', G[0], G[2], G[3]):
            check(p not in s, '%s is not listed (delivered, merged or refreshed)' % p)
        check(s.get(SETTINGS, '').startswith('NOT UPDATED because you had changed'), 'the settings the owner changed are listed after the entries are added')
        check(read(proj, G[0]) == 'plain 3\n', 'an unedited shared file is refreshed')
        check(read(proj, G[1]) == 'edited by the owner\n', 'an edited shared file is never overwritten')
        check(read(proj, G[2]) == 'fresh 3\n', 'a new shared file arrives')
        check(os.access(os.path.join(proj, G[3]), os.X_OK), 'a new shared hook arrives executable')
        st = json.loads(read(proj, SETTINGS))
        check(st.get('hooks', {}).get('UserPromptSubmit') == [hook], 'the new hook is wired once')
        check(st['permissions'].get('deny') == ['Edit(build/**)'], 'a new deny rule is added; an allowed one is not')
        check(st['permissions'].get('allow') == ['Bash(rm *)'], 'the owner allow rule is kept')
        check('because you allow it: deny Bash(rm *)' in out, 'the refused deny rule is reported')
        check('refreshed 1 shared file' in out and 'added 2 shared files' in out, 'the refresh lines are printed')
        changed = {l[3:] for l in git('-C', proj, 'status', '--porcelain', '-uall').splitlines()}
        beyond = changed - {'owned.md', 'merged.md', 'conflict.md', 'retired.md', A}
        check(beyond == {G[0], G[2], G[3], SETTINGS},
              'only the shared files and the settings changed beyond the update (%r)' % sorted(beyond))
        rec = git('-C', proj, 'rev-parse', 'refs/probe/template^').strip()
        check(rec == before, 'the new render is chained to the previous one')
        check(git('-C', proj, 'rev-parse', 'refs/probe/yours').strip() == git('-C', proj, 'rev-parse', 'HEAD').strip(),
              'refs/probe/yours is the pre-update HEAD')
        # Every printed command runs, offline, in a copy of the project.
        cmds = [l.split(':', 1)[1].strip() for l in out.splitlines()
                if re.match(r'\s+(compare|take|see|restore|yours):', l)]
        cmds += [l.strip() for l in out.splitlines() if l.strip().startswith('git ') and '<path>' not in l]
        for cmd in cmds:
            trial = os.path.join(tmp, 'trial')
            shutil.rmtree(trial, ignore_errors=True)
            shutil.copytree(proj, trial, symlinks=True)
            r = subprocess.run(shlex.split(cmd), cwd=trial, capture_output=True, text=True)
            check(r.returncode == 0, 'the printed command runs: %s (%s)' % (cmd, r.stderr.strip()[:80]))
        check(len(cmds) >= 12, 'the report printed its commands (%d)' % len(cmds))
        # A rerun at the same versions renders nothing and changes nothing.
        snap = (git('-C', proj, 'status', '--porcelain'), git('-C', proj, 'for-each-ref'))
        renders.clear()
        run(proj, 'update', '--to', shas['v3'], *common, env=env3)
        check(not renders and snap == (git('-C', proj, 'status', '--porcelain'), git('-C', proj, 'for-each-ref')),
              'a rerun renders nothing and changes nothing')
        # The next update at the same version is quiet.
        write(proj, 'conflict.md', 'template three\n')
        git('-C', proj, 'add', '-A')
        git('-C', proj, 'commit', '-q', '-m', 'updated to v3', env=IDENT)
        out = run(proj, 'update', '--to', shas['v3'], *common,
                  env={'VERSION_FROM': 'v3', 'VERSION_PEP440_FROM': '3', 'VERSION_PEP440_TO': '3'})
        check(out.strip().splitlines() == ['▸ probe update report, 3 → 3: the template did not change.'],
              'an update with nothing new is one quiet line (%r)' % out)
        check(not git('-C', proj, 'status', '--porcelain'), 'an update with nothing new changes nothing')

        # Rej mode, in the copy taken before step 2.
        proj_saved, proj = proj, rej_proj
        copier_update('v2', 'v3', 'rej')
        out = run(proj, 'update', '--to', shas['v3'], *common, env=env3)
        check(sections(out).get('conflict.md', '').startswith('REJECTED HUNKS'), 'rej mode: the .rej file is reported (%r)' % sections(out).get('conflict.md'))
        # The opt-out, a missing copier and a missing old version: one line each, exit 0.
        for label, env, prep in (('off', {'SYNTEK_UPDATE_REPORT': 'off'}, None),
                                 ('no copier', {'PROBE_NO_COPIER': '1'}, None),
                                 ('no old version', {'VERSION_FROM': 'v9'}, None)):
            clone = os.path.join(tmp, 'clone-' + label.replace(' ', '-'))
            git('clone', '-q', proj_saved, clone)
            out = run(clone, 'update', '--to', shas['v3'], *common, env={**env3, **env})
            # A clone holds no record: the owner's allow rule, and an entry the history keeps out,
            # are reported once more beside it.
            report = [l for l in out.strip().splitlines() if not l.startswith('▸ probe: not added')]
            check(len(report) == 1, '%s: one line (%r)' % (label, out))
        proj = proj_saved
        # The record keeps no path of this machine: no rendered answers file, no message.
        chain = git('-C', proj, 'rev-list', 'refs/probe/template').split()
        check(not git('-C', proj, 'grep', '-l', '-F', tmp, *chain, check=False).strip()
              and tmp not in git('-C', proj, 'log', '--format=%B', 'refs/probe/template'),
              'the render record holds no absolute path')
        check(all(not p.startswith('.copier-answers.') for p in tree_map_in(proj, 'refs/probe/template')),
              'the render record holds no answers file')
        check(re.search(r'^settings-offered: \d+$', git('-C', proj, 'log', '-1', '--format=%B', 'refs/probe/template'), re.M),
              'the render record lists the settings entries offered')
        # ── Later runs: each guard the refresh and the report rely on, one project each ──
        def fresh(name, v):
            d = os.path.join(tmp, name)
            git('init', '-q', d)
            for rel, text in releases[v].items():
                write(d, rel, text, 0o755 if rel.endswith('.sh') else None)
            write(d, A, '_commit: %s\nNAME: probe\n' % v)
            run(d, 'baseline', '--to', shas[v], *common)
            return d

        def commit_all(d, msg):
            git('-C', d, 'add', '-A')
            git('-C', d, 'commit', '-q', '-m', msg, env=IDENT)

        def sim_update(d, v_to):
            """Copier's update of an unedited project: template files written, retired ones deleted."""
            new = releases[v_to]
            for rel in ('owned.md', 'merged.md', 'conflict.md'):
                write(d, rel, new[rel])
            if 'retired.md' not in new and os.path.exists(os.path.join(d, 'retired.md')):
                os.remove(os.path.join(d, 'retired.md'))
            write(d, A, '_commit: %s\nNAME: probe\n' % v_to)

        def upd(d, v_from, v_to, extra=None):
            return run(d, 'update', '--to', shas[v_to], *common,
                       env={'VERSION_FROM': v_from, 'VERSION_PEP440_FROM': v_from[1:],
                            'VERSION_PEP440_TO': v_to[1:], **(extra or {})})

        # A refresh skipped (the report off, a render that failed): the next full run delivers it.
        for label, extra in (('off', {'SYNTEK_UPDATE_REPORT': 'off'}), ('failed', {'PROBE_NO_COPIER': '1'})):
            d = fresh('late-' + label, 'v2')
            commit_all(d, 'copied')
            sim_update(d, 'v3')
            upd(d, 'v2', 'v3', extra)
            check(read(d, G[2]) is None, '%s: the skipped run writes no shared file' % label)
            os.remove(os.path.join(d, G[0]))
            commit_all(d, 'updated, a shared file deleted')
            sim_update(d, 'v4')
            out = upd(d, 'v3', 'v4')
            check(read(d, G[2]) == 'fresh 3\n' and os.access(os.path.join(d, G[3]), os.X_OK),
                  '%s: the shared files a skipped refresh never wrote arrive with the next update (%r)' % (label, out))
            check(read(d, G[0]) is None, '%s: a shared file the owner deleted stays deleted' % label)
            check(has_hook(json.loads(read(d, SETTINGS)), 'UserPromptSubmit', hook),
                  '%s: the hook entry is wired beside its script' % label)

        # A recopy over a project an earlier version made, with no record: history seeded, refreshed.
        d = os.path.join(tmp, 'recopy')
        git('init', '-q', d)
        for rel, text in releases['v1'].items():
            write(d, rel, text)
        write(d, A, '_commit: v1\nNAME: probe\n')
        commit_all(d, 'copied without tasks')
        for rel, text in releases['v3'].items():
            kept = rel in ('README.md', '.gitignore', 'CONTEXT.md', 'example.md', SETTINGS) \
                or (rel in G and os.path.exists(os.path.join(d, rel)))
            if not kept:
                write(d, rel, text, 0o755 if rel.endswith('.sh') else None)
        os.remove(os.path.join(d, 'retired.md'))
        write(d, A, '_commit: v3\nNAME: probe\n')
        out = run(d, 'baseline', '--to', shas['v3'], *common)
        check(read(d, G[0]) == 'plain 3\n' and read(d, G[1]) == 'edited 3\n',
              'recopy: the unedited shared files the copy kept are refreshed (%r)' % out)
        check(verify('refs/probe/template^', cwd=d), 'recopy: the earlier render is seeded under the copy')
        commit_all(d, 'recopied')
        sim_update(d, 'v4')
        out = upd(d, 'v3', 'v4')
        check('you had changed' not in out, 'recopy: a later update names nothing as changed by the owner (%r)' % out)

        # settings.json changed only by this script: delivered, then the template's, never 'yours'.
        d = fresh('sblob', 'v2')
        commit_all(d, 'copied')
        sim_update(d, 'v3')
        out = upd(d, 'v2', 'v3')
        check(SETTINGS not in sections(out), 'settings: the release\'s entries added count as delivered (%r)' % out)
        commit_all(d, 'updated')
        sim_update(d, 'v4')
        out = upd(d, 'v3', 'v4')
        check(sections(out).get(SETTINGS, '').startswith('NOT UPDATED because files of this kind'),
              'settings: a file only this script changed is written once, not yours (%r)' % sections(out).get(SETTINGS))
        check(has_rule(json.loads(read(d, SETTINGS)), 'ask', 'Bash(git push *)'), 'settings: v4\'s ask rule is added')

        # The record alone knows an entry was offered: the owner removed it before any commit.
        d = fresh('srecord', 'v2')
        commit_all(d, 'copied')
        sim_update(d, 'v3')
        upd(d, 'v2', 'v3')
        st = json.loads(read(d, SETTINGS))
        st.pop('hooks', None)
        write(d, SETTINGS, json.dumps(st, indent=2) + '\n')
        commit_all(d, 'updated, the hook removed')
        sim_update(d, 'v4')
        upd(d, 'v3', 'v4')
        check(not has_hook(json.loads(read(d, SETTINGS)), 'UserPromptSubmit', hook),
              'recorded: a hook the record lists as offered is not added back, though no commit held it')

        # An update discarded (git reset --hard with git clean -fd; git stash -u) and run again
        # delivers what the first run did, recorded afresh on the record HEAD committed; a hand
        # rerun over the redo's uncommitted tree adds nothing and records nothing.
        def state(d):
            out = {}
            for entry in git('-C', d, 'status', '--porcelain', '-uall', '-z').split('\0'):
                if entry:
                    out[entry[3:]] = (entry[:2], read(d, entry[3:]))
            return out
        for how in ('reset', 'stash'):
            d = fresh('discard-' + how, 'v2')
            commit_all(d, 'copied')
            base_rec = git('-C', d, 'rev-parse', 'refs/probe/template').strip()
            sim_update(d, 'v3')
            upd(d, 'v2', 'v3')
            first, first_rec = state(d), git('-C', d, 'rev-parse', 'refs/probe/template').strip()
            if how == 'reset':
                git('-C', d, 'reset', '-q', '--hard')
                git('-C', d, 'clean', '-q', '-fd')
            else:
                git('-C', d, 'stash', 'push', '-q', '-u', env=IDENT)
            check(not git('-C', d, 'status', '--porcelain'), '%s: the update is discarded' % how)
            sim_update(d, 'v3')
            out = upd(d, 'v2', 'v3')
            again, rec = state(d), git('-C', d, 'rev-parse', 'refs/probe/template').strip()
            check(again == first and read(d, G[2]) == 'fresh 3\n' and has_hook(json.loads(read(d, SETTINGS)), 'UserPromptSubmit', hook),
                  '%s: the second run delivers what the first did (%r)' % (how, sorted(set(first.items()) ^ set(again.items()))))
            msg = git('-C', d, 'log', '-1', '--format=%B', rec)
            first_msg = git('-C', d, 'log', '-1', '--format=%B', first_rec)
            check(git('-C', d, 'rev-parse', rec + '^').strip() == base_rec
                  and offered_ids(msg) == offered_ids(first_msg) and written_blobs(msg) == written_blobs(first_msg)
                  and not set(G) & set(sections(out)),
                  '%s: the second run is recorded afresh on the record HEAD committed (%r)' % (how, out))
            snap = (git('-C', d, 'status', '--porcelain'), git('-C', d, 'for-each-ref'))
            upd(d, 'v2', 'v3')
            check(snap == (git('-C', d, 'status', '--porcelain'), git('-C', d, 'for-each-ref')),
                  '%s: a hand rerun over the uncommitted tree adds nothing and records nothing' % how)

        # An update discarded, then an update to a later release: the discarded record is never
        # read, so the result is a direct update's, its offers and written blobs included, and the
        # record sits on the one HEAD committed. A sibling's discarded record is not read either.
        def record_of(d):
            msg = git('-C', d, 'log', '-1', '--format=%B', 'refs/probe/template')
            return offered_ids(msg), offered_mcp(msg), written_blobs(msg)
        direct = fresh('later-direct', 'v2')
        commit_all(direct, 'copied')
        sim_update(direct, 'v4')
        upd(direct, 'v2', 'v4')
        d = fresh('later-discarded', 'v2')
        commit_all(d, 'copied')
        base_rec = git('-C', d, 'rev-parse', 'refs/probe/template').strip()
        sim_update(d, 'v3')
        upd(d, 'v2', 'v3')
        git('-C', d, 'reset', '-q', '--hard')
        git('-C', d, 'clean', '-q', '-fd')
        sim_update(d, 'v4')
        out = upd(d, 'v2', 'v4')
        check(state(d) == state(direct) and read(d, G[2]) == 'fresh 3\n' and has_hook(json.loads(read(d, SETTINGS)), 'UserPromptSubmit', hook)
              and has_rule(json.loads(read(d, SETTINGS)), 'ask', 'Bash(git push *)'),
              'later: an update discarded, then one to a later release, gives what a direct update gives (%r)'
              % sorted(set(state(d).items()) ^ set(state(direct).items())))
        check(record_of(d) == record_of(direct) and git('-C', d, 'rev-parse', 'refs/probe/template^').strip() == base_rec,
              'later: the offers and the written blobs are a direct update\'s, on the record HEAD committed (%r)' % out)
        write(d, '.copier-answers.sibling.yml', '_commit: s1\nNAME: sibling\n')
        commit_all(d, 'updated, and a sibling copied')
        os.chdir(d)
        try:
            chain = commit(git('rev-parse', 'refs/probe/template^{tree}').strip(),
                           'sibling render\n\ncommit: %s\nanswers: %s\n' % (
                               'c' * 40, git('rev-parse', 'HEAD:.copier-answers.sibling.yml').strip()))
            sib = git('hash-object', '-w', '--stdin', inp='sibling, discarded\n').strip()
            idx = os.path.join(tmp, 'sib-later.index')
            git('read-tree', 'refs/probe/template', env={'GIT_INDEX_FILE': idx})
            git('update-index', '--add', '--cacheinfo', '100644,%s,README.md' % sib, env={'GIT_INDEX_FILE': idx})
            later = git('write-tree', env={'GIT_INDEX_FILE': idx}).strip()
            commit(later, 'sibling render, discarded\n\ncommit: %s\nanswers: %s\n' % ('d' * 40, 'e' * 40),
                   'refs/sibling/template', chain)
            hist = others_history('probe').get('sibling', {})
        finally:
            os.chdir(tmp)
        check(sib not in hist.get('README.md', ()) and hist.get('README.md'),
              'later: a sibling\'s record HEAD never committed is not read (%r)' % hist.get('README.md'))

        # A recopy discarded, then made again: the baseline reads the record HEAD committed, not
        # the discarded copy's, so the second recopy wires the hook and the deny again, on it.
        def recopy_v3(d, extra=None):
            for rel, text in releases['v3'].items():
                if rel != SETTINGS:
                    write(d, rel, text, 0o755 if rel.endswith('.sh') else None)
            if os.path.exists(os.path.join(d, 'retired.md')):
                os.remove(os.path.join(d, 'retired.md'))
            write(d, A, '_commit: v3\nNAME: probe\n')
            return run(d, 'baseline', '--to', shas['v3'], *common, env=extra)
        d = fresh('recopy-discarded', 'v2')
        commit_all(d, 'copied')
        base_rec = git('-C', d, 'rev-parse', 'refs/probe/template').strip()
        recopy_v3(d)
        first = has_hook(json.loads(read(d, SETTINGS)), 'UserPromptSubmit', hook)
        git('-C', d, 'reset', '-q', '--hard')
        git('-C', d, 'clean', '-q', '-fd')
        out = recopy_v3(d)
        st = json.loads(read(d, SETTINGS))
        check(first and has_hook(st, 'UserPromptSubmit', hook) and has_rule(st, 'deny', 'Bash(rm *)')
              and git('-C', d, 'rev-parse', 'refs/probe/template^').strip() == base_rec,
              'baseline: a recopy discarded and made again wires the hook and the deny again, on the record '
              'HEAD committed (%r)' % out)

        # A moving adoption (copier copy --overwrite into a repository whose HEAD holds no answers
        # file) discarded and made again: HEAD's history never held the discarded copy's answers,
        # so the second baseline reads no record and wires the hook, the deny and the ask again.
        def adopt_v4(d):
            for rel, text in releases['v4'].items():
                if rel != SETTINGS:   # a seed: the copy keeps the owner's settings.json
                    write(d, rel, text, 0o755 if rel.endswith('.sh') else None)
            write(d, A, '_commit: v4\nNAME: probe\n')
            return run(d, 'baseline', '--to', shas['v4'], *common)
        d = os.path.join(tmp, 'adopt-discarded')
        git('init', '-q', d)
        write(d, SETTINGS, '{\n  "model": "opus"\n}\n')
        write(d, 'notes.md', 'my own notes\n')
        commit_all(d, 'my own project')
        adopt_v4(d)
        st = json.loads(read(d, SETTINGS))
        first = has_hook(st, 'UserPromptSubmit', hook) and has_rule(st, 'ask', 'Bash(git push *)')
        git('-C', d, 'reset', '-q', '--hard')
        git('-C', d, 'clean', '-q', '-fd')
        out = adopt_v4(d)
        st = json.loads(read(d, SETTINGS))
        check(first and has_hook(st, 'UserPromptSubmit', hook) and has_rule(st, 'deny', 'Edit(build/**)')
              and has_rule(st, 'deny', 'Bash(rm *)') and has_rule(st, 'ask', 'Bash(git push *)')
              and not verify('refs/probe/template^', cwd=d),
              'adoption: a moving adoption discarded and made again wires the hook, the deny and the ask '
              'again, on no record (%r)' % out)

        # A sibling's copy discarded (its record left, its answers file never committed): its
        # render is not read, so a shared file new in this release that it held is no file the
        # owner deleted, and the update adds it.
        d = fresh('sibling-discarded', 'v2')
        commit_all(d, 'copied')
        os.chdir(d)
        try:
            dis_blob = git('hash-object', '-w', '--stdin', inp='fresh, from the sibling\n').strip()
            dis_idx = os.path.join(tmp, 'sib-discarded.index')
            git('update-index', '--add', '--cacheinfo', '100644,%s,%s' % (dis_blob, G[2]),
                env={'GIT_INDEX_FILE': dis_idx})
            commit(git('write-tree', env={'GIT_INDEX_FILE': dis_idx}).strip(),
                   'sibling render, copied\n\ncommit: %s\nanswers: %s\n' % (
                       'c' * 40, git('hash-object', '--stdin', inp='_commit: s1\nNAME: sibling\n').strip()),
                   'refs/sibling/template')
            left_out = 'sibling' not in others_history('probe')
        finally:
            os.chdir(tmp)
        sim_update(d, 'v3')
        out = upd(d, 'v2', 'v3')
        check(left_out and read(d, G[2]) == 'fresh 3\n',
              'sibling discarded: its render is not read, so a shared file new in this release arrives (%r)' % out)

        # An update discarded, then an update with the report off committed (it records nothing),
        # then a full update: the discarded record is never read, so the result, its offers and
        # written blobs included, is what the same updates give without the discard.
        direct = fresh('off-direct', 'v1')
        commit_all(direct, 'copied')
        sim_update(direct, 'v2')
        upd(direct, 'v1', 'v2', {'SYNTEK_UPDATE_REPORT': 'off'})
        commit_all(direct, 'updated, the report off')
        sim_update(direct, 'v4')
        upd(direct, 'v2', 'v4')
        d = fresh('off-discarded', 'v1')
        commit_all(d, 'copied')
        base_rec = git('-C', d, 'rev-parse', 'refs/probe/template').strip()
        sim_update(d, 'v3')
        upd(d, 'v1', 'v3')
        git('-C', d, 'reset', '-q', '--hard')
        git('-C', d, 'clean', '-q', '-fd')
        sim_update(d, 'v2')
        upd(d, 'v1', 'v2', {'SYNTEK_UPDATE_REPORT': 'off'})
        commit_all(d, 'updated, the report off')
        sim_update(d, 'v4')
        out = upd(d, 'v2', 'v4')
        check(state(d) == state(direct) and record_of(d) == record_of(direct) and read(d, G[2]) == 'fresh 3\n'
              and has_hook(json.loads(read(d, SETTINGS)), 'UserPromptSubmit', hook)
              and git('-C', d, 'rev-parse', 'refs/probe/template~2').strip() == base_rec,
              'off: an update discarded, then one with the report off committed, then a full update gives '
              'what they give without the discard (%r)' % sorted(set(state(d).items()) ^ set(state(direct).items())))

        # The same at the release and answers the discarded update recorded: the run with the
        # report off finds the work tree back at HEAD where that record wrote, so it sets the
        # record back to the one HEAD committed, and committing the run never makes the discarded
        # record count. A hand rerun with the report off over the first run's writes keeps the
        # record, so an entry the owner removed after committing stays removed.
        same_direct = fresh('same-off-direct', 'v1')
        commit_all(same_direct, 'copied')
        sim_update(same_direct, 'v3')
        upd(same_direct, 'v1', 'v3', {'SYNTEK_UPDATE_REPORT': 'off'})
        commit_all(same_direct, 'updated, the report off')
        sim_update(same_direct, 'v4')
        upd(same_direct, 'v3', 'v4')
        d = fresh('same-off-discarded', 'v1')
        commit_all(d, 'copied')
        base_rec = git('-C', d, 'rev-parse', 'refs/probe/template').strip()
        sim_update(d, 'v3')
        upd(d, 'v1', 'v3')
        git('-C', d, 'reset', '-q', '--hard')
        git('-C', d, 'clean', '-q', '-fd')
        sim_update(d, 'v3')
        upd(d, 'v1', 'v3', {'SYNTEK_UPDATE_REPORT': 'off'})
        back = git('-C', d, 'rev-parse', 'refs/probe/template').strip() == base_rec
        commit_all(d, 'updated, the report off')
        sim_update(d, 'v4')
        out = upd(d, 'v3', 'v4')
        st = json.loads(read(d, SETTINGS))
        check(back and state(d) == state(same_direct) and record_of(d) == record_of(same_direct) and read(d, G[2]) == 'fresh 3\n'
              and has_hook(st, 'UserPromptSubmit', hook) and has_rule(st, 'deny', 'Bash(rm *)'),
              'same-off: an update discarded, then one to the same release with the report off committed, then a '
              'full update gives what they give without the discard (%r)' % sorted(set(state(d).items()) ^ set(state(same_direct).items())))
        d = fresh('same-off-rerun', 'v1')
        commit_all(d, 'copied')
        sim_update(d, 'v3')
        upd(d, 'v1', 'v3')
        first_rec = git('-C', d, 'rev-parse', 'refs/probe/template').strip()
        upd(d, 'v1', 'v3', {'SYNTEK_UPDATE_REPORT': 'off'})
        kept = git('-C', d, 'rev-parse', 'refs/probe/template').strip() == first_rec
        commit_all(d, 'updated')
        st = json.loads(read(d, SETTINGS))
        st['permissions']['deny'].remove('Bash(rm *)')
        write(d, SETTINGS, json.dumps(st, indent=2) + '\n')
        commit_all(d, 'the deny removed')
        sim_update(d, 'v4')
        out = upd(d, 'v3', 'v4')
        st = json.loads(read(d, SETTINGS))
        check(kept and not has_rule(st, 'deny', 'Bash(rm *)') and has_rule(st, 'ask', 'Bash(git push *)'),
              'same-off: a hand rerun with the report off over the first run\'s writes keeps the record, so a deny '
              'the owner removed after committing stays removed (%r)' % out)

        # A recopy discarded, then made again at the same release with the report off or a render
        # that failed (it records nothing) and committed: the discarded copy's record is set back,
        # so the next update wires the hook and the deny. A hand rerun of the baseline with the
        # report off over the first copy's writes keeps the record.
        for label, extra in (('off', {'SYNTEK_UPDATE_REPORT': 'off'}), ('failed', {'PROBE_NO_COPIER': '1'})):
            same_direct = fresh('recopy-%s-direct' % label, 'v2')
            commit_all(same_direct, 'copied')
            recopy_v3(same_direct, extra)
            commit_all(same_direct, 'recopied')
            sim_update(same_direct, 'v4')
            upd(same_direct, 'v3', 'v4')
            d = fresh('recopy-%s-discarded' % label, 'v2')
            commit_all(d, 'copied')
            base_rec = git('-C', d, 'rev-parse', 'refs/probe/template').strip()
            recopy_v3(d)
            git('-C', d, 'reset', '-q', '--hard')
            git('-C', d, 'clean', '-q', '-fd')
            recopy_v3(d, extra)
            back = git('-C', d, 'rev-parse', 'refs/probe/template').strip() == base_rec
            commit_all(d, 'recopied')
            sim_update(d, 'v4')
            out = upd(d, 'v3', 'v4')
            st = json.loads(read(d, SETTINGS))
            check(back and state(d) == state(same_direct) and record_of(d) == record_of(same_direct)
                  and has_hook(st, 'UserPromptSubmit', hook) and has_rule(st, 'deny', 'Bash(rm *)'),
                  'recopy-%s: a recopy discarded, then made again at the same release with nothing recorded and '
                  'committed: the next update gives what it gives without the discard (%r)' % (
                      label, sorted(set(state(d).items()) ^ set(state(same_direct).items()))))
        d = fresh('recopy-rerun', 'v2')
        commit_all(d, 'copied')
        recopy_v3(d)
        first_rec = git('-C', d, 'rev-parse', 'refs/probe/template').strip()
        run(d, 'baseline', '--to', shas['v3'], *common, env={'SYNTEK_UPDATE_REPORT': 'off'})
        kept = git('-C', d, 'rev-parse', 'refs/probe/template').strip() == first_rec
        commit_all(d, 'recopied')
        st = json.loads(read(d, SETTINGS))
        st['permissions']['deny'].remove('Bash(rm *)')
        write(d, SETTINGS, json.dumps(st, indent=2) + '\n')
        commit_all(d, 'the deny removed')
        sim_update(d, 'v4')
        out = upd(d, 'v3', 'v4')
        check(kept and not has_rule(json.loads(read(d, SETTINGS)), 'deny', 'Bash(rm *)'),
              'recopy: a hand rerun of the baseline with the report off keeps the record, so a deny the owner '
              'removed after committing stays removed (%r)' % out)

        # A shared file or folder the update cannot write (a file at mode 444, a skills folder at
        # 555): the first run reports it, and a hand rerun with the report off finds nothing there
        # it could refresh or add, so it keeps the record, and a deny the owner removed after
        # committing stays removed. Skipped as root, who can write anything.
        if os.geteuid() != 0:
            for label, locked, mode in (('a read-only shared file', G[0], 0o444),
                                        ('a shared folder it cannot write', '.claude/skills', 0o555)):
                d = fresh('locked-rerun-%o' % mode, 'v1')
                commit_all(d, 'copied')
                p = os.path.join(d, locked)
                was = os.stat(p).st_mode & 0o777
                os.chmod(p, mode)
                try:
                    sim_update(d, 'v3')
                    first = upd(d, 'v1', 'v3')
                    first_rec = git('-C', d, 'rev-parse', 'refs/probe/template').strip()
                    upd(d, 'v1', 'v3', {'SYNTEK_UPDATE_REPORT': 'off'})
                    kept = git('-C', d, 'rev-parse', 'refs/probe/template').strip() == first_rec
                    commit_all(d, 'updated')
                    st = json.loads(read(d, SETTINGS))
                    st['permissions']['deny'].remove('Bash(rm *)')
                    write(d, SETTINGS, json.dumps(st, indent=2) + '\n')
                    commit_all(d, 'the deny removed')
                    sim_update(d, 'v4')
                    out = upd(d, 'v3', 'v4')
                finally:
                    os.chmod(p, was)
                check('could not write 1 shared file' in first and kept
                      and not has_rule(json.loads(read(d, SETTINGS)), 'deny', 'Bash(rm *)'),
                      '%s: the first run reports it, and a hand rerun with the report off keeps the record, '
                      'so a deny the owner removed after committing stays removed (%r)' % (label, out))

        # A formatter rewrites the answers file before every commit ('---', other quotes, a
        # comment, another key order): each record still matches the answers HEAD committed, so a
        # deny the owner removed before committing stays removed and the records are the plain
        # flow's. A rewrite that changes the answers matches no record of them, as before.
        def formatted(d, msg, name='probe'):
            v = re.search(r'^_commit: (\S+)', read(d, A), re.M).group(1)
            write(d, A, "---\nNAME: '%s'   # formatted\n_commit: %s\n" % (name, v))
            commit_all(d, msg)
        flows = {}
        for label, cm in (('plain', commit_all), ('formatted', formatted)):
            d = fresh('fmt-' + label, 'v2')
            cm(d, 'copied')
            sim_update(d, 'v3')
            upd(d, 'v2', 'v3')
            st = json.loads(read(d, SETTINGS))
            st['permissions']['deny'].remove('Bash(rm *)')
            write(d, SETTINGS, json.dumps(st, indent=2) + '\n')
            cm(d, 'updated, a deny removed')
            sim_update(d, 'v4')
            out = upd(d, 'v3', 'v4')
            flows[label] = (has_rule(json.loads(read(d, SETTINGS)), 'deny', 'Bash(rm *)'), record_of(d),
                            git('-C', d, 'rev-list', '--count', 'refs/probe/template').strip(), out)
        check(not flows['formatted'][0] and flows['formatted'][1:] == flows['plain'][1:],
              'formatter: a deny removed before the commit stays removed, the records the plain '
              'flow\'s (%r)' % (flows['formatted'],))
        d = fresh('fmt-other', 'v2')
        commit_all(d, 'copied')
        sim_update(d, 'v3')
        upd(d, 'v2', 'v3')
        tip_rec = git('-C', d, 'rev-parse', 'refs/probe/template').strip()
        formatted(d, 'updated, the answers changed', 'other')
        os.chdir(d)
        try:
            base, _ = committed_record(ref_info('refs/probe/template'), None,
                                       git('rev-parse', 'HEAD:' + A).strip(), answers_held(A))
        finally:
            os.chdir(tmp)
        check(base and base['sha'] != tip_rec,
              'formatter: a rewrite that changes the answers matches no record of them')
        # With the formatter, a hand rerun over a tree whose answers file it rewrote adds and
        # records nothing; and an update discarded, then one with the report off, then a full
        # update give what off-direct above gives.
        d = fresh('fmt-rerun', 'v2')
        formatted(d, 'copied')
        sim_update(d, 'v3')
        upd(d, 'v2', 'v3')
        write(d, A, '# formatted\n_commit: v3\nNAME: "probe"\n')
        snap = (git('-C', d, 'status', '--porcelain'), git('-C', d, 'for-each-ref'))
        upd(d, 'v2', 'v3')
        check(snap == (git('-C', d, 'status', '--porcelain'), git('-C', d, 'for-each-ref')),
              'formatter: a hand rerun over the rewritten answers file adds and records nothing')
        d = fresh('fmt-off', 'v1')
        formatted(d, 'copied')
        base_rec = git('-C', d, 'rev-parse', 'refs/probe/template').strip()
        sim_update(d, 'v3')
        upd(d, 'v1', 'v3')
        git('-C', d, 'reset', '-q', '--hard')
        git('-C', d, 'clean', '-q', '-fd')
        sim_update(d, 'v2')
        upd(d, 'v1', 'v2', {'SYNTEK_UPDATE_REPORT': 'off'})
        formatted(d, 'updated, the report off')
        sim_update(d, 'v4')
        upd(d, 'v2', 'v4')
        st, direct_st = state(d), state(direct)
        st.pop(A, None)
        direct_st.pop(A, None)
        check(st == direct_st and record_of(d) == record_of(direct)
              and git('-C', d, 'rev-parse', 'refs/probe/template~2').strip() == base_rec,
              'formatter: an update discarded, then one with the report off, then a full update give '
              'what they give without the discard (%r)' % sorted(set(st.items()) ^ set(direct_st.items())))
        # A recopy over a record an older script wrote (no 'answers-key: ' line) whose answers file
        # the formatter rewrote before the commit, so git never stored the record's answers blob:
        # the recopy's answers file holds those same bytes, and its record still keeps their key,
        # so a deny the owner removed after the recopy stays removed on the next update. Each run
        # is a process of its own, so the cache of answers keys is emptied before the recopy and
        # before the update.
        def drop_deny(d):
            st = json.loads(read(d, SETTINGS))
            st['permissions']['deny'] = [r for r in st['permissions']['deny'] if r != 'Bash(rm *)']
            write(d, SETTINGS, json.dumps(st, indent=2) + '\n')
        d = os.path.join(tmp, 'fmt-old-tip')
        git('init', '-q', d)
        for rel, text in releases['v3'].items():
            write(d, rel, text, 0o755 if rel.endswith('.sh') else None)
        write(d, A, '_commit: v3\nNAME: key\n')
        run(d, 'baseline', '--to', shas['v3'], *common)
        os.chdir(d)
        try:
            old = ref_info('refs/probe/template')
            commit(old['tree'], re.sub(r'^answers-key: \S+\n', '', old['msg'], flags=re.M),
                   'refs/probe/template', old['parent'])
        finally:
            os.chdir(tmp)
        drop_deny(d)
        formatted(d, 'copied, a deny removed', 'key')
        write(d, A, '_commit: v3\nNAME: key\n')
        _ANSWERS.clear()
        run(d, 'baseline', '--to', shas['v3'], *common)
        keyed = re.search(r'^answers-key: [0-9a-f]{64}$',
                          git('-C', d, 'log', '-1', '--format=%B', 'refs/probe/template'), re.M)
        drop_deny(d)   # the recopy, whose base record it could not match, added it back
        sim_update(d, 'v4')
        write(d, A, '_commit: v4\nNAME: key\n')
        _ANSWERS.clear()
        out = upd(d, 'v3', 'v4')
        check(keyed and not has_rule(json.loads(read(d, SETTINGS)), 'deny', 'Bash(rm *)'),
              'formatter: a recopy over a record without its answers key, whose answers bytes equal the '
              'recopy\'s, writes the key, so a deny the owner removed stays removed (%r)' % out)

        # Where HEAD cannot say which records it committed, the tip is read, as where there is no
        # HEAD. Git ignores the answers file, so no commit holds it: a hook the tip offered, which
        # the owner removed before committing, stays removed, and the next record follows the tip.
        d = fresh('answers-ignored', 'v2')
        write(d, '.gitignore', 'build/\n/%s\n' % A)
        commit_all(d, 'copied, the answers file ignored')
        sim_update(d, 'v3')
        upd(d, 'v2', 'v3')
        tip_rec = git('-C', d, 'rev-parse', 'refs/probe/template').strip()
        st = json.loads(read(d, SETTINGS))
        st.pop('hooks', None)
        write(d, SETTINGS, json.dumps(st, indent=2) + '\n')
        commit_all(d, 'updated, the hook removed')
        sim_update(d, 'v4')
        out = upd(d, 'v3', 'v4')
        check(not git('-C', d, 'ls-files', A) and not has_hook(json.loads(read(d, SETTINGS)), 'UserPromptSubmit', hook)
              and tip_rec in git('-C', d, 'rev-list', 'refs/probe/template').split(),
              'answers ignored: the tip is read, so a hook it offered that the owner removed stays removed (%r)' % out)
        # Git cannot say whether it ignores the answers file (check-ignore exits 128 for that file
        # alone, through a git first on PATH that runs the real one for everything else): the tip
        # is read, where a git that can say gives the record whose answers HEAD's history held.
        d = fresh('answers-unsure', 'v2')
        commit_all(d, 'copied')
        sim_update(d, 'v3')
        upd(d, 'v2', 'v3')
        tip_rec = git('-C', d, 'rev-parse', 'refs/probe/template').strip()
        formatted(d, 'updated, the answers changed', 'other')
        unsure = os.path.join(tmp, 'unsure-bin')
        write(unsure, 'git', '#!/bin/sh\ncase " $* " in *" check-ignore "*" %s "*) exit 128 ;; esac\nexec %s "$@"\n'
              % (A, shlex.quote(shutil.which('git'))), 0o755)
        read_as, path = {}, os.environ.get('PATH', '')
        os.chdir(d)
        try:
            for label, p in (('sure', path), ('unsure', unsure + os.pathsep + path)):
                os.environ['PATH'] = p
                base, _ = committed_record(ref_info('refs/probe/template'), None,
                                           git('rev-parse', 'HEAD:' + A).strip(), answers_held(A))
                read_as[label] = (ignored(A), base and base['sha'] == tip_rec)
        finally:
            os.environ['PATH'] = path
            os.chdir(tmp)
        check(read_as == {'sure': (False, False), 'unsure': (None, True)},
              'answers unsure: where git cannot say whether it ignores the answers file, the tip is read (%r)' % read_as)

        # A settings.json git ignores (mode 000: never read) the new version changes: one line
        # names the entries to add by hand, the file is listed as not compared, nothing is
        # recorded as offered, and the next update names them again.
        d = fresh('signored', 'v2')
        commit_all(d, 'copied')
        write(d, '.gitignore', 'build/\n/.claude/settings.json\n')
        git('-C', d, 'rm', '-q', '--cached', SETTINGS)
        commit_all(d, 'the owner ignores settings.json')
        sim_update(d, 'v3')
        os.chmod(os.path.join(d, SETTINGS), 0)
        try:
            out = upd(d, 'v2', 'v3')
        finally:
            os.chmod(os.path.join(d, SETTINGS), 0o644)
        line = '%s is ignored by git, so it was not read' % SETTINGS
        check(out.count(line) == 1 and 'stopped' not in out and read(d, SETTINGS) == releases['v2'][SETTINGS]
              and sections(out).get(SETTINGS, '').startswith('NOT COMPARED because git ignores them')
              and not any(l.startswith('settings: hook') for l in git('-C', d, 'log', '-1', '--format=%B', 'refs/probe/template').splitlines()),
              'settings ignored: never read or written, one line, not compared, nothing recorded (%r)' % out)
        commit_all(d, 'updated')
        sim_update(d, 'v4')
        out = upd(d, 'v3', 'v4')
        check(out.count(line) == 1 and 'UserPromptSubmit hook' in out, 'settings ignored: the next update names the entries again (%r)' % out)

        # Guards: a branch and a tag called template, a foreign commit at the record's ref, stale
        # and ignored .rej files, an uncommitted change, an unedited retired file.
        d = fresh('probes', 'v2')
        write(d, 'README.md', 'my readme\n')
        write(d, G[0], 'MY OWN SKILL\n')
        write(d, G[1], 'custom\n')
        write(d, 'owned.md.rej', 'stale\n')
        write(d, '.gitignore', 'build/\nvendor/\n')
        write(d, 'vendor/pkg/fix.c', 'x\n')
        write(d, 'vendor/pkg/fix.c.rej', 'y\n')
        commit_all(d, 'worked')
        git('-C', d, 'branch', 'template')
        git('-C', d, 'tag', 'template')
        git('-C', d, 'update-ref', 'refs/probe/template', 'HEAD')
        write(d, G[1], 'edited 1\n')
        sim_update(d, 'v3')
        out = upd(d, 'v2', 'v3')
        s = sections(out)
        check(s.get('README.md', '').startswith('NOT UPDATED because you had changed'),
              'a branch or tag called template is no sibling (%r)' % s.get('README.md'))
        check(read(d, G[0]) == 'MY OWN SKILL\n' and s.get(G[0], '').startswith('NOT UPDATED because you had changed'),
              'a commit at the record\'s ref that is no record is never trusted (%r)' % s.get(G[0]))
        check(all(is_record(git('-C', d, 'log', '-1', '--format=%B', c))
                  for c in git('-C', d, 'rev-list', 'refs/probe/template').split()),
              'the new record is never chained onto a commit that is no record')
        check('REJECTED' not in out and 'owned.md' not in s and 'vendor/pkg/fix.c' not in s,
              'a stale or ignored .rej is no conflict of this update (%r)' % out)
        check(read(d, G[1]) == 'edited 1\n', 'a shared file whose work tree differs from HEAD is never refreshed')
        check('retired.md' not in s, 'an unedited retired file is delivered, not listed (%r)' % s.get('retired.md'))
        os.chdir(d)
        try:
            others = others_history('probe')
            check(not set(others) & {'probe', 'heads', 'tags'}, 'others_history names no own or Git ref (%r)' % sorted(others))
        finally:
            os.chdir(tmp)
        # A renamed path keeps its blob in a chain's history; a commit that is no record ends it.
        d = os.path.join(tmp, 'chain')
        git('init', '-q', d)
        os.chdir(d)
        try:
            write(d, 'zz/before.md', 'renamed\n')
            git('add', 'zz/before.md')
            tail = '\n\ncommit: %s\nanswers: %s\n' % ('c' * 40, 'd' * 40)
            git('commit', '-q', '-m', 'r1' + tail, env=IDENT)
            git('mv', 'zz/before.md', 'zz/after.md')
            git('commit', '-q', '-m', 'r2' + tail, env=IDENT)
            hist = history('HEAD')
            check('zz/after.md' in hist and 'zz/before.md' in hist, 'history keeps both paths of a rename (%r)' % sorted(hist))
            git('commit', '-q', '--allow-empty', '-m', 'not a record', env=IDENT)
            check(not history('HEAD'), 'history stops at a commit that is no record')
        finally:
            os.chdir(tmp)

        # A shared folder that is a link (inside the project, or out of it) is never written through.
        d = fresh('linked', 'v2')
        outside = os.path.join(tmp, 'outside-hooks')
        os.makedirs(outside)
        os.makedirs(os.path.join(d, 'elsewhere', 'fresh'))
        write(d, 'elsewhere/fresh/.keep', '')
        os.symlink('../../elsewhere/fresh', os.path.join(d, '.claude/skills/fresh'))
        os.symlink(outside, os.path.join(d, '.claude/hooks'))
        commit_all(d, 'linked')
        sim_update(d, 'v3')
        upd(d, 'v2', 'v3')
        check(not os.path.exists(os.path.join(d, 'elsewhere/fresh/SKILL.md')) and not os.listdir(outside),
              'a shared folder that is a link is never written through')
        check(not inside(os.path.join(d, '.claude/hooks'), os.path.realpath(d))
              and inside(os.path.join(d, '.claude/skills'), os.path.realpath(d)),
              'inside() tells a folder outside the project from one in it')

        # A shared file that cannot be written: reported, and the report and the record still follow.
        if os.geteuid() != 0:
            d = fresh('readonly', 'v2')
            os.chmod(os.path.join(d, G[0]), 0o444)
            commit_all(d, 'copied')
            sim_update(d, 'v3')
            out = upd(d, 'v2', 'v3')
            msg = git('-C', d, 'log', '-1', '--format=%B', 'refs/probe/template')
            check('could not write 1 shared file' in out and 'update report' in out
                  and ('commit: %s' % shas['v3']) in msg,
                  'an unwritable shared file is reported, and the update is still reported and recorded (%r)' % out)

        # family-refresh.json that does not parse, or has the wrong shape: nothing refreshed, said.
        import io
        import contextlib
        for label, text in (('truncated', '{"format": 1,'),
                            ('list', json.dumps({'format': 1, 'template': 'probe', 'refresh': [], 'settings': []}))):
            bad = os.path.join(tmp, 'bad-' + label)
            write(bad, REFRESH_DATA, text)
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                got = refresh_data(bad, 'probe')
            check(got is None and 'nothing refreshed' in buf.getvalue(),
                  'a %s family-refresh.json refreshes nothing and says so (%r)' % (label, buf.getvalue()))

        settings_probe(os.path.join(tmp, 'settings'), check)
        for probe in (lambda: mcp_probe(os.path.join(tmp, 'mcp'), check), lambda: allow_probe(check),
                      lambda: answers_probe(check), lambda: history_probe(os.path.join(tmp, 'history'), check)):
            try:
                probe()
            except Exception as err:   # a probe that raises is a failure, never a crash
                check(False, 'a probe raised %s: %s' % (type(err).__name__, err))

        # ── The read-only folders: restore ──
        # The data lists how-to under "restore": every update that runs in full puts the new
        # render's bytes back on each file it holds there that differs, a sibling's shared
        # version and a file Git does not hold excepted; a copy, the report off, a link and a
        # git-ignored file restore nothing. Each project starts from its own copy at h1.
        hsrc = os.path.join(tmp, 'tplh')
        os.makedirs(os.path.join(hsrc, 'migrations'))
        HDATA = {'format': 1, 'template': 'probe', 'refresh': ['how-to/CONTEXT.md'], 'restore': ['how-to'],
                 'settings': {}}
        write(hsrc, REFRESH_DATA, json.dumps(HDATA))
        git('init', '-q', hsrc)
        HS, HO, HK, HN = 'how-to/CONTEXT.md', 'how-to/own/ch.md', 'how-to/own/keep.md', 'how-to/own/new.md'
        releases['h1'] = {SETTINGS: '{\n  "model": "opus"\n}\n', HS: 'shared 1\n', HO: 'own 1\n', HK: 'keep\n'}
        releases['h2'] = {SETTINGS: json.dumps({'model': 'opus', 'permissions': {'deny': ['Edit(/how-to/**)']}}, indent=2) + '\n',
                          HS: 'shared 2\n', HO: 'own 2\n', HK: 'keep\n', HN: 'new 2\n'}
        for v in ('h1', 'h2'):
            write(hsrc, 'VERSION', v + '\n')
            git('-C', hsrc, 'add', '-A')
            git('-C', hsrc, 'commit', '-q', '-m', v, env=IDENT)
            shas[v] = verify('HEAD', cwd=hsrc)
            by_sha[shas[v]] = v
        hcommon = ['--src', hsrc, '--answers', A]

        def hfresh(name, edit=None):
            """A copy at h1, its baseline, then the owner's edits (None deletes), committed."""
            d = os.path.join(tmp, name)
            git('init', '-q', d)
            for rel, text in releases['h1'].items():
                write(d, rel, text)
            write(d, A, '_commit: h1\nNAME: probe\n')
            run(d, 'baseline', '--to', shas['h1'], *hcommon)
            for rel, text in (edit or {}).items():
                if text is None:
                    os.remove(os.path.join(d, rel))
                else:
                    write(d, rel, text)
            commit_all(d, 'copied and worked')
            return d

        def hsim(d, v_to='h2', keep=()):
            """Copier's update: this template's how-to files written, but keep (the owner's files
            Copier leaves); the shared file and the settings seed never rendered on update."""
            for rel, text in releases[v_to].items():
                if rel not in keep and rel not in (HS, SETTINGS):
                    write(d, rel, text)
            write(d, A, '_commit: %s\nNAME: probe\n' % v_to)

        def hupd(d, v_from='h1', v_to='h2', extra=None):
            return run(d, 'update', '--to', shas[v_to], *hcommon,
                       env={'VERSION_FROM': shas[v_from], 'VERSION_PEP440_FROM': v_from,
                            'VERSION_PEP440_TO': v_to, **(extra or {})})

        def entry(out, p):
            """The command lines printed under p's entry, stripped, or [] where it is not listed."""
            L = out.splitlines()
            for i, l in enumerate(L):
                if l == '    ' + p:
                    got, j = [], i + 1
                    while j < len(L) and L[j].startswith('        '):
                        got, j = got + [L[j].strip()], j + 1
                    return got
            return []

        def heads(out, title):
            return [l for l in out.splitlines() if l.startswith('  ' + title)]

        def sib_record(d, files, answers='_commit: s1\nNAME: sibling\n'):
            """A sibling template's render record holding files, and its answers file in the work
            tree (the caller commits it, as the project commits a sibling's copy)."""
            sdir = os.path.join(tmp, os.path.basename(d) + '-sibling')
            for rel, text in files.items():
                write(sdir, rel, text)
            senv = {'GIT_DIR': os.path.join(d, '.git'), 'GIT_WORK_TREE': sdir,
                    'GIT_INDEX_FILE': os.path.join(tmp, os.path.basename(d) + '-sibling.index')}
            git('add', '-A', '--force', '.', env=senv, cwd=sdir)
            stree = git('write-tree', env=senv, cwd=sdir).strip()
            write(d, '.copier-answers.sibling.yml', answers)
            os.chdir(d)
            try:
                commit(stree, 'sibling render\n\ncommit: %s\nanswers: %s\n' % (
                    'a' * 40, git('hash-object', '.copier-answers.sibling.yml').strip()), 'refs/sibling/template')
            finally:
                os.chdir(tmp)

        restored_dirs = []
        # R1. An owner's committed edit to a file the template did not change: put back, listed,
        # and the 'yours:' command prints the owner's text.
        d = hfresh('ro-edit', {HK: 'mine\n'})
        hsim(d, keep=(HK,))
        out = hupd(d)
        e = entry(out, HK)
        yours = [l.split(':', 1)[1].strip() for l in e if l.startswith('yours:')]
        shown = subprocess.run(shlex.split(yours[0]), cwd=d, capture_output=True, text=True).stdout if yours else None
        check(read(d, HK) == 'keep\n' and sections(out).get(HK, '').startswith('RESTORED') and shown == 'mine\n'
              and "1 file of how-to/, which is read-only, was put back to the template's text (RESTORED below)." in out,
              'R1 restore: an owner edit under how-to/ is put back and listed, its yours: command prints it (%r)' % out)
        restored_dirs.append(d)
        # R2. A file the owner deleted and committed: put back, 'was: missing'.
        d = hfresh('ro-deleted', {HO: None})
        hsim(d, keep=(HO,))
        out = hupd(d)
        check(read(d, HO) == 'own 2\n' and 'was:     missing before this update' in entry(out, HO),
              'R2 restore: a deleted file under how-to/ comes back, listed as missing before (%r)' % out)
        restored_dirs.append(d)
        # R3. A sibling's recorded version of the shared file, committed with its answers: left.
        d = hfresh('ro-sibling')
        sib_record(d, {HS: 'sibling\n'})
        write(d, HS, 'sibling\n')
        commit_all(d, 'the sibling copied')
        hsim(d)
        out = hupd(d)
        check(read(d, HS) == 'sibling\n' and sections(out).get(HS, '').startswith('LEFT AS IT IS')
              and any("it holds sibling's version" in l for l in entry(out, HS)) and not heads(out, 'RESTORED'),
              'R3 restore: a sibling\'s version of a shared file is left and listed, never put back (%r)' % out)
        # R3b. As R3 in a plain clone (no sibling record), the file at bytes no render here holds: left.
        d = hfresh('ro-plain-clone')
        sib_record(d, {HS: 'sibling\n'})
        write(d, HS, 'sibling\n')
        commit_all(d, 'the sibling copied')
        git('-C', d, 'update-ref', '-d', 'refs/sibling/template')
        write(d, HS, 'sibling newer\n')
        commit_all(d, "the sibling's newer version")
        hsim(d)
        out = hupd(d)
        check(read(d, HS) == 'sibling newer\n' and sections(out).get(HS, '').startswith('LEFT AS IT IS')
              and any('this clone holds no record of sibling' in l for l in entry(out, HS))
              and any('updating that template here, to a release that writes update records, settles it' in l
                      for l in entry(out, HS)),
              'R3b restore: a shared file a sibling with no record here may hold is left and listed (%r)' % out)
        # R4. An owner's own file under how-to/ that no render holds: never read, written or listed.
        d = hfresh('ro-mine', {'how-to/mine.md': 'my own guide\n'})
        hsim(d)
        out = hupd(d)
        check(read(d, 'how-to/mine.md') == 'my own guide\n' and 'how-to/mine.md' not in out and 'stopped' not in out,
              'R4 restore: a file under how-to/ the new render lacks is never touched or listed (%r)' % out)
        # R5. A git-ignored file the template changed: never read or written, listed as not compared.
        d = hfresh('ro-ignored')
        write(d, '.gitignore', '/how-to/own/ch.md\n')
        git('-C', d, 'rm', '-q', '--cached', HO)
        write(d, HO, 'mine\n')
        commit_all(d, 'the owner ignores a chapter')
        hsim(d, keep=(HO,))
        out = hupd(d)
        check(read(d, HO) == 'mine\n' and sections(out).get(HO, '').startswith('NOT COMPARED because git ignores them')
              and sum(1 for l in out.splitlines() if l == '    ' + HO) == 1,
              'R5 restore: a git-ignored file under how-to/ is never written, and listed only as not compared (%r)' % out)
        # R6. A conflict Copier left (markers in the file, stages in the index): put back, the index
        # left unmerged, 'then: git add', and not listed as a conflict.
        d = hfresh('ro-conflict', {HO: 'mine\n'})
        hsim(d, keep=(HO,))
        write(d, HO, '<<<<<<< before updating\nmine\n=======\nown 2\n>>>>>>> after updating\n')
        stages = [git('-C', d, 'hash-object', '-w', '--stdin', inp=x).strip() for x in ('own 1\n', 'mine\n', 'own 2\n')]
        git('-C', d, 'update-index', '--index-info',
            inp='0 %s\t%s\n100644 %s 1\t%s\n100644 %s 2\t%s\n100644 %s 3\t%s\n' % (
                '0' * 40, HO, stages[0], HO, stages[1], HO, stages[2], HO))
        out = hupd(d)
        check(read(d, HO) == 'own 2\n' and HO in git('-C', d, 'ls-files', '-u')
              and 'then:    git add -- %s' % HO in entry(out, HO)
              and sections(out).get(HO, '').startswith('RESTORED') and not heads(out, 'CONFLICT'),
              'R6 restore: a conflicted file is put back, the index left unmerged and the git add said (%r)' % out)
        restored_dirs.append(d)
        # R7. The report off, or a render that failed: nothing restored, and the line says so.
        for label, extra, said in (('off', {'SYNTEK_UPDATE_REPORT': 'off'}, 'no file of how-to/ is restored'),
                                   ('failed', {'PROBE_NO_COPIER': '1'}, 'no file of how-to/ was restored')):
            d = hfresh('ro-' + label, {HK: 'mine\n'})
            hsim(d, keep=(HK,))
            out = hupd(d, extra=extra)
            check(read(d, HK) == 'mine\n' and said in out,
                  'R7 restore: %s restores nothing and says so (%r)' % (
                      'SYNTEK_UPDATE_REPORT=off' if label == 'off' else 'a render that failed', out))
        # R8. The next update, once the restores are committed: nothing restored, nothing changed.
        for d in restored_dirs:
            commit_all(d, 'updated')
            out = hupd(d, 'h2', 'h2')
            check(not heads(out, 'RESTORED') and not git('-C', d, 'status', '--porcelain'),
                  'R8 restore: an update after a committed restore restores nothing (%s: %r)' % (os.path.basename(d), out))
        # R9. how-to a link to a folder inside the project: nothing written through it, every file left.
        d = hfresh('ro-link', {HK: 'mine\n'})
        os.rename(os.path.join(d, 'how-to'), os.path.join(d, 'elsewhere'))
        os.symlink('elsewhere', os.path.join(d, 'how-to'))
        commit_all(d, 'how-to as a link')
        hsim(d, keep=(HK,))
        out = hupd(d)
        check(read(d, 'elsewhere/own/keep.md') == 'mine\n' and read(d, 'elsewhere/CONTEXT.md') == 'shared 1\n'
              and all(sections(out).get(p, '').startswith('LEFT AS IT IS') for p in (HS, HO, HK, HN)),
              'R9 restore: how-to as a link is never written through, and its files are listed as left (%r)' % out)
        # R10 and R11. Data without "restore" restores nothing; a malformed one says so in one line.
        for label, data_now in (('none', {k: v for k, v in HDATA.items() if k != 'restore'}),
                                ('malformed', dict(HDATA, restore=['../x']))):
            write(hsrc, REFRESH_DATA, json.dumps(data_now))
            try:
                d = hfresh('ro-data-' + label, {HK: 'mine\n'})
                hsim(d, keep=(HK,))
                out = hupd(d)
            finally:
                write(hsrc, REFRESH_DATA, json.dumps(HDATA))
            said = out.count('lists "restore" in a form this script does not read, so no file was restored.')
            check(read(d, HK) == 'mine\n' and not heads(out, 'RESTORED') and 'update report' in out
                  and said == (1 if label == 'malformed' else 0),
                  'R%s restore: %s "restore" restores nothing%s (%r)' % (
                      '10' if label == 'none' else '11', 'no' if label == 'none' else 'a malformed',
                      '' if label == 'none' else ', in one line, and the report runs', out))
        # R12. A copy (baseline) over the owner's committed file at a how-to path restores nothing.
        d = os.path.join(tmp, 'ro-copy')
        git('init', '-q', d)
        write(d, HK, 'mine\n')
        commit_all(d, 'my own project')
        for rel, text in releases['h2'].items():
            if rel != HK:
                write(d, rel, text)
        write(d, A, '_commit: h2\nNAME: probe\n')
        out = run(d, 'baseline', '--to', shas['h2'], *hcommon)
        check(read(d, HK) == 'mine\n', 'R12 restore: a copy restores nothing (%r)' % out)
        # R13. The shared file's deletion committed, an untracked copy at bytes no render holds: left.
        d = hfresh('ro-untracked', {HS: None})
        write(d, HS, 'my untracked copy\n')
        hsim(d)
        out = hupd(d)
        check(read(d, HS) == 'my untracked copy\n' and sections(out).get(HS, '').startswith('LEFT AS IT IS')
              and any('Git does not hold your copy' in l for l in entry(out, HS)),
              'R13 restore: a file Git does not hold, at bytes no render holds, is left and listed (%r)' % out)
        # R14. A rejected hunk beside a how-to file: the .rej is removed, never the owner's text taken.
        d = hfresh('ro-rej', {HO: 'mine\n'})
        hsim(d)
        write(d, HO + '.rej', '@@ -1 +1 @@\n-own 1\n+mine\n')
        out = hupd(d)
        e = entry(out, HO)
        check(sections(out).get(HO, '').startswith('REJECTED HUNKS')
              and 'then:    rm -- %s.rej' % HO in e
              and not any(l.startswith('yours:') for l in e),
              'R14 restore: a .rej beside a how-to file offers rm of the .rej, never the owner\'s version (%r)' % out)
        # R15. A restore that raises: one line; the settings and MCP lanes, the report and the record follow.
        d = hfresh('ro-raises', {HK: 'mine\n'})
        hsim(d, keep=(HK,))
        write(hsrc, REFRESH_DATA, json.dumps(dict(HDATA, settings={'permissions': {'deny': ['Edit(/how-to/**)']}})))
        real_restore, real_mcp, mcp_calls = restore, mcp_lane, []

        def boom(*a, **k):
            raise RuntimeError('probe')

        def counted(*a, **k):
            mcp_calls.append(1)
            return real_mcp(*a, **k)
        globals()['restore'], globals()['mcp_lane'] = boom, counted
        try:
            out = hupd(d)
        finally:
            globals()['restore'], globals()['mcp_lane'] = real_restore, real_mcp
            write(hsrc, REFRESH_DATA, json.dumps(HDATA))
        check(out.count('the restore stopped') == 1 and 'refresh stopped' not in out and mcp_calls
              and has_rule(json.loads(read(d, SETTINGS)), 'deny', 'Edit(/how-to/**)') and 'update report' in out
              and read(d, HK) == 'mine\n'
              and ('commit: %s' % shas['h2']) in git('-C', d, 'log', '-1', '--format=%B', 'refs/probe/template'),
              'R15 restore: an error in the restore is one line, and the settings and MCP lanes, the report and '
              'the record still run (%r)' % out)

        # C1 and C2. A file new in this version that the owner's tree holds: the sibling's version
        # where a sibling's recorded render holds its bytes, else the owner's file.
        for label, sib_files, mine in (('C1', {'brand-new.md': 'sibling new\n'}, 'sibling new\n'),
                                       ('C2', None, 'mine new\n'),
                                       ('C2', {'brand-new.md': 'sibling other\n'}, 'mine new\n')):
            d = fresh('classify-%s-%s' % (label, 'record' if sib_files else 'none'), 'v2')
            commit_all(d, 'copied')
            if sib_files:
                sib_record(d, sib_files)
            write(d, 'brand-new.md', mine)
            commit_all(d, 'the file there')
            sim_update(d, 'v3')
            out = upd(d, 'v2', 'v3')
            want = ("NOT UPDATED because the file holds sibling's" if label == 'C1'
                    else 'NOT UPDATED because it is new in this version')
            check(sections(out).get('brand-new.md', '').startswith(want),
                  '%s classify: a file new in this version holding %s is listed as %r (%r)' % (
                      label, 'a sibling\'s recorded version' if label == 'C1' else 'bytes no sibling recorded', want,
                      sections(out).get('brand-new.md')))

        # ── The MCP lane through update and baseline: attribution, the opt-out, the root ──
        msrc = os.path.join(tmp, 'tplm')
        os.makedirs(os.path.join(msrc, 'migrations'))
        write(msrc, REFRESH_DATA, json.dumps({'format': 1, 'template': 'mprobe', 'refresh': [], 'settings': {},
                                              'mcp': {'servers': PROBE_MCP['servers'], 'files': {'.mcp.json': ['mcpServers']}}}))
        git('init', '-q', msrc)
        scr2 = dict(PROBE_SCR, args=['--from', 'scr==2', 'scr', 'mcp'])
        for v, servers in (('m1', {}), ('m2', {'code-review-graph': PROBE_CRG, 'scrapling': PROBE_SCR}),
                           ('m3', {'code-review-graph': PROBE_CRG, 'scrapling': scr2})):
            releases[v] = {'README.md': 'readme %s\n' % v, SETTINGS: '{\n  "model": "opus"\n}\n',
                           '.mcp.json': json.dumps({'mcpServers': servers}, indent=2 if servers else None) + '\n'}
            write(msrc, 'VERSION', v + '\n')
            git('-C', msrc, 'add', '-A')
            git('-C', msrc, 'commit', '-q', '-m', v, env=IDENT)
            shas[v] = verify('HEAD', cwd=msrc)
            by_sha[shas[v]] = v
        MA = '.copier-answers.mprobe.yml'
        mcommon = ['--src', msrc, '--answers', MA]

        def mfresh(name, edit=None):
            d = os.path.join(tmp, name)
            git('init', '-q', d)
            for rel, text in releases['m1'].items():
                write(d, rel, text)
            write(d, MA, '_commit: m1\nNAME: probe\n')
            run(d, 'baseline', '--to', shas['m1'], *mcommon)
            if edit:
                write(d, '.mcp.json', edit)
            commit_all(d, 'copied')
            return d

        def mupd(d, v_from, v_to, extra=None, cwd=None):
            write(d, 'README.md', releases[v_to]['README.md'])
            write(d, MA, '_commit: %s\nNAME: probe\n' % v_to)
            return run(cwd or d, 'update', '--to', shas[v_to], *mcommon,
                       env={'VERSION_FROM': shas[v_from], 'VERSION_PEP440_FROM': v_from, 'VERSION_PEP440_TO': v_to, **(extra or {})})

        def mrecord(d):
            return git('-C', d, 'log', '-1', '--format=%B', 'refs/mprobe/template')

        # Unedited: the lane writes the new render's bytes (delivered); written once on the next update.
        d = mfresh('mcp-unedited')
        out = mupd(d, 'm1', 'm2')
        msg = mrecord(d)
        check(read(d, '.mcp.json') == releases['m2']['.mcp.json'] and '.mcp.json' not in sections(out)
              and 'added 2 MCP servers to .mcp.json' in out, 'mcp flow: an unedited .mcp.json is delivered (%r)' % out)
        check(re.search(r'^mcp-offered: 2$', msg, re.M) and re.search(r'^mcp: \.mcp\.json scrapling [0-9a-f]{64}$', msg, re.M)
              and re.search(r'^written-blob: \.mcp\.json [0-9a-f]{40,64}$', msg, re.M), 'mcp flow: the record lists the offers and the blob (%r)' % msg[-400:])
        check(tmp not in git('-C', d, 'log', '--format=%B', 'refs/mprobe/template'), 'mcp flow: the record holds no absolute path')
        commit_all(d, 'updated')
        out = mupd(d, 'm2', 'm3')
        check(sections(out).get('.mcp.json', '').startswith('NOT UPDATED because files of this kind')
              and read(d, '.mcp.json') == releases['m2']['.mcp.json'] and 'MCP server' not in out,
              'mcp flow: a file only the lane wrote is written once next time, its offers quiet (%r)' % out)
        # Edited by the owner: 'you had changed them' on both updates.
        mine = '{\n    "mcpServers": {\n        "mine": {\n            "command": "x"\n        }\n    }\n}\n'
        d = mfresh('mcp-edited', mine)
        out = mupd(d, 'm1', 'm2')
        check(sections(out).get('.mcp.json', '').startswith('NOT UPDATED because you had changed')
              and list(json.loads(read(d, '.mcp.json'))['mcpServers']) == ['mine', 'code-review-graph', 'scrapling']
              and re.search(r'^written-blob: \.mcp\.json [0-9a-f]+ edited$', mrecord(d), re.M),
              'mcp flow: an owner-edited .mcp.json is yours, the servers added (%r)' % out)
        commit_all(d, 'updated')
        out = mupd(d, 'm2', 'm3')
        check(sections(out).get('.mcp.json', '').startswith('NOT UPDATED because you had changed'),
              'mcp flow: and still yours on the next update (%r)' % sections(out).get('.mcp.json'))
        # Reformatted by the owner, the servers inserted: equal to the new render's once written,
        # so the template's, never 'yours'.
        d = mfresh('mcp-reformatted', '{\n    "mcpServers": {}\n}\n')
        out = mupd(d, 'm1', 'm2')
        check('.mcp.json' not in sections(out) and re.search(r'^written-blob: \.mcp\.json [0-9a-f]+$', mrecord(d), re.M),
              'mcp flow: a write that leaves the file equal to the new render is delivered and the template\'s (%r)' % out)
        commit_all(d, 'updated')
        out = mupd(d, 'm2', 'm3')
        check(sections(out).get('.mcp.json', '').startswith('NOT UPDATED because files of this kind'),
              'mcp flow: and written once on the next update (%r)' % sections(out).get('.mcp.json'))
        # The opt-out: no lane; the next full update delivers it.
        d = mfresh('mcp-off')
        mupd(d, 'm1', 'm2', {'SYNTEK_UPDATE_REPORT': 'off'})
        check(read(d, '.mcp.json') == releases['m1']['.mcp.json'], 'mcp flow: SYNTEK_UPDATE_REPORT=off runs no lane')
        commit_all(d, 'updated, report off')
        mupd(d, 'm2', 'm3')
        check(set(json.loads(read(d, '.mcp.json'))['mcpServers']) == {'code-review-graph', 'scrapling'},
              'mcp flow: the next full update adds the servers')
        # Not at the repository root: the line says no MCP server was offered.
        d = mfresh('mcp-sub')
        os.makedirs(os.path.join(d, 'sub'))
        out = mupd(d, 'm1', 'm2', cwd=os.path.join(d, 'sub'))
        check('no settings entry or MCP server was offered' in out and read(d, '.mcp.json') == releases['m1']['.mcp.json'],
              'mcp flow: not at the root, no MCP server is offered (%r)' % out)
        # A git-ignored file the new version changes is never read: listed once as not compared,
        # with no compare or take command that would show it as deleted or overwrite it.
        d = mfresh('mcp-ignored')
        secret = '{"mcpServers": {"private": {"command": "secret-tool", "env": {"TOKEN": "probe-secret"}}}}\n'
        write(d, '.gitignore', '/.mcp.json\n')
        git('-C', d, 'rm', '-q', '--cached', '.mcp.json')
        write(d, '.mcp.json', secret)
        commit_all(d, 'the owner ignores .mcp.json')
        out = mupd(d, 'm1', 'm2')
        check(sections(out).get('.mcp.json', '').startswith('NOT COMPARED because git ignores them')
              and read(d, '.mcp.json') == secret and 'is ignored by git, so it was not read' in out
              and '-- .mcp.json' not in out and 'probe-secret' not in mrecord(d),
              'mcp flow: an ignored file is listed as not compared, never read, compared or taken (%r)' % out)
    # An older Python: a framed message on stderr naming what was skipped, the minimum and the
    # quoted rerun; exit 0 inside Copier, 1 for a self-test. Read from PYTHON_MIN, never typed.
    need = '%d.%d' % PYTHON_MIN
    older = (PYTHON_MIN[0], PYTHON_MIN[1] - 1)
    have = '%d.%d' % older
    rerun = "uvx --python '>=%s' copier update" % need
    old_u, old_b, old_t = (too_old(s, older) for s in ('update', 'baseline', '--self-test'))
    framed = lambda t: (t.splitlines()[0] == t.splitlines()[-1] == '  ' + '=' * 76 and t.endswith('\n'))
    check(all(framed(t) for t in (old_u, old_b, old_t))
          and ('  family-update did NOT run, because Copier runs on Python %s here and it needs Python %s or later.'
               % (have, need)) == old_u.splitlines()[1] == old_b.splitlines()[1]
          and all(w in old_u for w in ('printed no report', 'refreshed no shared file',
                                       'added no settings entry or MCP server', 'put back no guide file',
                                       'kept no record', 'Upgrade to Python %s or later.' % need,
                                       'conflict markers and .rej files', 'commit this update',
                                       'run the same update again, starting %s.' % rerun))
          and all(w in old_b for w in ('This copy recorded nothing', 'Upgrade to Python %s or later' % need, rerun))
          and old_t.splitlines()[1:3] == ['  family-update did NOT run, because this is Python %s and it needs '
                                          'Python %s or later.' % (have, need), '  The self-test did not run.'],
          'old Python: the framed message names what was skipped, the minimum and the quoted rerun (%r, %r, %r)'
          % (old_u, old_b, old_t))
    check(('Python %s or later (PYTHON_MIN, below)' % need) in ' '.join(__doc__.split())
          and ("uvx --python '>=%s'" % need) in __doc__,
          'old Python: the docstring states the minimum PYTHON_MIN sets')
    import ast
    with open(os.path.abspath(__file__), encoding='utf-8') as f:
        source = f.read()
    try:
        ast.parse(source, feature_version=(3, 8))
        parses = True
    except SyntaxError:
        parses = False
    check(parses, 'old Python: the file parses as Python 3.8, so an old Python reaches the message')
    check(source.index("sys.exit(1 if sys.argv[1:2] == ['--self-test'] else 0)") < source.index('\nimport copy\n'),
          'old Python: the version check runs before any other import')
    for sub, code in (('update', 0), ('baseline', 0), ('--self-test', 1)):
        r = subprocess.run([sys.executable, '-I', '-c',
                            'import runpy, sys; sys.version_info = %r; sys.argv = [%r, %r]; '
                            'runpy.run_path(sys.argv[0], run_name="__main__")'
                            % (older + (0, 'final', 0), os.path.abspath(__file__), sub)],
                           capture_output=True, text=True)
        check(r.returncode == code and r.stdout == '' and r.stderr == '\n' + too_old(sub, older),
              'old Python: %s exits %d, with the framed message alone, on stderr (%r)' % (sub, code, r))
    r = subprocess.run([sys.executable, '-I', '-c',
                        'import runpy, sys; sys.version_info = %r; sys.argv = [%r, "--help"]; '
                        'runpy.run_path(sys.argv[0], run_name="__main__")' % (older + (0, 'final', 0),
                                                                              os.path.abspath(__file__))],
                       capture_output=True, text=True)
    check(r.returncode == 0 and 'PYTHON_MIN' in r.stdout and r.stderr == '',
          'old Python: --help still prints the docstring (%r)' % r)
    two = unread_reason(['a', 'b'])
    check(two.startswith('this clone holds no record of a, b, so this may be the version of one of them')
          and 'updating each of them here' in two and 'their records' in two,
          'unread siblings: the reason reads for two templates (%r)' % two)
    RENDER = None
    for f in fails:
        print('  ✗ ' + f)
    print('%s family-update.py --self-test: %s' % ('✓' if not fails else '✗',
          'every class, the refresh, the commands, the rerun and the limits hold' if not fails else '%d failure(s)' % len(fails)))
    return 0 if not fails else 1


def main(argv):
    if len(argv) > 1 and argv[1] in ('--help', '-h'):
        print(__doc__)
        return 0
    if len(argv) > 1 and argv[1] == '--self-test':
        return self_test()
    _ANSWERS.clear()   # a file git never stored is read in its own run only
    try:
        sub = argv[1] if len(argv) > 1 else ''
        args, rest = {}, argv[2:]
        while rest:
            if rest[0] in ('--src', '--to', '--answers') and len(rest) > 1:
                args[rest[0]] = rest[1]
                rest = rest[2:]
            else:
                say('unknown argument %s; see --help.' % rest[0])
                return 0
        if sub == 'update':
            cmd_update(args)
        elif sub == 'baseline':
            cmd_baseline(args)
        else:
            say('usage: family-update.py update|baseline --src S --to SHA --answers F (or --help).')
    except Exception as err:   # a migration must never fail the update
        say('stopped: %s' % err)
    return 0


if __name__ == '__main__':
    try:   # an output that cannot show a character must never stop the run after a write
        sys.stdout.reconfigure(errors='replace')
    except (AttributeError, ValueError):
        pass
    sys.exit(main(sys.argv))
