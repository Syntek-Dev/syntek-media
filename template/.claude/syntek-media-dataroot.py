#!/usr/bin/env python3
"""The data-root tool: a project's binary files kept outside its repository, listed in it.

Why. Git keeps text well and binaries badly. A project may therefore keep its binary records
and issued copies (scans, signed and received copies, archives, issued PDF and Word copies,
generated audio) outside the repository, under one data root per machine, each file listed
with its checksum in a text manifest that Git does keep. This tool finds the root, files
copies there, verifies them, reports what is at risk and checks that names are safe on
Windows. Its guard subcommand is the hook that keeps the session's file tools out of the
root. Every template of the family ships these bytes, each under its own name
(.claude/syntek-<template>-dataroot.py), so either copy gives the same result.

The project is the Git top level of the current folder; outside a work tree, the nearest
folder above holding a .copier-answers.syntek-*.yml. The tool reads every such answers file
there and every .claude/syntek-*-dataroot.json (the maps, below), whichever template wrote it.

The store. Each template records DATA_STORE. 'external' files binaries under the data root;
'repo' keeps them in the repository as before, and the data commands then say so. Every
answers file that records a store must record the same one and, under 'external', the same
DATA_AREA, DATA_SLUG and kind folders, or the data commands refuse (exit 2) until they agree.
A record without DATA_STORE is 'not yet asked' (its template has not been updated): one
warning, never a refusal. A difference in DATA_PROVIDER moves no file: a warning only. A
store this tool does not know needs a newer template.

The root. The environment variable SYNTEK_DATA_ROOT names it on each machine, never a file in
the project. It must be an absolute path to a folder holding the marker file
.syntek-data-root, which the owner creates (touch "$SYNTEK_DATA_ROOT/.syntek-data-root") and
the tools never do: a volume that is not mounted is an empty folder, and the missing marker
gives it away. Presence is enough; a marker holding a 'format = N' line newer than this tool
knows is refused. A value that is set but invalid (empty, relative, not a folder, without the
marker, inside this repository or holding it) stops every data command but status with exit 2
and is never passed over for a later source, so a later release can add file sources after it;
so does a marker at or above the repository, because a sync service corrupts Git. Under
'repo', which files nothing under the root, the root and the repository containing one another,
or a marker above it, still stops path and every add with exit 2 before they answer; the other
invalid values do not. status, which needs no root, never refuses for one: it checks the work
tree and warns that it did not check the copies under the root (under 'repo' too, where the
root and the repository contain one another or a marker sits above it).

The layout. <root>/<DATA_AREA>/<kind folder>/<DATA_SLUG>/<project-relative path>: the path
under the root mirrors the path in the repository, so references keep their paths. The kind
folders are DATA_KIND_DOCS, DATA_KIND_PHOTOS, DATA_KIND_AUDIO and DATA_KIND_VIDEOS. Prose
names such a file ext:<project-relative path>.

The maps (format 1). Each template ships .claude/syntek-<template>-dataroot.json naming its
filing folders; this tool names none:
  {"format": 1,
   "folders": [{"path": "<project-relative folder>",      required; '/'-separated, Windows-safe
                "kind": "docs | photos | audio | videos",  optional: fixes every file's kind
                "warn_over_kib": <positive integer>,       optional: status warns above it
                "rows": "none"}],                          optional: working output, no rows
   "roles": [{"name": "<lower-case words joined by hyphens>",   the list is optional
              "evidence": true | false,                    required in each role
              "repo": "skip"}]}                            optional: under 'repo', never filed
A file belongs to the most specific folder that contains it; a folder the project lacks is
skipped. A folder marked "rows": "none" holds working output: add never files there, and status
and verify never list its files. Two maps naming one folder, or one inside the other, refuse
every data command that touches it (exit 2). A role is named in lower-case words joined by
hyphens (brand-export), never as a shared role or a kind; where two maps define one role
differently, evidence wins and status warns. A key this tool does not know, on a map, a folder
entry, a role entry or a row, is kept as it is and ignored. A map or manifest that is of a newer
format, does not parse or is invalid is reported and refuses only the commands that touch its
folders: every other command runs. The kind of a file no folder fixes follows its extension
(any case), and any other extension is a document:
  docs    pdf doc docx xls xlsx ppt pptx odt ods odp zip 7z tar gz eml msg
  photos  png jpg jpeg tif tiff heic webp gif psd bmp dng exr
  audio   mp3 wav flac m4a ogg aac aif aiff opus pcm
  videos  mp4 mov mkv webm mxf m4v mts m2ts avi braw r3d

The manifest (format 1): <folder>/external.toml, one per filing folder, created by the first
add; author content, never rendered and never ignored. Rows are appended as text, and the file
is replaced only when tomllib reads it back as exactly the planned rows. A row is never
deleted, and the one change in place is its state, from current to superseded or withdrawn:
  format = 1
  [[file]]
  path = "<project-relative path>"   inside the manifest's folder
  kind = "docs"                      the kind's role name, never the folder answer
  filed_under = "<area>/<kind folder>/<slug>"   where it went; never rewritten
  role = "signed"                    a shared role, or one a map defines
  evidence = true                    the role was evidence when filed; never rewritten
  sha256 = "<64 hex digits>"         taken when filed; never rewritten
  bytes = 184233
  filed = "DD/MM/YYYY"
  state = "current"                  current, superseded or withdrawn
  source = ""                        the project-relative source of an issued copy
  replaces = ""                      the kept copy this one supersedes, by its path
  label = ""                         where else a copy exists: a label, never a URL
  former_name = ""                   the original name, where a Windows-safe one was needed
  notes = ""
The file is at <root>/<filed_under>/<path>, so a later change of answers never loses it.
Shared roles: issued, signed, ingested, received, archive, evidence, asset, generated; signed,
evidence, ingested and received are evidence, as is a map role with "evidence": true. A row is
protected where its own evidence flag or any map's definition says so, and a row whose role no
map here defines is reported and treated as evidence. A protected row's file and hash are never
replaced (add --force refuses it), and a changed file is a failure, never an update.

Subcommands (exit 0 done, 1 a check failed, 2 it cannot act):
  root                 the root, its origin, the marker, the store, the layout per kind and
                       the provider's checklist; exit 2 when the root is set but invalid
  store                each answers file's store; exit 2 while two that record one disagree
  path REL [--kind K]  one line, where REL lives: the work tree under 'repo' (exit 2 where the
                       root and the repository contain one another or a marker sits above it);
                       under 'external' the work-tree file if there is one, else its place under
                       the root (a listed file where its row says, else the mirror path)
  add FILE --role R [--as REL] [--source S] [--label L] [--force]
                       file a copy under the root: copy to a temporary name, fsync, rename,
                       hash again, then write the row. Never overwrites: --force supersedes a
                       row that is not protected, keeping the listed copy under the root as
                       <stem>.superseded-DD-MM-YYYY<ext>, which the new row's replaces names;
                       only while that copy still hashes as its row says (exit 1 otherwise),
                       and only once the new copy is written and checked; an interrupt is
                       undone. REL is a file: never a filing folder or a folder.
                       Under 'repo' it refuses ('commit the file instead'), except --role
                       generated and a map role with "repo": "skip", which write nothing and
                       exit 0; where the root and the repository contain one another or a
                       marker sits above it, every add refuses with that error first (exit 2)
  verify [GLOB] [--hydrate]   hash every current row; list missing, changed and unlisted
                       files; fail on a row committed at HEAD that was removed or changed
                       (but for its state, from current), and on a tracked external.toml that
                       no map's folder names; an online-only file is not read unless --hydrate
  status               what is at risk: binaries Git ignores that no row lists, files over a
                       map's warn_over_kib, folders holding rows that differ from the
                       answers, unlisted files under the root (with conflict-copy hints),
                       those outside every map folder included; roles maps define differently.
                       With no valid root it warns that it did not check the copies (under
                       repo, only where the root and the repository contain one another or a
                       marker sits above it), and the root never makes it exit 2
  pull [GLOB]          copy listed files into the work tree, verifying each; never replaces
  plan [--copy] [--issue-statuses "S ..."]
                       tracked binaries, their destinations, roles and conflicts; --copy files
                       those with a role (a copy: never a move, never an untrack). The role
                       comes from whole words of the name (signed, countersigned, executed:
                       signed; receipt, remittance, statement but not 'statement of work',
                       received: received, never for a copy the house build made) or a
                       reading note beside it (ingested); beside a
                       same-stem .tex or .md, only from evidence: issued for a .pdf the house
                       build made (producer xdvipdfmx or XeTeX) from a source at an issuing
                       status (--issue-statuses, default final), with no digital signature
                       (which makes it signed) and, where Git holds both, first committed no
                       earlier than its source. A row it cannot prove shows role ? and why, is
                       never filed, and makes plan exit 1, as a conflict does. A file with no
                       source beside it is proposed as asset (photos) or archive
  check-names [PATH...]   Windows-safe names (and OneDrive's, under that provider)
  guard                the PreToolUse hook (below)
  --self-test, --help
GLOB is matched against each row's path with fnmatch ('*' crosses '/'). REL, FILE, --as and
--source are taken from the project's top. Warnings and refusals go to stderr, one line each
(the framed message of an older Python apart, below).
verify, status, pull and plan act on every folder they can read; a folder they cannot (its map
or manifest unreadable, or two maps claiming it) is refused alone, and they then exit 2 unless
a check of the others failed (exit 1).

The guard. The hook passes the call as JSON on stdin. For Edit, Write, MultiEdit,
NotebookEdit, Grep and Glob, a target at or under a data root (named by SYNTEK_DATA_ROOT, or
any folder above it holding the marker) exits 2 with one line naming the rules; a Glob call is
also judged by the folder an absolute pattern names, where the client searches; anything else,
and any error of its own, exits 0. Read is never blocked. On macOS, Linux and WSL Claude Code
searches through Bash, which the guard does not read, so there the rules alone keep searches
out of the root.

Python 3.14 or later (PYTHON_MIN, below), for every subcommand, the guard included. On an older
Python nothing runs: a subcommand prints a framed message on stderr saying it did NOT run, the
Python it found and the one it needs, and exits 2. The guard instead lets the call through
(exit 0, for a guard that cannot run must never block an edit) and prints on stdout the JSON
that has Claude Code warn the person (systemMessage) and the session (additionalContext) that
it did not check the call and that Python needs upgrading; it makes no permission decision,
so the usual permission rules still apply. --help prints this text on any Python. The check
runs before any other import, and the file parses as Python 3.8, so an old Python reaches the
message instead of a SyntaxError.

Never: a network connection, a sync, a provider's configuration, a deletion or overwrite of a
filed copy, a rename of a conflict copy. Python's own modules only.

Usage: python3 .claude/<this file> <subcommand> [options]
       python3 .claude/<this file> --self-test | --help
"""

from __future__ import annotations

import sys

# ── The Python minimum and the guard: reached before any other import, on Python 3.8 ──────

# The one place the minimum is set: the move to a newer Python changes this line and the text
# above, nothing else.
PYTHON_MIN = (3, 14)
RULE = "=" * 78


def too_old_text(command, version):
    """The framed message a subcommand prints on stderr, in place of running, on an older Python."""
    need, have = "%d.%d" % tuple(PYTHON_MIN), "%d.%d" % tuple(version[:2])
    return "\n".join([
        RULE,
        "ERROR: the data-root tool did NOT run %s, because this is Python %s and it needs Python %s "
        "or later." % (repr(command) if command else "its command", have, need),
        "Nothing was read, checked, filed, copied or changed.",
        "Upgrade to Python %s or later, then run the command again." % need,
        RULE]) + "\n"


def too_old_hook(version):
    """The JSON the guard prints on stdout on an older Python: no permission decision, so the call
    goes ahead under the usual rules, and Claude Code shows the person the systemMessage and adds
    the additionalContext to the session."""
    import json
    need, have = "%d.%d" % tuple(PYTHON_MIN), "%d.%d" % tuple(version[:2])
    person = ("WARNING: the data-root guard did NOT work: python3 here is Python %s, and the guard needs "
              "Python %s or later. It let this call through unchecked, leaving the rules alone to keep "
              "file tools out of the data root. Upgrade to Python %s or later." % (have, need, need))
    session = ("The project's data-root guard did not run for this call: python3 here is Python %s, and "
               "the guard needs Python %s or later, so it let the call through unchecked and will do so for "
               "every call until Python is upgraded. The person has to upgrade to Python %s or later for "
               "the guard to work, and needs to hear this from the session. Until then the project's rules "
               "alone keep the session's file tools out of the data root." % (have, need, need))
    return json.dumps({"systemMessage": person,
                       "hookSpecificOutput": {"hookEventName": "PreToolUse", "additionalContext": session}})


MARKER = ".syntek-data-root"
ROOT_ENV = "SYNTEK_DATA_ROOT"
# The tools the guard judges, and the field of each that names its target. Read is not here.
GUARD_FIELDS = {"Edit": "file_path", "Write": "file_path", "MultiEdit": "file_path",
                "NotebookEdit": "notebook_path", "Grep": "path", "Glob": "path"}
GUARD_BLOCK = ("This path is under the data root; records there are filed with the project's "
               "data-root commands (see the bridge, .claude/syntek-*-agents.md), never edited "
               "in place.")
GUARD_INSIDE = ("This repository lies under a data root (a .syntek-data-root marker above it), "
                "and a sync service corrupts Git: move the repository or the marker; until then "
                "every data command but status refuses, and status warns.")


def within(path, top):
    """True when the absolute path is top or lies under it."""
    import os
    try:
        a, b = os.path.normcase(path), os.path.normcase(top)
        return os.path.commonpath([a, b]) == b
    except ValueError:
        return False


def glob_base(pattern):
    """The folder an absolute glob pattern searches, as the client takes it (it searches there
    and ignores the call's path): the part before the first wildcard, cut back to the last
    separator; the pattern's own folder where it holds no wildcard."""
    import os
    import re
    m = re.search(r"[*?\[{]", pattern)
    if not m:
        return os.path.dirname(pattern) or pattern
    head = pattern[:m.start()]
    cut = max(head.rfind("/"), head.rfind(os.sep))
    return head[:cut] if cut > 0 else head[:1] if cut == 0 else head


def guard(text, environ, project, cwd=None):
    """Judge one PreToolUse call: (2, reason) for a target at or under a data root, else (0, '').
    A Glob call is judged by its path and, where its pattern is absolute, by the folder the
    pattern names, which is where the client searches."""
    import json
    import os
    try:
        data = json.loads(text)
    except ValueError:
        return 0, ""
    if not isinstance(data, dict):
        return 0, ""
    tool = data.get("tool_name")
    if not isinstance(tool, str) or tool not in GUARD_FIELDS:
        return 0, ""
    given = data.get("tool_input")
    if not isinstance(given, dict):
        return 0, ""
    targets = []
    target = given.get(GUARD_FIELDS[tool])
    if isinstance(target, str) and target:
        targets.append(target)
    pattern = given.get("pattern") if tool == "Glob" else None
    if isinstance(pattern, str) and pattern:
        pattern = os.path.expanduser(pattern)
        if os.path.isabs(pattern):
            targets.append(glob_base(pattern))
    found = (0, "")
    for target in targets:
        found = guard_one(target, data, environ, project, cwd)
        if found[0] == 2:
            return found
    return found


def guard_one(target, data, environ, project, cwd):
    """(2, reason) where one target lies at or under a data root, else (0, '')."""
    import os
    base = data.get("cwd")
    if not isinstance(base, str) or not os.path.isabs(base):
        base = cwd or os.getcwd()
    target = os.path.expanduser(target)
    if not os.path.isabs(target):
        target = os.path.join(base, target)
    real = os.path.realpath(target)
    roots = []
    value = environ.get(ROOT_ENV)
    if value:
        top = os.path.expanduser(value)
        if os.path.isabs(top) and os.path.isfile(os.path.join(top, MARKER)):
            roots.append(os.path.realpath(top))
    here = real
    while True:
        if os.path.isfile(os.path.join(here, MARKER)):
            roots.append(here)
            break
        up = os.path.dirname(here)
        if up == here:
            break
        here = up
    hits = [r for r in roots if within(real, r)]
    if not hits:
        return 0, ""
    nearest = max(hits, key=len)
    if project:
        mine = os.path.realpath(project)
        if within(real, mine) and within(mine, nearest):
            return 2, GUARD_INSIDE
    return 2, GUARD_BLOCK


def guard_main(version=None):
    """The hook's entry: exit 2 with one stderr line on a block; 0 on anything else at all. On a
    Python older than PYTHON_MIN it judges nothing: it reads the call, prints the warning JSON
    on stdout and returns 0."""
    if (version or sys.version_info) < PYTHON_MIN:
        try:
            stream = getattr(sys.stdin, "buffer", None)
            (stream or sys.stdin).read()   # the whole call, so the client never writes to a closed pipe
        except BaseException:
            pass
        try:
            sys.stdout.write(too_old_hook(version or sys.version_info) + "\n")
            sys.stdout.flush()
        except BaseException:
            pass
        return 0
    try:
        import os
        stream = getattr(sys.stdin, "buffer", None)
        raw = stream.read() if stream is not None else sys.stdin.read().encode("utf-8")
        project = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        code, reason = guard(raw.decode("utf-8", "replace"), os.environ, project)
        if code == 2:
            sys.stderr.write(reason + "\n")
            sys.stderr.flush()
            return 2
    except BaseException:  # fail open: a guard that errs must never block an edit
        pass
    return 0


if __name__ == "__main__" and sys.argv[1:2] == ["guard"]:
    sys.exit(guard_main())

if __name__ == "__main__" and sys.version_info < PYTHON_MIN and sys.argv[1:2] not in (["-h"], ["--help"]):
    sys.stderr.write(too_old_text(sys.argv[1] if len(sys.argv) > 1 else "", sys.version_info))
    sys.stderr.flush()
    sys.exit(2)

# A Python that passed the check but lacks tomllib (a stripped build): one line, never a traceback.
NEED_PYTHON = ("refused: this Python has no tomllib, which this tool needs: upgrade to Python %d.%d or later"
               % PYTHON_MIN)

# ── Everything else: Python 3.14 or later (PYTHON_MIN) ───────────────────────────────────

import argparse  # noqa: E402
import contextlib  # noqa: E402
import datetime  # noqa: E402
import fnmatch  # noqa: E402
import hashlib  # noqa: E402
import io  # noqa: E402
import os  # noqa: E402
import platform  # noqa: E402
import re  # noqa: E402
import shlex  # noqa: E402
import shutil  # noqa: E402
import stat as stat_mod  # noqa: E402
import subprocess  # noqa: E402
import tempfile  # noqa: E402
import unicodedata  # noqa: E402
from pathlib import Path  # noqa: E402

FORMAT = 1
ORIGIN_ENV = "the environment variable " + ROOT_ENV
MANIFEST = "external.toml"
TMP_SUFFIX = ".syntek-tmp"
STORES = ("external", "repo")
KINDS = ("docs", "photos", "audio", "videos")
KIND_KEYS = {"docs": "DATA_KIND_DOCS", "photos": "DATA_KIND_PHOTOS",
             "audio": "DATA_KIND_AUDIO", "videos": "DATA_KIND_VIDEOS"}
LAYOUT_KEYS = ("DATA_AREA", "DATA_SLUG") + tuple(KIND_KEYS[k] for k in KINDS)
EXTENSIONS = {
    "docs": ("pdf", "doc", "docx", "xls", "xlsx", "ppt", "pptx", "odt", "ods", "odp",
             "zip", "7z", "tar", "gz", "eml", "msg"),
    "photos": ("png", "jpg", "jpeg", "tif", "tiff", "heic", "webp", "gif", "psd", "bmp", "dng",
               "exr"),
    "audio": ("mp3", "wav", "flac", "m4a", "ogg", "aac", "aif", "aiff", "opus", "pcm"),
    "videos": ("mp4", "mov", "mkv", "webm", "mxf", "m4v", "mts", "m2ts", "avi", "braw", "r3d"),
}
EXT_KIND = {e: k for k, exts in EXTENSIONS.items() for e in exts}
SHARED_ROLES = ("issued", "signed", "ingested", "received", "archive", "evidence", "asset",
                "generated")
EVIDENCE_ROLES = ("signed", "evidence", "ingested", "received")
STATES = ("current", "superseded", "withdrawn")
SUPERSEDED, WITHDRAWN = STATES[1], STATES[2]
FIELDS = ("path", "kind", "filed_under", "role", "evidence", "sha256", "bytes", "filed", "state",
          "source", "replaces", "label", "former_name", "notes")
REQUIRED = ("path", "kind", "filed_under", "role", "sha256", "state")
NOT_TEXT = ("bytes", "evidence")   # the two fields that are not strings: an integer and a boolean
ANSWERS_NAME = re.compile(r"\.copier-answers\.(syntek-[^/\\]+)\.yml")
MAP_NAME = re.compile(r"(syntek-[^/\\]+)-dataroot\.json")
RESERVED = '<>:"/\\|?*'
DEVICES = ("CON", "PRN", "AUX", "NUL", "CONIN$", "CONOUT$")
SLUG = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")
ROLE_NAME = re.compile(r"[a-z][a-z0-9]*(?:-[a-z0-9]+)*")   # whole names only (fullmatch)
SHA = re.compile(r"[0-9a-f]{64}")
LAYOUT_CAP = 64
COMPONENT_CAP = 255           # UTF-16 units per name on NTFS
MAX_PATH = 260                # Windows MAX_PATH, and Office apps on OneDrive
ONEDRIVE_PATH = 400
WIN_RECALL = 0x00400000 | 0x00040000   # FILE_ATTRIBUTE_RECALL_ON_DATA_ACCESS and _ON_OPEN
MAC_DATALESS = 0x40000000              # SF_DATALESS
CHUNK = 1 << 20

SYNC_NAMES = ("OneDrive", "Dropbox", "My Drive", "Google Drive")
SYNC_PREFIXES = ("OneDrive - ", "Dropbox (")

# ── What root prints for the provider (the same in every template) ──────────────────────

EVERY_PROVIDER = (
    "Never put this repository inside a synced folder, and never put the data root inside a repository:",
    "  a sync service copies file by file and corrupts Git (Git FAQ).",
    "The template never syncs, uploads, downloads or deletes anything for you. You run the service.",
)
REPO_LINE = "The files are kept in the repository: this answer applies once you move them out."
CHECKLISTS = {
    "none": (
        "Provider: none. The data root exists on this machine only. Back it up yourself (an external disk,",
        "  a NAS, a cloud service), then re-answer DATA_PROVIDER so these checks match it.",
    ),
    "google-drive": (
        "Provider: Google Drive.",
        "- Keep files local: Drive for desktop in mirror mode, or add the data root under 'Folders from your",
        "  computer'. In stream mode, make the whole data root available offline.",
        "- macOS keeps Drive files under ~/Library/CloudStorage and that place cannot be changed: point",
        "  SYNTEK_DATA_ROOT there. Linux has no Drive for desktop: use rclone (see 'other cloud').",
        "- A conflicting edit leaves a second copy beside the original. Uploads that fail go to Drive's",
        "  lost_and_found folder, outside the data root.",
        "- Drive allows two files of one name in a folder, and names that differ only in case; a Windows or",
        "  macOS disk cannot hold both.",
    ),
    "onedrive": (
        "Provider: OneDrive or SharePoint.",
        "- The data root must sit inside the OneDrive or SharePoint library folder (NTFS, or case-insensitive",
        "  APFS): point SYNTEK_DATA_ROOT there. Choose 'Always keep on this device' for the data root.",
        "- Paths: at most 400 characters in the cloud, 260 in Office apps. OneDrive refuses desktop.ini,",
        "  .lock, names starting ~$ and names containing _vti_ (check-names applies these rules).",
        "- The losing side of a conflict is kept as a copy with a computer name added to its name.",
        "- A library that requires check-out or required columns syncs read-only. Use 'Sync' or 'Add",
        "  shortcut to My files' for a library, never both. No Microsoft client for Linux: use rclone.",
    ),
    "dropbox": (
        "Provider: Dropbox.",
        "- The data root must sit inside the Dropbox folder, on a local disk: Dropbox does not support a",
        "  network drive or a NAS. Make the data root available offline.",
        "- Conflicts are kept beside the original as '... conflicted copy YYYY-MM-DD' and '(Case Conflict)'.",
        "- Never mark the data root, or anything in it, as ignored: Dropbox then deletes its cloud copy.",
    ),
    "other-cloud": (
        "Provider: another cloud service, through a tool you run.",
        "- rclone sync is one-way and deletes at the destination what the source lacks: run --dry-run first.",
        "- rclone bisync is two-way and rclone calls it advanced: back up, start with --resync, and keep",
        "  --check-access --check-filename .syntek-data-root, so an empty or unmounted side stops it.",
        "- rclone mount needs --vfs-cache-mode writes or full; reading an uncached file downloads it.",
        "- bisync keeps conflicts as <name>.conflict1 and <name>.conflict2 (before v1.66: ..path1, ..path2).",
    ),
    "nas": (
        "Provider: a NAS or server on your network.",
        "- Where the share is the data root, create .syntek-data-root on the share: an unmounted share is an",
        "  empty folder, and the missing marker is how the tools notice.",
        "- Use hard NFS mounts (soft mounts can corrupt data silently). Windows and macOS clients, and Samba's",
        "  'case sensitive = auto', fold case: keep names Windows-safe (ntfs-3g: windows_names).",
        "- Keep this repository on a local disk: Git refuses a repository on a share owned by another user.",
        "- Where a tool such as Syncthing copies a local data root to the server, it keeps conflicts as",
        "  <stem>.sync-conflict-<date>-<time>-<device><ext>.",
    ),
}
UNKNOWN_PROVIDER = "Provider '{}': this tool does not know it; a newer template does."

# A name that looks like a sync service's conflict copy earns a hint, never a count or an exit
# code, and is never renamed or deleted. The OneDrive and Google Drive forms are common in
# ordinary names, so they count only beside a listed partner.
CONFLICTS = (
    ("Dropbox", re.compile(r"^(?P<base>.+) \((?P<who>.+)'s conflicted copy \d{4}-\d{2}-\d{2}(?: \(\d+\))?\)(?P<ext>\.[^.]*)?$")),
    ("Dropbox", re.compile(r"^(?P<base>.+) \((?:Case Conflict|Selective Sync Conflict)(?: \d+)?\)(?P<ext>\.[^.]*)?$")),
    ("rclone bisync", re.compile(r"^(?P<name>.+)\.conflict\d+$")),
    ("rclone bisync", re.compile(r"^(?P<name>.+)\.\.path[12]$")),
    ("Syncthing", re.compile(r"^(?P<base>.+)\.sync-conflict-\d{8}-\d{6}-[A-Z0-9]+(?P<ext>\.[^.]*)?$")),
)
GDRIVE_COPY = re.compile(r"^(?P<base>.+) \(\d+\)(?P<ext>\.[^.]*)?$")
HINT = "looks like a {} conflict copy of {}: compare them, keep one, and file it with add"

TODAY = None     # the self-test fixes the date
MACHINE = None   # and the machine's name
STAT = os.stat   # and what a file's attributes say


class Unreadable(Exception):
    """A map, manifest or answers file cannot be read as its format requires."""


class Unwritable(Exception):
    """A manifest cannot be rewritten as exactly the planned rows."""


class CopyMismatch(Exception):
    """A copy did not hash equal to what it was meant to be."""


def printable(text):
    """text as any output can show it: a name that is not UTF-8 (a surrogate escape) is written
    as its backslash escape, never an error halfway through a report."""
    return text.encode("utf-8", "backslashreplace").decode("utf-8")


def say(line=""):
    print(printable(line))


def warn(message):
    print("warning: " + printable(message), file=sys.stderr)


def refuse(message, code=2):
    print("refused: " + printable(message), file=sys.stderr)
    return code


def refuse_all(reasons):
    for r in reasons:
        refuse(r)
    return 2


def today():
    return TODAY or datetime.date.today()


def machine():
    name = MACHINE or os.environ.get("COMPUTERNAME") or platform.node()
    return name.split(".")[0]


def unique(values):
    out = []
    for v in values:
        if v not in out:
            out.append(v)
    return out


def listdir(path):
    try:
        return sorted(os.listdir(path))
    except OSError:
        return []


def human(n):
    for unit in ("bytes", "KB", "MB", "GB"):
        if n < 1024 or unit == "GB":
            return f"{n} {unit}" if unit == "bytes" else f"{n:.1f} {unit}"
        n /= 1024
    return f"{n} bytes"


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(CHUNK), b""):
            h.update(chunk)
    return h.hexdigest()


def norm(name):
    """The form two names are compared in for a clash: NFC, then case-folded."""
    return unicodedata.normalize("NFC", name).casefold()


def online_only(st, plat=None):
    """True when the operating system marks a file online-only (a read would download it)."""
    if (getattr(st, "st_file_attributes", 0) or 0) & WIN_RECALL:
        return True
    return (plat or sys.platform) == "darwin" and bool((getattr(st, "st_flags", 0) or 0) & MAC_DATALESS)


def file_online_only(path):
    try:
        return online_only(STAT(path))
    except OSError:
        return False


# ── Names ───────────────────────────────────────────────────────────────────────────────


def name_problem(name, cap=None):
    """Why one path component is not safe on Windows (and so on NTFS, SMB and APFS), or None."""
    if not name:
        return "is empty"
    try:
        name.encode("utf-8")
    except UnicodeEncodeError:
        return "is not valid UTF-8: rename it"
    bad = sorted({c for c in name if c in RESERVED})
    if bad:
        return "holds the reserved character " + " ".join(bad)
    if any(ord(c) < 32 or ord(c) == 127 for c in name):
        return "holds a control character"
    if name[-1] in ". ":
        return "ends with a dot or a space"
    if name[0] == " ":
        return "starts with a space"
    stem = name.split(".")[0].rstrip(" ").upper()
    if stem in DEVICES or (len(stem) == 4 and stem[:3] in ("COM", "LPT") and ("1" <= stem[3] <= "9" or stem[3] in "¹²³")):
        return "is a Windows device name"
    if cap and len(name) > cap:
        return f"is longer than {cap} characters"
    if len(name.encode("utf-16-le")) // 2 > COMPONENT_CAP:
        return f"is longer than {COMPONENT_CAP} characters, the NTFS limit"
    return None


def onedrive_problem(name):
    """Why OneDrive refuses one path component, or None."""
    low = name.lower()
    if low in ("desktop.ini", ".lock"):
        return "is a name OneDrive refuses"
    if name.startswith("~$"):
        return "starts with ~$, which OneDrive refuses"
    if "_vti_" in low:
        return "holds _vti_, which OneDrive refuses"
    return None


def slug_problem(slug):
    if not slug:
        return "is empty"
    if len(slug) > LAYOUT_CAP:
        return f"is longer than {LAYOUT_CAP} characters"
    if not SLUG.fullmatch(slug):
        return "may hold only a-z, 0-9 and single hyphens between them"
    if slug.upper() in DEVICES or (len(slug) == 4 and slug[:3] in ("com", "lpt") and "1" <= slug[3] <= "9"):
        return "is a Windows device name"
    return None


def rel_problem(rel):
    """Why a project-relative '/'-separated path is malformed, or None."""
    if not rel or rel.startswith("/") or rel.endswith("/") or "\\" in rel:
        return "must be a relative '/'-separated path"
    for part in rel.split("/"):
        if part in ("", ".", ".."):
            return "may hold no empty, '.' or '..' part"
        why = name_problem(part)
        if why:
            return f"'{part}' {why}"
    return None


def kind_of_name(rel):
    ext = rel.rsplit("/", 1)[-1].rpartition(".")[2].lower() if "." in rel.rsplit("/", 1)[-1] else ""
    return EXT_KIND.get(ext, "docs")


def is_binary(rel):
    name = rel.rsplit("/", 1)[-1]
    return "." in name and name.rpartition(".")[2].lower() in EXT_KIND


def case_clash(top, parts):
    """The first level under top where a part is missing but another spelling of it exists."""
    here = top
    for part in parts:
        try:
            names = [e.name for e in os.scandir(here)]
        except OSError:
            return None
        if part in names:
            here = os.path.join(here, part)
            continue
        same = [n for n in names if norm(n) == norm(part)]
        return (here, part, same[0]) if same else None
    return None


def superseded_name(name, stamp, exists):
    stem, ext = os.path.splitext(name)
    n = 1
    while True:
        suffix = "" if n == 1 else f"-{n}"
        candidate = f"{stem}.superseded-{stamp}{suffix}{ext}"
        if not exists(candidate):
            return candidate
        n += 1


def conflict_hint(name, rel, under, listed):
    """A hint for an unlisted file whose name looks like a sync service's conflict copy."""
    folder = rel.rsplit("/", 1)[0] + "/" if "/" in rel else ""
    if name.endswith(TMP_SUFFIX):
        return "an interrupted copy by this tool: compare it with its listed file, then remove it"
    for provider, rx in CONFLICTS:
        m = rx.match(name)
        if m:
            partner = m.groupdict().get("name") or (m["base"] + (m["ext"] or ""))
            return HINT.format(provider, folder + partner)
    stem, ext = os.path.splitext(name)
    host = machine()
    if host and stem.lower().endswith("-" + host.lower()):
        partner = folder + stem[:-(len(host) + 1)] + ext
        if (under, partner) in listed:
            return HINT.format("OneDrive", partner)
    m = GDRIVE_COPY.match(name)
    if m:
        partner = folder + m["base"] + (m["ext"] or "")
        if (under, partner) in listed:
            return HINT.format("Google Drive", partner)
    return None


# ── The answers files: a flat-scalar reader, so no YAML parser is needed ─────────────────

ESCAPES = {"0": "\0", "a": "\a", "b": "\b", "t": "\t", "\t": "\t", "n": "\n", "v": "\v",
           "f": "\f", "r": "\r", "e": "\x1b", " ": " ", '"': '"', "/": "/", "\\": "\\",
           "N": "\x85", "_": "\xa0", "L": "\u2028", "P": "\u2029"}


def yaml_scalar(raw):
    """One flat YAML scalar as a rendered answers file writes it: plain, '...' or "..."."""
    s = raw.strip()
    if not s:
        return None
    if s[0] == "'":
        out, i = [], 1
        while i < len(s):
            if s[i] == "'":
                if s[i + 1:i + 2] == "'":
                    out.append("'")
                    i += 2
                    continue
                return "".join(out)
            out.append(s[i])
            i += 1
        raise ValueError("a single-quoted value is not closed")
    if s[0] == '"':
        out, i = [], 1
        while i < len(s):
            c = s[i]
            if c == '"':
                return "".join(out)
            if c == "\\":
                nxt = s[i + 1:i + 2]
                if nxt in ESCAPES:
                    out.append(ESCAPES[nxt])
                    i += 2
                    continue
                width = {"x": 2, "u": 4, "U": 8}.get(nxt)
                if width and re.fullmatch(r"[0-9A-Fa-f]+", s[i + 2:i + 2 + width] or "-"):
                    out.append(chr(int(s[i + 2:i + 2 + width], 16)))
                    i += 2 + width
                    continue
                raise ValueError(f"an unknown escape \\{nxt}")
            out.append(c)
            i += 1
        raise ValueError("a double-quoted value is not closed")
    cut = re.search(r"\s#", s)
    if cut:
        s = s[:cut.start()].rstrip()
    return None if s in ("~", "null", "Null", "NULL") else s


def join_scalar(parts):
    first = parts[0].strip()
    if first.startswith('"'):
        text = parts[0].rstrip()
        for p in parts[1:]:
            if re.search(r"(?<!\\)(?:\\\\)*\\$", text):
                text = text[:-1] + p.lstrip()
            else:
                text = text + " " + p.lstrip()
        return yaml_scalar(text)
    return yaml_scalar(" ".join(p.strip() for p in parts if p.strip()))


def read_answers(path):
    """Every DATA_* key of one answers file, as strings (a null or empty value is left out)."""
    lines = Path(path).read_text(encoding="utf-8").splitlines()
    values = {}
    i = 0
    while i < len(lines):
        m = re.match(r"(DATA_[A-Z0-9_]+):(?:[ \t]+(.*))?$", lines[i].rstrip())
        i += 1
        if not m:
            continue
        parts = [m.group(2) or ""]
        while i < len(lines) and lines[i][:1] in (" ", "\t") and lines[i].strip():
            parts.append(lines[i])
            i += 1
        value = join_scalar(parts)
        if value:
            values[m.group(1)] = value
    return values


# ── The root: an ordered chain of sources ───────────────────────────────────────────────


class Root:
    def __init__(self, path, origin):
        self.path = path
        self.origin = origin


class RootInvalid:
    def __init__(self, reason, origin, marker, contained=False):
        self.reason = reason
        self.origin = origin
        self.marker = marker
        self.contained = contained   # the root and the repository contain one another


# Each source returns None when it is not set, or (value, origin) when it is. A source that
# is set but invalid stops the resolver (exit 2): it never falls through, so a later source
# can never silently replace a mistyped earlier one.
def from_environment(project, environ):
    if ROOT_ENV not in environ:
        return None
    return environ[ROOT_ENV], ORIGIN_ENV


# One source in this release. A later release appends file sources after it, each returning
# (value, origin) the same way; the order and 'set but invalid stops' never change.
SOURCES = (from_environment,)


def resolve(project, environ):
    for source in SOURCES:
        found = source(project, environ)
        if found is not None:
            return check(project, *found)
    return None


def marker_format(path):
    try:
        with open(path, "rb") as f:
            text = f.read(4096).decode("utf-8", "replace")
    except OSError:
        return None
    m = re.search(r"^[ \t]*format[ \t]*=[ \t]*(\d+)[ \t]*(?:#.*)?$", text, re.MULTILINE)
    return int(m.group(1)) if m else None


def check(project, value, origin):
    """What makes a root valid: Root, or RootInvalid with the one reason."""
    if value == "":
        return RootInvalid(f"{ROOT_ENV} is set but empty: unset it, or name the data root", origin, "not checked")
    path = os.path.expanduser(value)
    if not os.path.isabs(path):
        return RootInvalid(f"{ROOT_ENV} is '{value}', which is not an absolute path", origin, "not checked")
    path = os.path.normpath(path)
    if not os.path.isdir(path):
        what = "is not a folder" if os.path.exists(path) else "does not exist (is the volume mounted?)"
        return RootInvalid(f"{ROOT_ENV} names {path}, which {what}", origin, "not checked")
    marker = os.path.join(path, MARKER)
    if not os.path.isfile(marker):
        return RootInvalid(f"{path} holds no {MARKER} marker; if it is the data root, create it: "
                           f'touch "${ROOT_ENV}/{MARKER}" (the tools never do)', origin, "missing")
    fmt = marker_format(marker)
    if fmt is not None and fmt > FORMAT:
        return RootInvalid(f"{marker} is marker format {fmt}, and this tool knows format {FORMAT}: "
                           "it needs a newer template", origin, "newer format")
    real, mine = os.path.realpath(path), os.path.realpath(str(project))
    if within(real, mine):
        return RootInvalid(f"the data root {path} lies inside this repository, where Git would commit "
                           "or ignore its files by accident: move it out", origin, "present", True)
    if within(mine, real):
        return RootInvalid(f"the data root {path} holds this repository, and a sync service corrupts "
                           "Git: move the repository out of it", origin, "present", True)
    return Root(path, origin)


def marker_above(project):
    """The folder at or above the project that holds a marker, or None."""
    here = os.path.realpath(str(project))
    while True:
        if os.path.isfile(os.path.join(here, MARKER)):
            return here
        up = os.path.dirname(here)
        if up == here:
            return None
        here = up


def sync_ancestor(path):
    """The nearest folder at or above path that looks like a sync service's folder, or None."""
    parts = Path(os.path.realpath(path)).parts
    for i in range(len(parts), 0, -1):
        here = os.path.join(*parts[:i])
        name = parts[i - 1]
        if name in SYNC_NAMES or name.startswith(SYNC_PREFIXES):
            return here
        if i >= 2 and parts[i - 2] == "Library" and name == "CloudStorage":
            return here
        if os.path.isdir(os.path.join(here, ".stfolder")):
            return here
    return None


# ── The project: its answers, its maps, its manifests ───────────────────────────────────


def find_project(cwd):
    try:
        out = subprocess.run(["git", "rev-parse", "--show-toplevel"], cwd=cwd, capture_output=True, check=False)
        top = os.fsdecode(out.stdout).strip()
        if out.returncode == 0 and top:
            return Path(top)
    except OSError:
        pass
    here = Path(os.path.abspath(cwd))
    for folder in (here, *here.parents):
        if any(ANSWERS_NAME.fullmatch(n) for n in listdir(folder)):
            return folder
    return None


class Record:
    def __init__(self, template, name, values):
        self.template = template
        self.name = name
        self.values = values
        self.store = values.get("DATA_STORE")


class Folder:
    def __init__(self, path, kind, warn_over, source, takes_rows=True):
        self.path = path
        self.kind = kind
        self.warn_over = warn_over
        self.source = source
        self.takes_rows = takes_rows     # False for a folder marked "rows": "none"

    def holds(self, rel):
        return rel == self.path or rel.startswith(self.path + "/")

    def meets(self, path):
        """True when the folder and path overlap: one is the other, or lies inside it."""
        return self.holds(path) or path.startswith(self.path + "/") or self.path.startswith(path + "/")


class BadMap:
    """A map that cannot be read: its name, why, and the folders it names (None: unknown)."""

    def __init__(self, name, reason, claims):
        self.name = name
        self.reason = reason
        self.claims = claims

    def claim(self, path):
        """The folder of this map that path is, lies in or holds, or None."""
        return next((c for c in self.claims or [] if path == c or path.startswith(c + "/")
                     or c.startswith(path + "/")), None)

    def touches(self, path):
        return self.claim(path) is not None

    def refusal(self, path):
        return (f"{self.claim(path) or path} is named by .claude/{self.name}, which cannot be read "
                f"({self.reason}): the commands that touch its folders refuse until it is fixed")


class Layout:
    def __init__(self, area, slug, kinds):
        self.area = area
        self.slug = slug
        self.kinds = kinds

    def under(self, kind):
        return f"{self.area}/{self.kinds[kind]}/{self.slug}"


class Row:
    def __init__(self, raw, index, folder=None):
        self.raw = raw
        self.index = index
        self.folder = folder
        for f in FIELDS:
            setattr(self, f, raw.get(f, {"bytes": 0, "evidence": False}.get(f, "")))


def listing(records, key):
    return ", ".join(f"{r.template} '{r.values.get(key)}'" for r in records)


class Context:
    """Everything one run needs: the project, its answers, its maps, the root."""

    def __init__(self, project, environ):
        self.project = Path(project)
        self.environ = environ
        self.records = []
        self.problems = []
        self.warnings = []
        self.store = None
        self.layout = None
        self.providers = []
        self.folders = []
        self.clashes = []
        self.bad_maps = []
        self.roles = {r: r in EVIDENCE_ROLES for r in SHARED_ROLES}
        self.skip_roles = set()          # map roles that every defining map marks "repo": "skip"
        self.root = None
        self.root_error = None
        self.contained = False
        self.origin = None
        self.marker = "not checked"
        self.cache = {}
        self.load_records()
        self.load_maps()
        self.load_root()

    # The answers.
    def load_records(self):
        for name in listdir(self.project):
            m = ANSWERS_NAME.fullmatch(name)
            if not m or not (self.project / name).is_file():
                continue
            try:
                values = read_answers(self.project / name)
            except (OSError, UnicodeDecodeError, ValueError) as err:
                self.problems.append(f"{name} cannot be read: {err}")
                continue
            self.records.append(Record(m.group(1), name, values))
        for r in self.records:
            if not r.store:
                self.warnings.append(f"{r.name} records no DATA_STORE (not yet asked): {r.template} keeps "
                                     "its files in the repository until it is updated and answers")
        held = [r for r in self.records if r.store]
        if not self.records:
            self.problems.append("no .copier-answers.syntek-*.yml here records the project's answers")
        elif not held:
            self.problems.append("no answers file here records DATA_STORE yet: update a template so that it asks")
        elif len(unique(r.store for r in held)) > 1:
            self.problems.append(f"the answers files disagree on DATA_STORE ({listing(held, 'DATA_STORE')}): "
                                 "one project keeps one store, so answer the same in every template")
        else:
            self.store = held[0].store
            if self.store not in STORES:
                self.problems.append(f"this project's store '{self.store}' needs a newer template")
            elif self.store == "external":
                self.load_layout(held)
        given = [r for r in self.records if r.values.get("DATA_PROVIDER")]
        self.providers = unique(r.values["DATA_PROVIDER"] for r in given)
        if len(self.providers) > 1:
            self.warnings.append(f"the answers files differ on DATA_PROVIDER ({listing(given, 'DATA_PROVIDER')}): "
                                 "it moves no file, so nothing refuses; answer the same in every template "
                                 "so the checks match the service")

    def load_layout(self, held):
        values = {}
        for key in LAYOUT_KEYS:
            seen = []
            for r in held:
                if not r.values.get(key):
                    self.problems.append(f"{r.name} records DATA_STORE external but no {key}: update it and answer")
                    return
                seen.append(r.values[key])
            if len(unique(seen)) > 1:
                self.problems.append(f"the answers files disagree on {key} ({listing(held, key)}): every "
                                     "template files into one layout, so answer the same in each")
                return
            values[key] = seen[0]
        area, slug = values["DATA_AREA"], values["DATA_SLUG"]
        kinds = {k: values[KIND_KEYS[k]] for k in KINDS}
        bad = []
        why = name_problem(area, LAYOUT_CAP)
        if why:
            bad.append(f"DATA_AREA '{area}' {why}")
        why = slug_problem(slug)
        if why:
            bad.append(f"DATA_SLUG '{slug}' {why}")
        for k in KINDS:
            why = name_problem(kinds[k], LAYOUT_CAP)
            if why:
                bad.append(f"{KIND_KEYS[k]} '{kinds[k]}' {why}")
        if len({norm(v) for v in kinds.values()}) < len(KINDS):
            bad.append("the four kind folders must differ, ignoring case")
        for b in bad:
            self.problems.append(b + ": re-answer it")
        if not bad:
            self.layout = Layout(area, slug, kinds)

    # The maps. A map that cannot be read refuses only what touches its folders (BadMap).
    def load_maps(self):
        import json
        claude = self.project / ".claude"
        defined = {}
        for name in listdir(claude):
            m = MAP_NAME.fullmatch(name)
            if not m:
                continue
            template = m.group(1)
            data = None
            try:
                data = json.loads((claude / name).read_text(encoding="utf-8"))
                folders, roles = parse_map(data)
            except (OSError, UnicodeDecodeError, ValueError, Unreadable) as err:
                bad = BadMap(name, str(err), claimed_folders(data))
                self.bad_maps.append(bad)
                where = ", ".join(bad.claims) if bad.claims else "not known, so files outside every other map's folders are not judged"
                self.warnings.append(f".claude/{name} cannot be read: {err}; the commands that touch its folders "
                                     f"refuse until it is fixed, and every other command runs (its folders: {where})")
                continue
            for path, kind, warn_over, takes_rows in folders:
                self.folders.append(Folder(path, kind, warn_over, template, takes_rows))
            for role, evidence, skip in roles:
                defined.setdefault(role, []).append((template, evidence, skip))
        for role, defs in defined.items():
            self.roles[role] = any(evidence for _, evidence, _ in defs)
            if all(skip for _, _, skip in defs):
                self.skip_roles.add(role)
            if len({(evidence, skip) for _, evidence, skip in defs}) > 1:
                how = "; ".join(f"{t}: evidence {'true' if e else 'false'}" + (', "repo": "skip"' if s else "")
                                for t, e, s in defs)
                self.warnings.append(f"the maps define the role '{role}' differently ({how}): evidence wins, so it "
                                     f"is {'evidence' if self.roles[role] else 'not evidence'}, and it is skipped "
                                     "under repo only where every map says so")
        for i, a in enumerate(self.folders):
            for b in self.folders[i + 1:]:
                if a.source != b.source and (a.holds(b.path) or b.holds(a.path)):
                    self.clashes.append((a, b))

    def present(self):
        return [f for f in self.folders if (self.project / f.path).is_dir()]

    def filing(self):
        """The present folders that take rows."""
        return [f for f in self.present() if f.takes_rows]

    def folder_for(self, rel, folders=None):
        found = [f for f in (self.present() if folders is None else folders) if f.holds(rel)]
        return max(found, key=lambda f: len(f.path)) if found else None

    def clash_reason(self, a, b):
        return (f"{a.path} (in .claude/{a.source}-dataroot.json) and {b.path} (in "
                f".claude/{b.source}-dataroot.json) claim one folder: every folder belongs to one "
                "template's map")

    def blocked(self, rels):
        """Every reason the data commands cannot act on the project paths rels."""
        reasons = list(self.problems)
        for a, b in self.clashes:
            if any(a.holds(r) or b.holds(r) for r in rels):
                reasons.append(self.clash_reason(a, b))
        for bad in self.bad_maps:
            reasons.extend(bad.refusal(r) for r in rels if bad.touches(r))
        return reasons

    def folder_refusals(self, folder):
        """Why a whole-project command must leave one folder alone (its clashes, a bad map's claim)."""
        reasons = [self.clash_reason(a, b) for a, b in self.clashes if folder in (a, b)]
        reasons.extend(bad.refusal(folder.path) for bad in self.bad_maps if bad.touches(folder.path))
        return reasons

    def readable(self):
        """(rows, refused) over the present folders that take rows: refused is [(path, reason)],
        one per folder a whole-project command must leave alone (a clash, a manifest that cannot
        be read, or a present folder a map that cannot be read names), each refused alone."""
        rows, refused = [], []
        for f in self.filing():
            reasons = self.folder_refusals(f)
            if not reasons:
                try:
                    rows.extend(self.manifest(f)[1])
                    continue
                except Unreadable as err:
                    reasons = [str(err)]
            if f.path not in (p for p, _ in refused):
                refused.append((f.path, reasons[0]))
        for bad in self.bad_maps:
            for path in bad.claims or []:
                if (self.project / path).is_dir() and path not in (p for p, _ in refused):
                    refused.append((path, bad.refusal(path)))
        return rows, refused

    def judged(self, rel, refused=()):
        """True when a project file lies in a folder that takes rows and a command may read."""
        folder = self.folder_for(rel)
        return (folder is not None and folder.takes_rows and not any(rel.startswith(p + "/") for p in refused)
                and not any(b.touches(rel) for b in self.bad_maps))

    def unknown_maps(self):
        return [b for b in self.bad_maps if b.claims is None]

    def evidence(self, role):
        """Whether a role is evidence now: a shared evidence role, or a map's; unknown counts."""
        return self.roles.get(role, True)

    def protected(self, row):
        """A row is protected where its own flag or any present definition says so."""
        return row.evidence is True or self.evidence(row.role)

    def onedrive(self):
        return "onedrive" in self.providers

    # The root.
    def load_root(self):
        found = resolve(self.project, self.environ)
        if found is not None:
            self.origin = found.origin
        above = marker_above(self.project)
        # The repository and a data root contain one another: status warns of it under either
        # store, and says it did not check the copies; under repo, path and add refuse it.
        self.contained = bool(above) or (isinstance(found, RootInvalid) and found.contained)
        if above:
            self.root_error = (f"a {MARKER} marker in {above} puts this repository inside a data root, "
                               "and a sync service corrupts Git: move the repository or the marker")
            self.origin = self.origin or "a marker at or above the repository"
            self.marker = "present"
        elif isinstance(found, RootInvalid):
            self.root_error = found.reason
            self.marker = found.marker
        elif found is not None:
            self.root = found
            self.marker = "present"
        repo_sync = sync_ancestor(self.project)
        if repo_sync:
            self.warnings.append(f"this repository sits under {repo_sync}, which looks like a synced folder: "
                                 "a sync service copies file by file and corrupts Git; move the repository out")
        if self.root and (self.providers or ["none"]) == ["none"]:
            root_sync = sync_ancestor(self.root.path)
            if root_sync:
                self.warnings.append(f"the data root sits under {root_sync}, which looks like a synced "
                                     "folder, but DATA_PROVIDER is none: re-answer DATA_PROVIDER so the "
                                     "checks match the service")

    def no_root(self):
        if self.root_error:
            return self.root_error
        return (f"{ROOT_ENV} is not set: this project files its binaries under the data root "
                f"(DATA_STORE external), so name the root in {ROOT_ENV} on this machine (see README)")

    def place(self, under, rel):
        parts = [p for p in rel.split("/") if p]
        return os.path.join(self.root.path, *under.split("/"), *parts)

    def at(self, row):
        return self.place(row.filed_under, row.path)

    # The manifests.
    def manifest_path(self, folder):
        return self.project / folder.path / MANIFEST

    def manifest(self, folder):
        """(text or None, rows) of one folder's manifest; Unreadable on a bad one."""
        if folder.path not in self.cache:
            path = self.manifest_path(folder)
            if not path.exists():
                self.cache[folder.path] = (None, [])
            else:
                try:
                    text = path.read_bytes().decode("utf-8")   # line endings kept as they are
                except (OSError, UnicodeDecodeError) as err:
                    raise Unreadable(f"{folder.path}/{MANIFEST} cannot be read: {err}") from None
                self.cache[folder.path] = (text, parse_manifest(text, folder, self))
        return self.cache[folder.path]

    def warn_all(self):
        for w in self.warnings:
            warn(w)


def claimed_folders(data):
    """The folder paths a map that cannot be read still names, or None when they are not known."""
    entries = data.get("folders") if isinstance(data, dict) else None
    if not isinstance(entries, list):
        return None
    paths = [e.get("path") if isinstance(e, dict) else None for e in entries]
    if not all(isinstance(p, str) and not rel_problem(p) for p in paths):
        return None
    return unique(paths)


def parse_map(data):
    """The folders [(path, kind, warn_over in bytes, takes rows)] and roles [(name, evidence,
    skipped under repo)] of one map. A key this tool does not know is ignored."""
    if not isinstance(data, dict):
        raise Unreadable("it is not a JSON object")
    fmt = data.get("format")
    if isinstance(fmt, bool) or not isinstance(fmt, int):
        raise Unreadable("it has no integer format")
    if fmt > FORMAT:
        raise Unreadable(f"it is format {fmt}, and this tool reads format {FORMAT}: it needs a newer template")
    if fmt != FORMAT:
        raise Unreadable(f"its format {fmt} is not {FORMAT}")
    entries = data.get("folders")
    if not isinstance(entries, list):
        raise Unreadable("'folders' is not a list")
    folders, seen = [], set()
    for i, e in enumerate(entries):
        path = e.get("path") if isinstance(e, dict) else None
        if not isinstance(path, str):
            raise Unreadable(f"folders[{i}] has no path")
        why = rel_problem(path)
        if why:
            raise Unreadable(f"folders[{i}] path '{path}' {why}")
        if path in seen:
            raise Unreadable(f"folders[{i}] names '{path}' twice")
        seen.add(path)
        kind = e.get("kind")
        if kind is not None and kind not in KINDS:
            raise Unreadable(f"folders[{i}] kind '{kind}' is not one of {', '.join(KINDS)}")
        over = e.get("warn_over_kib")
        if over is not None and (isinstance(over, bool) or not isinstance(over, int) or over <= 0):
            raise Unreadable(f"folders[{i}] warn_over_kib is not a positive integer")
        rows = e.get("rows")
        if rows is not None and rows != "none":
            raise Unreadable(f"folders[{i}] rows is not \"none\" (the one value: working output that never takes rows)")
        folders.append((path, kind, over * 1024 if over else None, rows is None))
    roles, named = [], set()
    extra = data.get("roles", [])
    if not isinstance(extra, list):
        raise Unreadable("'roles' is not a list")
    for i, e in enumerate(extra):
        name = e.get("name") if isinstance(e, dict) else None
        if not isinstance(name, str) or not ROLE_NAME.fullmatch(name):
            raise Unreadable(f"roles[{i}] needs a name in lower-case words joined by hyphens (brand-export)")
        if name in SHARED_ROLES or name in KINDS:
            raise Unreadable(f"roles[{i}] '{name}' is a {'shared role' if name in SHARED_ROLES else 'kind'}'s name, "
                             "which a map never defines")
        if name in named:
            raise Unreadable(f"roles[{i}] defines '{name}' twice")
        named.add(name)
        evidence = e.get("evidence")
        if not isinstance(evidence, bool):
            raise Unreadable(f"roles[{i}] evidence is not true or false")
        repo = e.get("repo")
        if repo is not None and repo != "skip":
            raise Unreadable(f"roles[{i}] repo is not \"skip\" (the one value: under repo, never filed)")
        roles.append((name, evidence, repo == "skip"))
    return folders, roles


def row_problem(r, folder):
    """Why one row is not one a manifest of folder may hold (the text after 'row <n>'), or None.
    The reader refuses such a manifest, and add checks the row it plans by the same rules, so it
    never writes a row it would then refuse."""
    if not isinstance(r, dict):
        return " is not a table"
    for f in REQUIRED:
        if not isinstance(r.get(f), str) or not r.get(f):
            return f" has no {f}"
    for f in FIELDS:
        if f in r and f not in NOT_TEXT and not isinstance(r[f], str):
            return f"'s {f} is not a string"
    if "bytes" in r and (isinstance(r["bytes"], bool) or not isinstance(r["bytes"], int) or r["bytes"] < 0):
        return "'s bytes is not a whole number"
    if "evidence" in r and not isinstance(r["evidence"], bool):
        return "'s evidence is not true or false"
    why = rel_problem(r["path"])
    if why or not r["path"].startswith(folder.path + "/"):
        return f"'s path '{r['path']}' {why or 'lies outside ' + folder.path}"
    parts = r["filed_under"].split("/")
    if len(parts) != 3 or any(name_problem(p) or p in (".", "..") for p in parts):
        return f"'s filed_under '{r['filed_under']}' is not <area>/<kind folder>/<slug>"
    if r["kind"] not in KINDS:
        return f"'s kind '{r['kind']}' is not one of {', '.join(KINDS)}"
    if not SHA.fullmatch(r["sha256"]):
        return "'s sha256 is not 64 lower-case hex digits"
    if r["state"] not in STATES:
        return f"'s state '{r['state']}' is not one of {', '.join(STATES)}"
    return None


def parse_manifest(text, folder, ctx):
    import tomllib
    where = f"{folder.path}/{MANIFEST}"
    try:
        data = tomllib.loads(text)
    except tomllib.TOMLDecodeError as err:
        raise Unreadable(f"{where} is not valid TOML: {err}") from None
    fmt = data.get("format")
    if isinstance(fmt, bool) or not isinstance(fmt, int):
        raise Unreadable(f"{where} has no integer format")
    if fmt > FORMAT:
        raise Unreadable(f"{where} is format {fmt}, and this tool reads format {FORMAT}: it needs a newer template")
    if fmt != FORMAT:
        raise Unreadable(f"{where} is format {fmt}, not {FORMAT}")
    raw_rows = data.get("file", [])
    if not isinstance(raw_rows, list):
        raise Unreadable(f"{where}: 'file' is not a list of [[file]] rows")
    rows = []
    for i, r in enumerate(raw_rows):
        n = i + 1
        why = row_problem(r, folder)
        if why:
            raise Unreadable(f"{where}: row {n}{why}")
        if r["role"] not in ctx.roles:
            note = f"{where}: row {n}'s role '{r['role']}' is defined by no map here: it is treated as evidence"
            if note not in ctx.warnings:
                ctx.warnings.append(note)
                warn(note)
        rows.append(Row(r, i, folder))
    return rows


def toml_str(s):
    out = []
    for c in s:
        if c == "\\":
            out.append("\\\\")
        elif c == '"':
            out.append('\\"')
        elif ord(c) < 0x20 or ord(c) == 0x7F:
            out.append(f"\\u{ord(c):04x}")
        else:
            out.append(c)
    return '"' + "".join(out) + '"'


def row_text(row):
    lines = ["[[file]]"]
    for f in FIELDS:
        v = row[f]
        if f == "bytes":
            lines.append(f"{f} = {v}")
        elif f == "evidence":
            lines.append(f"{f} = {'true' if v else 'false'}")
        else:
            lines.append(f"{f} = {toml_str(v)}")
    return "\n".join(lines) + "\n"


STATE_LINE = re.compile(r"(?P<lead>[ \t]*state[ \t]*=[ \t]*)(?P<value>\"(?:[^\"\\\r\n]|\\.)*\"|'[^'\r\n]*')"
                        r"(?P<tail>[ \t]*(?:#[^\r\n]*)?(?:\r?\n)?)")


def replace_state(text, index, state):
    """text with the value on the state line of the index-th [[file]] block replaced, every other
    byte kept (a comment after it included); Unwritable where there is not exactly one."""
    lines = text.splitlines(keepends=True)
    heads = [i for i, line in enumerate(lines) if line.strip() == "[[file]]"]
    if index >= len(heads):
        raise Unwritable("its [[file]] headers do not match its rows")
    start = heads[index] + 1
    end = heads[index + 1] if index + 1 < len(heads) else len(lines)
    hits = [i for i in range(start, end) if re.match(r"[ \t]*state[ \t]*=", lines[i])]
    m = STATE_LINE.fullmatch(lines[hits[0]]) if len(hits) == 1 else None
    if not m:
        raise Unwritable(f"row {index + 1} has no single 'state = \"...\"' line")
    lines[hits[0]] = m["lead"] + toml_str(state) + m["tail"]
    return "".join(lines)


def write_manifest(path, text, rows, new_row, supersede=None):
    """Append new_row (and change one row's state to superseded) only if tomllib reads back
    exactly that plan: the old rows, every key kept, with that one state changed, then the new."""
    import tomllib
    expect = [dict(r.raw) for r in rows]
    nl = "\r\n" if text and "\r\n" in text else "\n"
    if text is None:
        out = f"format = {FORMAT}\n\n" + row_text(new_row)
    else:
        body = text
        if supersede is not None:
            body = replace_state(body, supersede, SUPERSEDED)
            expect[supersede]["state"] = SUPERSEDED
        if body and not body.endswith("\n"):
            body += nl
        out = body + nl + row_text(new_row).replace("\n", nl)
    expect.append(dict(new_row))
    try:
        got = tomllib.loads(out)
    except tomllib.TOMLDecodeError as err:
        raise Unwritable(f"the new text would not parse ({err})") from None
    if got.get("format") != FORMAT or got.get("file", []) != expect:
        raise Unwritable("it is not in the form this tool writes; add the row by hand")
    tmp = str(path) + TMP_SUFFIX
    with open(tmp, "w", encoding="utf-8", newline="") as f:
        f.write(out)
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp, path)


# ── Copies ──────────────────────────────────────────────────────────────────────────────


def fsync_dir(path):
    if os.name == "nt":
        return
    with contextlib.suppress(OSError):
        fd = os.open(path, os.O_RDONLY)
        try:
            os.fsync(fd)
        finally:
            os.close(fd)


def put_in_place(tmp, dest):
    """Move tmp to dest, never over an existing file."""
    try:
        os.link(tmp, dest)
    except FileExistsError:
        os.unlink(tmp)
        raise
    except OSError:
        if os.path.lexists(dest):
            os.unlink(tmp)
            raise FileExistsError(dest) from None
        os.rename(tmp, dest)
        return
    os.unlink(tmp)


def copy_verified(src, dest, expect=None):
    """Copy src to dest by way of dest.syntek-tmp: fsync, link or rename, hash again."""
    tmp = dest + TMP_SUFFIX
    if os.path.lexists(tmp):
        if os.path.islink(tmp) or not os.path.isfile(tmp):
            raise OSError(f"{tmp} is in the way")
        os.unlink(tmp)
    h, size = hashlib.sha256(), 0
    with open(src, "rb") as fin:
        fd = os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_BINARY", 0), 0o644)
        try:
            with os.fdopen(fd, "wb") as fout:
                for chunk in iter(lambda: fin.read(CHUNK), b""):
                    h.update(chunk)
                    size += len(chunk)
                    fout.write(chunk)
                fout.flush()
                os.fsync(fout.fileno())
        except BaseException:
            with contextlib.suppress(OSError):
                os.unlink(tmp)
            raise
    sha = h.hexdigest()
    if expect is not None and sha != expect:
        os.unlink(tmp)
        raise CopyMismatch(f"{src} does not hash as its row says")
    put_in_place(tmp, dest)
    fsync_dir(os.path.dirname(dest))
    if sha256_file(dest) != sha:
        os.unlink(dest)
        raise CopyMismatch(f"{dest} did not hash equal to its source after the copy, so it was removed")
    return sha, size


# ── Git (names only: the tool hashes a file the owner names or a listed row, nothing else) ─


def git_out(ctx, *args):
    try:
        out = subprocess.run(["git", "-C", str(ctx.project), *args], capture_output=True, check=False)
    except OSError:
        return None
    return out if out.returncode in (0, 1) else None


def git_ok(ctx, *args):
    """git's stdout when it exits 0, else None (no work tree, no HEAD, no such path)."""
    out = git_out(ctx, *args)
    return out.stdout if out is not None and out.returncode == 0 else None


def git_files(ctx, paths, *flags):
    """Project-relative files git lists under paths, or None outside a work tree."""
    out = git_out(ctx, "ls-files", "-z", *flags, "--", *paths)
    if out is None or out.returncode != 0:
        return None
    return [os.fsdecode(p) for p in out.stdout.split(b"\0") if p]


def git_ignored(ctx, rels):
    if not rels:
        return set()
    out = git_out(ctx, "check-ignore", "-z", "--", *rels)
    if out is None:
        return None
    return {os.fsdecode(p) for p in out.stdout.split(b"\0") if p}


def walk_files(ctx, folder):
    top = ctx.project / folder.path
    out = []
    for here, dirs, files in os.walk(top):
        dirs[:] = sorted(d for d in dirs if d != ".git")
        for n in sorted(files):
            out.append(os.path.relpath(os.path.join(here, n), ctx.project).replace(os.sep, "/"))
    return out


def project_rel(ctx, value):
    """value (from the project's top, or absolute inside it) as a project path, or None outside."""
    p = os.path.expanduser(value)
    if not os.path.isabs(p):
        p = os.path.join(str(ctx.project), p)
    for top, cand in ((str(ctx.project), os.path.abspath(p)),
                      (os.path.realpath(str(ctx.project)), os.path.realpath(p))):
        mine = os.path.normpath(top)
        if within(cand, mine):
            rel = os.path.relpath(cand, mine)
            return "" if rel == "." else rel.replace(os.sep, "/")
    return None


def mirror_files(ctx, rows):
    """(under, rel, full path) of every file in every folder of the root this project uses."""
    unders = {r.filed_under for r in rows}
    if ctx.layout:
        unders |= {ctx.layout.under(k) for k in KINDS}
    out = []
    for under in sorted(unders):
        top = os.path.join(ctx.root.path, *under.split("/"))
        for here, dirs, files in os.walk(top):
            dirs.sort()
            for n in sorted(files):
                full = os.path.join(here, n)
                out.append((under, os.path.relpath(full, top).replace(os.sep, "/"), full))
    return out


def listed_files(rows):
    """(filed_under, path) of every file the rows list: each row's own file, and each kept copy
    a superseding row's replaces names, under the filed_under of the row it superseded (the
    last row before it, in the same manifest, of the same path)."""
    listed = {(r.filed_under, r.path) for r in rows}
    seen = {}
    for r in rows:
        group = seen.setdefault(id(r.folder), [])
        if r.replaces:
            before = [o for o in group if o.path == r.path]
            listed.add(((before[-1] if before else r).filed_under, r.replaces))
        group.append(r)
    return listed


def unlisted(ctx, rows, files, want, refused=()):
    """([(under, rel, note)], unjudged) for the mirror files no row lists. A file under a folder
    a command left alone, or named by a map that cannot be read, is not judged, nor is one
    outside every map folder while some map's folders are unknown; a folder marked "rows":
    "none" is never listed."""
    listed = listed_files(rows)
    unknown = bool(ctx.unknown_maps())
    out, unjudged = [], 0
    for under, rel, _ in files:
        if (under, rel) in listed or not want(rel):
            continue
        if any(rel.startswith(p + "/") for p in refused) or any(b.touches(rel) for b in ctx.bad_maps):
            unjudged += 1
            continue
        folder = ctx.folder_for(rel, ctx.folders)
        if folder is not None and not folder.takes_rows:
            continue
        if folder is None and unknown:
            unjudged += 1
            continue
        notes = [] if folder else ["outside every map folder, where no row can list it"]
        hint = conflict_hint(rel.rsplit("/", 1)[-1], rel, under, listed)
        out.append((under, rel, "; ".join(notes + ([hint] if hint else []))))
    return out, unjudged


def say_unlisted(extra, unjudged):
    for under, rel, note in extra:
        say(f"unlisted: {under}/{rel}" + (f" ({note})" if note else ""))
    if unjudged:
        warn(f"{unjudged} file(s) under the data root were not judged: they lie in a folder left alone "
             "above, or where a map that cannot be read may name one")


def glob_meets(glob, path):
    """True when a GLOB may match a file under the folder path: its literal start and the
    folder's path agree as far as both go (no GLOB: every folder)."""
    if not glob:
        return True
    start = re.split(r"[*?[]", glob, maxsplit=1)[0]
    folder = path + "/"
    return folder.startswith(start) or start.startswith(folder)


def layout_clashes(ctx):
    seen = []
    for k in KINDS:
        clash = case_clash(ctx.root.path, ctx.layout.under(k).split("/"))
        if clash and clash not in seen:
            seen.append(clash)
            here, part, found = clash
            warn(f"{os.path.join(here, found)} differs only in case or Unicode form from this project's "
                 f"'{part}': a case-insensitive disk treats them as one folder, others as two; rename "
                 "the folder, or re-answer, so that every machine files into one")


def restore_args(ctx, under):
    area, folder, slug = under.split("/")
    args = []
    if not ctx.layout or area != ctx.layout.area:
        args.append("--data " + shlex.quote(f"DATA_AREA={area}"))
    if not ctx.layout or slug != ctx.layout.slug:
        args.append("--data " + shlex.quote(f"DATA_SLUG={slug}"))
    return args, folder


def stale_folders(ctx, rows):
    """Warn for every folder of the root that holds current rows but differs from the answers."""
    groups = {}
    for r in rows:
        if r.state == "current" and (not ctx.layout or r.filed_under != ctx.layout.under(r.kind)):
            groups.setdefault((r.filed_under, r.kind), []).append(r)
    for (under, kind), rs in sorted(groups.items()):
        args, folder = restore_args(ctx, under)
        if not ctx.layout or folder != ctx.layout.kinds[kind]:
            args.append("--data " + shlex.quote(f"{KIND_KEYS[kind]}={folder}"))
        if ctx.store == "external" and ctx.layout:
            warn(f"{len(rs)} current row(s) are filed under '{under}', not this project's "
                 f"'{ctx.layout.under(kind)}': the files stay there, and verify and pull find them; "
                 f"to file there again, update every template with {' '.join(args)}")
        else:
            warn(f"{len(rs)} current row(s) are filed under '{under}' under the data root, and this "
                 "project does not file there now: to return, update every template with "
                 f"--data DATA_STORE=external {' '.join(args)}")


# ── Subcommands ─────────────────────────────────────────────────────────────────────────


def cmd_root(ctx, args):
    ctx.warn_all()
    held = [r for r in ctx.records if r.store]
    say("root: " + (ctx.root.path if ctx.root else ("invalid" if ctx.root_error else "none")))
    say("origin: " + (ctx.origin or "none"))
    say("marker: " + ctx.marker)
    if ctx.store:
        say("store: " + ctx.store + ("" if ctx.store in STORES else " (unknown)"))
    elif len(unique(r.store for r in held)) > 1:
        say("store: disagreement (" + listing(held, "DATA_STORE") + ")")
    else:
        say("store: not recorded")
    base = ctx.root.path if ctx.root else "<root>"
    if ctx.layout:
        say("area: " + ctx.layout.area)
        say("slug: " + ctx.layout.slug)
        for k in KINDS:
            say(f"kind: {k} = {os.path.join(base, *ctx.layout.under(k).split('/'))}{os.sep}")
    else:
        note = "not used under repo" if ctx.store == "repo" else "unknown"
        say("area: " + note)
        say("slug: " + note)
        for k in KINDS:
            say(f"kind: {k} = {note}")
    say("provider: " + (", ".join(ctx.providers) or "not recorded"))
    say()
    for line in provider_text(ctx.providers, ctx.store):
        say(line)
    if ctx.root and ctx.layout:
        layout_clashes(ctx)
    rows, refused = ctx.readable()
    stale_folders(ctx, rows)
    for reason in ctx.problems:
        warn("the data commands refuse until this is fixed: " + reason)
    for path, reason in refused:
        if not any(b.touches(path) for b in ctx.bad_maps):   # a map that cannot be read is warned of above
            warn(f"the commands that touch {path} refuse until this is fixed: {reason}")
    if ctx.root_error:
        return refuse(ctx.root_error)
    return 0


def provider_text(providers, store):
    lines = list(EVERY_PROVIDER)
    if store == "repo":
        lines.append(REPO_LINE)
    if not providers:
        lines.append("Provider: not recorded in any answers file.")
    for p in providers:
        lines.extend(CHECKLISTS[p] if p in CHECKLISTS else (UNKNOWN_PROVIDER.format(p),))
    return lines


def cmd_store(ctx, args):
    ctx.warn_all()
    if not ctx.records:
        return refuse("no .copier-answers.syntek-*.yml here records the project's answers")
    for r in ctx.records:
        say(f"{r.template}: {r.store or 'not yet asked'}")
    held = [r for r in ctx.records if r.store]
    if len(unique(r.store for r in held)) > 1:
        return refuse(f"the answers files disagree on DATA_STORE ({listing(held, 'DATA_STORE')}): "
                      "one project keeps one store, so answer the same in every template")
    return 0


def cmd_path(ctx, args):
    ctx.warn_all()
    rel = project_rel(ctx, args.rel)
    if rel is None:
        return refuse(f"{args.rel} lies outside this project")
    reasons = ctx.blocked([rel])
    if reasons:
        return refuse_all(reasons)
    # A folder whose manifest cannot be read refuses the path, as a bad map's folder does,
    # whether or not the work tree holds the file.
    folder = ctx.folder_for(rel)
    rows = []
    if folder and folder.takes_rows:
        try:
            rows = ctx.manifest(folder)[1]
        except Unreadable as err:
            return refuse(str(err))
    if ctx.store == "repo":
        if ctx.contained:
            # No root is used under repo, but a sync service corrupts Git, and a root inside the
            # repository mixes its files with the project's: refuse first, as under external.
            return refuse(ctx.root_error)
        say(os.path.join(str(ctx.project), *[p for p in rel.split("/") if p]))
        return 0
    if not ctx.root:
        return refuse(ctx.no_root())
    here = os.path.join(str(ctx.project), *[p for p in rel.split("/") if p])
    if rel and os.path.isfile(here):
        say(here)
        return 0
    if folder:
        for r in rows:
            if r.path == rel and r.state == "current":
                say(ctx.at(r))
                return 0
        if folder.kind and args.kind and args.kind != folder.kind:
            return refuse(f"{folder.path} fixes the kind {folder.kind} for every file in it (per folder, never per file)")
    kind = (folder.kind if folder else None) or args.kind or kind_of_name(rel)
    say(ctx.place(ctx.layout.under(kind), rel))
    return 0


def names_refusal(ctx, rel):
    for part in rel.split("/"):
        why = name_problem(part) or (onedrive_problem(part) if ctx.onedrive() else None)
        if why:
            return f"'{part}' {why}"
    return None


def long_path(ctx, full, label):
    if len(full) > MAX_PATH:
        warn(f"{label} is {len(full)} characters under this machine's root, over Windows' {MAX_PATH}: "
             "a shorter name or folder keeps it openable everywhere")
    if ctx.onedrive() and len(full) > ONEDRIVE_PATH:
        warn(f"{label} is over the {ONEDRIVE_PATH} characters OneDrive allows")


def cmd_add(ctx, args):
    ctx.warn_all()
    src = os.path.expanduser(args.file)
    if not os.path.isabs(src):
        src = os.path.join(str(ctx.project), src)
    rel = project_rel(ctx, args.as_ if args.as_ else args.file)
    reasons = ctx.blocked([rel] if rel else [])
    if reasons:
        return refuse_all(reasons)
    if args.role not in ctx.roles:
        return refuse(f"'{args.role}' is not a role here: use one of {', '.join(ctx.roles)}")
    if ctx.store == "repo":
        if ctx.contained:
            return refuse(ctx.root_error)   # before the roles that write nothing, as cmd_path
        if args.role == "generated":
            say("not filed: generated files stay git-ignored in the work tree (this project keeps its files in the repository)")
            return 0
        if args.role in ctx.skip_roles:
            say(f"not filed: the role '{args.role}' is never filed under repo (its map says \"repo\": \"skip\"), "
                "so the file stays where it is in the work tree (this project keeps its files in the repository)")
            return 0
        return refuse("this project keeps its files in the repository (DATA_STORE repo): commit the file instead")
    if not ctx.root:
        return refuse(ctx.no_root())
    if not os.path.isfile(src):
        return refuse(f"{args.file} is not a file")
    if within(os.path.realpath(src), os.path.realpath(ctx.root.path)):
        return refuse(f"{args.file} is already under the data root: add files a copy of a file outside it")
    if rel is None:
        what = f"--as {args.as_}" if args.as_ else f"{args.file}"
        return refuse(f"{what} lies outside this project: name where the file belongs with --as <project path>")
    if not rel or rel.split("/")[0] == ".git" or rel.endswith(("/" + MANIFEST, TMP_SUFFIX)):
        return refuse(f"'{rel or '.'}' cannot be filed")
    folder = ctx.folder_for(rel)
    if not folder:
        names = ", ".join(f.path for f in ctx.filing()) or "none present"
        return refuse(f"{rel} is in no filing folder (the maps name {names})")
    if not folder.takes_rows:
        return refuse(f"{rel} is in {folder.path}, which .claude/{folder.source}-dataroot.json marks as working "
                      "output (\"rows\": \"none\"): it never takes rows, so nothing is filed from it")
    if any(f.path == rel or f.path.startswith(rel + "/") for f in ctx.folders):
        return refuse(f"{rel} is a filing folder, not a file: name the file with --as {rel}/<name>")
    if os.path.isdir(os.path.join(str(ctx.project), *rel.split("/"))):
        return refuse(f"{rel} is a folder in the work tree, not a file: name a file inside it with --as {rel}/<name>")
    source = ""
    if args.source:
        source = project_rel(ctx, args.source)
        if not source:
            return refuse(f"--source {args.source} lies outside this project")
    label = args.label or ""
    if "://" in label:
        warn(f"the label '{label}' looks like a URL: a label says where else a copy is, never a link")
    former = ""
    original = os.path.basename(src)
    if args.as_ and original != rel.rsplit("/", 1)[-1] and (
            name_problem(original) or (ctx.onedrive() and onedrive_problem(original))):
        former = original
    return file_one(ctx, src, rel, folder, args.role, source, label, args.force, former)


def file_one(ctx, src, rel, folder, role, source, label, force, former):
    """File one copy (the add procedure); returns the exit code."""
    why = names_refusal(ctx, rel)
    if why:
        return refuse(f"{rel}: {why}; file it under a Windows-safe name with --as "
                      "(the original name is kept as former_name)")
    if ctx.onedrive() and ctx.layout.area.casefold() == "forms":
        return refuse("OneDrive refuses a folder named forms at the top of what it syncs: re-answer DATA_AREA")
    kind = folder.kind or kind_of_name(rel)
    under = ctx.layout.under(kind)
    dest = ctx.place(under, rel)
    long_path(ctx, dest, rel)
    try:
        text, rows = ctx.manifest(folder)
    except Unreadable as err:
        return refuse(str(err))
    mpath = ctx.manifest_path(folder)
    listed = f"{folder.path}/{MANIFEST}"
    current = [r for r in rows if r.path == rel and r.state == "current"]
    if current and not force:
        if any(ctx.protected(r) for r in current):
            return refuse(f"{rel} is already filed as evidence (a current '{current[0].role}' row in {listed}), "
                          "whose file and hash are never replaced: file a new version under its own name")
        return refuse(f"{rel} is already filed (a current row in {listed}): file a new version under its "
                      "own name, or add --force to supersede it (the listed copy is kept)")
    if len(current) > 1:
        return refuse(f"{listed} holds {len(current)} current rows for {rel}: settle them by hand first")
    if current and ctx.protected(current[0]):
        why = ("its row records evidence = true" if current[0].evidence is True else
               f"the role '{current[0].role}' is evidence" if current[0].role in ctx.roles else
               f"no map here defines the role '{current[0].role}', so it counts as evidence")
        return refuse(f"{rel} is filed as evidence ({why}): add --force never replaces an evidence row's file "
                      "or hash; file a new version under its own name")
    clash = case_clash(ctx.root.path, under.split("/") + rel.split("/"))
    if clash:
        here, part, found = clash
        return refuse(f"{here} holds '{found}', which differs only in case or Unicode form from '{part}': "
                      "add never creates the second spelling; rename the folder under the data root, "
                      "or re-answer to match it")
    stale_folders(ctx, rows)
    inside = [r.path for r in rows if r.path.startswith(rel + "/")]
    if inside:
        return refuse(f"{listed} lists files inside {rel} ({inside[0]}): {rel} is a folder there, not a file")
    if os.path.isdir(dest):
        return refuse(f"{dest} is a folder under the data root, not a file: name a file inside it with --as")
    up = os.path.dirname(dest)
    while up and not os.path.lexists(up) and os.path.dirname(up) != up:
        up = os.path.dirname(up)
    if up and not os.path.isdir(up):
        return refuse(f"{up} under the data root is a file where {rel} needs a folder: add never replaces it")
    old = current[0] if current else None
    old_loc = kept = kept_rel = None
    if old:
        old_loc = ctx.at(old)
        if not os.path.isfile(old_loc):
            return refuse(f"the listed copy of {rel} is missing at {old_loc}: restore it first (verify lists what is missing)")
        # The copy kept as superseded must be the one the row lists: a changed copy is a failure
        # for verify to report, never one for --force to keep and so hide.
        if file_online_only(old_loc):
            return refuse(f"the listed copy of {rel} at {old_loc} is online only: run verify --hydrate on it first, "
                          "so add --force can check it is unchanged before keeping it as superseded")
        if sha256_file(old_loc) != old.sha256:
            return refuse(f"the listed copy of {rel} at {old_loc} no longer hashes as its row says (verify lists it "
                          "as changed): add --force never keeps a changed copy as the superseded one; restore it "
                          "from a backup first, or file the new copy under its own name", code=1)
        where, name = os.path.split(old_loc)
        kept_name = superseded_name(name, today().strftime("%d-%m-%Y"),
                                    lambda n: os.path.lexists(os.path.join(where, n)))
        kept = os.path.join(where, kept_name)
        kept_rel = "/".join(old.path.split("/")[:-1] + [kept_name])
    if os.path.lexists(dest) and not (old and os.path.normpath(dest) == os.path.normpath(old_loc)):
        return refuse(f"{dest} already exists under the data root and no current row lists it there: "
                      "compare it first (status lists it); add never overwrites")
    plan = {"path": rel, "kind": kind, "filed_under": under, "role": role, "evidence": ctx.evidence(role),
            "sha256": "0" * 64, "bytes": 0, "filed": today().strftime("%d/%m/%Y"), "state": "current",
            "source": source, "replaces": kept_rel or "", "label": label, "former_name": former, "notes": ""}
    why = row_problem(plan, folder)
    if why:
        return refuse(f"the row add would write{why}, which {listed} may not hold: nothing was filed")
    # The new copy is written and checked first, while the listed copy is still where its row
    # says; a superseding copy is staged beside it. Only then are the two swapped and the row
    # written, and anything that stops that (an interrupt included) is undone.
    staged = (dest + TMP_SUFFIX) if old else None
    placed = renamed = False
    if staged and os.path.lexists(staged):
        if os.path.islink(staged) or not os.path.isfile(staged):
            return refuse(f"could not copy {src} to {dest}: {staged} is in the way")
        with contextlib.suppress(OSError):
            os.unlink(staged)   # this tool's own temporary name, left by a run that stopped
    try:
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        sha, size = copy_verified(src, staged or dest)
        placed = not old
    except CopyMismatch as err:
        return refuse(str(err), code=1)
    except OSError as err:
        return refuse(f"could not copy {src} to {dest}: {err}")
    except BaseException:
        with contextlib.suppress(OSError):
            if os.path.lexists(staged or dest):   # an interrupt after the copy was put in place
                os.unlink(staged or dest)
        raise
    row = dict(plan, sha256=sha, bytes=size)

    def ours():
        if placed:
            return True
        with contextlib.suppress(OSError):
            return bool(staged) and os.path.lexists(dest) and os.path.samefile(dest, staged)
        return False

    try:
        if old:
            os.rename(old_loc, kept)
            renamed = True
            put_in_place(staged, dest)   # a link: never over a file, and dest is free now
            placed = True
            fsync_dir(os.path.dirname(dest))
        write_manifest(mpath, text, rows, row, old.index if old else None)
    except BaseException as err:
        if ours():
            with contextlib.suppress(OSError):
                os.unlink(dest)
        if staged:
            with contextlib.suppress(OSError):
                os.unlink(staged)
        if renamed:
            with contextlib.suppress(OSError):
                os.rename(kept, old_loc)
        if isinstance(err, (OSError, Unwritable)):
            return refuse(f"could not write {listed}: {err}; nothing was filed")
        raise
    ctx.cache.pop(folder.path, None)
    say(f"filed: {rel} -> {dest} ({role}, {size} bytes, sha256 {sha[:12]})")
    if old:
        say(f"superseded: {old.path} -> {kept_rel} (kept under the data root; its row's state is now "
            "superseded, and the new row's replaces names the kept copy)")
    return 0


def data_ready(ctx, verb):
    """The refusal code for verify, pull and plan, or None when they can act."""
    if ctx.problems:
        return refuse_all(ctx.problems)
    if ctx.store != "external":
        return refuse(f"this project keeps its files in the repository (DATA_STORE repo): there is nothing to {verb} under the data root")
    if not ctx.root:
        return refuse(ctx.no_root())
    return None


def readable_for(ctx, verb, glob=None):
    """The rows a whole-project command reads, after one refusal line for each folder it must
    leave alone (only those a GLOB may touch); returns (rows, refused paths)."""
    rows, refused = ctx.readable()
    left = []
    for path, reason in refused:
        if glob_meets(glob, path):
            refuse(f"{verb} leaves {path} alone: {reason}")
            left.append(path)
    return rows, [p for p, _ in refused], left


def same(a, b):
    return type(a) is type(b) and a == b


def committed_changes(ctx, want, refused):
    """A line for each row committed at HEAD that the work tree removed or changed: rows are
    appended only, and the one change allowed is a state from current to superseded or withdrawn."""
    import tomllib
    if git_ok(ctx, "rev-parse", "--verify", "-q", "HEAD") is None:
        return []
    lines, gone = [], object()
    for f in ctx.folders:
        if not f.takes_rows or f.path in refused or ctx.folder_refusals(f):
            continue
        rel = f"{f.path}/{MANIFEST}"
        blob = git_ok(ctx, "cat-file", "blob", f"HEAD:{rel}")
        if blob is None:
            continue
        try:
            head = tomllib.loads(blob.decode("utf-8")).get("file", [])
            now = [r.raw for r in ctx.manifest(f)[1]]
        except (UnicodeDecodeError, tomllib.TOMLDecodeError, Unreadable) as err:
            warn(f"the rows of {rel} were not compared with HEAD: {err}")
            continue
        for i, entry in enumerate(head if isinstance(head, list) else []):
            h = entry if isinstance(entry, dict) else {}
            path = str(h.get("path", ""))
            if not want(path):
                continue
            if i >= len(now):
                lines.append(f"committed: {rel} row {i + 1} ({path}) is committed at HEAD but gone from the work "
                             "tree: rows are never deleted")
                continue
            w = now[i]
            diff = [k for k in unique([*h, *w]) if k != "state" and not same(h.get(k, gone), w.get(k, gone))]
            was, now_state = h.get("state"), w.get("state")
            if not same(was, now_state) and not (was == "current" and now_state in (SUPERSEDED, WITHDRAWN)):
                diff.append("state")
            if diff:
                lines.append(f"committed: {rel} row {i + 1} ({path}) differs from HEAD in {', '.join(diff)}: a "
                             "row is never edited; only its state changes, from current to superseded or withdrawn")
    return lines


def orphaned(ctx, want):
    """A line for each tracked manifest no present map's folder names (its rows are never read)."""
    tracked = git_files(ctx, [":(glob)**/" + MANIFEST])
    named = {f"{f.path}/{MANIFEST}": f for f in ctx.folders}
    claimed = {f"{c}/{MANIFEST}" for b in ctx.bad_maps for c in (b.claims or [])}
    lines, unjudged = [], []
    for m in sorted(tracked or []):
        f = named.get(m)
        if not want(m) or (f and f.takes_rows) or m in claimed:
            continue
        if f:
            lines.append(f"orphaned: {m} is tracked in {f.path}, which .claude/{f.source}-dataroot.json marks as "
                         "working output (\"rows\": \"none\"), so its rows are never read")
        elif ctx.unknown_maps():
            unjudged.append(m)
        else:
            lines.append(f"orphaned: {m} is tracked, but no map here names its folder, so its rows are never read: "
                         "restore the map that names it, or settle its rows by hand")
    if unjudged:
        warn(f"{', '.join(unjudged)}: no readable map names its folder, and a map here cannot be read, so it is not "
             "judged as orphaned")
    return lines


def cmd_verify(ctx, args):
    ctx.warn_all()
    code = data_ready(ctx, "verify")
    if code is not None:
        return code
    rows, refused, left = readable_for(ctx, "verify", args.glob)
    layout_clashes(ctx)
    stale_folders(ctx, rows)

    def want(rel):
        return not args.glob or fnmatch.fnmatchcase(rel, args.glob)

    verified = online = missing = changed = 0
    for r in rows:
        if r.state != "current" or not want(r.path):
            continue
        loc = ctx.at(r)
        if not os.path.isfile(loc):
            say(f"missing: {r.path} (expected at {loc})")
            missing += 1
        elif not args.hydrate and file_online_only(loc):
            say(f"online only: {r.path} (not read)")
            online += 1
        elif sha256_file(loc) != r.sha256:
            note = ": an evidence row, so a failure, never an update" if ctx.protected(r) else ""
            say(f"changed: {r.path} at {loc}{note}")
            changed += 1
        else:
            verified += 1
    extra, unjudged = unlisted(ctx, rows, mirror_files(ctx, rows), want, refused)
    say_unlisted(extra, unjudged)
    committed = committed_changes(ctx, want, refused)
    orphans = orphaned(ctx, want)
    for line in committed + orphans:
        say(line)
    say(f"verified {verified}, online only {online} (not read: verify --hydrate reads them, which "
        f"downloads them); missing {missing}, changed {changed}, unlisted {len(extra)}; committed rows "
        f"removed or changed {len(committed)}, orphaned manifests {len(orphans)}"
        + (f"; folders left alone {len(left)}" if left else ""))
    if missing or changed or extra or committed or orphans:
        return 1
    return 2 if left else 0


def cmd_status(ctx, args):
    ctx.warn_all()
    if ctx.problems:
        return refuse_all(ctx.problems)
    rows, refused, left = readable_for(ctx, "status")
    folders = [f for f in ctx.filing() if f.path not in refused]

    def judged(rel):
        return ctx.judged(rel, refused)

    current = {r.path for r in rows if r.state == "current"}
    paths = [f.path for f in folders]
    at_risk = not_filed = 0
    if paths:
        ignored = git_files(ctx, paths, "--others", "--ignored", "--exclude-standard")
        tracked = git_files(ctx, paths)
        if ignored is None or tracked is None:
            warn("this project is not a Git work tree: every binary in the filing folders counts as kept outside Git")
            ignored = [p for f in folders for p in walk_files(ctx, f)]
            tracked = []
        for rel in sorted(p for p in ignored if is_binary(p) and judged(p) and p not in current):
            size = human(os.path.getsize(ctx.project / rel)) if (ctx.project / rel).is_file() else "gone"
            if ctx.store == "external":
                say(f"not filed: {rel} ({size}): Git ignores it and no row lists it, so it is on this "
                    "machine only; file it with add")
                not_filed += 1
            else:
                say(f"local only: {rel} ({size}): Git ignores it, and this project keeps its files in the repository")
        if ctx.store == "external":
            still = [p for p in tracked if is_binary(p) and judged(p)]
            if still:
                say(f"tracked: {len(still)} binaries in the filing folders are still in Git: plan lists them and where each would go")
        for f in folders:
            if not f.warn_over:
                continue
            for rel in walk_files(ctx, f):
                if not judged(rel):
                    continue
                try:
                    st = os.lstat(ctx.project / rel)
                except OSError as err:
                    warn(f"{rel} could not be read ({err.strerror or err}), so its size was not checked")
                    continue
                if not stat_mod.S_ISREG(st.st_mode):
                    continue   # a link (a dangling one included) is judged by what it is, never followed
                size = st.st_size
                if size > f.warn_over:
                    warn(f"{rel} is {human(size)}, over the {human(f.warn_over)} the map sets for {f.path}: "
                         "keep a large file under the data root")
    stale_folders(ctx, rows)
    online = 0
    extra = []
    if ctx.store == "external":
        if ctx.root:
            layout_clashes(ctx)
            files = mirror_files(ctx, rows)
            online = sum(1 for _, _, full in files if file_online_only(full))
            extra, unjudged = unlisted(ctx, rows, files, lambda rel: True, refused)
            say_unlisted(extra, unjudged)
        else:
            warn(ctx.no_root() + "; the copies under the data root were not checked")
    elif ctx.contained:
        # Under repo too: whatever the store, a sync service corrupts Git, and a root inside the
        # repository mixes its files with the project's.
        warn(ctx.root_error + "; the copies under the data root were not checked")
    at_risk = not_filed + len(extra)
    say(f"status: {not_filed} not filed, {len(extra)} unlisted under the data root, {online} online only"
        + (f"; folders left alone {len(left)}" if left else ""))
    if at_risk:
        return 1
    return 2 if left else 0


def cmd_pull(ctx, args):
    ctx.warn_all()
    code = data_ready(ctx, "pull")
    if code is not None:
        return code
    rows, _, left = readable_for(ctx, "pull", args.glob)
    told = False
    failed = in_place = 0
    pulled = []
    for r in rows:
        if r.state != "current" or (args.glob and not fnmatch.fnmatchcase(r.path, args.glob)):
            continue
        loc = ctx.at(r)
        dest = os.path.join(str(ctx.project), *r.path.split("/"))
        if not os.path.isfile(loc):
            say(f"missing: {r.path} (expected at {loc})")
            failed += 1
            continue
        if not told and file_online_only(loc):
            warn("some files are online only: reading one downloads it, which pull does because you asked")
            told = True
        if os.path.lexists(dest):
            if os.path.isfile(dest) and sha256_file(dest) == r.sha256:
                in_place += 1
            else:
                say(f"differs: {r.path}: the work-tree file differs from the filed copy, and pull never replaces it")
                failed += 1
            continue
        try:
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            copy_verified(loc, dest, expect=r.sha256)
        except CopyMismatch:
            note = ", an evidence row" if ctx.protected(r) else ""
            say(f"changed: {r.path} at {loc} no longer hashes as filed{note}, so it was not copied")
            failed += 1
            continue
        except OSError as err:
            say(f"failed: {r.path}: {err}")
            failed += 1
            continue
        pulled.append(r.path)
        say(f"pulled: {r.path}")
    ignored = git_ignored(ctx, pulled)
    for rel in pulled:
        if ignored is not None and rel not in ignored:
            warn(f"{rel} is not ignored by Git here: never commit it, or it is tracked twice")
    say(f"pull: {len(pulled)} copied, {in_place} already in place, {failed} not copied"
        + (f"; folders left alone {len(left)}" if left else ""))
    if failed:
        return 1
    return 2 if left else 0


# Whole words of a file's name that propose a role: the name split on '-', '_', '.' and spaces,
# any case, so 'designer-brief' matches nothing. 'statement' before 'of work' is the house's
# statement of work, never a received statement.
SIGNED_WORDS = ("signed", "countersigned", "executed")
RECEIVED_WORDS = ("receipt", "remittance", "statement", "received")
ISSUE_STATUSES = ("final",)
# What the house build writes as a PDF's producer: XeLaTeX hands its output to xdvipdfmx, on
# both routes (a .tex through xelatex, a .md through Pandoc with pdf-engine xelatex).
PDF_STRING_MAX = 4096  # a PDF string longer than this is not a producer name
HOUSE_PRODUCERS = ("xdvipdfmx", "xetex")
PDF_WINDOW = 256 * 1024
NOT_SHOWN = "a Word copy beside its source cannot be shown to be the issued one"


def name_role(base):
    """signed or received from whole words of a file's name, else None."""
    words = [w for w in re.split(r"[-_.\s]+", base.casefold()) if w]
    if any(w in SIGNED_WORDS for w in words):
        return "signed"
    for i, w in enumerate(words):
        if w in RECEIVED_WORDS and not (w == "statement" and words[i + 1:i + 3] == ["of", "work"]):
            return "received"
    return None


def source_status(path):
    """A source's status as make reads it: a .tex's '% status:' line in its leading block of %
    lines; a .md's top-level status key in its frontmatter (quotes and a trailing comment dropped)."""
    try:
        with open(path, encoding="utf-8", errors="replace") as f:
            lines = [line.rstrip("\n").removesuffix("\r") for line in f]
    except OSError:
        return ""
    if path.endswith(".tex"):
        for line in lines:
            if not line.startswith("%"):
                return ""
            m = re.match(r"%[ \t]*status:[ \t]*(.*)$", line)
            if m:
                return m.group(1).rstrip()
        return ""
    if not lines or not re.fullmatch(r"---[ \t]*", lines[0]):
        return ""
    for line in lines[1:]:
        if re.fullmatch(r"(---|\.\.\.)[ \t]*", line):
            return ""
        if line.startswith("status:"):
            v = re.sub(r"[ \t]+#.*$", "", line[len("status:"):].lstrip(" \t"))
            return v.replace('"', "").replace("'", "").rstrip()
    return ""


def pdf_text(raw):
    """A PDF text string's bytes as text: UTF-16 after its byte-order mark, else PDFDocEncoding
    (read as Latin-1, which agrees for every name a producer uses)."""
    if raw.startswith(b"\xfe\xff"):
        return raw[2:].decode("utf-16-be", "replace")
    if raw.startswith(b"\xef\xbb\xbf"):
        return raw[3:].decode("utf-8", "replace")
    return raw.decode("latin-1")


def pdf_string(data, i):
    """The literal (...) or hex <...> string starting at data[i], as text, or None."""
    limit = min(len(data), i + PDF_STRING_MAX)
    if data[i:i + 1] == b"<":
        end = data.find(b">", i, limit)
        hexed = re.sub(rb"\s", b"", data[i + 1:end]) if end > 0 else b"!"
        if not re.fullmatch(rb"[0-9A-Fa-f]*", hexed):
            return None
        return pdf_text(bytes.fromhex((hexed + b"0" * (len(hexed) % 2)).decode("ascii")))
    if data[i:i + 1] != b"(":
        return None
    out, depth, j = bytearray(), 1, i + 1
    escapes = {ord("n"): b"\n", ord("r"): b"\r", ord("t"): b"\t", ord("b"): b"\b", ord("f"): b"\f"}
    while j < limit:
        c = data[j]
        if c == 0x5C:  # a backslash
            j += 1
            if j >= limit:
                break
            e = data[j]
            if e in escapes:
                out += escapes[e]
            elif 0x30 <= e <= 0x37:
                k = j
                while k < limit and k < j + 3 and 0x30 <= data[k] <= 0x37:
                    k += 1
                out.append(int(data[j:k], 8) & 0xFF)
                j = k
                continue
            elif e in (0x0A, 0x0D):
                if e == 0x0D and data[j + 1:j + 2] == b"\n":
                    j += 1
            else:
                out.append(e)
        elif c == 0x28:
            depth += 1
            out.append(c)
        elif c == 0x29:
            depth -= 1
            if not depth:
                return pdf_text(bytes(out))
            out.append(c)
        else:
            out.append(c)
        j += 1
    return None


def producers_in(data):
    found = []
    for m in re.finditer(rb"/Producer\s*", data):
        value = pdf_string(data, m.end())
        if value is not None:
            found.append(value)
    for m in re.finditer(rb"<pdf:Producer>([^<]*)</pdf:Producer>|pdf:Producer\s*=\s*\"([^\"]*)\"", data):
        found.append((m.group(1) or m.group(2) or b"").decode("utf-8", "replace"))
    return found


def object_streams(data):
    """The decompressed bytes of each Flate object stream that starts and ends inside data."""
    try:
        import zlib
    except ImportError:  # a Python built without zlib reads only uncompressed objects
        return
    for m in re.finditer(rb"/Type\s*/ObjStm(?![A-Za-z0-9])", data):
        head = data.rfind(b"obj", 0, m.start())
        s = data.find(b"stream", m.end())
        if head < 0 or s < 0:
            continue
        dictionary = data[head:s]
        if b"/FlateDecode" not in dictionary or b"/DecodeParms" in dictionary:
            continue
        start = s + 6
        start += 2 if data[start:start + 2] == b"\r\n" else 1 if data[start:start + 1] in (b"\n", b"\r") else 0
        end = data.find(b"endstream", start)
        if end < 0:
            continue
        try:
            yield zlib.decompressobj().decompress(data[start:end], 4 * 1024 * 1024)
        except zlib.error:
            continue


def pdf_evidence(path):
    """(producers, signed): the producers a PDF names in its first and last PDF_WINDOW bytes
    (Info dictionary, compressed object streams and XMP), and whether it carries a digital
    signature (a /ByteRange array or a /FT /Sig field; /Type is optional there)."""
    try:
        size = os.path.getsize(path)
        with open(path, "rb") as f:
            if size <= 2 * PDF_WINDOW:
                blobs = [f.read()]
            else:
                head = f.read(PDF_WINDOW)
                f.seek(size - PDF_WINDOW)
                blobs = [head, f.read()]
    except OSError:
        return [], False
    producers, signed = [], False
    for blob in blobs:
        producers += producers_in(blob)
        for inner in object_streams(blob):
            producers += producers_in(inner)
        # /Type is optional in a signature dictionary; its /ByteRange array, or a /FT /Sig field, is not.
        if re.search(rb"/ByteRange\s*\[", blob) or re.search(rb"/FT\s*/Sig(?![A-Za-z0-9])", blob):
            signed = True
    return producers, signed


def first_added(ctx, rel):
    """When Git first holds rel (the committer time of its earliest adding commit), or None."""
    out = git_ok(ctx, "log", "--diff-filter=A", "--format=%ct", "--", ":(literal)" + rel)
    times = [int(t) for t in (out or b"").split() if t.isdigit()]
    return min(times) if times else None


def issued_proof(ctx, rel, source, statuses):
    """(role, reason, house): house says the producer is the house build. issued only on evidence: a .pdf whose producer is the house build, with no
    digital signature, beside a same-stem source at an issuing status, and (where Git holds both)
    first committed no earlier than that source. A signature makes it signed."""
    if not rel.lower().endswith(".pdf"):
        return None, NOT_SHOWN, False
    producers, signed = pdf_evidence(str(ctx.project / rel))
    if signed:
        return "signed", "", False
    house = any(h in p.casefold() for p in producers for h in HOUSE_PRODUCERS)
    status = source_status(str(ctx.project / source))
    if status not in statuses:
        return None, (f"its source is at status '{status or 'none'}', and only {' '.join(statuses)} issues"), house
    if not house:
        named = next((p.strip() for p in producers if p.strip()), "")
        return None, (f"its producer is '{named}', not the house build (XeLaTeX through xdvipdfmx)" if named
                      else "it names no producer, so the house build cannot be shown"), house
    made, wrote = first_added(ctx, rel), first_added(ctx, source)
    if made is not None and wrote is not None and made < wrote:
        return None, "Git held it before its source, so it was not built from it", house
    return "issued", "", house


def guess_role(ctx, rel, kind, statuses=ISSUE_STATUSES):
    """(role, source, reason): the role plan proposes, from the file's own name, its neighbours and
    its own bytes, never its folder. Beside a same-stem source a role is proposed only on evidence:
    None, with the reason, where it cannot be shown."""
    stem, ext = os.path.splitext(rel)
    base = os.path.basename(stem)
    near = (ctx.project / rel).parent
    by_name = name_role(base)
    if by_name == "signed":
        return "signed", "", ""
    if (near / (os.path.basename(rel) + ".reading.md")).is_file() or (near / (base + ".reading.md")).is_file():
        return "ingested", "", ""
    if ext.lower() in (".pdf", ".docx"):
        for origin in (".tex", ".md"):
            if (near / (base + origin)).is_file():
                role, reason, house = issued_proof(ctx, rel, stem + origin, statuses)
                if role == "issued":
                    return role, stem + origin, ""
                if role:
                    return role, "", ""
                # A word of the name never outweighs the house build: a house copy that fails the
                # proof (a receipt at draft) is the author's to name, never received.
                if by_name and not house:
                    return by_name, "", ""
                return None, stem + origin, reason
    if by_name:
        return by_name, "", ""
    return ("asset" if kind == "photos" else "archive"), "", ""


def cmd_plan(ctx, args):
    ctx.warn_all()
    code = data_ready(ctx, "plan")
    if code is not None:
        return code
    rows, refused, left = readable_for(ctx, "plan")
    folders = [f for f in ctx.filing() if f.path not in refused]
    paths = [f.path for f in folders]
    tracked = git_files(ctx, paths) if paths else []
    if tracked is None:
        warn("this project is not a Git work tree: every binary in the filing folders is listed")
        tracked = [p for f in folders for p in walk_files(ctx, f)]
    modified = set(git_files(ctx, paths, "--modified") or []) if paths else set()
    current = {r.path: r for r in rows if r.state == "current"}
    planned = []
    conflicts = done = unknown = 0
    statuses = tuple((args.issue_statuses or "").split()) or ISSUE_STATUSES
    for rel in sorted(p for p in tracked if is_binary(p) and ctx.judged(p, refused)):
        src = os.path.join(str(ctx.project), *rel.split("/"))
        if not os.path.isfile(src):
            continue
        folder = ctx.folder_for(rel)
        kind = folder.kind or kind_of_name(rel)
        under = ctx.layout.under(kind)
        dest = ctx.place(under, rel)
        if rel in current:
            if current[rel].sha256 == sha256_file(src):
                done += 1
                continue
            say(f"conflict: {rel}: a current row lists other bytes; file this version under its own name "
                "with add" + ("" if ctx.protected(current[rel]) else ", or supersede the listed one with add --force"))
            conflicts += 1
            continue
        why = names_refusal(ctx, rel)
        clash = case_clash(ctx.root.path, under.split("/") + rel.split("/"))
        if why:
            say(f"conflict: {rel}: {why}; file it under a Windows-safe name with add --as")
        elif clash:
            say(f"conflict: {rel}: {clash[0]} holds '{clash[2]}', which differs only in case from '{clash[1]}'")
        elif os.path.lexists(dest):
            same = os.path.isfile(dest) and sha256_file(dest) == sha256_file(src)
            say(f"conflict: {rel}: {dest} already exists " + ("with the same bytes but no row: compare, then file it by hand"
                                                              if same else "with other bytes"))
        else:
            role, source, reason = guess_role(ctx, rel, kind, statuses)
            note = " (it has uncommitted changes: the copy is of the work-tree file)" if rel in modified else ""
            if role is None:
                say(f"plan: {rel} -> {dest} (role ?, beside {source}: {reason}, {human(os.path.getsize(src))}){note}; "
                    "choose its role and file it with add --role: plan never files a row without one")
                unknown += 1
                continue
            extra = f", source {source}" if source else ""
            say(f"plan: {rel} -> {dest} (role {role}{extra}, {human(os.path.getsize(src))}){note}")
            planned.append((src, rel, folder, role, source))
            continue
        conflicts += 1
    copied = failed = 0
    if args.copy:
        for src, rel, folder, role, source in planned:
            if file_one(ctx, src, rel, folder, role, source, "", False, ""):
                failed += 1
            else:
                copied += 1
    say(f"plan: {len(planned)} to file, {unknown} need a role, {done} filed already, {conflicts} conflicts"
        + (f"; copied {copied}, {failed} failed" if args.copy else "; run plan --copy to file them")
        + ". Nothing is moved or untracked: verify the data root on every machine before you untrack anything"
        + (f" (folders left alone {len(left)})" if left else ""))
    if conflicts or failed or unknown:
        return 1
    return 2 if left else 0


def cmd_check_names(ctx, args):
    ctx.warn_all()
    items = []
    bad = 0
    if args.paths:
        for value in args.paths:
            rel = project_rel(ctx, value)
            if rel is None:
                say(f"unsafe: {value}: it lies outside this project")
                bad += 1
                continue
            items.append(rel)
            full = ctx.project / rel
            if rel and full.is_dir():
                for here, dirs, files in os.walk(full):
                    dirs[:] = sorted(d for d in dirs if d != ".git")
                    for n in sorted(dirs + files):
                        items.append(os.path.relpath(os.path.join(here, n), ctx.project).replace(os.sep, "/"))
    else:
        if ctx.layout:
            if ctx.onedrive() and ctx.layout.area.casefold() == "forms":
                say(f"unsafe: DATA_AREA '{ctx.layout.area}': OneDrive refuses a folder named forms at the top of what it syncs")
                bad += 1
            for v in (ctx.layout.area, *ctx.layout.kinds.values()):
                why = onedrive_problem(v) if ctx.onedrive() else None
                if why:
                    say(f"unsafe: '{v}' {why}")
                    bad += 1
        for f in ctx.present():
            items.append(f.path)
            for here, dirs, files in os.walk(ctx.project / f.path):
                dirs[:] = sorted(d for d in dirs if d != ".git")
                for n in sorted(dirs + files):
                    items.append(os.path.relpath(os.path.join(here, n), ctx.project).replace(os.sep, "/"))
    pairs = set()
    listings = {}
    for rel in items:
        if not rel:
            continue
        why = names_refusal(ctx, rel)
        if why:
            say(f"unsafe: {rel}: {why}")
            bad += 1
        parent, _, name = rel.rpartition("/")
        if parent not in listings:
            groups = {}
            for other in listdir(ctx.project / parent if parent else ctx.project):
                groups.setdefault(norm(other), []).append(other)
            listings[parent] = groups
        for other in listings[parent].get(norm(name), []):
            pair = tuple(sorted((other, name)))
            if other != name and (parent, pair) not in pairs:
                pairs.add((parent, pair))
                say(f"unsafe: {parent + '/' if parent else ''}{pair[0]} and {pair[1]} differ only in case or "
                    "Unicode form, and Windows and macOS cannot hold both")
                bad += 1
        if ctx.layout:
            folder = ctx.folder_for(rel)
            kind = (folder.kind if folder else None) or kind_of_name(rel)
            parts = [ctx.layout.area, ctx.layout.kinds[kind], ctx.layout.slug, *rel.split("/")]
            full = os.path.join(ctx.root.path, *parts) if ctx.root else "/".join(parts)
            long_path(ctx, full, rel)
    say(f"check-names: {len(items)} checked, {bad} unsafe")
    return 1 if bad else 0


COMMANDS = {"root": cmd_root, "store": cmd_store, "path": cmd_path, "add": cmd_add,
            "verify": cmd_verify, "status": cmd_status, "pull": cmd_pull, "plan": cmd_plan,
            "check-names": cmd_check_names}


class Parser(argparse.ArgumentParser):
    def error(self, message):
        refuse(f"{message} (see --help)")
        raise SystemExit(2)


def build_parser():
    p = Parser(prog="dataroot", add_help=False)
    sub = p.add_subparsers(dest="command", required=True, parser_class=Parser)
    sub.add_parser("root")
    sub.add_parser("store")
    q = sub.add_parser("path")
    q.add_argument("rel")
    q.add_argument("--kind", choices=KINDS)
    q = sub.add_parser("add")
    q.add_argument("file")
    q.add_argument("--role", required=True)
    q.add_argument("--as", dest="as_")
    q.add_argument("--source")
    q.add_argument("--label")
    q.add_argument("--force", action="store_true")
    q = sub.add_parser("verify")
    q.add_argument("glob", nargs="?")
    q.add_argument("--hydrate", action="store_true")
    sub.add_parser("status")
    q = sub.add_parser("pull")
    q.add_argument("glob", nargs="?")
    q = sub.add_parser("plan")
    q.add_argument("--copy", action="store_true")
    q.add_argument("--issue-statuses", default=None)
    q = sub.add_parser("check-names")
    q.add_argument("paths", nargs="*")
    return p


def main(argv=None, cwd=None, environ=None, version=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    if argv[:1] in (["-h"], ["--help"]):
        print(__doc__)
        return 0
    if argv[:1] == ["guard"]:
        return guard_main(version)
    if (version or sys.version_info) < PYTHON_MIN:
        sys.stderr.write(too_old_text(argv[0] if argv else "", version or sys.version_info))
        return 2
    try:
        import tomllib  # noqa: F401  (every subcommand but guard needs it)
    except ImportError:
        print(NEED_PYTHON, file=sys.stderr)
        return 2
    if argv == ["--self-test"]:
        return self_test()
    try:
        args = build_parser().parse_args(argv)
    except SystemExit as stop:
        return stop.code if isinstance(stop.code, int) else 2
    environ = os.environ if environ is None else environ
    project = find_project(cwd or os.getcwd())
    if project is None:
        return refuse("no project here: run this from inside a project that holds a .copier-answers.syntek-*.yml")
    try:
        ctx = Context(project, environ)
        return COMMANDS[args.command](ctx, args)
    except Unreadable as err:
        return refuse(str(err))
    except OSError as err:
        return refuse(f"{err}")
    except UnicodeError as err:
        return refuse(f"a name or a file here is not valid UTF-8 ({err}): rename it")


# ── Self-test (temporary folders only; the inherited root is never read) ──────────────────

FAMILY = "syntek-"              # every fixture template is named from the family prefix
ONE, TWO = FAMILY + "one", FAMILY + "two"
MAP_ONE = {"format": 1, "folders": [{"path": "papers/src", "kind": "docs"}, {"path": "notes/src"},
                                    {"path": "pictures", "warn_over_kib": 1},
                                    {"path": "sounds/src"}, {"path": "absent/src"}]}
MAP_TWO = {"format": 1, "folders": [{"path": "footage/src", "kind": "videos"}],
           "roles": [{"name": "take", "evidence": True, "repo": "skip"},
                     {"name": "brand-export", "evidence": False}]}
EXTERNAL = {"DATA_STORE": "external", "DATA_AREA": "business", "DATA_SLUG": "demo-project",
            "DATA_KIND_DOCS": "docs", "DATA_KIND_PHOTOS": "photos", "DATA_KIND_AUDIO": "audio",
            "DATA_KIND_VIDEOS": "videos", "DATA_PROVIDER": "none"}
SEED_GUARD = ("ROOT=$(git rev-parse --show-toplevel 2>/dev/null) || exit 0; for f in "
              '"$ROOT"/.claude/syntek-*-dataroot.py; do [ -f "$f" ] && exec python3 "$f" guard; done; exit 0')


def self_test():
    import json
    import tomllib
    global TODAY, MACHINE, STAT
    fails = probes = 0

    def check(label, ok):
        nonlocal fails, probes
        probes += 1
        print(f"  {'✓' if ok else '✗'} {label}")
        fails += 0 if ok else 1

    saved = {k: os.environ.pop(k) for k in list(os.environ)
             if k == ROOT_ENV or k.startswith("GIT_")}
    keep = (TODAY, MACHINE, STAT)
    TODAY, MACHINE = datetime.date(2026, 10, 16), "LAPTOP1"
    print("▸ dataroot --self-test\n")
    try:
        with tempfile.TemporaryDirectory(prefix="dataroot-selftest-") as tmp:
            base = Path(os.path.realpath(tmp))
            os.environ.update({"GIT_CONFIG_GLOBAL": os.devnull, "GIT_CONFIG_NOSYSTEM": "1",
                               "GIT_CEILING_DIRECTORIES": str(base)})
            for part in (lambda: self_test_units(check),
                         lambda: self_test_projects(check, base, json, tomllib)):
                try:
                    part()
                except Exception as err:  # a crash is a failed probe, named, never a traceback
                    check(f"the cases ran to the end ({type(err).__name__}: {err})", False)
    finally:
        TODAY, MACHINE, STAT = keep
        for k in [k for k in os.environ if k.startswith("GIT_")]:
            del os.environ[k]
        os.environ.update(saved)
    print()
    if fails:
        print(f"✗ Self-test failed: {fails} of {probes} probes.")
        return 1
    print(f"✓ Self-test passed — {probes} probes.")
    return 0


def self_test_units(check):
    import ast
    import tomllib
    source = Path(__file__).read_text(encoding="utf-8")
    try:
        ast.parse(source, feature_version=(3, 8))
        parses = True
    except SyntaxError:
        parses = False
    check("the file parses as Python 3.8, so an old python3 reaches the guard and the version check", parses)
    first = ast.parse(source).body[1]
    check("it opens with 'from __future__ import annotations' after its docstring",
          isinstance(first, ast.ImportFrom) and first.module == "__future__"
          and [a.name for a in first.names] == ["annotations"])
    opens = ("<" + "%", "<" + ":", "<" + "~")
    check("it holds no template delimiter", not any(d in source for d in opens))
    names = set(re.findall(r"syntek[-_]?[a-z][a-z0-9]*(?:-[a-z0-9]+)*", source, re.IGNORECASE))
    check("it names no template (only the marker, the variable and the temporary suffix)",
          names <= {"syntek-data-root", "SYNTEK_DATA", "syntek-tmp"})
    check("it cites no decision number", not re.search(r"\bD\d+\b", source))
    check("it holds no run of seven digits (the shape of an account number)",
          not re.search(r"(^|[^0-9A-Za-z_.:-])[0-9]{7,}([^0-9A-Za-z_]|$)", source, re.MULTILINE))
    check("the guard runs before any other import",
          source.index("sys.exit(guard_main())") < source.index("import argparse"))
    check("the version check runs before any other import",
          source.index("sys.version_info < PYTHON_MIN and sys.argv[1:2]") < source.index("import argparse"))
    need = "%d.%d" % PYTHON_MIN
    check("the docstring states the minimum PYTHON_MIN sets",
          f"Python {need} or later (PYTHON_MIN, below)" in " ".join(__doc__.split()))

    # The answers reader, on the corpus a rendered answers file was probed to write.
    for raw, want in (("Client Work", "Client Work"), ("Geschäft", "Geschäft"), (".hidden", ".hidden"),
                      ("COM0", "COM0"), ("O'Brien", "O'Brien"), ("a#b", "a#b"), ("Café Notes", "Café Notes"),
                      ("'yes'", "yes"), ("'123'", "123"), ("'null'", "null"), ("'O''Brien'", "O'Brien"),
                      ('"a\\"b\\\\c\\u00e9"', 'a"b\\cé'), ("external   # a comment", "external"),
                      ("~", None), ("", None)):
        check(f"answers reader: {raw!r} -> {want!r}", yaml_scalar(raw) == want)
    check("answers reader: a folded plain value joins its lines", join_scalar(["Client", "  Work"]) == "Client Work")
    check("answers reader: a double-quoted value continued with a backslash",
          join_scalar(['"Client\\', '  Work"']) == "ClientWork")
    try:
        yaml_scalar("'open")
        unclosed = False
    except ValueError:
        unclosed = True
    check("answers reader: an unclosed quote is an error, never a guess", unclosed)

    # Names.
    for name, bad in (("a:b.pdf", True), ("CON.pdf", True), ("con", True), ("COM1", True), ("COM0", False),
                      ("LPT¹.txt", True), ("conin$", True), ("name.", True), ("name ", True), (" name", True),
                      (".", True), ("..", True), ("Geschäft", False), ("tab\there", True), ("a" * 256, True),
                      ("quote.pdf", False), ("Café Notes", False), ("a|b", True)):
        check(f"name check: {name[:20]!r} {'refused' if bad else 'accepted'}", bool(name_problem(name)) == bad)
    check("name check: the 64-character cap applies to the layout answers", bool(name_problem("a" * 65, LAYOUT_CAP)))
    for slug, bad in (("my-book", False), ("-a", True), ("a-", True), ("a--b", True), ("A", True),
                      ("café", True), ("a" * 65, True), ("con", True), ("com1", True), ("123-go", False)):
        check(f"slug check: {slug[:20]!r} {'refused' if bad else 'accepted'}", bool(slug_problem(slug)) == bad)
    for name, bad in (("desktop.ini", True), ("Desktop.INI", True), (".lock", True), ("~$draft.docx", True),
                      ("a_vti_b", True), ("quote.pdf", False)):
        check(f"OneDrive names: {name!r} {'refused' if bad else 'accepted'}", bool(onedrive_problem(name)) == bad)
    for rel, kind in (("x/a.PDF", "docs"), ("a.jpeg", "photos"), ("a.m4a", "audio"), ("a.mkv", "videos"),
                      ("a.tar.gz", "docs"), ("a.xyz", "docs"), ("noext", "docs"), ("dir.png/file", "docs")):
        check(f"kind by extension: {rel} -> {kind}", kind_of_name(rel) == kind)
    later = {"videos": "webm mxf m4v mts m2ts avi braw r3d", "audio": "aac aif aiff opus pcm", "photos": "psd bmp dng exr"}
    for kind, exts in later.items():
        check(f"kind by extension: {exts} (any case) -> {kind}",
              all(kind_of_name(f"x/take.{e}") == kind and kind_of_name(f"x/TAKE.{e.upper()}") == kind for e in exts.split()))
    check("binary types: every extension of the table counts as a binary, in any case",
          all(is_binary("x/a." + e) and is_binary("x/a." + e.upper()) for exts in EXTENSIONS.values() for e in exts))

    # Role names: lower-case words joined by hyphens, never a shared role's or a kind's name.
    for name, ok in (("take", True), ("brand-export", True), ("approved-master", True), ("a1-b2", True),
                     ("brand-", False), ("a--b", False), ("-a", False), ("Take", False), ("1take", False),
                     ("ta ke", False), ("brand_export", False)):
        check(f"role name: {name!r} {'accepted' if ok else 'refused'}", bool(ROLE_NAME.fullmatch(name)) == ok)
    for name in ("brand-", "a--b", "docs", "photos", "audio", "videos", "signed", "evidence", "Take"):
        try:
            parse_map({"format": 1, "folders": [], "roles": [{"name": name, "evidence": True}]})
            refused = False
        except Unreadable:
            refused = True
        check(f"maps: a role named {name!r} makes the map invalid", refused)
    folders, roles = parse_map({"format": 1, "later": {"x": 1},
                                "folders": [{"path": "a/src", "later": True}, {"path": "a/src/out", "rows": "none"}],
                                "roles": [{"name": "brand-export", "evidence": False, "later": [1]},
                                          {"name": "take", "evidence": True, "repo": "skip"}]})
    check("maps: unknown keys on the map, a folder entry and a role entry are ignored; rows and repo are read",
          folders == [("a/src", None, None, True), ("a/src/out", None, None, False)]
          and roles == [("brand-export", False, False), ("take", True, True)])
    for bad, why in (({"format": 1, "folders": [{"path": "a", "rows": "some"}]}, "rows"),
                     ({"format": 1, "folders": [], "roles": [{"name": "take", "evidence": True, "repo": "commit"}]}, "repo"),
                     ({"format": 1, "folders": [], "roles": [{"name": "take", "evidence": True},
                                                             {"name": "take", "evidence": False}]}, "twice")):
        try:
            parse_map(bad)
            raised = ""
        except Unreadable as err:
            raised = str(err)
        check(f"maps: a malformed map is refused ({why})", why in raised)
    check("maps: the folders a broken map still names are known where every entry has a safe path",
          claimed_folders({"format": 9, "folders": [{"path": "a/src", "glob": "*"}]}) == ["a/src"]
          and claimed_folders({"format": 9, "folders": [{"glob": "a/*"}]}) is None
          and claimed_folders(None) is None and claimed_folders({"folders": []}) == [])
    for glob, path, meets in ((None, "a/src", True), ("a/*", "a/src", True), ("b/*", "a/src", False),
                              ("*.pdf", "a/src", True), ("a/src/x/*", "a/src", True), ("a/srcs/*", "a/src", False),
                              ("a", "a/src", True)):
        check(f"GLOB {glob!r} {'may touch' if meets else 'cannot touch'} {path}", glob_meets(glob, path) == meets)
    check("norm: NFC and NFD spellings, and case, compare equal",
          norm("Gescha\u0308ft") == norm("GESCHÄFT"))

    # Conflict-copy hints: each pattern, and near misses that must not match.
    listed = {("u", "d/quote.pdf")}
    for name, provider in (("quote (Ada's conflicted copy 2026-10-16).pdf", "Dropbox"),
                           ("quote (Ada's conflicted copy 2026-10-16 (1)).pdf", "Dropbox"),
                           ("quote (Case Conflict).pdf", "Dropbox"), ("quote (Selective Sync Conflict 2).pdf", "Dropbox"),
                           ("quote.pdf.conflict1", "rclone bisync"), ("quote.pdf..path2", "rclone bisync"),
                           ("quote.sync-conflict-20261016-101500-ABCDEF1.pdf", "Syncthing"),
                           ("quote-LAPTOP1.pdf", "OneDrive"), ("quote (1).pdf", "Google Drive")):
        hint = conflict_hint(name, "d/" + name, "u", listed) or ""
        check(f"hint: {name} -> {provider} copy of d/quote.pdf", f"a {provider} conflict copy of d/quote.pdf" in hint)
    for name in ("quote (Ada conflicted copy 2026-10-16).pdf", "quote (Case Conflicts).pdf", "quote.conflict.pdf",
                 "quote.pdf..path3", "quote.sync-conflict-2026101-101500-ABC.pdf", "other-LAPTOP1.pdf",
                 "other (1).pdf", "quote-DESKTOP9.pdf", "quote.pdf"):
        check(f"no hint: {name}", conflict_hint(name, "d/" + name, "u", listed) is None)
    check("hint: a leftover temporary copy", "interrupted" in (conflict_hint("a.pdf" + TMP_SUFFIX, "a.pdf" + TMP_SUFFIX, "u", set()) or ""))

    # Online-only attributes (simulated: no real placeholder is needed).
    class Fake:
        def __init__(self, attrs=0, flags=0):
            self.st_file_attributes, self.st_flags = attrs, flags

    check("online only: Windows RECALL_ON_DATA_ACCESS", online_only(Fake(attrs=0x00400000), "win32"))
    check("online only: Windows RECALL_ON_OPEN", online_only(Fake(attrs=0x00040000), "win32"))
    check("online only: macOS SF_DATALESS", online_only(Fake(flags=0x40000000), "darwin"))
    check("online only: the same flag means nothing off macOS", not online_only(Fake(flags=0x40000000), "linux"))
    check("online only: a plain file", not online_only(Fake(), "win32"))

    # The manifest writer.
    tricky = 'a "quoted" \\ back\tslash é \x01'
    for flag in (True, False):
        row = {f: tricky for f in FIELDS}
        row["bytes"], row["evidence"] = 7, flag
        check(f"row text round-trips through tomllib (evidence = {'true' if flag else 'false'})",
              tomllib.loads(row_text(row))["file"][0] == row)
    check("row text writes every field, evidence as a TOML boolean right after role",
          [line.split(" =")[0] for line in row_text(row).splitlines()[1:]] == list(FIELDS)
          and "\nevidence = false\n" in row_text(row))
    check("superseded names count up within a day",
          superseded_name("q.pdf", "16-10-2026", lambda n: n == "q.superseded-16-10-2026.pdf")
          == "q.superseded-16-10-2026-2.pdf")
    text = ('format = 1\nlater = "a top-level key"\n\n[[file]]\npath = "a/b.pdf"\nstate   =  "current"   # kept\n'
            'footage_id = "x-1"\n\n[[file]]\r\npath = "a/c.pdf"\r\nstate = \'current\'\r\n')
    check("state rewrite: only the value changes, its spacing, comment and the other rows' bytes kept",
          replace_state(text, 0, SUPERSEDED) == text.replace('"current"   # kept', '"superseded"   # kept')
          and replace_state(text, 1, WITHDRAWN) == text.replace("'current'\r\n", '"withdrawn"\r\n'))
    for broken in ('[[file]]\npath = "a"\n', '[[file]]\nstate = "current"\nstate = "current"\n',
                   '[[file]]\nstate = """current"""\n'):
        try:
            replace_state(broken, 0, SUPERSEDED)
            refused = False
        except Unwritable:
            refused = True
        check(f"state rewrite: refused where there is no single plain state line ({broken[9:30]!r})", refused)
    fake = type("F", (), {})()
    chain = [Row({"path": "a/q.pdf", "filed_under": "x/docs/old", "state": "superseded"}, 0, fake),
             Row({"path": "a/q.pdf", "filed_under": "x/docs/new", "state": "superseded",
                  "replaces": "a/q.superseded-1.pdf"}, 1, fake),
             Row({"path": "a/q.pdf", "filed_under": "x/docs/new", "state": "current",
                  "replaces": "a/q.superseded-2.pdf"}, 2, fake)]
    check("kept copies: each is listed under the filed_under of the row it superseded",
          listed_files(chain) == {("x/docs/old", "a/q.pdf"), ("x/docs/new", "a/q.pdf"),
                                  ("x/docs/old", "a/q.superseded-1.pdf"), ("x/docs/new", "a/q.superseded-2.pdf")})

    # The provider text.
    for value in PROVIDERS_FOR_TEST:
        lines = provider_text([value], "external")
        check(f"root: the {value} checklist follows the lines for every value",
              lines[:3] == list(EVERY_PROVIDER) and lines[3] == CHECKLISTS[value][0])
    lines = provider_text(["dropbox"], "repo")
    check("root: under repo the checklist opens with the repository line", lines[3] == REPO_LINE and lines[4] == "Provider: Dropbox.")
    check("root: an unknown provider is named, with the lines for every value",
          provider_text(["icloud"], "external") == list(EVERY_PROVIDER) + [UNKNOWN_PROVIDER.format("icloud")])
    check("root: two providers print both checklists",
          provider_text(["none", "nas"], "external")[3:] == list(CHECKLISTS["none"]) + list(CHECKLISTS["nas"]))

    # Python versions: read from PYTHON_MIN, never typed.
    import json
    need = "%d.%d" % PYTHON_MIN
    for older in ((PYTHON_MIN[0], PYTHON_MIN[1] - 1), (3, 8)):
        have = "%d.%d" % older
        buf = io.StringIO()
        with contextlib.redirect_stderr(buf):
            code = main(["root"], version=older)
        lines = buf.getvalue().splitlines()
        check(f"Python {have}: a data command exits 2 with the framed ERROR message",
              code == 2 and buf.getvalue() == too_old_text("root", older) and lines[0] == lines[-1] == RULE
              and lines[1] == (f"ERROR: the data-root tool did NOT run 'root', because this is Python {have} "
                               f"and it needs Python {need} or later.")
              and lines[3] == f"Upgrade to Python {need} or later, then run the command again.")
        held, out, err = sys.stdin, io.StringIO(), io.StringIO()
        sys.stdin = io.TextIOWrapper(io.BytesIO(b'{"tool_name": "Write", "tool_input": {"file_path": "/x/a.pdf"}}'))
        try:
            with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
                code = main(["guard"], version=older)
        finally:
            sys.stdin = held
        try:
            said = json.loads(out.getvalue())
        except ValueError:
            said = {}
        spec = said.get("hookSpecificOutput") if isinstance(said, dict) else None
        check(f"Python {have}: the guard lets the call through (0) and warns the person and the session",
              code == 0 and err.getvalue() == "" and out.getvalue().count("\n") == 1
              and sorted(said) == ["hookSpecificOutput", "systemMessage"]
              and isinstance(spec, dict) and sorted(spec) == ["additionalContext", "hookEventName"]
              and spec["hookEventName"] == "PreToolUse"
              and said["systemMessage"].startswith("WARNING: the data-root guard did NOT work: python3 here is "
                                                   f"Python {have}, and the guard needs Python {need} or later.")
              and f"Upgrade to Python {need} or later." in said["systemMessage"]
              and f"upgrade to Python {need} or later" in spec["additionalContext"])
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        code = main(["--help"], version=(3, 8))
    check("--help works on any Python", code == 0 and "Subcommands" in buf.getvalue())
    buf = io.StringIO()
    with contextlib.redirect_stderr(buf):
        code = main(["frobnicate"])
    check("an unknown subcommand exits 2 with one refusal line",
          code == 2 and buf.getvalue().startswith("refused: ") and buf.getvalue().count("\n") == 1)


PROVIDERS_FOR_TEST = ("none", "google-drive", "onedrive", "dropbox", "other-cloud", "nas")


def answers_text(values, extra=""):
    lines = ["# Changes here will be overwritten by Copier; NEVER EDIT MANUALLY", "_commit: v0.5.0",
             "_src_path: gh:example/template", "AGENT_CLIENTS:", "- codex"]
    lines += [f"{k}: {v}" for k, v in values.items()]
    return "\n".join(lines) + "\n" + extra


def self_test_projects(check, base, json, tomllib):
    global STAT
    has_git = shutil.which("git") is not None
    n = [0]

    def git(cwd, *args):
        subprocess.run(["git", "-c", "init.defaultBranch=main", *args], cwd=cwd, check=True,
                       capture_output=True)

    def project(answers, maps=None, use_git=True):
        n[0] += 1
        p = base / f"project-{n[0]}"
        (p / ".claude").mkdir(parents=True)
        for t, values in answers.items():
            (p / f".copier-answers.{t}.yml").write_text(values if isinstance(values, str) else answers_text(values),
                                                        encoding="utf-8")
        for t, m in (maps if maps is not None else {ONE: MAP_ONE}).items():
            (p / ".claude" / f"{t}-dataroot.json").write_text(json.dumps(m), encoding="utf-8")
        for folder in ("papers/src", "notes/src", "pictures", "sounds/src", "footage/src"):
            (p / folder).mkdir(parents=True, exist_ok=True)
        (p / "papers/src/.gitignore").write_text("*.[pP][dD][fF]\n*.syntek-tmp\n!external.toml\n", encoding="utf-8")
        (p / "sounds/src/.gitignore").write_text("lang/*/audio/\n", encoding="utf-8")
        if use_git and has_git:
            git(p, "init", "-q")
        return p

    def data_root(name="root", marker=""):
        r = base / name
        r.mkdir(parents=True, exist_ok=True)
        if marker is not None:
            (r / MARKER).write_text(marker, encoding="utf-8")
        return r

    def run(argv, cwd, env=None):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = main(argv, cwd=str(cwd), environ=dict(env or {}))
        return code, out.getvalue(), err.getvalue()

    def tree(path):
        return sorted(str(p.relative_to(path)) for p in Path(path).rglob("*")) if Path(path).exists() else []

    def one_line_each(err):
        return all(line.startswith(("warning: ", "refused: ")) for line in err.splitlines())

    root = data_root()
    env = {ROOT_ENV: str(root)}

    def own_root(name):
        r = data_root(name)
        return r, {ROOT_ENV: str(r)}

    # ── The root: every way a set value can be invalid, and the marker ──
    p = project({ONE: EXTERNAL})
    check("root: unset -> no root, nothing to stop text work", resolve(p, {}) is None)
    cases = (("", "set but empty"), ("relative/root", "not an absolute path"),
             (str(base / "missing"), "does not exist"), (str(p / ".claude" / f"{ONE}-dataroot.json"), "not a folder"))
    for value, why in cases:
        found = resolve(p, {ROOT_ENV: value})
        check(f"root: {why} -> invalid", isinstance(found, RootInvalid) and why in found.reason)
    bare = data_root("bare", marker=None)
    found = resolve(p, {ROOT_ENV: str(bare)})
    check("root: no marker -> invalid, with the touch command to run",
          isinstance(found, RootInvalid) and f'touch "${ROOT_ENV}/{MARKER}"' in found.reason)
    newer = data_root("newer", marker="format = 2\n")
    check("root: a marker of a newer format -> invalid", isinstance(resolve(p, {ROOT_ENV: str(newer)}), RootInvalid))
    check("root: a marker of format 1 -> valid", isinstance(resolve(p, {ROOT_ENV: str(data_root("fmt1", "format = 1\n"))}), Root))
    check("root: an empty marker (touch) -> valid", isinstance(resolve(p, env), Root))
    inside = p / "inner-root"
    inside.mkdir()
    (inside / MARKER).write_text("", encoding="utf-8")
    found = resolve(p, {ROOT_ENV: str(inside)})
    check("root: inside the repository -> invalid", isinstance(found, RootInvalid) and "inside this repository" in found.reason)
    code, _, err = run(["status"], p, {ROOT_ENV: str(inside)})
    check("status: a root inside the repository warns that it did not check the copies, and never exits 2",
          code in (0, 1) and "inside this repository" in err and "were not checked" in err)
    (inside / MARKER).unlink()
    (base / MARKER).write_text("", encoding="utf-8")
    found = resolve(p, {ROOT_ENV: str(base)})
    check("root: holding the repository -> invalid", isinstance(found, RootInvalid) and "holds this repository" in found.reason)
    code, out, err = run(["root"], p, {})
    check("root: a marker above the repository refuses, whatever the variable says",
          code == 2 and "puts this repository inside a data root" in err and "root: invalid" in out)
    code, _, err = run(["path", "papers/src/a.pdf"], p, env)
    check("path: a marker above the repository refuses the data commands", code == 2)
    code, _, err = run(["status"], p, env)
    check("status: a marker above the repository warns that it did not check the copies, and never exits 2",
          code in (0, 1) and "puts this repository inside a data root" in err and "were not checked" in err)
    (base / MARKER).unlink()

    # ── The self-test reads no inherited root: commands use only the environment they are given ──
    os.environ[ROOT_ENV] = str(root)
    code, out, _ = run(["root"], p, {})
    check("a root set in the process environment is never read by a run given none", out.startswith("root: none"))
    del os.environ[ROOT_ENV]

    # ── root's report ──
    code, out, err = run(["root"], p, env)
    lines = out.splitlines()
    check("root: exit 0 and the lines in their fixed order",
          code == 0 and [line.split(":")[0] for line in lines[:11]]
          == ["root", "origin", "marker", "store", "area", "slug", "kind", "kind", "kind", "kind", "provider"])
    check("root: the layout per kind", f"kind: docs = {root}{os.sep}business{os.sep}docs{os.sep}demo-project{os.sep}" in lines)
    check("root: the origin and the marker", f"origin: {ORIGIN_ENV}" in lines and "marker: present" in lines)
    check("root: the provider's checklist after a blank line",
          lines[11] == "" and lines[12:15] == list(EVERY_PROVIDER) and lines[15] == CHECKLISTS["none"][0])
    code, out, err = run(["root"], p, {})
    check("root: unset -> exit 0, 'root: none', the layout under '<root>'",
          code == 0 and "root: none" in out and "kind: docs = <root>" in out)
    code, out, err = run(["root"], p, {ROOT_ENV: str(bare)})
    check("root: set but invalid -> exit 2, one refusal line", code == 2 and "refused: " in err and one_line_each(err))
    synced = base / "Dropbox" / "inner"
    synced.mkdir(parents=True)
    ps = project({ONE: EXTERNAL})
    shutil.move(str(ps), str(synced / ps.name))
    ps = synced / ps.name
    code, out, err = run(["root"], ps, env)
    check("root: a repository under a sync folder warns, exit unchanged",
          code == 0 and "looks like a synced folder" in err and "corrupts Git" in err)
    od = data_root("OneDrive/data")
    code, out, err = run(["root"], p, {ROOT_ENV: str(od)})
    check("root: a data root under a sync folder with DATA_PROVIDER none asks for a re-answer",
          code == 0 and "re-answer DATA_PROVIDER" in err)
    pr = project({ONE: {"DATA_STORE": "repo", "DATA_PROVIDER": "dropbox"}})
    code, out, err = run(["root"], pr, env)
    check("root: under repo, the layout is not used and the checklist opens with the repository line",
          code == 0 and "area: not used under repo" in out and REPO_LINE in out and "Provider: Dropbox." in out)

    # ── The store across answers files ──
    p2 = project({ONE: EXTERNAL, TWO: {"DATA_PROVIDER": "none"}})
    code, out, err = run(["store"], p2, env)
    check("store: a record without DATA_STORE is 'not yet asked', with one warning and exit 0",
          code == 0 and f"{TWO}: not yet asked" in out and f"{ONE}: external" in out
          and err.count("not yet asked") == 1 and one_line_each(err))
    code, out, _ = run(["path", "papers/src/a.pdf"], p2, env)
    check("path: a sibling not yet asked never refuses", code == 0 and out.count("\n") == 1)
    p3 = project({ONE: EXTERNAL, TWO: {"DATA_STORE": "repo"}})
    code, out, err = run(["store"], p3, env)
    check("store: two stores disagree -> exit 2", code == 2 and "disagree on DATA_STORE" in err)
    code, out, err = run(["path", "papers/src/a.pdf"], p3, env)
    check("path: a repo record beside an external one is a store disagreement, never a layout one",
          code == 2 and out == "" and "disagree on DATA_STORE" in err and "DATA_AREA" not in err)
    p4 = project({ONE: EXTERNAL, TWO: dict(EXTERNAL, DATA_SLUG="other-slug")})
    code, _, err = run(["path", "papers/src/a.pdf"], p4, env)
    check("path: both external, another slug -> exit 2", code == 2 and "disagree on DATA_SLUG" in err)
    p5 = project({ONE: EXTERNAL, TWO: dict(EXTERNAL, DATA_PROVIDER="dropbox")})
    code, out, err = run(["path", "papers/src/a.pdf"], p5, env)
    check("path: a DATA_PROVIDER difference warns and never refuses", code == 0 and "differ on DATA_PROVIDER" in err)
    code, out, _ = run(["root"], p5, env)
    check("root: a provider difference prints both checklists",
          "provider: none, dropbox" in out and "Provider: Dropbox." in out and CHECKLISTS["none"][0] in out)
    p6 = project({ONE: dict(EXTERNAL, DATA_STORE="lfs")})
    code, _, err = run(["path", "papers/src/a.pdf"], p6, env)
    check("path: a store this tool does not know needs a newer template", code == 2 and "needs a newer template" in err)
    code, out, _ = run(["root"], p6, env)
    check("root: an unknown store is named, exit 0", code == 0 and "store: lfs (unknown)" in out)
    p7 = project({ONE: dict(EXTERNAL, DATA_AREA="a:b")})
    code, _, err = run(["path", "papers/src/a.pdf"], p7, env)
    check("path: an answer that is not Windows-safe refuses", code == 2 and "DATA_AREA 'a:b'" in err)
    p8 = project({ONE: dict(EXTERNAL, DATA_KIND_PHOTOS="Docs")})
    code, _, err = run(["path", "papers/src/a.pdf"], p8, env)
    check("path: kind folders equal ignoring case refuse", code == 2 and "must differ" in err)
    quoted = answers_text({}) + ("DATA_STORE: external\nDATA_AREA: 'Client Work'\nDATA_SLUG: demo-project\n"
                                 "DATA_KIND_DOCS: \"Docs \\u00e9\"\nDATA_KIND_PHOTOS: 'yes'\nDATA_KIND_AUDIO: O'Brien\n"
                                 "DATA_KIND_VIDEOS: a#b\nDATA_PROVIDER: none\n")
    p9 = project({ONE: quoted})
    code, out, _ = run(["root"], p9, env)
    check("root: quoted answers are read as written",
          "area: Client Work" in out and "Docs é" in out and f"{os.sep}yes{os.sep}" in out and "O'Brien" in out and "a#b" in out)

    # ── Maps ──
    clash_two = {"format": 1, "folders": [{"path": "papers/src"}]}
    pm = project({ONE: EXTERNAL}, {ONE: MAP_ONE, TWO: clash_two})
    code, _, err = run(["path", "papers/src/a.pdf"], pm, env)
    check("maps: two maps claiming one folder -> exit 2", code == 2 and "claim one folder" in err)
    code, _, _ = run(["path", "notes/src/a.pdf"], pm, env)
    check("maps: a folder no other map claims still works", code == 0)
    code, out, err = run(["root"], pm, env)
    check("root: names both maps of a clash", f"{ONE}-dataroot.json" in err and f"{TWO}-dataroot.json" in err)
    pn = project({ONE: EXTERNAL}, {ONE: MAP_ONE, TWO: {"format": 1, "folders": [{"path": "papers"}]}})
    code, _, err = run(["path", "papers/src/a.pdf"], pn, env)
    check("maps: one folder inside another map's -> exit 2", code == 2 and "claim one folder" in err)
    pf = project({ONE: EXTERNAL}, {ONE: dict(MAP_ONE, format=2)})
    code, _, err = run(["path", "papers/src/a.pdf"], pf, env)
    check("maps: a newer map format -> exit 2", code == 2 and "newer template" in err)
    for bad, why in (({"format": 1, "folders": [{"path": "../x"}]}, "'..'"),
                     ({"format": 1, "folders": [{"path": "a", "kind": "pictures"}]}, "kind"),
                     ({"format": 1, "folders": [{"path": "a", "warn_over_kib": True}]}, "warn_over_kib"),
                     ({"format": 1, "folders": [], "roles": [{"name": "signed", "evidence": False}]}, "shared role")):
        try:
            parse_map(bad)
            raised = ""
        except Unreadable as err:
            raised = str(err)
        check(f"maps: a malformed map is refused ({why})", why in raised)
    code, out, _ = run(["path", "papers/src/x.jpg"], p, env)
    check("maps: a folder's fixed kind wins over the extension", f"{os.sep}docs{os.sep}" in out and "photos" not in out)
    code, out, _ = run(["path", "notes/src/x.jpg"], p, env)
    check("maps: otherwise the extension decides the kind", f"{os.sep}photos{os.sep}" in out)

    # ── path ──
    code, out, err = run(["path", "notes/src/x.pdf"], p, env)
    check("path: under external, exactly one line, the mirror path",
          code == 0 and out == os.path.join(str(root), "business", "docs", "demo-project", "notes", "src", "x.pdf") + "\n")
    code, out, err = run(["path", "notes/src/x.pdf"], p, {})
    check("path: under external with no root -> exit 2, nothing on stdout", code == 2 and out == "" and ROOT_ENV in err)
    code, out, _ = run(["path", "notes/src/x.pdf"], pr, {})
    check("path: under repo -> the work-tree path, with no root needed", code == 0 and out == str(pr / "notes/src/x.pdf") + "\n")
    (p / "notes/src/here.pdf").write_bytes(b"in the work tree")
    code, out, _ = run(["path", "notes/src/here.pdf"], p, env)
    check("path: under external, a work-tree file first", out == str(p / "notes/src/here.pdf") + "\n")
    code, out, _ = run(["path", "../elsewhere.pdf"], p, env)
    check("path: outside the project -> exit 2", code == 2 and out == "")
    code, _, err = run(["path", "papers/src/x.png", "--kind", "photos"], p, env)
    check("path: --kind cannot override a folder's fixed kind", code == 2 and "fixes the kind" in err)
    code, out, _ = run(["path", "notes/src/sub", "--kind", "audio"], p, env)
    check("path: --kind places a folder under that kind", f"{os.sep}audio{os.sep}" in out)
    code, out, _ = run(["path", "papers/src/a.pdf"], p / "papers", env)
    check("path: from a sub-folder, paths are taken from the project's top", out.endswith(os.path.join("papers", "src", "a.pdf") + "\n"))

    # ── add ──
    pdf = p / "papers/src/client/a.pdf"
    pdf.parent.mkdir(parents=True)
    pdf.write_bytes(b"%PDF issued copy")
    code, out, err = run(["add", "papers/src/client/a.pdf", "--role", "issued", "--source", "papers/src/client/a.tex"], p, env)
    dest = root / "business/docs/demo-project/papers/src/client/a.pdf"
    mpath = p / "papers/src" / MANIFEST
    rows = tomllib.loads(mpath.read_text(encoding="utf-8"))["file"] if mpath.exists() else []
    check("add: exit 0, the copy at the mirror path with the same bytes",
          code == 0 and dest.read_bytes() == pdf.read_bytes())
    check("add: the row records path, kind, filed_under, role, evidence, hash, size, date and state",
          len(rows) == 1 and rows[0]["path"] == "papers/src/client/a.pdf" and rows[0]["kind"] == "docs"
          and rows[0]["filed_under"] == "business/docs/demo-project" and rows[0]["role"] == "issued"
          and rows[0]["evidence"] is False
          and rows[0]["sha256"] == hashlib.sha256(pdf.read_bytes()).hexdigest() and rows[0]["bytes"] == 16
          and rows[0]["filed"] == "16/10/2026" and rows[0]["state"] == "current"
          and rows[0]["source"] == "papers/src/client/a.tex")
    check("add: the manifest opens with format = 1", mpath.read_text(encoding="utf-8").startswith("format = 1\n"))
    check("add: no temporary copy is left", not any(TMP_SUFFIX in s for s in tree(root) + tree(p)))
    before = mpath.read_bytes()
    code, out, err = run(["add", "papers/src/client/a.pdf", "--role", "issued"], p, env)
    check("add: a second add refuses (exit 2) and changes nothing",
          code == 2 and "already filed" in err and mpath.read_bytes() == before)
    pdf.write_bytes(b"%PDF issued again")
    code, out, err = run(["add", "papers/src/client/a.pdf", "--role", "issued", "--force"], p, env)
    kept = root / "business/docs/demo-project/papers/src/client/a.superseded-16-10-2026.pdf"
    after = mpath.read_bytes()
    rows = tomllib.loads(after.decode("utf-8"))["file"]
    check("add --force: the listed copy is kept as <stem>.superseded-DD-MM-YYYY",
          code == 0 and kept.read_bytes() == b"%PDF issued copy" and dest.read_bytes() == b"%PDF issued again")
    check("add --force: rows are appended; the old row keeps its path and hash, and only its state changes",
          len(rows) == 2 and rows[0]["state"] == "superseded" and rows[0]["path"] == "papers/src/client/a.pdf"
          and rows[0]["sha256"] == hashlib.sha256(b"%PDF issued copy").hexdigest()
          and {k: v for k, v in rows[0].items() if k != "state"}
          == {k: v for k, v in tomllib.loads(before.decode("utf-8"))["file"][0].items() if k != "state"})
    check("add --force: the new current row's replaces names the kept copy",
          rows[1]["state"] == "current" and rows[1]["path"] == "papers/src/client/a.pdf"
          and rows[1]["replaces"] == "papers/src/client/a.superseded-16-10-2026.pdf")
    check("add --force: the old text is kept byte for byte but for the one state value",
          after.startswith(before.replace(b'state = "current"', b'state = "superseded"')))
    pdf.write_bytes(b"%PDF issued a third time")
    code, _, _ = run(["add", "papers/src/client/a.pdf", "--role", "issued", "--force"], p, env)
    check("add --force twice in a day: the second superseded copy is -2",
          code == 0 and (kept.parent / "a.superseded-16-10-2026-2.pdf").is_file())
    code, out, _ = run(["verify"], p, env)
    check("verify: after the adds, everything verifies and the kept copies are listed (exit 0)",
          code == 0 and "unlisted 0" in out and "verified 1," in out)
    signed = p / "papers/src/client/b-signed.pdf"
    signed.write_bytes(b"%PDF signed copy")
    code, out, err = run(["add", "papers/src/client/b-signed.pdf", "--role", "signed"], p, env)
    bdest = root / "business/docs/demo-project/papers/src/client/b-signed.pdf"
    before = mpath.read_bytes()
    check("add: a signed copy's row records evidence = true",
          code == 0 and tomllib.loads(before.decode("utf-8"))["file"][-1]["evidence"] is True)
    signed.write_bytes(b"%PDF signed again")
    code, out, err = run(["add", "papers/src/client/b-signed.pdf", "--role", "signed", "--force"], p, env)
    check("add --force on an evidence row: exit 2, a new version under its own name, nothing changed",
          code == 2 and "file a new version under its own name" in err and bdest.read_bytes() == b"%PDF signed copy"
          and mpath.read_bytes() == before and not list(bdest.parent.glob("b-signed.superseded-*")))
    code, out, err = run(["add", "papers/src/client/b-signed.pdf", "--role", "signed"], p, env)
    check("add on an evidence row without --force: the refusal never offers --force",
          code == 2 and "--force" not in err and "own name" in err)
    pcr = project({ONE: EXTERNAL})
    _, env_cr = own_root("root-crlf")
    (pcr / "notes/src/w.pdf").write_bytes(b"one")
    run(["add", "notes/src/w.pdf", "--role", "archive"], pcr, env_cr)
    crlf = pcr / "notes/src" / MANIFEST
    crlf.write_bytes(crlf.read_bytes().replace(b"\n", b"\r\n"))
    (pcr / "notes/src/w.pdf").write_bytes(b"two")
    code, _, _ = run(["add", "notes/src/w.pdf", "--role", "archive", "--force"], pcr, env_cr)
    raw = crlf.read_bytes()
    check("add --force on a CRLF manifest keeps CRLF on every line",
          code == 0 and raw.count(b"\n") == raw.count(b"\r\n") and len(tomllib.loads(raw.decode())["file"]) == 2)

    # add never files a folder, and --force never keeps a changed copy or half a supersede.
    pf = project({ONE: EXTERNAL})
    rf, env_f = own_root("root-force")
    mirror_f = rf / "business/docs/demo-project/notes/src"
    (pf / "loose.pdf").write_bytes(b"loose")
    code, _, err = run(["add", "loose.pdf", "--role", "archive", "--as", "notes/src"], pf, env_f)
    check("add --as the filing folder itself: exit 2, nothing written, the manifest still readable",
          code == 2 and "is a filing folder" in err and not (pf / "notes/src" / MANIFEST).exists() and not mirror_f.exists())
    (pf / "notes/src/sub").mkdir()
    code, _, err = run(["add", "loose.pdf", "--role", "archive", "--as", "notes/src/sub"], pf, env_f)
    check("add --as a folder of the work tree: exit 2, nothing written",
          code == 2 and "is a folder in the work tree" in err and not mirror_f.exists())
    (pf / "notes/src/c.pdf").write_bytes(b"first")
    run(["add", "notes/src/c.pdf", "--role", "archive"], pf, env_f)
    mf = pf / "notes/src" / MANIFEST
    (mirror_f / "c.pdf").write_bytes(b"CORRUPTED")
    (pf / "notes/src/c.pdf").write_bytes(b"second")
    before = mf.read_bytes()
    code, _, err = run(["add", "notes/src/c.pdf", "--role", "archive", "--force"], pf, env_f)
    check("add --force over a listed copy that no longer hashes as its row: exit 1, nothing kept or written",
          code == 1 and "no longer hashes" in err and mf.read_bytes() == before
          and (mirror_f / "c.pdf").read_bytes() == b"CORRUPTED" and not list(mirror_f.glob("c.superseded-*")))
    code, out, _ = run(["verify"], pf, env_f)
    check("and verify still reports the change (exit 1)", code == 1 and "changed: notes/src/c.pdf" in out)
    (pf / "notes/src/i.pdf").write_bytes(b"one")
    run(["add", "notes/src/i.pdf", "--role", "archive"], pf, env_f)
    (pf / "notes/src/i.pdf").write_bytes(b"two")
    before = mf.read_bytes()
    for name in ("copy_verified", "write_manifest"):
        real = globals()[name]

        def stop(*a, **k):
            raise KeyboardInterrupt

        globals()[name] = stop
        try:
            run(["add", "notes/src/i.pdf", "--role", "archive", "--force"], pf, env_f)
            stopped = False
        except KeyboardInterrupt:
            stopped = True
        finally:
            globals()[name] = real
        check(f"add --force interrupted in {name}: the listed copy is where its row says, nothing kept, no temporary left",
              stopped and (mirror_f / "i.pdf").read_bytes() == b"one" and mf.read_bytes() == before
              and not list(mirror_f.glob("i.superseded-*")) and not any(TMP_SUFFIX in s for s in tree(rf)))
    code, _, _ = run(["add", "notes/src/i.pdf", "--role", "archive", "--force"], pf, env_f)
    check("add --force after an interrupt: the retry keeps the listed bytes as the superseded copy",
          code == 0 and (mirror_f / "i.pdf").read_bytes() == b"two"
          and [k.read_bytes() for k in mirror_f.glob("i.superseded-*")] == [b"one"])
    mf.write_text(mf.read_text(encoding="utf-8").replace("format = 1", "format = 2", 1), encoding="utf-8")
    code, out, err = run(["path", "notes/src/i.pdf"], pf, env_f)
    check("path: a folder whose manifest is newer refuses even where the work tree holds the file (exit 2)",
          code == 2 and out == "" and "needs a newer template" in err)
    mf.write_text(mf.read_text(encoding="utf-8").replace("format = 2", "format = 1", 1), encoding="utf-8")
    try:
        os.symlink("/nonexistent/logo.png", str(pf / "pictures/logo-link.png"))
        code, out, err = run(["status"], pf, env_f)
        dangling = code in (0, 1) and "status: " in out and "refused" not in err
    except (OSError, NotImplementedError):
        dangling = True
    check("status: a dangling link in a folder with warn_over_kib is passed over, the report completes", dangling)
    with contextlib.suppress(OSError):
        os.unlink(str(pf / "pictures/logo-link.png"))
    try:
        with open(os.fsencode(str(pf / "papers/src")) + b"/bad\xffname.pdf", "wb") as f:
            f.write(b"x")
        odd = True
    except (OSError, ValueError):
        odd = False   # a file system that holds only UTF-8 names (APFS, NTFS)
    if odd:
        code, out, err = run(["check-names"], pf, env_f)
        check("check-names: a name that is not UTF-8 is reported unsafe (exit 1), never a crash",
              code == 1 and "is not valid UTF-8" in out and "\\udcff" in out)
        code, _, err = run(["add", "papers/src/bad\udcffname.pdf", "--role", "archive"], pf, env_f)
        check("add: a name that is not UTF-8 refuses (exit 2)", code == 2 and "not valid UTF-8" in err)
        if has_git:
            done = subprocess.run([sys.executable, "-I", str(Path(__file__)), "status"], cwd=str(pf), capture_output=True,
                                  env=dict(env_f, PATH=os.environ.get("PATH", ""), PYTHONIOENCODING="utf-8:strict"))
            check("status: a name that is not UTF-8 is printed escaped, and the report completes",
                  done.returncode in (0, 1) and b"Traceback" not in done.stderr and b"status: " in done.stdout)
        with contextlib.suppress(OSError):
            os.unlink(os.fsencode(str(pf / "papers/src")) + b"/bad\xffname.pdf")
    marked_repo = base / "marked-store" / "proj"
    (marked_repo / ".claude").mkdir(parents=True)
    (marked_repo.parent / MARKER).write_text("", encoding="utf-8")
    (marked_repo / f".copier-answers.{ONE}.yml").write_text(answers_text({"DATA_STORE": "repo"}), encoding="utf-8")
    (marked_repo / ".claude" / f"{ONE}-dataroot.json").write_text(json.dumps(MAP_ONE), encoding="utf-8")
    code, _, err = run(["status"], marked_repo, {})
    check("status under repo with a marker above the repository warns that a sync service corrupts Git",
          "puts this repository inside a data root" in err)
    check("status under repo with a marker above says it did not check the copies, and never exits 2",
          code in (0, 1) and "were not checked" in err)
    repo_in = project({ONE: {"DATA_STORE": "repo"}})
    (repo_in / "inner-root").mkdir()
    (repo_in / "inner-root" / MARKER).write_text("", encoding="utf-8")
    code, _, err = run(["status"], repo_in, {ROOT_ENV: str(repo_in / "inner-root")})
    check("status under repo with the root inside the repository warns that it did not check the copies, never exit 2",
          code in (0, 1) and "lies inside this repository" in err and "were not checked" in err)
    # Under repo, path and add use no root, but they refuse one that contains the repository or
    # lies inside it, and a marker above it, before any shortcut (exit 2, nothing written).
    (marked_repo / ".claude" / f"{TWO}-dataroot.json").write_text(json.dumps(MAP_TWO), encoding="utf-8")
    repo_two = project({ONE: {"DATA_STORE": "repo"}}, {ONE: MAP_ONE, TWO: MAP_TWO})
    (repo_two / "inner-root").mkdir()
    (repo_two / "inner-root" / MARKER).write_text("", encoding="utf-8")
    env_in = {ROOT_ENV: str(repo_two / "inner-root")}
    (repo_two / "footage/src/take.wav").write_bytes(b"take")
    (repo_two / "sounds/src/g.mp3").write_bytes(b"ID3 generated")
    for where, proj, env_c, says in (("a marker above the repository", marked_repo, {}, "puts this repository inside a data root"),
                                     ("the root inside the repository", repo_two, env_in, "lies inside this repository")):
        before = tree(proj)
        code, out, err = run(["path", "notes/src/x.pdf"], proj, env_c)
        check(f"path under repo with {where}: exit 2 with the root error, nothing on stdout",
              code == 2 and out == "" and says in err)
        for role, rel in (("generated", "sounds/src/g.mp3"), ("take", "footage/src/take.wav")):
            code, out, err = run(["add", rel, "--role", role], proj, env_c)
            check(f"add --role {role} under repo with {where} (a role never filed there): exit 2 with the "
                  "root error before its shortcut, nothing written",
                  code == 2 and out == "" and says in err and "not filed" not in out and tree(proj) == before)
        code, _, err = run(["add", "notes/src/x.pdf", "--role", "archive"], proj, env_c)
        check(f"add --role archive under repo with {where}: the root error first (exit 2)",
              code == 2 and says in err and "commit the file instead" not in err)
        code, _, err = run(["check-names"], proj, env_c)
        check(f"check-names under repo with {where} still runs (never the root error)", code in (0, 1) and says not in err)
        code, _, err = run(["status"], proj, env_c)
        check(f"status under repo with {where} still warns and never exits 2", code in (0, 1) and says in err)
    (marked_repo.parent / MARKER).unlink()
    unmarked = data_root("repo-unmarked", marker=None)
    valid = data_root("repo-valid")   # a marked root outside the repository, as an owner sets one
    for what, env_c in (("an unmarked", {ROOT_ENV: str(unmarked)}), ("an empty", {ROOT_ENV: ""}),
                        ("a valid, marked", {ROOT_ENV: str(valid)})):
        code, out, _ = run(["path", "notes/src/x.pdf"], repo_two, env_c)
        check(f"path under repo with {what} root that does not hold the repository: the work-tree path, exit 0",
              code == 0 and out == str(repo_two / "notes/src/x.pdf") + "\n")
        code, out, _ = run(["add", "sounds/src/g.mp3", "--role", "generated"], repo_two, env_c)
        code2, out2, _ = run(["add", "footage/src/take.wav", "--role", "take"], repo_two, env_c)
        check(f"add --role generated and a \"repo\": \"skip\" role under repo with {what} root: exit 0, nothing written",
              code == 0 and code2 == 0 and out.startswith("not filed: ") and out2.startswith("not filed: ")
              and not (repo_two / "sounds/src" / MANIFEST).exists()
              and not (repo_two / "footage/src" / MANIFEST).exists() and tree(valid) == [MARKER])
    for name in ("a:b.pdf", "trail."):
        bad = p / "notes/src" / name
        bad.write_bytes(b"x")
        code, _, err = run(["add", f"notes/src/{name}", "--role", "archive"], p, env)
        check(f"add: a name that is not Windows-safe ({name}) refuses, exit 2, nothing written",
              code == 2 and "Windows-safe" in err and not (root / "business/docs/demo-project/notes").exists())
    (p / "notes/src/ok.pdf").write_bytes(b"fine")
    code, _, err = run(["add", "notes/src/ok.pdf", "--as", "notes/src/CON.pdf", "--role", "archive"], p, env)
    check("add: --as a device name refuses", code == 2 and "device name" in err)
    code, _, _ = run(["add", "notes/src/a:b.pdf", "--as", "notes/src/a-b.pdf", "--role", "archive"], p, env)
    nrows = tomllib.loads((p / "notes/src" / MANIFEST).read_text(encoding="utf-8"))["file"]
    check("add: --as a safe name files it, and former_name keeps the original",
          code == 0 and nrows[-1]["path"] == "notes/src/a-b.pdf" and nrows[-1]["former_name"] == "a:b.pdf")
    code, _, err = run(["add", "notes/src/ok.pdf", "--role", "take"], p, env)
    check("add: a role no map defines refuses", code == 2 and "not a role" in err)
    p2m = project({ONE: EXTERNAL}, {ONE: MAP_ONE, TWO: MAP_TWO})
    (p2m / "footage/src/t.mov").write_bytes(b"take one")
    code, _, _ = run(["add", "footage/src/t.mov", "--role", "take"], p2m, own_root("root-roles")[1])
    check("add: a role another template's map defines is accepted", code == 0)
    (p / "notes/src/link.pdf").write_bytes(b"l")
    code, _, err = run(["add", "notes/src/link.pdf", "--role", "archive", "--label", "https://example.com/x"], p, env)
    check("add: a label that looks like a URL warns", code == 0 and "looks like a URL" in err)
    code, _, err = run(["add", "notes/src/ok.pdf", "--role", "archive"], p, {})
    check("add: no root -> exit 2, nothing written", code == 2 and "ok.pdf" not in str(tree(root)))
    code, _, err = run(["add", str(dest), "--as", "notes/src/again.pdf", "--role", "archive"], p, env)
    check("add: a file already under the data root refuses", code == 2 and "already under the data root" in err)
    outside = base / "outside.pdf"
    outside.write_bytes(b"from elsewhere")
    code, _, err = run(["add", str(outside), "--role", "received"], p, env)
    check("add: a file outside the project needs --as", code == 2 and "--as" in err)
    code, _, _ = run(["add", str(outside), "--as", "notes/src/received.pdf", "--role", "received"], p, env)
    check("add: with --as it is filed", code == 0)
    (p / "absent/x.pdf").parent.mkdir(parents=True)
    (p / "absent/x.pdf").write_bytes(b"x")
    code, _, err = run(["add", "absent/x.pdf", "--role", "archive"], p, env)
    check("add: a file in no filing folder refuses", code == 2 and "no filing folder" in err)
    code, out, err = run(["add", "notes/src/ok.pdf", "--role", "archive"], pr, env)
    check("add: under repo -> exit 2, 'commit the file instead'", code == 2 and "commit the file instead" in err)
    audio = pr / "sounds/src/lang/x/audio/a.mp3"
    audio.parent.mkdir(parents=True)
    audio.write_bytes(b"ID3 generated")
    code, out, err = run(["add", "sounds/src/lang/x/audio/a.mp3", "--role", "generated"], pr, env)
    check("add --role generated under repo: exit 0, nothing written",
          code == 0 and "stay git-ignored" in out and not (pr / "sounds/src" / MANIFEST).exists())
    gen = p / "sounds/src/lang/x/audio/a.mp3"
    gen.parent.mkdir(parents=True)
    gen.write_bytes(b"ID3 generated")
    code, _, _ = run(["add", "sounds/src/lang/x/audio/a.mp3", "--role", "generated"], p, env)
    grows = tomllib.loads((p / "sounds/src" / MANIFEST).read_text(encoding="utf-8"))["file"]
    check("add --role generated under external: filed under the audio kind with a generated row",
          code == 0 and grows[0]["kind"] == "audio" and grows[0]["role"] == "generated"
          and (root / "business/audio/demo-project/sounds/src/lang/x/audio/a.mp3").is_file())
    code, out, _ = run(["verify"], p, env)
    check("verify: after filing generated audio, nothing is unlisted", code == 0 and "unlisted 0" in out)

    # ── The case-only clash ──
    croot = data_root("case-root")
    (croot / "business").mkdir()
    pc = project({ONE: dict(EXTERNAL, DATA_AREA="Business")})
    code, _, err = run(["root"], pc, {ROOT_ENV: str(croot)})
    check("root: a folder differing only in case warns", code == 0 and "differs only in case" in err)
    (pc / "notes/src/c.pdf").write_bytes(b"c")
    code, _, err = run(["add", "notes/src/c.pdf", "--role", "archive"], pc, {ROOT_ENV: str(croot)})
    check("add: refuses to create the second spelling, exit 2",
          code == 2 and "never creates the second spelling" in err and "Business" not in os.listdir(croot))

    # ── verify ──
    bdest.write_bytes(b"%PDF signed copz")
    code, out, _ = run(["verify"], p, env)
    check("verify: a flipped byte -> exit 1, changed, an evidence failure",
          code == 1 and "changed: papers/src/client/b-signed.pdf" in out and "an evidence row" in out)
    bdest.write_bytes(b"%PDF signed copy")
    dest.write_bytes(b"%PDF issued a third timf")
    code, out, _ = run(["verify"], p, env)
    check("verify: a flipped byte in an issued copy -> exit 1, changed, with no evidence note",
          code == 1 and "changed: papers/src/client/a.pdf at" in out and "evidence" not in out)
    dest.write_bytes(b"%PDF issued a third time")
    moved = root / "business/docs/demo-project/notes/src/ok.pdf"
    target = root / "business/docs/demo-project/notes/src/received.pdf"
    target.rename(moved)
    code, out, _ = run(["verify"], p, env)
    check("verify: a missing file -> exit 1", code == 1 and "missing: notes/src/received.pdf" in out)
    check("verify: an unlisted file -> exit 1", "unlisted: business/docs/demo-project/notes/src/ok.pdf" in out)
    moved.rename(target)
    conflict = root / "business/docs/demo-project/notes/src/received (Ada's conflicted copy 2026-10-16).pdf"
    conflict.write_bytes(b"other")
    code, out, _ = run(["verify"], p, env)
    check("verify: an unlisted conflict copy carries a hint naming its listed file",
          code == 1 and "a Dropbox conflict copy of notes/src/received.pdf" in out)
    conflict.unlink()
    code, out, _ = run(["verify", "papers/*"], p, env)
    check("verify GLOB: only matching rows", code == 0 and "verified 2," in out)
    STAT = fake_stat({str(target)})
    code, out, _ = run(["verify"], p, env)
    check("verify: an online-only file is not read, and is no failure",
          code == 0 and "online only: notes/src/received.pdf (not read)" in out and "online only 1 (not read" in out)
    target.write_bytes(b"tampered")
    code, out, _ = run(["verify"], p, env)
    check("verify: an online-only file is never opened (its change goes unseen)", code == 0)
    code, out, _ = run(["verify", "--hydrate"], p, env)
    check("verify --hydrate: reads it like any other file", code == 1 and "changed: notes/src/received.pdf" in out)
    target.write_bytes(b"from elsewhere")
    code, out, err = run(["status"], p, env)
    check("status: counts online-only files in its summary", "1 online only" in out)
    STAT = os.stat

    # ── A change of layout answers: filed_under keeps the old folder findable ──
    po = project({ONE: EXTERNAL})
    _, env = own_root("root-layout")
    (po / "notes/src/old.pdf").write_bytes(b"old slug")
    run(["add", "notes/src/old.pdf", "--role", "archive"], po, env)
    (po / f".copier-answers.{ONE}.yml").write_text(answers_text(dict(EXTERNAL, DATA_SLUG="new-slug")), encoding="utf-8")
    code, out, _ = run(["verify"], po, env)
    check("verify: a row filed under an older slug verifies at its old folder", code == 0 and "verified 1," in out)
    code, out, err = run(["status"], po, env)
    check("status: names the old folder and the --data line that restores it",
          "'business/docs/demo-project'" in err and "--data DATA_SLUG=demo-project" in err)
    (po / "notes/src/old.pdf").unlink()
    code, out, _ = run(["path", "notes/src/old.pdf"], po, env)
    check("path: a listed file outside the work tree is found where its row says",
          code == 0 and "demo-project" in out and "new-slug" not in out)
    (po / f".copier-answers.{ONE}.yml").write_text(answers_text({"DATA_STORE": "repo"}), encoding="utf-8")
    code, out, err = run(["status"], po, env)
    check("status: under repo, rows still filed under the root are named, with the way back",
          code == 0 and "--data DATA_STORE=external" in err and "DATA_AREA=business" in err)

    # ── status: loss detection (needs git) ──
    root, env = own_root("root-status")
    if has_git:
        ps2 = project({ONE: EXTERNAL})
        (ps2 / "papers/src/lost.pdf").write_bytes(b"dropped in")
        (ps2 / "pictures/big.png").write_bytes(b"x" * 1025)
        (ps2 / "pictures/small.png").write_bytes(b"x" * 1024)
        (ps2 / "sounds/src/lang/y/audio").mkdir(parents=True)
        (ps2 / "sounds/src/lang/y/audio/z.wav").write_bytes(b"RIFF")
        code, out, err = run(["status"], ps2, env)
        check("status: an ignored PDF with no row -> not filed, exit 1",
              code == 1 and "not filed: papers/src/lost.pdf" in out)
        check("status: ignored audio in an ignored folder is found too", "not filed: sounds/src/lang/y/audio/z.wav" in out)
        check("status: a file over the map's warn_over_kib warns", "pictures/big.png is" in err and "over the 1.0 KB" in err)
        check("status: a file under it does not", "pictures/small.png" not in err)
        run(["add", "papers/src/lost.pdf", "--role", "received"], ps2, env)
        run(["add", "sounds/src/lang/y/audio/z.wav", "--role", "generated"], ps2, env)
        code, out, _ = run(["status"], ps2, env)
        check("status: once filed, nothing is at risk (exit 0)", code == 0 and "0 not filed" in out)
        (root / "business/docs/demo-project/papers/src/stray.pdf").write_bytes(b"stray")
        code, out, _ = run(["status"], ps2, env)
        check("status: an unlisted file under the root -> exit 1", code == 1 and "unlisted: business/docs/demo-project/papers/src/stray.pdf" in out)
        (root / "business/docs/demo-project/papers/src/stray.pdf").unlink()
        code, out, err = run(["status"], ps2, {})
        check("status: with no root, the work tree is still checked and the root is a warning",
              code == 0 and "were not checked" in err)
        prs = project({ONE: {"DATA_STORE": "repo"}})
        (prs / "papers/src/local.pdf").write_bytes(b"local")
        code, out, _ = run(["status"], prs, {})
        check("status: under repo, an ignored binary is 'local only', exit 0", code == 0 and "local only: papers/src/local.pdf" in out)

        # ── pull ──
        (ps2 / "papers/src/lost.pdf").unlink()
        code, out, _ = run(["pull"], ps2, env)
        check("pull: copies a listed file back into the work tree, verified",
              code == 0 and (ps2 / "papers/src/lost.pdf").read_bytes() == b"dropped in")
        (ps2 / "papers/src/lost.pdf").write_bytes(b"edited here")
        code, out, _ = run(["pull"], ps2, env)
        check("pull: never replaces a different work-tree file (exit 1)",
              code == 1 and "differs: papers/src/lost.pdf" in out and (ps2 / "papers/src/lost.pdf").read_bytes() == b"edited here")
        (ps2 / "papers/src/lost.pdf").unlink()
        filed = root / "business/docs/demo-project/papers/src/lost.pdf"
        filed.write_bytes(b"changed under the root")
        code, out, _ = run(["pull"], ps2, env)
        check("pull: a file changed under the root is not copied (exit 1)",
              code == 1 and "changed: papers/src/lost.pdf" in out and not (ps2 / "papers/src/lost.pdf").exists())
        filed.write_bytes(b"dropped in")
        STAT = fake_stat({str(filed)})
        code, out, err = run(["pull", "papers/*"], ps2, env)
        check("pull: says once, before the first online-only file, that reading it downloads it",
              code == 0 and err.count("online only") == 1)
        STAT = os.stat

        # ── plan ──
        root, env = own_root("root-plan")
        pp = project({ONE: EXTERNAL})
        (pp / "notes/src/deed-signed.pdf").write_bytes(b"signed deed")
        (pp / "notes/src/memo.pdf").write_bytes(b"issued memo")
        (pp / "notes/src/memo.md").write_text("# memo\n", encoding="utf-8")
        (pp / "notes/src/scan.pdf").write_bytes(b"a scan")
        (pp / "notes/src/scan.pdf.reading.md").write_text("reading\n", encoding="utf-8")
        (pp / "notes/src/photo.png").write_bytes(b"png")
        (pp / "notes/src/misc.zip").write_bytes(b"zip")
        (pp / "notes/src/clash.pdf").write_bytes(b"mine")
        git(pp, "add", "-A")
        taken = root / "business/docs/demo-project/notes/src/clash.pdf"
        taken.parent.mkdir(parents=True, exist_ok=True)
        taken.write_bytes(b"theirs")
        code, out, _ = run(["plan"], pp, env)
        check("plan: lists each tracked binary with its destination and proposed role",
              "plan: notes/src/deed-signed.pdf -> " in out and "(role signed," in out
              and "(role ingested," in out and "(role asset," in out and "(role archive," in out)
        check("plan: a PDF beside a source with no proof of the house build is role ?, with why and what to do",
              "plan: notes/src/memo.pdf -> " in out and "(role ?, beside notes/src/memo.md: its source is at status 'none'" in out
              and "choose its role and file it with add --role" in out and "role issued" not in out)
        check("plan: an existing target with other bytes is a conflict (exit 1)",
              code == 1 and "conflict: notes/src/clash.pdf" in out and "with other bytes" in out)
        taken.unlink()
        code, out, _ = run(["plan", "--copy"], pp, env)
        prow = tomllib.loads((pp / "notes/src" / MANIFEST).read_text(encoding="utf-8"))["file"]
        listed_now = subprocess.run(["git", "ls-files"], cwd=pp, capture_output=True, text=True, check=False).stdout
        check("plan --copy: files every one with a role, copy only, and never a role ? row (exit 1)",
              code == 1 and len(prow) == 5 and "notes/src/memo.pdf" not in [r["path"] for r in prow]
              and "plan: 5 to file, 1 need a role," in out
              and (root / "business/photos/demo-project/notes/src/photo.png").is_file()
              and not (root / "business/docs/demo-project/notes/src/memo.pdf").exists())
        check("plan --copy: nothing is untracked or moved", "notes/src/memo.pdf" in listed_now and (pp / "notes/src/memo.pdf").is_file())
        code, out, _ = run(["plan"], pp, env)
        check("plan: a second run finds them filed, and still names the one that needs a role",
              code == 1 and "5 filed already" in out and "1 need a role" in out)

        # plan proposes issued only on evidence (the house producer, an issuing status, no
        # signature, not committed before its source), and signed or received from whole words.
        def pdf(producer=b"", extra=b"", objstm=False):
            info = b"<< /Producer " + producer + b" >>" if producer else b"<< >>"
            if objstm:
                import zlib
                packed = zlib.compress(b"2 0 " + info)
                body = (b"5 0 obj\n<< /Type /ObjStm /N 1 /First 4 /Filter /FlateDecode /Length "
                        + str(len(packed)).encode() + b" >>\nstream\n" + packed + b"\nendstream\nendobj\n")
            else:
                body = b"2 0 obj\n" + info + b"\nendobj\n"
            return b"%PDF-1.7\n" + body + extra + b"%%EOF\n"
        house = b"(xdvipdfmx \\(2025\\))"
        final_md, final_tex = "---\ntitle: x\nstatus: final # issued\n---\nbody\n", "% status: final\n\\begin{document}\n"
        root, env = own_root("root-plan-proof")
        pq = project({ONE: EXTERNAL})
        cases = {
            "house.pdf": (pdf(house), "house.md", final_md),
            "packed.pdf": (pdf(house, objstm=True), "packed.tex", final_tex),
            "wide.pdf": (pdf(b"<FEFF" + "xdvipdfmx".encode("utf-16-be").hex().encode() + b">"), "wide.tex", final_tex),
            "scanner.pdf": (pdf(b"(Canon iR-ADV C5535)"), "scanner.md", final_md),
            "drafted.pdf": (pdf(house), "drafted.md", "---\nstatus: 'draft'\n---\n"),
            "approved.pdf": (pdf(house), "approved.tex", "% status: approved\n"),
            "sealed.pdf": (pdf(house, b"7 0 obj\n<< /Type /Sig /Filter /Adobe.PPKLite /ByteRange [0 10 20 30] >>\nendobj\n"),
                           "sealed.md", final_md),
            "contract-countersigned.pdf": (pdf(), "contract-countersigned.md", final_md),
            "acme-receipt-2026-03.pdf": (pdf(), "acme-receipt-2026-03.md", final_md),
            "receipt-2026-001.pdf": (pdf(house), "receipt-2026-001.tex", final_tex),
            "receipt-2026-002.pdf": (pdf(house), "receipt-2026-002.tex", "% status: draft\n"),
            "seal-untyped.pdf": (pdf(house, b"7 0 obj\n<< /Filter /Adobe.PPKLite /SubFilter /adbe.pkcs7.detached "
                                       b"/ByteRange [0 10 20 30] /Contents <00> >>\nendobj\n"), "seal-untyped.md", final_md),
            "unclosed.pdf": (pdf(b"(" + b"x" * 64) + b"/Producer (" * 4000, "unclosed.md", final_md),
            "statement-of-work-acme.pdf": (pdf(), "statement-of-work-acme.md", final_md),
            "designer-brief.pdf": (pdf(), "designer-brief.md", final_md),
            "letter.docx": (b"PK docx", "letter.md", final_md),
            "signed-nda.pdf": (pdf(), None, None),
        }
        for name, (data, source, text) in cases.items():
            (pq / "notes/src" / name).write_bytes(data)
            if source:
                (pq / "notes/src" / source).write_text(text, encoding="utf-8")
        git(pq, "add", "-A")

        def role_of(out, name):
            line = next((x for x in out.splitlines() if x.startswith(f"plan: notes/src/{name} -> ")), "")
            m = re.search(r"\(role (\S+?)[,)]", line)
            return m.group(1) if m else None
        code, out, _ = run(["plan"], pq, env)
        want = {"house.pdf": "issued", "packed.pdf": "issued", "wide.pdf": "issued", "scanner.pdf": "?",
                "drafted.pdf": "?", "approved.pdf": "?", "sealed.pdf": "signed", "contract-countersigned.pdf": "signed",
                "acme-receipt-2026-03.pdf": "received", "receipt-2026-001.pdf": "issued", "receipt-2026-002.pdf": "?",
                "seal-untyped.pdf": "signed", "unclosed.pdf": "?",
                "statement-of-work-acme.pdf": "?", "designer-brief.pdf": "?", "letter.docx": "?", "signed-nda.pdf": "signed"}
        got = {name: role_of(out, name) for name in want}
        check("plan: issued only for the house build at an issuing status; a signature or a whole word of the "
              "name makes it signed or received; the rest are role ? (exit 1)",
              code == 1 and got == want and "(role issued, source notes/src/house.md," in out
              and "its producer is 'Canon iR-ADV C5535', not the house build" in out
              and "its source is at status 'draft', and only final issues" in out
              and "beside notes/src/letter.md: a Word copy beside its source cannot be shown" in out
              and "plan: 9 to file, 8 need a role," in out)
        code, out, _ = run(["plan", "--issue-statuses", "final approved"], pq, env)
        check("plan --issue-statuses: a source at another issuing status proves the house build issued",
              role_of(out, "approved.pdf") == "issued" and role_of(out, "drafted.pdf") == "?")
        code, out, _ = run(["plan", "--copy"], pq, env)
        qrow = {r["path"]: r["role"] for r in tomllib.loads((pq / "notes/src" / MANIFEST).read_text(encoding="utf-8"))["file"]}
        check("plan --copy: files the rows with a role and none without, reports them and exits 1",
              code == 1 and len(qrow) == 9 and qrow["notes/src/house.pdf"] == "issued"
              and qrow["notes/src/sealed.pdf"] == "signed" and "notes/src/scanner.pdf" not in qrow
              and "plan: 9 to file, 8 need a role," in out and "copied 9, 0 failed" in out)
        pr = project({ONE: EXTERNAL})
        (pr / "notes/src/early.pdf").write_bytes(pdf(house))
        git(pr, "add", "-A")
        dated = dict(os.environ, GIT_AUTHOR_DATE="2026-01-01T00:00:00Z", GIT_COMMITTER_DATE="2026-01-01T00:00:00Z")
        subprocess.run(["git", "-c", "user.name=Self Test", "-c", "user.email=test@example.com", "commit", "-q", "-m", "pdf"],
                       cwd=pr, check=True, capture_output=True, env=dated)
        (pr / "notes/src/early.md").write_text(final_md, encoding="utf-8")
        git(pr, "add", "-A")
        git(pr, "-c", "user.name=Self Test", "-c", "user.email=test@example.com", "commit", "-q", "-m", "source")
        code, out, _ = run(["plan"], pr, env)
        check("plan: a house-built PDF Git held before its source is role ?",
              code == 1 and role_of(out, "early.pdf") == "?" and "Git held it before its source" in out)

        # ── The guard as the seed's hook command runs it ──
        if shutil.which("bash"):
            hook = project({ONE: EXTERNAL})
            (hook / ".claude" / f"{ONE}-dataroot.py").write_bytes(Path(__file__).read_bytes())
            (hook / "sub").mkdir()
            call = json.dumps({"tool_name": "Write", "tool_input": {"file_path": str(root / "x.pdf")}})

            def seed(cwd, text):
                return subprocess.run(["bash", "-c", SEED_GUARD], cwd=cwd, input=text, capture_output=True, text=True, check=False,
                                      env=dict(os.environ, PATH=os.path.dirname(sys.executable) + os.pathsep + os.environ.get("PATH", "")))
            r = seed(hook / "sub", call)
            check("the seed's hook command, from a sub-folder: a write under the root exits 2 with one line",
                  r.returncode == 2 and r.stderr == GUARD_BLOCK + "\n")
            r = seed(hook / "sub", json.dumps({"tool_name": "Write", "tool_input": {"file_path": str(hook / "a.md")}}))
            check("the seed's hook command: a write in the project exits 0", r.returncode == 0)
            nowhere = base / "no-work-tree"
            nowhere.mkdir()
            check("the seed's hook command outside a work tree exits 0", seed(nowhere, call).returncode == 0)
            bare_repo = project({ONE: EXTERNAL})
            check("the seed's hook command with no resolver exits 0", seed(bare_repo, call).returncode == 0)
    else:
        check("git is not installed: the status, pull and plan cases are skipped", True)

    # ── The guard ──
    root, env = base / "root", {ROOT_ENV: str(base / "root")}

    def judge(tool, field, target, environ=None, project_dir=None, extra=None):
        data = {"tool_name": tool, "tool_input": {field: target}}
        data.update(extra or {})
        return guard(json.dumps(data), environ or {}, str(project_dir or p))

    check("guard: Write under the root (by the variable) -> 2", judge("Write", "file_path", str(root / "a.pdf"), env) == (2, GUARD_BLOCK))
    check("guard: Edit under the root, the variable unset, found by its marker -> 2",
          judge("Edit", "file_path", str(dest))[0] == 2)
    check("guard: MultiEdit under the root -> 2", judge("MultiEdit", "file_path", str(dest))[0] == 2)
    check("guard: NotebookEdit's notebook_path under the root -> 2", judge("NotebookEdit", "notebook_path", str(root / "n.ipynb"))[0] == 2)
    check("guard: Grep at the root itself -> 2", judge("Grep", "path", str(root))[0] == 2)
    check("guard: Glob under the root -> 2", judge("Glob", "path", str(root / "business"))[0] == 2)
    check("guard: Glob with an absolute pattern under the root and no path -> 2",
          judge("Glob", "pattern", str(root / "business" / "**" / "*.pdf"))[0] == 2)
    check("guard: Glob with an absolute pattern under the root and a path in the project -> 2 (the client searches the pattern's folder)",
          guard(json.dumps({"tool_name": "Glob", "tool_input": {"pattern": str(root) + "/*.pdf", "path": str(p)}}), {}, str(p))[0] == 2)
    check("guard: Glob with a relative pattern and a path in the project -> 0",
          guard(json.dumps({"tool_name": "Glob", "tool_input": {"pattern": "**/*.pdf", "path": str(p)}}), env, str(p))[0] == 0)
    check("guard: glob_base takes the folder before the first wildcard",
          glob_base("/a/b/**/*.pdf") == "/a/b" and glob_base("/a/b/c.pdf") == "/a/b" and glob_base("/*.pdf") == "/"
          and glob_base("/a/b*/c") == "/a")
    check("guard: Read under the root is allowed -> 0", judge("Read", "file_path", str(dest))[0] == 0)
    check("guard: a write in the project -> 0", judge("Write", "file_path", str(p / "notes.md"), env)[0] == 0)
    check("guard: Grep with no path (the working folder) -> 0", guard(json.dumps({"tool_name": "Grep", "tool_input": {"pattern": "x"}}), env, str(p))[0] == 0)
    check("guard: a relative path is taken from the hook's cwd",
          judge("Write", "file_path", "business/new.pdf", extra={"cwd": str(root)})[0] == 2)
    try:
        os.symlink(str(root / "business"), str(p / "link-into-root"))
        linked = judge("Edit", "file_path", str(p / "link-into-root" / "docs" / "x.pdf"))[0] == 2
    except (OSError, NotImplementedError):
        linked = True
    check("guard: a symbolic link into the root -> 2", linked)
    for text in ("not json", "[1, 2]", '{"tool_name": "Write"}', '{"tool_name": "Write", "tool_input": {"file_path": 7}}',
                 '{"tool_name": ["Write"], "tool_input": {}}', ""):
        check(f"guard: bad input {text[:28]!r} -> 0", guard(text, env, str(p))[0] == 0)
    check("guard: a set variable without a marker protects nothing by itself",
          judge("Write", "file_path", str(bare / "a.pdf"), {ROOT_ENV: str(bare)})[0] == 0)
    marked = base / "marked"
    inner = marked / "repo"
    inner.mkdir(parents=True)
    (marked / MARKER).write_text("", encoding="utf-8")
    check("guard: a repository under a marked root is told so, not given the filing advice",
          judge("Edit", "file_path", str(inner / "a.md"), project_dir=inner) == (2, GUARD_INSIDE))
    stdin = sys.stdin

    class Broken:
        def read(self):
            raise OSError("no stdin")

    sys.stdin = Broken()
    try:
        failed_open = guard_main() == 0
    finally:
        sys.stdin = stdin
    check("guard: an error of its own fails open -> 0", failed_open)

    # The guard and the data commands on an older Python, run as the hook and a person run them.
    older = (PYTHON_MIN[0], PYTHON_MIN[1] - 1)

    def older_python(argv, text, cwd):
        code = ("import runpy, sys; sys.version_info = %r; sys.argv = [%r] + %r; "
                "runpy.run_path(sys.argv[0], run_name='__main__')" % (older + (0, "final", 0), str(Path(__file__)), argv))
        return subprocess.run([sys.executable, "-I", "-c", code], input=text, capture_output=True, text=True, check=False,
                              cwd=str(cwd), env=dict(os.environ, **{ROOT_ENV: str(root)}))
    r = older_python(["guard"], json.dumps({"tool_name": "Write", "tool_input": {"file_path": str(root / "a.pdf")}}), p)
    check("older Python: the guard lets a write under the root through (0) with the warning JSON on stdout",
          r.returncode == 0 and r.stderr == "" and r.stdout == too_old_hook(older) + "\n")
    for argv in (["root"], ["--self-test"], []):
        r = older_python(argv, "", p)
        check(f"older Python: {' '.join(argv) or 'no subcommand'} exits 2 with the framed message alone, on stderr",
              r.returncode == 2 and r.stdout == "" and r.stderr == too_old_text(argv[0] if argv else "", older))
    r = older_python(["--help"], "", p)
    check("older Python: --help still prints the docstring", r.returncode == 0 and "PYTHON_MIN" in r.stdout and r.stderr == "")

    # The guard and the data commands on an interpreter without tomllib (a stripped build: every
    # Python the version check lets through ships it).
    def blocked_tomllib(argv, text, cwd):
        code = ("import runpy, sys; sys.modules['tomllib'] = None; "
                f"sys.argv = [{str(Path(__file__))!r}] + {argv!r}; runpy.run_path(sys.argv[0], run_name='__main__')")
        return subprocess.run([sys.executable, "-I", "-c", code], input=text, capture_output=True, text=True, check=False,
                              cwd=str(cwd), env=dict(os.environ, **{ROOT_ENV: str(root)}))
    r = blocked_tomllib(["guard"], json.dumps({"tool_name": "Write", "tool_input": {"file_path": str(root / "a.pdf")}}), p)
    check("no tomllib: guard still blocks under a root (2)", r.returncode == 2 and r.stderr == GUARD_BLOCK + "\n")
    r = blocked_tomllib(["guard"], json.dumps({"tool_name": "Write", "tool_input": {"file_path": str(p / "a.md")}}), p)
    check("no tomllib: guard still passes elsewhere (0)", r.returncode == 0 and r.stderr == "")
    r = blocked_tomllib(["root"], "", p)
    check("no tomllib: a data command exits 2 with its one line", r.returncode == 2 and r.stderr == NEED_PYTHON + "\n")

    # ── check-names ──
    pk = project({ONE: EXTERNAL})
    (pk / "notes/src/foo.pdf").write_bytes(b"f")
    for name in ("a:b.pdf", "CON.pdf", "x."):
        code, out, _ = run(["check-names", f"notes/src/{name}"], pk, env)
        check(f"check-names: {name} -> exit 1", code == 1 and "unsafe:" in out)
    code, out, _ = run(["check-names", "notes/src/Foo.pdf"], pk, env)
    check("check-names: Foo.pdf beside foo.pdf -> exit 1", code == 1 and "differ only in case" in out)
    code, out, _ = run(["check-names", "notes/src/fine.pdf"], pk, env)
    check("check-names: a safe name -> exit 0", code == 0)
    code, out, _ = run(["check-names", "notes/src/desktop.ini"], pk, env)
    check("check-names: OneDrive's names pass under another provider", code == 0)
    (pk / f".copier-answers.{ONE}.yml").write_text(answers_text(dict(EXTERNAL, DATA_PROVIDER="onedrive")), encoding="utf-8")
    code, out, _ = run(["check-names", "notes/src/desktop.ini"], pk, env)
    check("check-names: under onedrive, desktop.ini is refused", code == 1 and "OneDrive" in out)
    code, out, err = run(["check-names", "notes/src/" + "x" * 240 + ".pdf"], pk, env)
    check("check-names: a path over 260 characters under the root warns", code == 0 and "over Windows' 260" in err)
    code, out, _ = run(["check-names"], pk, env)
    check("check-names with no path: the filing folders' files", code == 0 and "checked" in out)

    self_test_role_rules(check, base, json, tomllib, project, run, own_root, git, has_git)

    # ── Outside a work tree: the project is the folder holding an answers file ──
    pg = project({ONE: EXTERNAL}, use_git=False)
    (pg / "deep/er").mkdir(parents=True)
    code, out, _ = run(["path", "notes/src/a.pdf"], pg / "deep/er", env)
    check("outside a work tree: the nearest folder holding an answers file is the project",
          code == 0 and "notes" in out)
    lonely = base / "lonely"
    lonely.mkdir()
    code, _, err = run(["root"], lonely, env)
    check("no project at all -> exit 2", code == 2 and "no project here" in err)


def self_test_role_rules(check, base, json, tomllib, project, run, own_root, git, has_git):
    """The manifest's role rules: evidence, unknown keys, maps and manifests that cannot be read,
    roles two maps define, "repo": "skip", "rows": "none", stray files, HEAD and orphans."""

    def rows_of(proj, folder):
        path = proj / folder / MANIFEST
        return tomllib.loads(path.read_text(encoding="utf-8"))["file"] if path.exists() else []

    def write_map(proj, template, data):
        (proj / ".claude" / f"{template}-dataroot.json").write_text(
            data if isinstance(data, str) else json.dumps(data), encoding="utf-8")

    def commit(cwd, message):
        git(cwd, "add", "-A")
        git(cwd, "-c", "user.name=Self Test", "-c", "user.email=test@example.com", "commit", "-q", "-m", message)

    # ── Evidence: recorded at filing, honoured by --force ──
    pe = project({ONE: EXTERNAL}, {ONE: MAP_ONE, TWO: MAP_TWO})
    root_e, env_e = own_root("root-evidence")
    mirror_e = root_e / "business/docs/demo-project/notes/src"
    for role, evidence in (("signed", True), ("evidence", True), ("ingested", True), ("received", True),
                           ("take", True), ("issued", False), ("archive", False), ("asset", False),
                           ("generated", False), ("brand-export", False)):
        work = pe / f"notes/src/r-{role}.pdf"
        work.write_bytes(b"first " + role.encode())
        code, _, _ = run(["add", f"notes/src/r-{role}.pdf", "--role", role], pe, env_e)
        row = (rows_of(pe, "notes/src") or [{}])[-1]
        work.write_bytes(b"second " + role.encode())
        before = (pe / "notes/src" / MANIFEST).read_bytes()
        forced, _, err = run(["add", f"notes/src/r-{role}.pdf", "--role", role, "--force"], pe, env_e)
        if evidence:
            honoured = (forced == 2 and "own name" in err and (pe / "notes/src" / MANIFEST).read_bytes() == before
                        and (mirror_e / f"r-{role}.pdf").read_bytes() == b"first " + role.encode())
        else:
            honoured = forced == 0 and (mirror_e / f"r-{role}.pdf").read_bytes() == b"second " + role.encode()
        check(f"evidence: a row of the role '{role}' records evidence = {'true' if evidence else 'false'}, and add --force "
              f"{'refuses it, the filed copy and the manifest unchanged' if evidence else 'supersedes it'}",
              code == 0 and row.get("role") == role and row.get("evidence") is evidence and honoured)
    write_map(pe, TWO, dict(MAP_TWO, roles=[{"name": "take", "evidence": False}, {"name": "brand-export", "evidence": False}]))
    code, _, err = run(["add", "notes/src/r-take.pdf", "--role", "take", "--force"], pe, env_e)
    check("evidence: a row filed as evidence stays protected when its map later says otherwise",
          code == 2 and "evidence = true" in err)
    write_map(pe, TWO, dict(MAP_TWO, roles=[{"name": "take", "evidence": False}, {"name": "brand-export", "evidence": True}]))
    code, _, err = run(["add", "notes/src/r-brand-export.pdf", "--role", "brand-export", "--force"], pe, env_e)
    check("evidence: a row is protected where the present definition says so, whatever its own flag",
          code == 2 and "the role 'brand-export' is evidence" in err)
    (pe / ".claude" / f"{TWO}-dataroot.json").unlink()
    code, _, err = run(["add", "notes/src/r-brand-export.pdf", "--role", "archive", "--force"], pe, env_e)
    check("evidence: a row whose role no map here defines is reported and treated as evidence",
          code == 2 and "no map here defines the role 'brand-export'" in err and "treated as evidence" in err)

    # ── Unknown keys: on a map, its folder and role entries, and a row, kept and ignored ──
    later_map = dict(MAP_ONE, later={"x": 1}, folders=[dict(e, later=True) for e in MAP_ONE["folders"]],
                     roles=[{"name": "brand-export", "evidence": False, "later": [1]}])
    pu = project({ONE: EXTERNAL}, {ONE: later_map})
    _, env_u = own_root("root-keys")
    (pu / "notes/src/k.pdf").write_bytes(b"k one")
    code_a, _, _ = run(["add", "notes/src/k.pdf", "--role", "brand-export"], pu, env_u)
    man = pu / "notes/src" / MANIFEST
    text = man.read_text(encoding="utf-8").replace("format = 1\n", 'format = 1\nlater = "kept"\n', 1).replace(
        'notes = ""\n', 'notes = ""\nfootage_id = "x-1"   # a later key\nrights = { holder = "Ada", until = 2030 }\n', 1)
    man.write_text(text, encoding="utf-8")
    code_v, _, _ = run(["verify"], pu, env_u)
    (pu / "notes/src/k.pdf").write_bytes(b"k two")
    code, _, _ = run(["add", "notes/src/k.pdf", "--role", "brand-export", "--force"], pu, env_u)
    new = man.read_text(encoding="utf-8")
    check("unknown keys: a map's, a folder entry's and a role entry's are ignored, and verify passes with a row's",
          code_a == 0 and code_v == 0)
    check("unknown keys: a row's are kept byte for byte through a supersede, only its state value changed",
          code == 0 and new.startswith(text.replace('state = "current"', 'state = "superseded"', 1))
          and tomllib.loads(new)["file"][0]["footage_id"] == "x-1" and len(tomllib.loads(new)["file"]) == 2)

    # ── A map or manifest that cannot be read refuses only what touches its folders ──
    root_b, env_b = own_root("root-broken")
    pb = project({ONE: EXTERNAL}, {ONE: MAP_ONE, TWO: dict(MAP_TWO, format=2)})
    (pb / "notes/src/n.pdf").write_bytes(b"n")
    (pb / "footage/src/t.mov").write_bytes(b"t")
    code_a, _, err_a = run(["add", "notes/src/n.pdf", "--role", "archive"], pb, env_b)
    code_p, _, _ = run(["path", "papers/src/a.pdf"], pb, env_b)
    code_f, _, err_f = run(["add", "footage/src/t.mov", "--role", "archive"], pb, env_b)
    check("maps: a sibling's newer map is reported, and this map's add and path still run (exit 0)",
          code_a == 0 and code_p == 0 and "cannot be read" in err_a and "newer template" in err_a)
    check("maps: a command that touches the newer map's folder refuses (exit 2), nothing written",
          code_f == 2 and "footage/src is named by" in err_f and not (root_b / "business/videos").exists())
    stray = root_b / "business/videos/demo-project/footage/src/u.mov"
    stray.parent.mkdir(parents=True)
    stray.write_bytes(b"u")
    code, out, err = run(["verify"], pb, env_b)
    check("verify: with a newer sibling map, this map's rows verify, its folder is left alone (exit 2) and its files "
          "are never called unlisted", code == 2 and "verified 1," in out and "verify leaves footage/src alone" in err
          and "unlisted: " not in out and "not judged" in err)
    code, out, _ = run(["verify", "notes/*"], pb, env_b)
    check("verify GLOB: a GLOB that cannot touch the unreadable map's folder exits 0", code == 0 and "verified 1," in out)
    code, _, err = run(["status"], pb, env_b)
    check("status: the newer map's folder is left alone (exit 2), never a blanket refusal",
          code == 2 and "status leaves footage/src alone" in err and err.count("refused:") == 1)
    write_map(pb, TWO, "{not json")
    code, out, err = run(["verify"], pb, env_b)
    check("verify: an unparseable sibling map is reported; this map's rows verify, and files its folders may "
          "hold are not judged (exit 0)", code == 0 and "cannot be read" in err and "not judged" in err and "unlisted: " not in out)
    write_map(pb, TWO, dict(MAP_TWO, roles=[{"name": "docs", "evidence": True}]))
    code_f, _, err_f = run(["add", "footage/src/t.mov", "--role", "archive"], pb, env_b)
    code_p, _, _ = run(["path", "notes/src/n.pdf"], pb, env_b)
    check("maps: an invalid sibling map (a role named after a kind) refuses only its own folder",
          code_f == 2 and "kind's name" in err_f and code_p == 0)
    write_map(pb, TWO, MAP_TWO)
    (pb / "footage/src" / MANIFEST).write_text("format = 2\n", encoding="utf-8")
    stray.unlink()
    (pb / "notes/src/m.pdf").write_bytes(b"m")
    code_a, _, _ = run(["add", "notes/src/m.pdf", "--role", "archive"], pb, env_b)
    code_f, _, err_f = run(["add", "footage/src/t.mov", "--role", "take"], pb, env_b)
    code, out, err = run(["verify"], pb, env_b)
    check("manifests: a newer manifest in another map's folder refuses only that folder; add and verify of "
          "the others run", code_a == 0 and code_f == 2 and "newer template" in err_f and code == 2
          and "verified 2," in out and "verify leaves footage/src alone" in err)
    pm = project({ONE: EXTERNAL}, {ONE: MAP_ONE, TWO: {"format": 1, "folders": [{"path": "papers/src"}]}})
    _, env_m = own_root("root-clash")
    code, out, err = run(["verify"], pm, env_m)
    check("verify: a folder two maps claim is left alone (exit 2) while the others verify",
          code == 2 and "verify leaves papers/src alone" in err and "claim one folder" in err and "verified 0," in out)

    # ── Roles two maps define differently: evidence wins, status warns, nothing refuses ──
    pd = project({ONE: EXTERNAL}, {ONE: dict(MAP_ONE, roles=[{"name": "take", "evidence": False, "repo": "skip"}]),
                                   TWO: MAP_TWO})
    _, env_d = own_root("root-differ")
    code, _, err = run(["status"], pd, env_d)
    check("roles: two maps defining one role differently: status warns, evidence wins, nothing refuses",
          code == 0 and "define the role 'take' differently" in err and "evidence wins" in err and "refused:" not in err)
    (pd / "notes/src/d.wav").write_bytes(b"d")
    code, _, _ = run(["add", "notes/src/d.wav", "--role", "take"], pd, env_d)
    check("roles: a role two maps define differently is filed as evidence",
          code == 0 and rows_of(pd, "notes/src")[-1]["evidence"] is True)

    # ── "repo": "skip" under repo ──
    pk = project({ONE: {"DATA_STORE": "repo"}}, {ONE: MAP_ONE, TWO: MAP_TWO})
    (pk / "footage/src/take.wav").write_bytes(b"take")
    code, out, _ = run(["add", "footage/src/take.wav", "--role", "take"], pk, {})
    code2, _, err2 = run(["add", "footage/src/take.wav", "--role", "brand-export"], pk, {})
    check('repo: a map role with "repo": "skip" exits 0 and writes nothing',
          code == 0 and out.startswith("not filed: ") and not (pk / "footage/src" / MANIFEST).exists())
    check("repo: a map role without it still says to commit the file (exit 2)",
          code2 == 2 and "commit the file instead" in err2)
    # add --role generated under repo with the root unset: its shortcut needs no root.
    (pk / "sounds/src/g.mp3").write_bytes(b"ID3 generated")

    def work_tree(proj):
        return {str(x.relative_to(proj)): (x.read_bytes() if x.is_file() and not x.is_symlink() else None)
                for x in proj.rglob("*") if ".git" not in x.relative_to(proj).parts}
    before = work_tree(pk)
    code, out, err = run(["add", "sounds/src/g.mp3", "--role", "generated"], pk, {})
    check("repo: add --role generated with the root unset exits 0, writes nothing and says 'not filed:'",
          code == 0 and out.startswith("not filed: ") and "refused:" not in err and work_tree(pk) == before
          and not (pk / "sounds/src" / MANIFEST).exists())
    write_map(pk, ONE, dict(MAP_ONE, roles=[{"name": "take", "evidence": True}]))
    code, _, err = run(["add", "footage/src/take.wav", "--role", "take"], pk, {})
    check("repo: a role one map skips and another does not is not skipped (exit 2)",
          code == 2 and "commit the file instead" in err)

    # ── "rows": "none" and stray files under the root ──
    pw = project({ONE: EXTERNAL}, {ONE: dict(MAP_ONE, folders=MAP_ONE["folders"] + [{"path": "pictures/renders", "rows": "none"}])})
    root_w, env_w = own_root("root-working")
    (pw / "pictures/renders").mkdir()
    (pw / "pictures/renders/.gitignore").write_text("*.png\n", encoding="utf-8")
    (pw / "pictures/renders/r.png").write_bytes(b"r" * 2048)
    code, _, err = run(["add", "pictures/renders/r.png", "--role", "asset"], pw, env_w)
    check('add: a folder marked "rows": "none" never takes a row (exit 2), nothing written',
          code == 2 and "working output" in err and not (pw / "pictures/renders" / MANIFEST).exists()
          and not (root_w / "business").exists())
    held = root_w / "business/photos/demo-project/pictures/renders/r.png"
    held.parent.mkdir(parents=True)
    held.write_bytes(b"r")
    code_v, out_v, err_v = run(["verify"], pw, env_w)
    code_s, out_s, err_s = run(["status"], pw, env_w)
    check('verify and status: files under a "rows": "none" folder, in the work tree or under the root, are never listed',
          code_v == 0 and code_s == 0 and "renders" not in out_v + err_v + out_s + err_s)
    stray = root_w / "business/docs/demo-project/elsewhere/x.pdf"
    stray.parent.mkdir(parents=True)
    stray.write_bytes(b"x")
    code_v, out_v, _ = run(["verify"], pw, env_w)
    code_s, out_s, _ = run(["status"], pw, env_w)
    check("verify and status: a file under the project's folders of the root outside every map folder is reported (exit 1)",
          code_v == 1 and code_s == 1 and "unlisted: business/docs/demo-project/elsewhere/x.pdf (outside every map folder" in out_v
          and "unlisted: business/docs/demo-project/elsewhere/x.pdf" in out_s)
    stray.unlink()
    if not has_git:
        check("git is not installed: the HEAD and orphaned-manifest cases are skipped", True)
        return
    git(pw, "add", "-f", "pictures/renders/r.png")
    code, out, _ = run(["plan"], pw, env_w)
    check('plan: a tracked binary in a "rows": "none" folder is never proposed', code == 0 and "renders" not in out)
    (pw / "pictures/renders" / MANIFEST).write_text("format = 1\n", encoding="utf-8")
    git(pw, "add", "-f", "pictures/renders/" + MANIFEST)
    code, out, _ = run(["verify"], pw, env_w)
    check('verify: a tracked external.toml in a "rows": "none" folder -> exit 1, orphaned',
          code == 1 and "orphaned: pictures/renders/external.toml" in out)

    # ── verify against HEAD: rows are appended, and only a state changes ──
    ph = project({ONE: EXTERNAL})
    _, env_h = own_root("root-head")
    for name in ("h1", "h2"):
        (ph / f"notes/src/{name}.pdf").write_bytes(name.encode())
        run(["add", f"notes/src/{name}.pdf", "--role", "archive"], ph, env_h)
    commit(ph, "filed")
    man = ph / "notes/src" / MANIFEST
    good = [man.read_bytes()]

    def edited(old, new):
        man.write_bytes(good[0].replace(old, new, 1))
        result = run(["verify"], ph, env_h)
        man.write_bytes(good[0])
        return result

    code, out, _ = run(["verify"], ph, env_h)
    check("verify: rows as committed at HEAD -> exit 0", code == 0 and "committed rows removed or changed 0" in out)
    code, out, _ = edited(b'label = ""', b'label = "edited"')
    check("verify: a committed row edited by hand -> exit 1, naming the row and the field",
          code == 1 and "row 1 (notes/src/h1.pdf) differs from HEAD in label" in out)
    code, out, _ = edited(b'path = "notes/src/h1.pdf"', b'path = "notes/src/h1.superseded-16-10-2026.pdf"')
    check("verify: a committed row's path rewritten in place -> exit 1", code == 1 and "differs from HEAD in path" in out)
    code, out, _ = edited(b'state = "current"', b'state = "withdrawn"')
    check("verify: the one allowed change, a state from current to withdrawn -> exit 0", code == 0)
    man.write_bytes(good[0][:good[0].rindex(b"[[file]]")])
    code, out, _ = run(["verify"], ph, env_h)
    check("verify: a committed row removed -> exit 1", code == 1 and "row 2 (notes/src/h2.pdf) is committed at HEAD but gone" in out)
    man.unlink()
    code, out, _ = run(["verify"], ph, env_h)
    check("verify: the committed manifest deleted -> exit 1, every committed row gone",
          code == 1 and out.count("gone from the work tree") == 2)
    man.write_bytes(good[0])
    (ph / "notes/src/h1.pdf").write_bytes(b"h1 again")
    code_f, _, _ = run(["add", "notes/src/h1.pdf", "--role", "archive", "--force"], ph, env_h)
    code, out, _ = run(["verify"], ph, env_h)
    check("verify: a superseding copy filed after the commit (one state change, one new row) -> exit 0",
          code_f == 0 and code == 0)
    commit(ph, "superseded")
    good[0] = man.read_bytes()
    code, out, _ = edited(b'state = "superseded"', b'state = "current"')
    check("verify: a committed state turned back from superseded to current -> exit 1",
          code == 1 and "differs from HEAD in state" in out)
    code, out, _ = run(["verify", "papers/*"], ph, env_h)
    check("verify GLOB: committed rows outside the GLOB are not compared", code == 0)

    # ── Orphaned manifests: tracked, and named by no present map's folder ──
    orphan = ph / "old/src" / MANIFEST
    orphan.parent.mkdir(parents=True)
    orphan.write_bytes(good[0])
    code, out, _ = run(["verify"], ph, env_h)
    check("verify: an untracked external.toml outside every map folder is not an orphan (exit 0)", code == 0)
    git(ph, "add", "old/src/" + MANIFEST)
    code, out, _ = run(["verify"], ph, env_h)
    check("verify: a tracked external.toml no map's folder names -> exit 1, orphaned",
          code == 1 and "orphaned: old/src/external.toml" in out and "orphaned manifests 1" in out)
    write_map(ph, TWO, "{not json")
    code, out, err = run(["verify"], ph, env_h)
    check("verify: while a map cannot be read, an unnamed manifest is not judged an orphan",
          code == 0 and "not judged as orphaned" in err)


def fake_stat(paths):
    """os.stat, with the given files marked online only (Windows' recall attribute)."""
    class Marked:
        def __init__(self, st):
            self.st = st
            self.st_file_attributes = WIN_RECALL

        def __getattr__(self, name):
            return getattr(self.st, name)

    def stat(path, *args, **kwargs):
        st = os.stat(path, *args, **kwargs)
        return Marked(st) if str(path) in paths else st
    return stat


if __name__ == "__main__":
    sys.exit(main())
