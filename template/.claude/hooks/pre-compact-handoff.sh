#!/usr/bin/env bash
# pre-compact-handoff.sh — intercept context compaction; steer the session to the handoff skill.
#
# Registered in .claude/settings.json under hooks.PreCompact, twice: matcher "auto" passes
# `auto` as $1, matcher "manual" passes `manual`. Each entry resolves this script from the git
# root and guards it with [ -f … ], so a missing script is a silent no-op, never an error.
#
# A hook runs a shell command. It CANNOT invoke a skill, write a handoff or stop the session;
# only the model can. So this script's job is narrow: stop silent auto-compaction and surface a
# loud, actionable reminder to hand off instead. The rule it enforces, and the reasons for it,
# live in the session-boundaries rule (07-session-boundaries.md in the project's rules under
# .claude/rules/); the procedure is the handoff skill (.claude/skills/handoff/SKILL.md).
# context-threshold-handoff.sh warns earlier, while the window still has room for a handoff.
#
#   $1 = auto    → auto-compaction fired: BLOCK it (exit 2) and remind. Never compact silently.
#   $1 = manual  → /compact was run deliberately: WARN only (exit 0); never block a choice.
#
# Exit codes: 2 = compaction blocked (auto) · 0 = compaction allowed with a warning (manual)
set -uo pipefail

mode="${1:-auto}"

remind() {
  cat >&2 <<'MSG'
STOP: compaction intercepted. Do not compact this session; hand off instead.

House rule: the session-boundaries rule in the project's rules (.claude/rules/): hand off,
never compact.
  1. Record any durable knowledge in its real home FIRST: .claude/MEMORY.md (through its gate),
     the brief of the work in hand, or the folder's CONTEXT.md / CLAUDE.md.
  2. Invoke the `handoff` skill. It writes the handoff in the folder and filename form the
     project's rules give (by default handoffs/HANDOFF-<DESCRIPTOR>-DD-MM-YYYY.md), including
     the part its mode files say this project must never drop.
  3. Print the handoff path and STOP the turn.
  4. The author or owner runs /clear and resumes from the handoff in a fresh context window.
MSG
}

remind

if [ "$mode" = "manual" ]; then
  printf '\n(Manual /compact allowed, but a handoff gives a cleaner boundary between sessions.)\n' >&2
  exit 0
fi

# Auto-compaction: block it, so nothing is silently summarised.
exit 2
