#!/usr/bin/env python3
"""Carry the deny and ask rules of .claude/settings.json to the other coding agents.

Claude Code reads its permission rules from .claude/settings.json. Codex, Gemini CLI,
OpenCode and Antigravity each keep their own, in their own format. This script reads
permissions.{allow, ask, deny} from .claude/settings.json and, for each client:

  - prints the plan: every rule it can write, where, and in what form;
  - prints every rule it cannot express there, and why;
  - reports every allow rule as left to the client (an allow is never written: a Codex
    allow, for one, runs the command outside the sandbox);
  - with --write, adds the missing rules to a client file that ALREADY exists, changing
    only that file's permission keys. It never creates a file or a folder, never removes
    or reorders a rule, and never writes outside the project.

Drift is a mapped rule missing from an existing client file, or one a later, less strict
rule overrides: in opencode.json that includes an agent's own rules (agents.<id>.permissions),
which OpenCode applies after the file's, so --write cannot outweigh them and only reports
them. Rules a client file holds beyond the mapped ones belong to the project's owner and are
never flagged or removed. Rules OpenCode reads from outside the project (the user's own
configuration) are beyond what this script can see.

What is written (version 1: deny and ask rules only):

  OpenCode (opencode.json, the V2 'permissions' array; the last matching rule wins;
  resources are relative to the folder OpenCode starts in, the project root, and '*'
  crosses '/'):
    Edit(**/*.ext)    -> {"action": "edit", "resource": "*.ext", "effect": ...}
    Edit(dir/**)      -> {"action": "edit", "resource": "dir/*", ...}
    Edit(**/dir/**)   -> "dir/*" and "*/dir/*"
    mcp__S__T         -> {"action": "S_T", "resource": "*", ...}
    Bash(cmd *)       -> {"action": "shell", "resource": "cmd *", ...} (plain words only)
    AskUserQuestion   -> deferred: whether a deny hides OpenCode's question tool is unverified
  Asks are appended, then denies, after every existing rule, so no broad rule overrides them.

  Codex (.codex/config.toml):
    mcp__S__T ask     -> [mcp_servers.S.tools.T] approval_mode = "prompt", only where the
                         file declares [mcp_servers.S]
    path rules        -> cannot be expressed (a glob rule stops Codex starting)
    AskUserQuestion   -> nothing to write (Codex offers no such tool in Default mode)

  Gemini CLI (.gemini/settings.json):
    AskUserQuestion   -> tools.exclude contains "ask_user"
    mcp__S__T ask     -> tools.confirmationRequired contains "mcp_S_T" (S must hold no '_')
    path rules        -> cannot be expressed in a project file (workspace policies are
                         disabled); a user policy sketch is printed for the owner

  Antigravity: nothing is written; the script prints what to set in the app (a
  'dir/**' rule as write_file(dir), which covers the folder; other globs are reported).

  Gemini CLI warns at every start that tools.exclude is deprecated (0.64.0). It is the
  only project-level way to hide ask_user while workspace policies are disabled, so it
  stays until Gemini CLI removes it.

What Codex and Gemini CLI read takes effect only in a trusted project or folder.

Python 3.11 or later, standard library only, no network.

Usage: python3 .claude/<this file> [--check | --write] [--client NAME]... [--root DIR]
       python3 .claude/<this file> --self-test

Exit codes: 0 = every expressible rule is in place (or written)
            1 = drift: a rule is missing or overridden (--check), or could not be written
            2 = an input could not be read, or bad arguments
"""

from __future__ import annotations

import sys

if sys.version_info < (3, 11):
    sys.stderr.write("This script needs Python 3.11 or later (tomllib).\n")
    sys.exit(2)

import argparse
import contextlib
import io
import json
import os
import re
import tempfile
import tomllib
from pathlib import Path

CLIENTS = ("opencode", "codex", "gemini-cli", "antigravity")
STRICTNESS = {"allow": 0, "ask": 1, "deny": 2}
SHELL_SAFE = re.compile(r"[A-Za-z0-9_./=,+@%-]+")
NAME_SAFE = re.compile(r"[A-Za-z0-9_-]+")
TOML_BARE = re.compile(r"[A-Za-z0-9_-]+")


class Unreadable(Exception):
    """An input file is missing, or is not what its format requires."""


# ── Reading the Claude rules ────────────────────────────────────────────────


def read_rules(root: Path) -> list[tuple[str, str]]:
    """Every (effect, rule) of .claude/settings.json, in file order: deny, ask, allow."""
    path = root / ".claude" / "settings.json"
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise Unreadable(f"{path} does not exist") from None
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as err:
        raise Unreadable(f"{path} is not readable JSON: {err}") from None
    perms = data.get("permissions", {}) if isinstance(data, dict) else None
    if not isinstance(perms, dict):
        raise Unreadable(f"{path}: 'permissions' is not an object")
    rules = []
    for effect in ("deny", "ask", "allow"):
        items = perms.get(effect, [])
        if not isinstance(items, list) or not all(isinstance(i, str) for i in items):
            raise Unreadable(f"{path}: permissions.{effect} is not a list of strings")
        rules.extend((effect, i.strip()) for i in items)
    return rules


def split_rule(rule: str) -> tuple[str, str | None]:
    """'Edit(build/**)' -> ('Edit', 'build/**'); 'AskUserQuestion' -> ('AskUserQuestion', None)."""
    m = re.fullmatch(r"([A-Za-z0-9_-]+)(?:\((.*)\))?", rule, re.S)
    if not m:
        return rule, ""
    return m.group(1), m.group(2)


def mcp_parts(tool: str) -> tuple[str, str] | None:
    """'mcp__server__tool' -> ('server', 'tool'); None for any other name."""
    m = re.fullmatch(r"mcp__(.+?)__(.+)", tool)
    return (m.group(1), m.group(2)) if m else None


def edit_resources(spec: str | None) -> tuple[list[str] | None, str]:
    """A Claude Edit path pattern as OpenCode resources, or (None, why it cannot be exact)."""
    if spec is None or spec in ("**", "*", "**/*"):
        return ["*"], ""
    p = spec
    if p.startswith("//") or p.startswith("~"):
        return None, "an absolute or home path; OpenCode resources are relative to the project"
    if p.startswith("./"):
        p = p[2:]
    elif p.startswith("/"):
        p = p[1:]
    if any(c in p for c in "?[]{}!\\"):
        return None, "a character class, brace or escape has no OpenCode equivalent"
    lead = p.startswith("**/")
    if lead:
        p = p[3:]
    trail = p.endswith("/**")
    if trail:
        p = p[:-3]
    if not p or "**" in p:
        return None, "'**' inside a path has no exact OpenCode equivalent"
    star = "*" in p
    if lead and not trail and star and "/" not in p and p.startswith("*") and "*" not in p[1:]:
        return [p], ""  # **/*.ext: OpenCode's '*' already crosses '/'
    if star:
        return None, "OpenCode's '*' crosses '/', so this '*' would deny more than Claude does"
    if lead:
        return ([f"{p}/*", f"*/{p}/*"] if trail else [p, f"*/{p}"]), ""
    return ([f"{p}/*"] if trail else [p]), ""


def shell_resource(spec: str | None) -> tuple[str | None, str]:
    """A Claude Bash pattern as an OpenCode shell resource, when it is plain words."""
    if spec is None or spec in ("*", ""):
        return "*", ""
    p = spec[:-2] + " *" if spec.endswith(":*") else spec
    words = p[:-2] if p.endswith(" *") else p
    if words and all(SHELL_SAFE.fullmatch(w) for w in words.split(" ")):
        return p, ""
    return None, "only plain words, optionally ending ' *', map exactly to an OpenCode shell rule"


# ── Planning ────────────────────────────────────────────────────────────────


class Plan:
    """What one client receives: the rules to hold, and what is reported instead."""

    def __init__(self, client: str) -> None:
        self.client = client
        self.wanted: list[tuple[str, object, str]] = []  # (effect, client rule, from)
        self.unmapped: list[str] = []
        self.left: list[str] = []
        self.notes: list[str] = []


def opencode_plan(rules: list[tuple[str, str]]) -> Plan:
    plan = Plan("opencode")
    for effect, rule in rules:
        if effect == "allow":
            plan.left.append(f"{rule} (OpenCode's defaults already allow most tools)")
            continue
        tool, spec = split_rule(rule)
        mcp = mcp_parts(tool) if spec is None else None
        if tool == "Edit":
            res, why = edit_resources(spec)
            if res is None:
                plan.unmapped.append(f"{rule}: {why}")
            for r in res or []:
                plan.wanted.append((effect, {"action": "edit", "resource": r, "effect": effect}, rule))
        elif mcp:
            s, t = mcp
            if NAME_SAFE.fullmatch(s) and NAME_SAFE.fullmatch(t):
                plan.wanted.append((effect, {"action": f"{s}_{t}", "resource": "*", "effect": effect}, rule))
            else:
                plan.unmapped.append(f"{rule}: a server or tool name outside [A-Za-z0-9_-]; OpenCode's action name is unverified")
        elif tool == "Bash":
            res, why = shell_resource(spec)
            if res is None:
                plan.unmapped.append(f"{rule}: {why}")
            else:
                plan.wanted.append((effect, {"action": "shell", "resource": res, "effect": effect}, rule))
        elif tool == "AskUserQuestion" and spec is None:
            plan.unmapped.append(f"{rule}: deferred: unverified (OpenCode's action is 'question'; whether a deny hides the tool is untested)")
        else:
            plan.unmapped.append(f"{rule}: not mapped in version 1")
    # Asks first, then denies: the last match wins, so a deny is never overridden by an ask.
    plan.wanted.sort(key=lambda w: STRICTNESS[w[0]])
    return plan


def codex_plan(rules: list[tuple[str, str]]) -> Plan:
    plan = Plan("codex")
    for effect, rule in rules:
        if effect == "allow":
            plan.left.append(f"{rule} (never written: a Codex allow runs the command outside the sandbox)")
            continue
        tool, spec = split_rule(rule)
        mcp = mcp_parts(tool) if spec is None else None
        if mcp and effect == "ask":
            plan.wanted.append((effect, mcp, rule))
        elif tool in ("Edit", "Read", "Write"):
            plan.unmapped.append(f"{rule}: cannot be expressed (a glob path rule stops Codex starting)")
        elif tool == "AskUserQuestion" and spec is None:
            plan.unmapped.append(f"{rule}: nothing to write (Codex offers no question tool in Default mode)")
        else:
            plan.unmapped.append(f"{rule}: not mapped in version 1")
    return plan


def gemini_policy(rule: str, spec: str | None) -> str:
    p = (spec or "**").removeprefix("./").lstrip("/").removeprefix("**/")
    rx = re.escape(p).replace(r"\*\*", '[^"]*').replace(r"\*", '[^/"]*')
    return (
        f"      # {rule} (a sketch to adapt and test; tool arguments carry absolute paths)\n"
        "      [[rule]]\n"
        '      toolName = "write_file"   # repeat the rule for "replace"\n'
        f"      argsPattern = '\"file_path\":\"[^\"]*/{rx}\"'\n"
        '      decision = "deny"\n'
        "      priority = 500"
    )


def gemini_plan(rules: list[tuple[str, str]]) -> Plan:
    plan = Plan("gemini-cli")
    for effect, rule in rules:
        if effect == "allow":
            plan.left.append(f"{rule} (a later version may write tools.allowed)")
            continue
        tool, spec = split_rule(rule)
        mcp = mcp_parts(tool) if spec is None else None
        if tool == "AskUserQuestion" and spec is None and effect == "deny":
            plan.wanted.append((effect, ("exclude", "ask_user"), rule))
        elif mcp and effect == "ask":
            s, t = mcp
            if "_" in s:
                plan.unmapped.append(f"{rule}: the server name holds '_', which Gemini CLI's tool name cannot carry")
            else:
                plan.wanted.append((effect, ("confirmationRequired", f"mcp_{s}_{t}"), rule))
        elif tool in ("Edit", "Write") and effect == "deny":
            plan.unmapped.append(
                f"{rule}: cannot be expressed in a project file (workspace policies are disabled); "
                "a user policy in ~/.gemini/policies/ could hold:\n" + gemini_policy(rule, spec)
            )
        else:
            plan.unmapped.append(f"{rule}: not mapped in version 1")
    return plan


def antigravity_folder(spec: str | None) -> str | None:
    """'dir/**' (no other wildcard, relative) as the folder an Antigravity rule names, else None."""
    if not spec or not spec.endswith("/**"):
        return None
    p = spec[:-3]
    if p.startswith("./"):
        p = p[2:]
    if not p or p.startswith(("/", "~")) or any(c in p for c in "*?[]{}!\\"):
        return None
    return p


def antigravity_plan(rules: list[tuple[str, str]]) -> Plan:
    plan = Plan("antigravity")
    plan.notes.append("Antigravity keeps its permissions in the app; nothing is written here.")
    for effect, rule in rules:
        tool, spec = split_rule(rule)
        mcp = mcp_parts(tool) if spec is None else None
        if effect == "allow":
            plan.left.append(rule)
        elif mcp:
            plan.notes.append(f"set in the app: {rule} -> {effect} mcp({mcp[0]}/{mcp[1]}) "
                              "(MCP tools default to 'ask' under the Default and Request Review presets; Turbo allows them)")
        elif tool in ("Edit", "Write"):
            folder = antigravity_folder(spec)
            if folder:
                plan.notes.append(f"set in the app: {rule} -> {effect} write_file({folder}) (a folder rule covers everything in it)")
            else:
                plan.unmapped.append(f"{rule}: cannot be expressed (Antigravity's file rules take a path or a folder, not a glob)")
        elif tool == "AskUserQuestion":
            plan.unmapped.append(f"{rule}: cannot be expressed")
        else:
            plan.unmapped.append(f"{rule}: not mapped in version 1")
    return plan


PLANNERS = {"opencode": opencode_plan, "codex": codex_plan, "gemini-cli": gemini_plan, "antigravity": antigravity_plan}
FILES = {"opencode": "opencode.json", "codex": ".codex/config.toml", "gemini-cli": ".gemini/settings.json"}


# ── Reading and writing client files ────────────────────────────────────────


def load_json(path: Path) -> dict:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as err:
        raise Unreadable(f"{path} is not readable JSON: {err}") from None
    if not isinstance(data, dict):
        raise Unreadable(f"{path}: the top level is not an object")
    return data


def dump_json(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def glob_match(value: str, pattern: str) -> bool:
    """OpenCode's wildcard match: '*' is any run of characters, '?' one; a trailing ' *' is optional."""
    rx = re.sub(r"[.+^${}()|\[\]\\]", lambda m: "\\" + m.group(0), pattern.replace("\\", "/"))
    rx = rx.replace("*", ".*").replace("?", ".")
    if rx.endswith(" .*"):
        rx = rx[:-3] + "( .*)?"
    return re.fullmatch(rx, value.replace("\\", "/"), re.S) is not None


def opencode_state(rules: list, want: dict) -> str:
    """'ok', 'missing' or 'overridden' for one wanted rule in an OpenCode permissions array."""
    level = STRICTNESS[want["effect"]]
    last = -1
    for i, r in enumerate(rules):
        if (
            isinstance(r, dict)
            and r.get("action") == want["action"]
            and r.get("resource") == want["resource"]
            and STRICTNESS.get(r.get("effect"), -1) >= level
        ):
            last = i
    if last < 0:
        return "missing"
    for r in rules[last + 1:]:
        if (
            isinstance(r, dict)
            and isinstance(r.get("action"), str)
            and isinstance(r.get("resource"), str)
            and STRICTNESS.get(r.get("effect"), 3) < level
            and glob_match(want["action"], r["action"])
            and glob_match(want["resource"], r["resource"])
        ):
            return "overridden"
    return "ok"


def agent_overrides(data: dict, rules: list, want: dict) -> list[str]:
    """The agents whose own permissions array overrides one wanted rule. OpenCode appends an
    agent's rules (agents.<id>.permissions) after the file's own, and the last match wins, so a
    less strict rule there outweighs anything the top-level array holds."""
    agents = data.get("agents")
    if not isinstance(agents, dict):
        return []
    base = rules if opencode_state(rules, want) == "ok" else rules + [want]
    return [str(name) for name, agent in agents.items()
            if isinstance(agent, dict) and isinstance(agent.get("permissions"), list)
            and opencode_state(base + agent["permissions"], want) == "overridden"]


def apply_opencode(path: Path, plan: Plan, write: bool, out: list[str]) -> int:
    data = load_json(path)
    if "permissions" not in data and "permission" in data:
        out.append(f"  ! {path.name} uses the V1 'permission' key; move it to the V2 'permissions' array by hand")
        return len(plan.wanted)
    rules = data.get("permissions", [])
    if not isinstance(rules, list):
        raise Unreadable(f"{path}: 'permissions' is not a list")
    drift = stuck = 0
    for _effect, want, src in plan.wanted:
        state = opencode_state(rules, want)
        if state != "ok":
            drift += 1
            if write:
                rules.append(dict(want))
                out.append(f"  + {src} -> {json.dumps(want)} (was {state}; appended)")
            else:
                out.append(f"  ✗ {src} -> {json.dumps(want)} is {state}")
        # An agent's own rules come after the file's, so --write cannot outweigh them: they are
        # the owner's, reported and never changed.
        agents = agent_overrides(data, rules, want)
        if agents:
            stuck += 1
            out.append(f"  ✗ {src} -> {json.dumps(want)} is overridden by "
                       + ", ".join(f"agents.{a}.permissions" for a in agents)
                       + ", which OpenCode applies after these rules: change that rule by hand")
        elif state == "ok":
            out.append(f"  ✓ {src} -> {json.dumps(want)}")
    if write:
        if drift:
            data["permissions"] = rules
            dump_json(path, data)
        return stuck
    return drift + sum(1 for _e, want, _s in plan.wanted
                       if opencode_state(rules, want) == "ok" and agent_overrides(data, rules, want))


def toml_key(k: str) -> str:
    return k if TOML_BARE.fullmatch(k) else json.dumps(k)


def apply_codex(path: Path, plan: Plan, write: bool, out: list[str]) -> int:
    try:
        text = path.read_text(encoding="utf-8")
        data = tomllib.loads(text)
    except (OSError, UnicodeDecodeError, tomllib.TOMLDecodeError) as err:
        raise Unreadable(f"{path} is not readable TOML: {err}") from None
    servers = data.get("mcp_servers", {})
    drift = 0
    additions = []
    for _effect, (s, t), src in plan.wanted:
        server = servers.get(s) if isinstance(servers, dict) else None
        if not isinstance(server, dict):
            out.append(f"  - {src}: [mcp_servers.{toml_key(s)}] is not declared here, so nothing is written")
            continue
        tool = server.get("tools", {}).get(t) if isinstance(server.get("tools"), dict) else None
        label = f"[mcp_servers.{toml_key(s)}.tools.{toml_key(t)}] approval_mode = \"prompt\""
        if isinstance(tool, dict) and tool.get("approval_mode") == "prompt":
            out.append(f"  ✓ {src} -> {label}")
            continue
        drift += 1
        if tool is not None:
            out.append(f"  ✗ {src} -> {label}: the table exists with another value; set it by hand")
            continue
        additions.append(f"\n[mcp_servers.{toml_key(s)}.tools.{toml_key(t)}]\napproval_mode = \"prompt\"\n")
        out.append(f"  {'+' if write else '✗'} {src} -> {label}{' (appended)' if write else ' is missing'}")
    if write and additions:
        new = text + ("" if text.endswith("\n") or not text else "\n") + "".join(additions)
        try:
            tomllib.loads(new)
        except tomllib.TOMLDecodeError as err:
            out.append(f"  ! appending would break {path.name} ({err}); add the tables by hand")
            return drift
        path.write_text(new, encoding="utf-8")
        drift -= len(additions)
    return drift


def apply_gemini(path: Path, plan: Plan, write: bool, out: list[str]) -> int:
    data = load_json(path)
    tools = data.get("tools", {})
    if not isinstance(tools, dict):
        raise Unreadable(f"{path}: 'tools' is not an object")
    for key in ("exclude", "confirmationRequired"):
        if not isinstance(tools.get(key, []), list):
            raise Unreadable(f"{path}: tools.{key} is not a list")
    drift = 0
    for _effect, (key, name), src in plan.wanted:
        if name in tools.get(key, []):
            out.append(f"  ✓ {src} -> tools.{key} holds {json.dumps(name)}")
            continue
        drift += 1
        if write:
            tools.setdefault(key, []).append(name)
            out.append(f"  + {src} -> tools.{key} += {json.dumps(name)}")
        else:
            out.append(f"  ✗ {src} -> tools.{key} lacks {json.dumps(name)}")
    if write and drift:
        data["tools"] = tools
        dump_json(path, data)
        return 0
    return drift


APPLIERS = {"opencode": apply_opencode, "codex": apply_codex, "gemini-cli": apply_gemini}


# ── The run ─────────────────────────────────────────────────────────────────


def run(root: Path, clients: list[str], write: bool) -> int:
    rules = read_rules(root)
    print(f"Rules from {root / '.claude' / 'settings.json'}: "
          f"{sum(e == 'deny' for e, _ in rules)} deny, {sum(e == 'ask' for e, _ in rules)} ask, "
          f"{sum(e == 'allow' for e, _ in rules)} allow")
    total = 0
    for client in clients:
        plan = PLANNERS[client](rules)
        out: list[str] = []
        rel = FILES.get(client)
        if rel is None:
            head = f"{client}: document only"
        elif not (root / rel).is_file():
            head = f"{client}: {rel} is not present; nothing checked or written"
        else:
            head = f"{client}: {rel}"
            total += APPLIERS[client](root / rel, plan, write, out)
        print(f"\n{head}")
        if rel is not None and not (root / rel).is_file():
            out = [f"  · would hold {json.dumps(w[1]) if isinstance(w[1], dict) else w[1]} ({w[2]})" for w in plan.wanted]
        for line in out + [f"  {n}" for n in plan.notes]:
            print(line)
        for line in plan.unmapped:
            print(f"  not expressed: {line}")
        for line in plan.left:
            print(f"  left to the client: {line}")
    print()
    if total:
        print(f"✗ {total} rule(s) missing or overridden" + ("; they could not be written, so set them by hand" if write else "; run with --write to add them"))
        return 1
    print("✓ Every expressible rule is in place." if not write else "✓ Every expressible rule is in place; nothing else was changed.")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Carry the deny and ask rules of .claude/settings.json to Codex, Gemini CLI, "
        "OpenCode and Antigravity.",
        epilog="Exit codes: 0 = in place; 1 = drift; 2 = unreadable input or bad arguments.",
    )
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true", help="report the plan and any drift (the default)")
    mode.add_argument("--write", action="store_true", help="add missing rules to client files that already exist")
    mode.add_argument("--self-test", action="store_true", help="prove every mapping in temporary folders")
    parser.add_argument("--client", action="append", choices=CLIENTS, help="limit the run to one client (repeatable)")
    parser.add_argument("--root", type=Path, help="the project root (default: the folder above .claude/)")
    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:
        return 0 if exc.code == 0 else 2
    if args.self_test:
        return self_test()
    root = (args.root or Path(__file__).resolve().parent.parent).resolve()
    clients = [c for c in CLIENTS if c in (args.client or CLIENTS)]
    try:
        return run(root, clients, args.write)
    except Unreadable as err:
        print(f"error: {err}", file=sys.stderr)
        return 2


# ── Self-test ───────────────────────────────────────────────────────────────

SETTINGS = {
    "model": "opus",
    "permissions": {
        "allow": ["Bash(make *)", "WebSearch"],
        "ask": ["mcp__voice__speak", "mcp__my_srv__go", "Bash(git push *)"],
        "deny": [
            "AskUserQuestion",
            "Edit(**/*.pdf)",
            "Edit(build/**)",
            "Edit(**/generated/**)",
            "Edit(/out/x.txt)",
            "Edit(src/*.tex)",
            "Edit(//etc/**)",
            "Bash(rm -rf $(pwd))",
            "WebFetch",
        ],
    },
    "hooks": {},
}
OPENCODE = {
    "$schema": "https://opencode.ai/config.json",
    "model": "named/model",
    "compaction": {"auto": False},
    "permissions": [{"action": "edit", "resource": "notes/*", "effect": "deny"}],
}
GEMINI = {"model": {"name": "m"}, "mcpServers": {}}
CODEX = "# a comment the owner wrote\nmodel = 'm'\n\n[mcp_servers.voice]\ncommand = 'voice-mcp'\n"


def self_test() -> int:
    fails = 0
    probes = 0

    def check(label: str, ok: bool) -> None:
        nonlocal fails, probes
        probes += 1
        print(f"  {'✓' if ok else '✗'} {label}")
        fails += 0 if ok else 1

    def quiet(argv: list[str]) -> tuple[int, str]:
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
            code = main(argv)
        return code, buf.getvalue()

    print("▸ permissions --self-test\n")
    # The mappings themselves.
    check("Edit(**/*.pdf) -> *.pdf", edit_resources("**/*.pdf") == (["*.pdf"], ""))
    check("Edit(build/**) -> build/*", edit_resources("build/**") == (["build/*"], ""))
    check("Edit(**/generated/**) -> generated/* and */generated/*",
          edit_resources("**/generated/**") == (["generated/*", "*/generated/*"], ""))
    check("Edit(sample/src/parts/.base/**) -> sample/src/parts/.base/*",
          edit_resources("sample/src/parts/.base/**") == (["sample/src/parts/.base/*"], ""))
    check("Edit(/out/x.txt) -> out/x.txt", edit_resources("/out/x.txt") == (["out/x.txt"], ""))
    check("Edit(**/secret.txt) -> secret.txt and */secret.txt",
          edit_resources("**/secret.txt") == (["secret.txt", "*/secret.txt"], ""))
    check("bare Edit -> *", edit_resources(None) == (["*"], ""))
    for bad in ("src/*.tex", "//etc/**", "~/x/**", "a/**/b", "**/x?.md", "**/foo*.txt"):
        check(f"Edit({bad}) is reported, not approximated", edit_resources(bad)[0] is None)
    check("Bash(git push *) -> shell 'git push *'", shell_resource("git push *") == ("git push *", ""))
    check("Bash(npm run:*) -> shell 'npm run *'", shell_resource("npm run:*") == ("npm run *", ""))
    check("Bash(rm -rf $(pwd)) is reported", shell_resource("rm -rf $(pwd)")[0] is None)
    check("mcp__S__T splits at the first '__'", mcp_parts("mcp__my_srv__go__now") == ("my_srv", "go__now"))
    check("OpenCode's matcher: '*' crosses '/'", glob_match("a/b/c.pdf", "*.pdf") and glob_match("make", "make *"))

    rules = [(e, r) for e in ("deny", "ask", "allow") for r in SETTINGS["permissions"][e]]
    oc = opencode_plan(rules)
    wanted = [w[1] for w in oc.wanted]
    check("OpenCode: asks come before denies", [w["effect"] for w in wanted] == sorted((w["effect"] for w in wanted), key=STRICTNESS.get))
    check("OpenCode: mcp__voice__speak -> action voice_speak", {"action": "voice_speak", "resource": "*", "effect": "ask"} in wanted)
    check("OpenCode: AskUserQuestion is deferred", any("AskUserQuestion: deferred: unverified" in u for u in oc.unmapped))
    check("OpenCode: allow rules are left to the client", len(oc.left) == 2)
    check("OpenCode: an overriding later allow is drift",
          opencode_state([{"action": "edit", "resource": "*.pdf", "effect": "deny"},
                          {"action": "*", "resource": "*", "effect": "allow"}],
                         {"action": "edit", "resource": "*.pdf", "effect": "deny"}) == "overridden")
    check("OpenCode: a stricter owner rule satisfies an ask",
          opencode_state([{"action": "voice_speak", "resource": "*", "effect": "deny"}],
                         {"action": "voice_speak", "resource": "*", "effect": "ask"}) == "ok")
    gm = gemini_plan(rules)
    check("Gemini CLI: AskUserQuestion -> tools.exclude ask_user", ("exclude", "ask_user") in [w[1] for w in gm.wanted])
    check("Gemini CLI: mcp__voice__speak -> confirmationRequired mcp_voice_speak",
          ("confirmationRequired", "mcp_voice_speak") in [w[1] for w in gm.wanted])
    check("Gemini CLI: a server name with '_' is reported", any("mcp__my_srv__go" in u for u in gm.unmapped))
    check("Gemini CLI: path rules print a user policy", any("[[rule]]" in u for u in gm.unmapped))
    cx = codex_plan(rules)
    check("Codex: path rules are reported", any("Edit(build/**): cannot be expressed" in u for u in cx.unmapped))
    check("Codex: AskUserQuestion has nothing to write", any("AskUserQuestion: nothing to write" in u for u in cx.unmapped))
    ag = antigravity_plan(rules)
    check("Antigravity: document only", any("mcp(voice/speak)" in n for n in ag.notes))
    check("Antigravity: Edit(build/**) -> deny write_file(build)", any("deny write_file(build)" in n for n in ag.notes))
    check("Antigravity: Edit(**/*.pdf) is reported", any(u.startswith("Edit(**/*.pdf): cannot be expressed") for u in ag.unmapped))
    check("Gemini CLI: the policy sketch for **/*.pdf", '[^"]*/[^/"]*\\.pdf"' in gemini_policy("Edit(**/*.pdf)", "**/*.pdf"))

    # A project: check, write, write again.
    with tempfile.TemporaryDirectory(prefix="permissions-selftest-") as tmp:
        root = Path(tmp)
        (root / ".claude").mkdir()
        (root / ".claude" / "settings.json").write_text(json.dumps(SETTINGS), encoding="utf-8")
        r = ["--root", str(root)]
        code, text = quiet(r)
        check("no client file present: exit 0, nothing created",
              code == 0 and sorted(p.name for p in root.iterdir()) == [".claude"] and "is not present" in text)
        (root / ".codex").mkdir()
        (root / ".gemini").mkdir()
        (root / ".codex" / "config.toml").write_text(CODEX, encoding="utf-8")
        dump_json(root / ".gemini" / "settings.json", GEMINI)
        dump_json(root / "opencode.json", OPENCODE)
        before = {p: p.read_bytes() for p in (root / "opencode.json", root / ".gemini/settings.json", root / ".codex/config.toml")}
        code, text = quiet(r + ["--check"])
        check("--check on files lacking the rules exits 1", code == 1)
        check("--check changes nothing", all(p.read_bytes() == b for p, b in before.items()))
        code, _ = quiet(r + ["--write", "--client", "gemini-cli"])
        check("--client limits --write to one client",
              code == 0 and (root / "opencode.json").read_bytes() == before[root / "opencode.json"])
        code, _ = quiet(r + ["--write"])
        check("--write exits 0", code == 0)
        oc_after = load_json(root / "opencode.json")
        check("--write keeps every other key and its order",
              list(oc_after) == list(OPENCODE) and oc_after["model"] == "named/model")
        check("--write keeps the owner's rule first and appends denies last",
              oc_after["permissions"][0] == OPENCODE["permissions"][0]
              and oc_after["permissions"][-1]["effect"] == "deny")
        check("--write writes 2-space JSON with a trailing newline",
              (root / "opencode.json").read_text() == json.dumps(oc_after, indent=2) + "\n")
        gm_after = load_json(root / ".gemini" / "settings.json")
        check("Gemini CLI: tools.exclude and tools.confirmationRequired written",
              gm_after["tools"] == {"exclude": ["ask_user"], "confirmationRequired": ["mcp_voice_speak"]}
              and list(gm_after)[:2] == ["model", "mcpServers"])
        cx_text = (root / ".codex" / "config.toml").read_text()
        check("Codex: the declared server's tool gets approval_mode = \"prompt\", the rest untouched",
              cx_text.startswith(CODEX) and tomllib.loads(cx_text)["mcp_servers"]["voice"]["tools"]["speak"] == {"approval_mode": "prompt"}
              and "my_srv" not in cx_text)
        after = {p: p.read_bytes() for p in before}
        code, _ = quiet(r + ["--write"])
        check("a second --write changes nothing", code == 0 and all(p.read_bytes() == b for p, b in after.items()))
        code, _ = quiet(r + ["--check"])
        check("--check after --write exits 0", code == 0)
        data = load_json(root / "opencode.json")
        data["permissions"] = [p for p in data["permissions"] if p.get("resource") != "build/*"]
        dump_json(root / "opencode.json", data)
        code, text = quiet(r + ["--check", "--client", "opencode"])
        check("a dropped rule is drift, named", code == 1 and '"build/*"' in text and "missing" in text)
        data["permissions"].append({"action": "edit", "resource": "*", "effect": "allow"})
        dump_json(root / "opencode.json", data)
        quiet(r + ["--write", "--client", "opencode"])
        code, _ = quiet(r + ["--check", "--client", "opencode"])
        check("--write re-asserts an overridden deny after the broad allow", code == 0)
        data = load_json(root / "opencode.json")
        data["agents"] = {"build": {"permissions": [{"action": "voice_*", "resource": "*", "effect": "allow"}]}}
        dump_json(root / "opencode.json", data)
        code, text = quiet(r + ["--check", "--client", "opencode"])
        check("OpenCode: an agent's own allow that overrides an ask is drift, named",
              code == 1 and "agents.build.permissions" in text and "voice_speak" in text)
        code, text = quiet(r + ["--write", "--client", "opencode"])
        check("OpenCode: --write cannot outweigh an agent's rule: exit 1, and the agent's rule is kept",
              code == 1 and load_json(root / "opencode.json")["agents"] == data["agents"])
        data["agents"] = {"build": {"permissions": [{"action": "voice_*", "resource": "*", "effect": "allow"},
                                                     {"action": "voice_speak", "resource": "*", "effect": "ask"}]}}
        dump_json(root / "opencode.json", data)
        code, _ = quiet(r + ["--check", "--client", "opencode"])
        check("OpenCode: an agent whose own later ask restores the prompt is no drift", code == 0)
        del data["agents"]
        dump_json(root / "opencode.json", data)
        (root / ".gemini" / "settings.json").write_text("{ // a comment\n}\n", encoding="utf-8")
        code, _ = quiet(r + ["--check"])
        check("an unreadable client file exits 2", code == 2)
        (root / ".gemini" / "settings.json").unlink()
        (root / ".claude" / "settings.json").write_text("{", encoding="utf-8")
        code, _ = quiet(r)
        check("an unreadable settings.json exits 2", code == 2)
        code, _ = quiet(["--client", "nobody"])
        check("an unknown client exits 2", code == 2)
        check("no file or folder was created", sorted(os.listdir(root)) == [".claude", ".codex", ".gemini", "opencode.json"])

    print()
    if fails:
        print(f"✗ Self-test failed: {fails} of {probes} probes.")
        return 1
    print(f"✓ Self-test passed — {probes} probes.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
