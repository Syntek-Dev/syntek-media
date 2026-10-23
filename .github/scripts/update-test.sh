#!/usr/bin/env bash
#
# update-test.sh — Prove `copier update` keeps the author's work and delivers the template's.
#
#                  A generated project lives for years and takes template improvements by
#                  `copier update -a .copier-answers.syntek-media.yml` (DESIGN.md D3). Each
#                  ownership class (Section 3) is a promise about what an update does: a seed
#                  the author edited is kept, and one they deleted comes back; a seed-once
#                  example they deleted stays deleted; a copy-only shared file is never touched
#                  again, deleted or edited; their own pieces are never touched; a
#                  template-owned file takes the new version; a platform taken away takes the
#                  files it generated and nothing else, and leaves what the author wrote in a
#                  folder it gates. Every one of those promises rests on a line in
#                  copier.yml, and none of them fails loudly when the line is wrong — the
#                  update reports success either way. So this test performs real updates, the
#                  way an author meets them, per brand kind:
#
#                    1. snapshot the working tree as a template and render a project from it;
#                    2. act as the author: add a MEMORY.md entry, edit tokens.css, delete the
#                       seed-once examples, delete publish-log.md, write a piece of their own,
#                       delete .claude/skills/CLAUDE.md and edit CONTEXT.md; commit;
#                    3. change a template-owned skill in the template; commit;
#                    4. `copier update -a` (the answers file is not Copier's default); commit;
#                    5. update again with nothing changed;
#                    6. in a clone, try an update that changes BRAND_KIND (D14 refuses it);
#                    7. update with one platform taken away — the one with the most catalogue
#                       paths (podcast, where the project has it: DESIGN.md Section 7), after
#                       writing and committing a show register and its saved feed, as the
#                       author's project would, in the folder that platform gates;
#                    8. assert.
#
#                  Twenty-three checks per brand kind:
#                    1. The project renders.
#                    2. `copier update` succeeds.
#                    3. The author's MEMORY.md entry survives.
#                    4. The author's edit to brand/src/design-system/tokens.css survives.
#                    5. The deleted seed-once examples stay deleted (and at least one shipped).
#                    6. The deleted publishing/src/publish-log.md comes back (skills cite it).
#                    7. The author's own piece is byte-for-byte untouched.
#                    8. The template-owned skill carries the template's change.
#                    9. No conflict is left behind (no *.rej file, no conflict marker).
#                   10. An update that changes BRAND_KIND is refused, by BRAND_KIND's own
#                       validator ("BRAND_KIND cannot change on update"), not by some other
#                       failure such as a dirty tree.
#                   11. The refused update touched nothing: the clone's work tree is clean and
#                       its answers file still records the original BRAND_KIND.
#                   12. The update printed _message_before_update ("Before you answer: removing
#                       a platform or a media kind deletes …"), naming every platform and every
#                       media kind — the only warning before a removal deletes filled-in seeds.
#                   13. An update that takes one platform away succeeds, deletes exactly the
#                       files the project held under that platform's catalogue paths and
#                       nothing else, and leaves no conflict (D16). The platform is the one
#                       with the most catalogue paths (_common.sh removable_value): two files
#                       for most; for podcast also the feed folder's pair, the feed workflow's
#                       four files and the feed guide. Where it is podcast, a fixture show
#                       register publishing/src/podcast/harbour-lane-talks.toml and its saved
#                       feed harbour-lane-talks.feed.xml, written and committed before the
#                       removal, are still there and byte-identical after it (D59: the
#                       author's registers and feeds stay).
#                   14. A copy-only shared file the author deleted stays deleted, and one they
#                       edited stays as edited (D11: copy only, never on update).
#                       D73 and D76 extend this to every agent path, preserving an edited
#                       skills link target and native configuration as well as deleted
#                       entrypoints, and never recreating the retired .claude/mcp_config.json.
#                   15. A second update with no template change leaves `git status
#                       --porcelain` empty.
#
#                   16. Copies over existing agent entrypoints, configuration, a real .agents
#                       folder, a real .agents/skills folder, a .agents/skills link to another
#                       folder in the project, an .agents link to another folder in the
#                       project and the 0.4.1 link to .claude preserve every prior byte and
#                       link target, write nothing new through or into an existing .agents
#                       link, skills folder or skills link, and explain manual setup (D73,
#                       D76). A copy takes D76's pre-copy check (_common.sh
#                       sm_agents_copy_args): an .agents link or file is copied with
#                       --exclude /.agents, a real .agents/skills folder with --exclude
#                       /.agents/skills, and a .agents/skills link of any target with no
#                       exclude at all (Copier skips it).
#                   17. An update that crosses v0.4.2 from a project in the 0.4.1 shape
#                       (.agents -> .claude, an author-edited .claude/mcp_config.json)
#                       succeeds, and the D76 migration converts it: .agents a real folder,
#                       .agents/skills the link ../.claude/skills, .agents/mcp_config.json
#                       the author's bytes, .claude/mcp_config.json gone, every action printed,
#                       and the commit hint names .claude/mcp_config.json because it moved. Run
#                       by hand where _src_path is Copier's gh: shorthand and no
#                       .claude/mcp_config.json exists, its 'run again' line clones a URL git
#                       understands (no gh:) and its commit hint names only .agents.
#                   18. The migration is idempotent: run again it changes no byte and says
#                       nothing changed, and a further update crosses no version and runs
#                       nothing (git status stays empty).
#                   19. The migration leaves every other .agents untouched and says so: a real
#                       folder, a link to another folder in the project, none at all, and a
#                       link checked out as a text file (core.symlinks=false).
#                   20. An update across v0.4.2 where .agents is a link to a folder OUTSIDE the
#                       project (which Copier refuses to render beneath, before _exclude is
#                       read) succeeds through D76's unversioned hold/restore pair: the link
#                       comes back with the same target, no .agents.syntek-held is left,
#                       Git sees no change to either, the restore is printed, and nothing is
#                       written in the folder the link points to (D11's second, transient
#                       exception: the link alone is renamed, aside and back).
#                   21. A stranded hold prints its fix: an update of that project that stops
#                       between the stages (a refused BRAND_KIND, in a clone) leaves the link
#                       held as .agents.syntek-held, and the hold stage itself prints the hand
#                       fix, whose first step is 'ls -ld .agents .agents.syntek-held' and
#                       whose last is 'mv .agents.syntek-held .agents'; that last step, run
#                       once .agents is absent, leaves the clone's work tree clean and the
#                       link's target unchanged. No line the update prints but the hold
#                       stage's own (each carries 'agents-outside-link:') holds that bare mv
#                       (since 0.4.5 _message_before_update points to the fix instead, D85):
#                       run while .agents stands, it moves the held link into the folder
#                       outside the project.
#                   22. _message_before_update ends with the crash pointer (DESIGN.md Sections
#                       3.5 and 10): 'If this update stops with OSError: [Errno 39] Directory
#                       not empty, never commit what it left', which sends the owner to
#                       README.md 'Updating a project' for the recovery; the protected command
#                       itself cannot go in the message, which prints after the command was
#                       typed.
#                   23. A stop after the render (DESIGN.md D76, D85): an update over a
#                       committed outside link that stops after its render (a failing
#                       after-stage entry, declared above restore in a scratch release
#                       v0.4.3, stands in for Copier's clean-up crash) leaves the link held
#                       and .agents absent: /.agents is in _skip_if_exists, and Copier 9.12.0
#                       and later leave every such path out of the diff they apply, so Copier
#                       never puts it back. The hand fix, run step by step as the hold stage
#                       prints it, puts the held link back there, and discarding the stopped
#                       update then leaves the project clean. On a copy where .agents stands
#                       again after git reset --hard (which restores the committed link and
#                       keeps the untracked held link: what an owner meets who runs it before
#                       the fix, and what syntek-author's update leaves beside media), the
#                       hand fix (rm .agents, then the mv) puts the held link back too.
#                       Neither writes anything outside the project. On another such copy the
#                       bare mv, run first, writes the held link into the outside folder (the
#                       control). And a held link committed beside an identical .agents makes
#                       the next update move nothing and ask for 'rm .agents.syntek-held'.
#
#                  Copier prints a MissingFileWarning on a fresh copy and on every update (the
#                  previous answers are read through _external_data, D14). It is expected and
#                  never a finding: only exit statuses, messages and files are judged.
#
#                  Numbers are stable identifiers. Append, never renumber.
#
#                  What it CANNOT check: an upgrade from a real earlier release. Checks 17–21
#                  and 23 tag the snapshot v0.4.1 and v0.4.2 (and 23 a clone of it v0.4.3)
#                  and shape the old project by hand, so they prove the migration and its
#                  version gate, not 0.4.1's own files. Nor a project applied over
#                  syntek-author, which is coexist-test.sh's. Check 22 proves only that the
#                  pointer is printed last. Check 23 stops Copier where its Errno 39
#                  clean-up crash stops it (after the render and the diff, before restore),
#                  but by a failing task, not the crash itself, and it runs the README's
#                  recovery only as far as the hand fix and the discard. It stands .agents up
#                  again with git reset --hard, never with syntek-author's update. It proves
#                  the committed link only: a git-ignored link, which git clean would delete
#                  once held, is the vendored script's own --self-test's case (run-all.sh,
#                  CI), not a real update's.
#
# SELF-TEST. --self-test runs the whole flow against the fixture media template of _common.sh,
#            as an author-nonfiction project, so the platform taken away is podcast and the
#            fixture show register and saved feed are written; proves the result clean, then
#            mutates the result once per check and asserts exactly one finding each — the
#            register deleted by the removal among them.
#
# Requirements: bash 4.3+, git, rsync, uvx (or COPIER_CMD). Network on the first uvx run only.
#
# Usage: update-test.sh [--root DIR] [--brand-kind K[,K…]] [--quiet] [--self-test] [--help]
#        --brand-kind defaults to business,author-fiction,author-nonfiction.
#
# Exit codes:  0 = every promise held, for every brand kind tested
#              1 = finding(s), or the self-test no longer separates
#              2 = script error (bad arguments, missing tools, a template with nothing to update)

set -euo pipefail
SCRIPT_NAME="update-test.sh"
# shellcheck source=_common.sh
source "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/_common.sh"

KINDS="$SM_KINDS"
SELF_TEST=false

usage() {
  cat <<'EOF'
update-test.sh — Prove `copier update` keeps the author's work and delivers the template's

Usage: update-test.sh [--root DIR] [--brand-kind K[,K…]] [--quiet] [--self-test] [--help]

  --root DIR         The template repository (default: this repository)
  --brand-kind LIST  Which kinds to test (default: business,author-fiction,author-nonfiction)
  --quiet            Print findings only
  --self-test        Prove the checks still fire against the fixture template
  --help             Show this message

Exit codes: 0 = every promise held  1 = finding(s), or the self-test no longer separates
            2 = script error
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --root)       [[ $# -gt 1 ]] || die "--root needs a value"; SM_ROOT="$(cd "$2" && pwd)" || die "no such directory: $2"; shift 2 ;;
    --brand-kind) [[ $# -gt 1 ]] || die "--brand-kind needs a value"; KINDS="${2//,/ }"; shift 2 ;;
    --quiet|-q)   QUIET=true; shift ;;
    --self-test)  SELF_TEST=true; shift ;;
    --help|-h)    usage; exit 0 ;;
    *)            die "unknown argument: $1" ;;
  esac
done

MEMORY_MARK="Update-test entry"
TOKENS_MARK="/* update-test: the author's own token edit */"
SHARED_MARK="<!-- update-test: the author's own line in a shared file -->"
TEMPLATE_MARK="<!-- update-test: a template change -->"
TOKENS=brand/src/design-system/tokens.css
PUBLISH_LOG=publishing/src/publish-log.md
OWN_PIECE=scripts/src/pieces/101-update-test-piece/brief.md
DELETED_SHARED=.claude/skills/CLAUDE.md
EDITED_SHARED=CONTEXT.md

# State the checks read. --self-test mutates it.
KIND=""; PROJ=""; W=""; COPY_STATUS=0; UPDATE_STATUS=0; OWN_SUM=""; TARGET_REL=""
UPDATE_LOG=""; SWITCH_STATUS=0; SWITCH_LOG=""; SWITCH_DIRTY=""; SWITCH_RECORDED=""
AGAIN_STATUS=0; AGAIN_DIRTY=""; REMOVE_STATUS=0; REMOVE_PLATFORM=""; REMOVED=""; REMOVE_CONFLICTS=""
REMOVE_WANT=""
DELETED=()
declare -A FIXTURE_SUMS=() AGENT_EXPECTED=() AGENT_COPY_ROOT=() AGENT_COPY_STATUS=() AGENT_COPY_SUMS=() AGENT_COPY_ARGS=()
# D76's migration flow (checks 17–19).
MIG_PROJ=""; MIG_STATUS=0; MIG_LOG=""; MIG_MCP_SUM=""; MIG_AGAIN_OUT=""; MIG_AGAIN_DIFF=""
MIG_UPD_AGAIN_STATUS=0; MIG_UPD_AGAIN_DIRTY=""; MIG_UPD_AGAIN_RAN=false
MIG_GH_OUT=""   # the script run by hand over a gh: _src_path with no .claude/mcp_config.json (R1, R2)
declare -A MIG_SHAPE_STATUS=() MIG_SHAPE_DIFF=() MIG_SHAPE_SAID=()
MIG_SHAPES="realdir otherlink missing textfile"
# D76's outside-link pair (checks 20–21).
OUT_PROJ=""; OUT_DIR=""; OUT_LOG=""; OUT_STATUS=0; OUT_TARGET=""; OUT_AFTER_TARGET=""
OUT_SUMS_BEFORE=""; OUT_SUMS_AFTER=""; OUT_HELD_LEFT=false; OUT_DIRTY=""
STRAND_LOG=""; STRAND_STATUS=0; STRAND_HELD=false; STRAND_FIXED_DIRTY=""; STRAND_FIXED_TARGET=""
# A stop after the render, the hand fix run step by step, its control, and a held link committed
# beside .agents (check 23).
CRASH_LOG=""; CRASH_STATUS=0; CRASH_HELD=false; CRASH_LEFT=""; CRASH_FIXED=""; CRASH_STANDING=""; CRASH_STANDING_FIXED=""
CRASH_FIXED_DIRTY=""; CRASH_FIXED_TARGET=""; CRASH_SUMS_BEFORE=""; CRASH_SUMS_AFTER=""
CRASH_CONTROL_WROTE=false; CRASH_FOUND_HELD=false; CRASH_FOUND_MOVED=""

# The author's own files in the folder the podcast platform gates (DESIGN.md D59, Section 6.17):
# a show register and the feed as last published. Invented (Harbour Lane Studio, example.com),
# written at run time, never in the repository.
FEED_DIR=publishing/src/podcast
FEED_FIXTURES="$FEED_DIR/harbour-lane-talks.toml $FEED_DIR/harbour-lane-talks.feed.xml"

write_feed_fixtures() { # $1 = project — writes both fixtures and records their hashes
  local f
  mkdir -p "$1/$FEED_DIR"
  cat > "$1/$FEED_DIR/harbour-lane-talks.toml" <<'TOML'
# Show register: harbour-lane-talks (update-test fixture; the author's own file).
[show]
show = "harbour-lane-talks"
title = "Harbour Lane Talks"
author = "Harbour Lane Studio"
feed_url = "https://example.com/podcast/harbour-lane-talks.xml"
podcast_guid = "00000000-0000-5000-8000-000000000000"

[[episode]]
piece = "101-update-test-piece"
guid = "00000000-0000-5000-8000-000000000001"
title = "The tide decides"
status = "published"
TOML
  cat > "$1/$FEED_DIR/harbour-lane-talks.feed.xml" <<'XML'
<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd" xmlns:podcast="https://podcastindex.org/namespace/1.0">
  <channel>
    <title>Harbour Lane Talks</title>
    <podcast:guid>00000000-0000-5000-8000-000000000000</podcast:guid>
    <item>
      <title>The tide decides</title>
      <guid isPermaLink="false">00000000-0000-5000-8000-000000000001</guid>
    </item>
  </channel>
</rss>
XML
  FIXTURE_SUMS=()
  for f in $FEED_FIXTURES; do FIXTURE_SUMS["$f"]="$(sha1sum < "$1/$f")"; done
}

# The files a tree list holds under one value's catalogue paths, the feed fixtures excepted, in
# the list's (sorted) order.
files_under_catalogue() { # $1 = tree list file, $2 = gate atom
  local kind path
  local -a pats=()
  while read -r kind path; do
    [[ -n "$path" ]] || continue
    if [[ "$kind" == d ]]; then pats+=("$path/"); else pats+=("$path"); fi
  done < <(catalogue_paths "$2")
  awk -v fx=" $FEED_FIXTURES " -v pats="${pats[*]}" '
    BEGIN { n = split(pats, p, " ") }
    index(fx, " " $0 " ") { next }
    { for (i = 1; i <= n; i++) if ((substr(p[i], length(p[i])) == "/" && index($0, p[i]) == 1) || $0 == p[i]) { print; next } }
  ' "$1"
}

other_kind() { # the kind a BRAND_KIND change is attempted to
  case "$1" in business) echo author-fiction ;; author-fiction) echo author-nonfiction ;; *) echo business ;; esac
}

run_flow() { # $1 = template repo, $2 = BRAND_KIND, $3 = work dir — fills the state
  local src="$1" tpl="$3/tpl" e log="$3/flow.log" clone="$3/proj-switch" before
  KIND="$2"; W="$3"; PROJ="$3/proj"; COPY_STATUS=0; UPDATE_STATUS=0; DELETED=()
  UPDATE_LOG="$3/update.log"; SWITCH_STATUS=0; SWITCH_LOG="$3/switch.log"; SWITCH_DIRTY=""; SWITCH_RECORDED=""
  AGAIN_STATUS=0; AGAIN_DIRTY=""; REMOVE_STATUS=0; REMOVE_PLATFORM=""; REMOVED=""; REMOVE_CONFLICTS=""
  REMOVE_WANT=""; FIXTURE_SUMS=(); AGENT_EXPECTED=(); AGENT_COPY_ROOT=(); AGENT_COPY_STATUS=(); AGENT_COPY_SUMS=(); AGENT_COPY_ARGS=()
  MIG_PROJ=""; MIG_STATUS=0; MIG_LOG=""; MIG_MCP_SUM=""; MIG_AGAIN_OUT=""; MIG_AGAIN_DIFF=""
  MIG_UPD_AGAIN_STATUS=0; MIG_UPD_AGAIN_DIRTY=""; MIG_UPD_AGAIN_RAN=false; MIG_GH_OUT=""
  MIG_SHAPE_STATUS=(); MIG_SHAPE_DIFF=(); MIG_SHAPE_SAID=()
  OUT_PROJ=""; OUT_DIR=""; OUT_LOG=""; OUT_STATUS=0; OUT_TARGET=""; OUT_AFTER_TARGET=""
  OUT_SUMS_BEFORE=""; OUT_SUMS_AFTER=""; OUT_HELD_LEFT=false; OUT_DIRTY=""
  STRAND_LOG=""; STRAND_STATUS=0; STRAND_HELD=false; STRAND_FIXED_DIRTY=""; STRAND_FIXED_TARGET=""
  CRASH_LOG=""; CRASH_STATUS=0; CRASH_HELD=false; CRASH_LEFT=""; CRASH_FIXED=""; CRASH_STANDING=""; CRASH_STANDING_FIXED=""
  CRASH_FIXED_DIRTY=""; CRASH_FIXED_TARGET=""; CRASH_SUMS_BEFORE=""; CRASH_SUMS_AFTER=""
  CRASH_CONTROL_WROTE=false; CRASH_FOUND_HELD=false; CRASH_FOUND_MOVED=""
  : > "$UPDATE_LOG"; : > "$SWITCH_LOG"
  sm_snapshot "$src" "$tpl" >>"$log" 2>&1 || die "could not snapshot $src"

  sm_render "$tpl" "$PROJ" "$KIND" >>"$log" 2>&1 || COPY_STATUS=$?
  [[ "$COPY_STATUS" -eq 0 ]] || return 0
  [[ -d "$PROJ/.git" ]] || sm_git "$PROJ" init -q
  sm_commit_all "$PROJ" 'generated'

  # D73, D76: fresh copies preserve a real .agents folder, a real .agents/skills folder, a link
  # to another folder in the project, and the 0.4.1 link to .claude.
  local shape target path digest
  local -a copy_args
  for shape in directory skills-dir skills-link link legacy; do
    target="$W/agent-copy-$shape"; AGENT_COPY_ROOT["$shape"]="$target"
    mkdir -p "$target/.claude" "$target/.codex"
    for path in AGENTS.md GEMINI.md .codex/config.toml .codex/CONTEXT.md .codex/CLAUDE.md .claude/mcp_config.json; do
      # The 0.4.1 shape has no .claude/mcp_config.json of its own here, so a write through the
      # link (.agents/mcp_config.json landing in .claude/) is visible as a new file.
      [[ "$shape" == legacy && "$path" == .claude/mcp_config.json ]] && continue
      printf '# Existing author configuration: preserve it.\n' > "$target/$path"
    done
    case "$shape" in
      directory) mkdir "$target/.agents"; printf 'Owner skill tree.\n' > "$target/.agents/keep.md" ;;
      skills-dir) mkdir -p "$target/.agents/skills/own"; printf 'Owner skill.\n' > "$target/.agents/skills/own/SKILL.md" ;;
      skills-link) mkdir -p "$target/.owner-skills/own" "$target/.agents"
                   printf 'Owner skill.\n' > "$target/.owner-skills/own/SKILL.md"
                   ln -s ../.owner-skills "$target/.agents/skills" ;;
      link) mkdir "$target/.owner-agents"; printf 'Owner skill tree.\n' > "$target/.owner-agents/keep.md"
            ln -s .owner-agents "$target/.agents" ;;
      legacy) mkdir -p "$target/.claude/skills"; ln -s .claude "$target/.agents" ;;
    esac
    while IFS=$'\t' read -r path digest; do
      AGENT_COPY_SUMS["$shape:$path"]="$digest"
    done < <(hash_tree "$target")
    AGENT_COPY_STATUS["$shape"]=0
    # D76's documented pre-copy check: Copier writes through an .agents link and cannot skip
    # a link landing on a real folder.
    mapfile -t copy_args < <(sm_agents_copy_args "$target")
    AGENT_COPY_ARGS["$shape"]="${copy_args[*]}"
    sm_render "$tpl" "$target" "$KIND" "${copy_args[@]}" >"$W/agent-copy-$shape.log" 2>&1 || AGENT_COPY_STATUS["$shape"]=$?
    [[ -d "$target/.git" ]] || sm_git "$target" init -q
    sm_commit_all "$target" 'existing agent configuration'
  done

  # The author at work.
  printf -- '- **01/01/2027** — **%s.** An author decision that must survive every update.\n' "$MEMORY_MARK" >> "$PROJ/.claude/MEMORY.md"
  printf '\n%s\n' "$TOKENS_MARK" >> "$PROJ/$TOKENS"
  for e in $SM_EXAMPLES; do
    [[ -e "$PROJ/$e" ]] && { rm -rf "${PROJ:?}/$e"; DELETED+=("$e"); }
  done
  rm -f "$PROJ/$PUBLISH_LOG"
  mkdir -p "$(dirname "$PROJ/$OWN_PIECE")"
  printf -- '---\npiece: 101-update-test-piece\nstatus: briefed\n---\n\n# Written by the author\n\nA brief no update may touch.\n' > "$PROJ/$OWN_PIECE"
  OWN_SUM="$(sha1sum < "$PROJ/$OWN_PIECE")"
  rm -f "$PROJ/$DELETED_SHARED"
  printf '\n%s\n' "$SHARED_MARK" >> "$PROJ/$EDITED_SHARED"
  # D73: every new shared path keeps an edit or stays deleted, including a dangling alias.
  for e in AGENTS.md GEMINI.md .agents/skills .agents/mcp_config.json .codex/config.toml .codex/CONTEXT.md .codex/CLAUDE.md .claude/mcp_config.json; do
    case "$e" in
      GEMINI.md|.codex/CONTEXT.md|.agents/mcp_config.json|.claude/mcp_config.json) rm -f "$PROJ/$e" ;;
      .agents/skills) rm -f "$PROJ/$e"; ln -s ../author-agent-tree "$PROJ/$e" ;;
      *) printf '\n# Author setting: preserve this file.\n' >> "$PROJ/$e" ;;
    esac
    AGENT_EXPECTED["$e"]="$(path_fingerprint "$PROJ/$e")"
  done
  sm_commit_all "$PROJ" 'the author at work'

  # The template moves on: a template-owned skill every kind ships, or the layout rule.
  TARGET_REL=".claude/skills/run-media-workflow/SKILL.md"
  [[ -f "$tpl/template/$TARGET_REL" ]] || TARGET_REL=".claude/rules/syntek-media/01-layout-and-routing.md"
  [[ -f "$tpl/template/$TARGET_REL" ]] || die "the template has neither run-media-workflow/SKILL.md nor the layout rule — nothing template-owned to update"
  printf '\n%s\n' "$TEMPLATE_MARK" >> "$tpl/template/$TARGET_REL"
  sm_commit_all "$tpl" 'a template change'
  for shape in "${!AGENT_COPY_ROOT[@]}"; do
    [[ "${AGENT_COPY_STATUS[$shape]}" -eq 0 ]] || continue
    sm_update "${AGENT_COPY_ROOT[$shape]}" >>"$W/agent-copy-$shape.log" 2>&1 || AGENT_COPY_STATUS["$shape"]=$?
  done

  sm_update "$PROJ" >"$UPDATE_LOG" 2>&1 || UPDATE_STATUS=$?
  cat "$UPDATE_LOG" >>"$log"
  sm_commit_all "$PROJ" 'updated'

  # Again, with nothing changed.
  sm_update "$PROJ" >>"$log" 2>&1 || AGAIN_STATUS=$?
  AGAIN_DIRTY="$(git -C "$PROJ" status --porcelain 2>/dev/null)"
  sm_commit_all "$PROJ" 'updated again'

  # A changed BRAND_KIND, tried in a clone so the other checks judge the real update alone. The
  # clone starts clean and committed, so a refusal can only come from the template.
  git clone -q "$PROJ" "$clone" >>"$log" 2>&1 || die "could not clone $PROJ"
  sm_update "$clone" --data "BRAND_KIND=$(other_kind "$KIND")" >"$SWITCH_LOG" 2>&1 || SWITCH_STATUS=$?
  cat "$SWITCH_LOG" >>"$log"
  SWITCH_DIRTY="$(git -C "$clone" status --porcelain 2>/dev/null)"
  SWITCH_RECORDED="$(answer_value BRAND_KIND "$clone/$SM_ANSWERS_FILE")"

  # One platform taken away (D16): the files it generated go, nothing else does — the author's
  # show register and saved feed in the podcast folder included (D59).
  REMOVE_PLATFORM="$(removable_value PLATFORMS "$PROJ/$SM_ANSWERS_FILE" "$tpl/copier.yml")"
  if [[ -n "$REMOVE_PLATFORM" ]]; then
    if [[ "$REMOVE_PLATFORM" == podcast ]]; then
      write_feed_fixtures "$PROJ"
      sm_commit_all "$PROJ" "the author's show register and saved feed"
    fi
    before="$(mktemp)"; tree_files "$PROJ" > "$before"
    REMOVE_WANT="$(files_under_catalogue "$before" "p:$REMOVE_PLATFORM" | paste -sd' ' -)"
    sm_update "$PROJ" --data "PLATFORMS=$(list_without PLATFORMS "$PROJ/$SM_ANSWERS_FILE" "$REMOVE_PLATFORM")" >"$3/remove.log" 2>&1 || REMOVE_STATUS=$?
    cat "$3/remove.log" >>"$log"
    REMOVED="$(tree_files "$PROJ" | LC_ALL=C comm -23 "$before" - | awk -v fx=" $FEED_FIXTURES " '!index(fx, " " $0 " ")' | paste -sd' ' -)"
    REMOVE_CONFLICTS="$(conflicts_in "$PROJ" | paste -sd' ' -)"
    rm -f "$before"
    sm_commit_all "$PROJ" 'a platform taken away'
  fi
  run_migration_flow "$tpl" "$3"
  return 0
}

# D76: the first migration, across a real version gate. The snapshot is tagged v0.4.1, then an
# empty commit v0.4.2, so the update crosses the migration's version and nothing else changes;
# each old project is copied at v0.4.1 and shaped by hand as 0.4.1 left it (or as the author
# changed it), committed, and updated to v0.4.2.
mig_project() { # $1 = template, $2 = dest, $3 = shape — copy at v0.4.1, reshape, commit
  local d="$2"
  SM_VCS_REF=v0.4.1 sm_render "$1" "$d" "$KIND" >>"$W/mig.log" 2>&1 || return 1
  [[ -d "$d/.git" ]] || sm_git "$d" init -q
  rm -rf "${d:?}/.agents"
  case "$3" in
    legacy)    ln -s .claude "$d/.agents"
               printf '{"mcpServers": {"author-server": {}}}\n' > "$d/.claude/mcp_config.json" ;;
    realdir)   mkdir "$d/.agents"; printf 'Owner skill tree.\n' > "$d/.agents/keep.md"
               printf '{"mcpServers": {}}\n' > "$d/.claude/mcp_config.json" ;;
    otherlink) mkdir "$d/.owner-agents"; printf 'Owner skill tree.\n' > "$d/.owner-agents/keep.md"
               ln -s .owner-agents "$d/.agents"; printf '{"mcpServers": {}}\n' > "$d/.claude/mcp_config.json" ;;
    missing)   printf '{"mcpServers": {}}\n' > "$d/.claude/mcp_config.json" ;;
    textfile)  printf '.claude' > "$d/.agents"; printf '{"mcpServers": {}}\n' > "$d/.claude/mcp_config.json" ;;
    # A link to the author's own agent tree beside the project, outside it (checks 20–21).
    outside)   ln -s "../${OUT_DIR##*/}" "$d/.agents"; printf '{"mcpServers": {}}\n' > "$d/.claude/mcp_config.json" ;;
  esac
  sm_commit_all "$d" "the 0.4.1 shape: $3"
}

run_migration_flow() { # $1 = template snapshot, $2 = work dir
  local tpl="$1" shape d before after script
  script="$tpl/$SM_D76_MIGRATION"
  sm_git "$tpl" tag -f v0.4.1 >/dev/null
  sm_git "$tpl" commit -q --allow-empty -m 'D76 release' && sm_git "$tpl" tag -f "$SM_D76_VERSION" >/dev/null
  MIG_PROJ="$2/mig-legacy"; MIG_LOG="$2/mig-update.log"; : > "$MIG_LOG"
  if ! mig_project "$tpl" "$MIG_PROJ" legacy; then MIG_STATUS=99; return 0; fi
  MIG_MCP_SUM="$(sha1sum < "$MIG_PROJ/.claude/mcp_config.json")"
  SM_VCS_REF="$SM_D76_VERSION" sm_update "$MIG_PROJ" >"$MIG_LOG" 2>&1 || MIG_STATUS=$?
  sm_commit_all "$MIG_PROJ" 'updated to v0.4.2'
  # 18: the script again, then the update again.
  before="$(hash_tree "$MIG_PROJ")"
  MIG_AGAIN_OUT="$(cd "$MIG_PROJ" && python3 -I "$script" 2>&1 || true)"
  after="$(hash_tree "$MIG_PROJ")"
  MIG_AGAIN_DIFF="$(diff <(printf '%s\n' "$before") <(printf '%s\n' "$after") | grep -c '^[<>]' || true)"
  SM_VCS_REF="$SM_D76_VERSION" sm_update "$MIG_PROJ" >"$2/mig-again.log" 2>&1 || MIG_UPD_AGAIN_STATUS=$?
  grep -qF 'v0.4.2-agents-folder.py' "$2/mig-again.log" && MIG_UPD_AGAIN_RAN=true
  MIG_UPD_AGAIN_DIRTY="$(git -C "$MIG_PROJ" status --porcelain 2>/dev/null)"
  # 17 (R1, R2): the script by hand where _src_path is Copier's gh: shorthand and there is no
  # .claude/mcp_config.json to move.
  d="$2/mig-gh"; rm -rf "$d"; mkdir -p "$d/.claude/skills"
  printf '_src_path: gh:Syntek-Dev/syntek-media\n' > "$d/$SM_ANSWERS_FILE"
  ln -s .claude "$d/.agents"
  sm_git "$d" init -q
  MIG_GH_OUT="$(cd "$d" && python3 -I "$script" 2>&1 || true)"
  # 19: every other shape, through a real update.
  for shape in $MIG_SHAPES; do
    d="$2/mig-$shape"; MIG_SHAPE_STATUS["$shape"]=0
    if ! mig_project "$tpl" "$d" "$shape"; then MIG_SHAPE_STATUS["$shape"]=99; continue; fi
    before="$(hash_tree "$d" | grep -v "^$SM_ANSWERS_FILE"$'\t')"
    SM_VCS_REF="$SM_D76_VERSION" sm_update "$d" >"$2/mig-$shape.log" 2>&1 || MIG_SHAPE_STATUS["$shape"]=$?
    after="$(hash_tree "$d" | grep -v "^$SM_ANSWERS_FILE"$'\t')"
    MIG_SHAPE_DIFF["$shape"]="$(diff <(printf '%s\n' "$before") <(printf '%s\n' "$after") | { grep '^[<>]' || true; } | cut -c3- | cut -f1 | LC_ALL=C sort -u | paste -sd' ' -)"
    MIG_SHAPE_SAID["$shape"]="$(grep -cF 'nothing changed' "$2/mig-$shape.log" || true)"
  done
  run_outside_flow "$tpl" "$2"
  run_crash_flow "$tpl" "$2"
}

# D76, D11's second exception: an .agents link to a folder outside the project. The outside
# folder sits beside the project in the work dir, holds an author's file, and is hashed before
# and after every run, so a write through the link is seen.
run_outside_flow() { # $1 = template snapshot (tagged v0.4.1 and v0.4.2), $2 = work dir
  local tpl="$1" clone="$2/mig-outside-stranded"
  OUT_PROJ="$2/mig-outside"; OUT_DIR="$2/outside-agents"; OUT_LOG="$2/mig-outside.log"; : > "$OUT_LOG"
  STRAND_LOG="$2/mig-outside-stranded.log"; : > "$STRAND_LOG"
  rm -rf "$OUT_DIR"; mkdir -p "$OUT_DIR"
  printf "The author's own agent tree, outside the project.\n" > "$OUT_DIR/note.md"
  OUT_SUMS_BEFORE="$(hash_tree "$OUT_DIR")"
  if ! mig_project "$tpl" "$OUT_PROJ" outside; then OUT_STATUS=99; return 0; fi
  OUT_TARGET="$(readlink "$OUT_PROJ/.agents")"
  # 20: the update across v0.4.2.
  SM_VCS_REF="$SM_D76_VERSION" sm_update "$OUT_PROJ" >"$OUT_LOG" 2>&1 || OUT_STATUS=$?
  OUT_AFTER_TARGET="$(readlink "$OUT_PROJ/.agents" 2>/dev/null || printf 'not a link')"
  [[ -L "$OUT_PROJ/$SM_OUTSIDE_HELD" || -e "$OUT_PROJ/$SM_OUTSIDE_HELD" ]] && OUT_HELD_LEFT=true
  OUT_DIRTY="$(git -C "$OUT_PROJ" status --porcelain -- .agents "$SM_OUTSIDE_HELD" 2>/dev/null | paste -sd' ' -)"
  sm_commit_all "$OUT_PROJ" 'updated to v0.4.2'
  # 21: an update that stops between the stages, in a clone, then the printed fix.
  git clone -q "$OUT_PROJ" "$clone" >>"$W/mig.log" 2>&1 || { STRAND_STATUS=99; return 0; }
  SM_VCS_REF="$SM_D76_VERSION" sm_update "$clone" --data "BRAND_KIND=$(other_kind "$KIND")" >"$STRAND_LOG" 2>&1 || STRAND_STATUS=$?
  [[ -L "$clone/$SM_OUTSIDE_HELD" && ! -L "$clone/.agents" && ! -e "$clone/.agents" ]] && STRAND_HELD=true
  if $STRAND_HELD; then (cd "$clone" && $SM_OUTSIDE_FIX) >>"$STRAND_LOG" 2>&1 || true; fi
  STRAND_FIXED_DIRTY="$(git -C "$clone" status --porcelain 2>/dev/null | paste -sd' ' -)"
  STRAND_FIXED_TARGET="$(readlink "$clone/.agents" 2>/dev/null || printf 'not a link')"
  OUT_SUMS_AFTER="$(hash_tree "$OUT_DIR")"
}

# 23: a stop AFTER the render. A failing after-stage entry, declared above restore, stands in for
# Copier's clean-up crash (Errno 39): Copier has rendered and applied its diff, and stops before
# restore runs (a task that exits non-zero ends the update; after-stage entries run in declared
# order). The entry is committed only in a clone of the snapshot, tagged SM_CRASH_VERSION, so no
# other flow sees it; the real copier.yml never carries it, and shipped-seeds.sh reads the real
# one. Copier never puts media's .agents back: /.agents is in _skip_if_exists (D11), and Copier
# 9.12.0 and later leave every file the diff touches that matches _skip_if_exists out of the
# diff they apply (git apply --exclude; 9.19.1 _main.py:1552-1586). So the stop leaves .agents
# absent, and the hand fix runs there. .agents stands again after a discard (git reset --hard
# restores the committed link and keeps the untracked held link) or beside syntek-author, whose
# update puts it back; that state is made with git reset --hard on two copies of the stopped
# project: the hand fix runs on one, and the control, the bare mv run first, on the other. Each
# project is a clone of OUT_PROJ (its outside link committed, at v0.4.2) in a folder of its own
# beside its own copy of the outside folder, so its relative .agents link leaves the project to
# that copy and check 20's folder is never touched.
run_crash_flow() { # $1 = template snapshot (tagged v0.4.1 and v0.4.2), $2 = work dir
  local tpl="$1" ctpl="$2/tpl-crash" o="${OUT_DIR##*/}" d="$2/crash" s="$2/crash-standing"
  local c="$2/crash-control" f="$2/crash-found" q="'" moved="" sums copy
  CRASH_LOG="$2/crash.log"; : > "$CRASH_LOG"
  if [[ "$OUT_STATUS" -ne 0 || ! -d "$OUT_PROJ/.git" ]]; then CRASH_STATUS=99; return 0; fi
  git clone -q "$tpl" "$ctpl" >>"$W/mig.log" 2>&1 || { CRASH_STATUS=99; return 0; }
  awk -v q="$q" '/agents-outside-link\.py" restore/ && !done {
      print "  - command: \"false\""; print "    when: \"<% _stage == " q "after" q " %>\""; done = 1 }
    { print }' "$ctpl/copier.yml" > "$2/copier.yml.crash" && mv "$2/copier.yml.crash" "$ctpl/copier.yml"
  grep -qxF '  - command: "false"' "$ctpl/copier.yml" || { CRASH_STATUS=99; return 0; }
  sm_commit_all "$ctpl" 'a stop after the render (update-test.sh check 23 only)'
  sm_git "$ctpl" tag -f "$SM_CRASH_VERSION" >/dev/null
  # The stopped update. Copier takes an update's source only from the answers file, so the
  # clone's _src_path is pointed at the scratch release (a harness device; nothing else moves).
  mkdir -p "$d"; cp -a "$OUT_DIR" "$d/$o"
  git clone -q "$OUT_PROJ" "$d/proj" >>"$W/mig.log" 2>&1 || { CRASH_STATUS=99; return 0; }
  awk -v src="$ctpl" '/^_src_path:/ { print "_src_path: " src; next } { print }' "$d/proj/$SM_ANSWERS_FILE" > "$d/answers" \
    && mv "$d/answers" "$d/proj/$SM_ANSWERS_FILE"
  sm_commit_all "$d/proj" 'the scratch release as the source'
  CRASH_SUMS_BEFORE="$(hash_tree "$d/$o")"
  SM_VCS_REF="$SM_CRASH_VERSION" sm_update "$d/proj" >"$CRASH_LOG" 2>&1 || CRASH_STATUS=$?
  [[ -L "$d/proj/$SM_OUTSIDE_HELD" && "$(readlink "$d/proj/$SM_OUTSIDE_HELD")" == "$OUT_TARGET" ]] && CRASH_HELD=true
  CRASH_LEFT="$(stands_at "$d/proj/.agents")"
  if $CRASH_HELD && [[ "$CRASH_LEFT" == absent ]]; then
    # The same stop with .agents standing again, as git reset --hard leaves it, twice: once for
    # the hand fix, once for the control, the bare mv run first.
    for copy in "$s" "$c"; do
      mkdir -p "$copy"; cp -a "$OUT_DIR" "$copy/$o"; cp -a "$d/proj" "$copy/proj"
      git -C "$copy/proj" reset -q --hard >>"$CRASH_LOG" 2>&1 || true
    done
    CRASH_STANDING="$(stands_at "$s/proj/.agents")"
    (cd "$c/proj" && $SM_OUTSIDE_FIX) >>"$CRASH_LOG" 2>&1 || true
    [[ -L "$c/$o/$SM_OUTSIDE_HELD" ]] && CRASH_CONTROL_WROTE=true
    CRASH_STANDING_FIXED="$(hand_fix "$s/proj")"
    [[ "$(hash_tree "$s/$o")" == "$CRASH_SUMS_BEFORE" ]] || CRASH_STANDING_FIXED+=" (wrote outside)"
    # The stopped project as Copier left it: the hand fix, then the discard (the dry run first).
    CRASH_FIXED="$(hand_fix "$d/proj")"
    (cd "$d/proj" && git clean -n -d && git reset --hard && git clean -fd) >>"$CRASH_LOG" 2>&1 || true
  fi
  CRASH_FIXED_DIRTY="$(git -C "$d/proj" status --porcelain 2>/dev/null | paste -sd' ' -)"
  CRASH_FIXED_TARGET="$(readlink "$d/proj/.agents" 2>/dev/null || printf 'not a link')"
  CRASH_SUMS_AFTER="$(hash_tree "$d/$o")"
  # found_held(): a held link committed beside an identical .agents. The next update must move
  # nothing, say so, and ask for the held link's removal; Copier then refuses the outside link.
  mkdir -p "$f"; cp -a "$OUT_DIR" "$f/$o"
  git clone -q "$OUT_PROJ" "$f/proj" >>"$W/mig.log" 2>&1 || return 0
  ln -s "$OUT_TARGET" "$f/proj/$SM_OUTSIDE_HELD"
  sm_commit_all "$f/proj" 'a held link committed beside .agents'
  sums="$(hash_tree "$f/$o")"
  SM_VCS_REF="$SM_D76_VERSION" sm_update "$f/proj" >"$2/crash-found.log" 2>&1 || true
  grep -F 'agents-outside-link: found' "$2/crash-found.log" 2>/dev/null | grep -qF "rm $SM_OUTSIDE_HELD" && CRASH_FOUND_HELD=true
  [[ "$(readlink "$f/proj/.agents" 2>/dev/null)" == "$OUT_TARGET" ]] || moved+=" .agents"
  [[ "$(readlink "$f/proj/$SM_OUTSIDE_HELD" 2>/dev/null)" == "$OUT_TARGET" ]] || moved+=" $SM_OUTSIDE_HELD"
  [[ "$(hash_tree "$f/$o")" == "$sums" ]] || moved+=" the outside folder"
  CRASH_FOUND_MOVED="${moved# }"
}

# What stands at a path, as the vendored script words it: absent, a link to <target>, a folder
# or a file.
stands_at() { # $1 = path
  if [[ -L "$1" ]]; then printf 'a link to %s' "$(readlink "$1")"
  elif [[ -d "$1" ]]; then printf 'a folder'
  elif [[ -e "$1" ]]; then printf 'a file'
  else printf 'absent'; fi
}

# The hand fix, step by step, as the hold stage prints it and README.md 'Migrations' gives it:
# 1. ls -ld .agents .agents.syntek-held, and where it shows no held link, stop and change
# nothing; 2. a link at .agents removed alone (rm .agents), a folder or a file moved aside
# (mv .agents .agents.from-update); 3. once ls -ld .agents finds nothing,
# mv .agents.syntek-held .agents. Prints what then stands at .agents, and whether a held link
# is left.
hand_fix() { # $1 = project
  local out
  out="$(cd "$1" && $SM_OUTSIDE_CHECK 2>&1)" || true
  printf '%s\n' "$out" >>"$CRASH_LOG"
  if grep -qE '[[:space:]]\.agents\.syntek-held( -> |$)' <<< "$out"; then
    if grep -qE '[[:space:]]\.agents -> ' <<< "$out"; then
      (cd "$1" && rm .agents) >>"$CRASH_LOG" 2>&1 || true
    elif [[ -e "$1/.agents" ]]; then
      (cd "$1" && mv .agents .agents.from-update) >>"$CRASH_LOG" 2>&1 || true
    fi
    if ! (cd "$1" && ls -ld .agents) >/dev/null 2>&1; then
      (cd "$1" && $SM_OUTSIDE_FIX) >>"$CRASH_LOG" 2>&1 || true
    fi
  fi
  printf '%s; held link %s' "$(stands_at "$1/.agents")" "$([[ -L "$1/$SM_OUTSIDE_HELD" ]] && printf left || printf gone)"
}

run_checks() {
  FINDINGS=()
  local e f text want
  local L="[$KIND]"
  if [[ "$COPY_STATUS" -ne 0 ]]; then
    finding "check 1 — $L the project did not render (exit $COPY_STATUS) — see $W/flow.log"
    return 0
  fi
  [[ "$UPDATE_STATUS" -eq 0 ]] || finding "check 2 — $L copier update failed (exit $UPDATE_STATUS) — see $UPDATE_LOG"
  grep -qF "$MEMORY_MARK" "$PROJ/.claude/MEMORY.md" 2>/dev/null \
    || finding "check 3 — $L the author's MEMORY.md entry did not survive the update"
  grep -qF "$TOKENS_MARK" "$PROJ/$TOKENS" 2>/dev/null \
    || finding "check 4 — $L the author's edit to $TOKENS did not survive the update"
  [[ ${#DELETED[@]} -gt 0 ]] \
    || finding "check 5 — $L the render shipped no seed-once example to delete, so 'stays deleted' was never tested"
  for e in "${DELETED[@]}"; do
    [[ -e "$PROJ/$e" ]] && finding "check 5 — $L the deleted example $e came back on update"
  done
  [[ -f "$PROJ/$PUBLISH_LOG" ]] \
    || finding "check 6 — $L the deleted $PUBLISH_LOG was not recreated — skills cite it"
  [[ -f "$PROJ/$OWN_PIECE" && "$(sha1sum < "$PROJ/$OWN_PIECE")" == "$OWN_SUM" ]] \
    || finding "check 7 — $L the author's own $OWN_PIECE changed or vanished"
  grep -qF "$TEMPLATE_MARK" "$PROJ/$TARGET_REL" 2>/dev/null \
    || finding "check 8 — $L $TARGET_REL did not take the template's change"
  while IFS= read -r f; do
    [[ -n "$f" ]] && finding "check 9 — $L conflict left behind: $f"
  done < <(conflicts_in "$PROJ")
  if [[ "$SWITCH_STATUS" -eq 0 ]]; then
    finding "check 10 — $L an update changing BRAND_KIND to $(other_kind "$KIND") was accepted — it must be refused (DESIGN.md D14)"
  elif ! grep -qF "$SM_KIND_REFUSAL" "$SWITCH_LOG" 2>/dev/null; then
    finding "check 10 — $L the BRAND_KIND change failed (exit $SWITCH_STATUS), but not with BRAND_KIND's validator message — see $SWITCH_LOG"
  fi
  if [[ -n "$SWITCH_DIRTY" || "$SWITCH_RECORDED" != "$KIND" ]]; then
    finding "check 11 — $L the refused BRAND_KIND change touched the project ($(printf '%s\n' "$SWITCH_DIRTY" | grep -c . || true) path(s) changed; the answers record '$SWITCH_RECORDED')"
  fi
  text="$(copier_message_text "$UPDATE_LOG")"
  if [[ "$text" != *"$SM_BEFORE_UPDATE_MARK"* ]]; then
    finding "check 12 — $L copier update printed no removal warning (_message_before_update)"
  else
    text="${text#*"$SM_BEFORE_UPDATE_MARK"}"
    for e in $SM_PLATFORMS $SM_MEDIA_KINDS; do
      [[ "$text" == *"$e"* ]] || finding "check 12 — $L the removal warning does not name $e"
    done
  fi
  text="$(copier_message_text "$UPDATE_LOG")"
  if [[ "$text" != *"$SM_BEFORE_UPDATE_CRASH"* ]]; then
    finding "check 22 — $L _message_before_update does not end with the crash pointer (none is printed)"
  else
    text="${text##*"$SM_BEFORE_UPDATE_CRASH"}"
    [[ "$text" == *"$SM_BEFORE_UPDATE_CRASH_END Updating to template version"* \
      || "$text" == *"$SM_BEFORE_UPDATE_CRASH_END Keeping template version"* ]] \
      || finding "check 22 — $L _message_before_update does not end with the crash pointer"
  fi
  if [[ -z "$REMOVE_PLATFORM" ]]; then
    finding "check 13 — $L the project's PLATFORMS name no gated platform that could be taken away"
  elif [[ "$REMOVE_STATUS" -ne 0 ]]; then
    finding "check 13 — $L the update taking $REMOVE_PLATFORM away failed (exit $REMOVE_STATUS) — see $W/remove.log"
  else
    want="$REMOVE_WANT"
    if [[ -z "$want" ]]; then
      finding "check 13 — $L the project held no file under $REMOVE_PLATFORM's catalogue paths, so taking it away proved nothing"
    elif [[ "$REMOVED" != "$want" ]]; then
      finding "check 13 — $L taking $REMOVE_PLATFORM away deleted '${REMOVED:-nothing}', not exactly the files it generated ($want)"
    fi
    [[ -z "$REMOVE_CONFLICTS" ]] \
      || finding "check 13 — $L taking $REMOVE_PLATFORM away left a conflict: $REMOVE_CONFLICTS"
    for f in "${!FIXTURE_SUMS[@]}"; do
      if [[ ! -f "$PROJ/$f" ]]; then
        finding "check 13 — $L taking $REMOVE_PLATFORM away deleted the author's $f (DESIGN.md D59: show registers and saved feeds stay)"
      elif [[ "$(sha1sum < "$PROJ/$f")" != "${FIXTURE_SUMS[$f]}" ]]; then
        finding "check 13 — $L taking $REMOVE_PLATFORM away changed the author's $f"
      fi
    done
  fi
  [[ -e "$PROJ/$DELETED_SHARED" ]] \
    && finding "check 14 — $L the shared $DELETED_SHARED, deleted by the author, came back on update (D11: copy only)"
  grep -qF "$SHARED_MARK" "$PROJ/$EDITED_SHARED" 2>/dev/null \
    || finding "check 14 — $L the author's edit to the shared $EDITED_SHARED did not survive the update"
  for f in "${!AGENT_EXPECTED[@]}"; do
    [[ "$(path_fingerprint "$PROJ/$f")" == "${AGENT_EXPECTED[$f]}" ]] \
      || finding "check 14 — $L the author's shared agent path $f changed or was recreated on update"
  done
  local shape key path
  for shape in "${!AGENT_COPY_ROOT[@]}"; do
    if [[ "${AGENT_COPY_STATUS[$shape]}" -ne 0 ]]; then
      finding "check 16 — $L a copy over an existing agent $shape failed (exit ${AGENT_COPY_STATUS[$shape]})"
      continue
    fi
    for key in "${!AGENT_COPY_SUMS[@]}"; do
      [[ "$key" == "$shape:"* ]] || continue
      path="${key#*:}"
      [[ "$(path_fingerprint "${AGENT_COPY_ROOT[$shape]}/$path")" == "${AGENT_COPY_SUMS[$key]}" ]] \
        || finding "check 16 — $L copy changed the author's agent $shape path $path"
    done
    grep -qF 'manual' "$W/agent-copy-$shape.log" \
      || finding "check 16 — $L copy did not explain manual agent setup for the existing $shape"
    # D76's pre-copy check (R5): only an .agents link or file excludes the folder, only a real
    # .agents/skills folder excludes the skills path, and a skills link of any target needs none.
    case "$shape" in
      link|legacy) want='--exclude /.agents' ;;
      skills-dir)  want='--exclude /.agents/skills' ;;
      *)           want='' ;;
    esac
    [[ "${AGENT_COPY_ARGS[$shape]-}" == "$want" ]] \
      || finding "check 16 — $L the pre-copy check gave '${AGENT_COPY_ARGS[$shape]-}' for the existing agent $shape, not '$want'"
    # D76: nothing new through an existing link, or inside an existing skills folder.
    while IFS=$'\t' read -r path _; do
      [[ -n "${AGENT_COPY_SUMS[$shape:$path]:-}" ]] && continue
      case "$shape:$path" in
        link:.owner-agents/*|skills-dir:.agents/skills/*|skills-link:.owner-skills/*|legacy:.claude/mcp_config.json)
          finding "check 16 — $L copy wrote $path into the author's existing agent $shape" ;;
      esac
    done < <(hash_tree "${AGENT_COPY_ROOT[$shape]}")
  done
  # ── 17–19. The D76 migration ─────────────────────────────────────────────────
  local p_ag="$MIG_PROJ/.agents"
  if [[ "$MIG_STATUS" -ne 0 ]]; then
    finding "check 17 — $L the update across $SM_D76_VERSION from the 0.4.1 shape failed (exit $MIG_STATUS) — see $MIG_LOG"
  else
    if [[ -L "$p_ag" || ! -d "$p_ag" ]]; then
      finding "check 17 — $L the migration left .agents as a link or absent: it was the 0.4.1 link to .claude"
    elif [[ ! -L "$p_ag/skills" || "$(readlink "$p_ag/skills")" != "$SM_AGENTS_SKILLS_LINK" ]]; then
      finding "check 17 — $L the migrated .agents/skills is not the link $SM_AGENTS_SKILLS_LINK"
    elif [[ ! -f "$p_ag/mcp_config.json" || "$(sha1sum < "$p_ag/mcp_config.json")" != "$MIG_MCP_SUM" ]]; then
      finding "check 17 — $L .agents/mcp_config.json is missing or is not the author's .claude/mcp_config.json, moved"
    elif [[ -e "$MIG_PROJ/.claude/mcp_config.json" ]]; then
      finding "check 17 — $L .claude/mcp_config.json is still there: the migration moves it"
    fi
    grep -qE 'moved +\.claude/mcp_config\.json -> \.agents/mcp_config\.json' "$MIG_LOG" 2>/dev/null \
      || finding "check 17 — $L the update did not print what the migration did — see $MIG_LOG"
    grep -qE 'Review and commit: git add -A \.agents \.claude/mcp_config\.json ' "$MIG_LOG" 2>/dev/null \
      || finding "check 17 — $L the commit hint does not name the moved .claude/mcp_config.json — see $MIG_LOG"
  fi
  # R1 and R2: the hand run over a gh: _src_path, with no .claude/mcp_config.json to move.
  local gh_rerun gh_hint
  gh_rerun="$(printf '%s\n' "$MIG_GH_OUT" | grep -F 'v0.4.2-agents-folder.py' | grep -F 'git clone' || true)"
  gh_hint="$(printf '%s\n' "$MIG_GH_OUT" | grep -F 'Review and commit:' || true)"
  if [[ -z "$gh_rerun" ]]; then
    finding "check 17 — $L the migration run by hand printed no 'run again' line with a clone"
  elif [[ "$gh_rerun" == *'gh:'* || "$gh_rerun" != *'https://github.com/'* ]]; then
    finding "check 17 — $L the 'run again' line passes Copier's gh: shorthand to git clone: $gh_rerun"
  fi
  if [[ -z "$gh_hint" ]]; then
    finding "check 17 — $L the migration run by hand converted the link but printed no commit hint"
  elif [[ "$gh_hint" == *'.claude/mcp_config.json'* ]]; then
    finding "check 17 — $L the commit hint names .claude/mcp_config.json, which never existed (git add would stop on the pathspec): $gh_hint"
  fi
  if [[ "${MIG_AGAIN_DIFF:-0}" -ne 0 || "$MIG_AGAIN_OUT" != *'nothing changed'* ]]; then
    finding "check 18 — $L the migration run again changed $MIG_AGAIN_DIFF path(s) or did not say nothing changed: it must be idempotent"
  fi
  if [[ "$MIG_UPD_AGAIN_STATUS" -ne 0 || -n "$MIG_UPD_AGAIN_DIRTY" ]] || $MIG_UPD_AGAIN_RAN; then
    finding "check 18 — $L a second update at $SM_D76_VERSION was not a no-op (exit $MIG_UPD_AGAIN_STATUS; ran the migration: $MIG_UPD_AGAIN_RAN)"
  fi
  for shape in $MIG_SHAPES; do
    if [[ "${MIG_SHAPE_STATUS[$shape]:-1}" -ne 0 ]]; then
      finding "check 19 — $L the update across $SM_D76_VERSION with a $shape .agents failed (exit ${MIG_SHAPE_STATUS[$shape]:-none})"
    elif [[ -n "${MIG_SHAPE_DIFF[$shape]}" ]]; then
      finding "check 19 — $L the migration changed a $shape .agents project: ${MIG_SHAPE_DIFF[$shape]}"
    elif [[ "${MIG_SHAPE_SAID[$shape]:-0}" -eq 0 ]]; then
      finding "check 19 — $L the migration left a $shape .agents alone but did not report it"
    fi
  done
  # ── 20–21. D76's outside-link pair ─────────────────────────────────────────────
  if [[ "$OUT_STATUS" -ne 0 ]]; then
    finding "check 20 — $L the update across $SM_D76_VERSION with .agents linked outside the project failed (exit $OUT_STATUS) — see $OUT_LOG"
  else
    [[ "$OUT_AFTER_TARGET" == "$OUT_TARGET" ]] \
      || finding "check 20 — $L the outside .agents link was not restored unchanged: it is '$OUT_AFTER_TARGET', it was '$OUT_TARGET'"
    $OUT_HELD_LEFT && finding "check 20 — $L the update left $SM_OUTSIDE_HELD behind"
    [[ -z "$OUT_DIRTY" ]] || finding "check 20 — $L Git sees the outside link changed after the update: $OUT_DIRTY"
    grep -qF "restored .agents -> $OUT_TARGET" "$OUT_LOG" 2>/dev/null \
      || finding "check 20 — $L the update did not print the outside link's restore — see $OUT_LOG"
  fi
  [[ "$OUT_SUMS_AFTER" == "$OUT_SUMS_BEFORE" ]] \
    || finding "check 20 — $L an update wrote into the folder outside the project that .agents links to"
  if [[ "$OUT_STATUS" -eq 0 ]]; then
    if [[ "$STRAND_STATUS" -eq 0 ]]; then
      finding "check 21 — $L the update meant to stop between the stages (a changed BRAND_KIND) was accepted, so no stranded hold was tested"
    elif ! $STRAND_HELD; then
      finding "check 21 — $L the update that stopped did not leave the link held as $SM_OUTSIDE_HELD (exit $STRAND_STATUS) — see $STRAND_LOG"
    elif ! grep -qF "$SM_OUTSIDE_FIX" "$STRAND_LOG" 2>/dev/null; then
      finding "check 21 — $L the update that stopped with the link held did not print the hand fix '$SM_OUTSIDE_FIX'"
    elif ! grep -F 'agents-outside-link:' "$STRAND_LOG" 2>/dev/null | grep -qF "$SM_OUTSIDE_CHECK"; then
      finding "check 21 — $L the hold stage did not print the hand fix's first step '$SM_OUTSIDE_CHECK'"
    elif grep -vF 'agents-outside-link:' "$STRAND_LOG" 2>/dev/null | grep -qF "$SM_OUTSIDE_FIX"; then
      finding "check 21 — $L the update printed the bare '$SM_OUTSIDE_FIX' outside the hold stage's fix (_message_before_update?): run while .agents stands, it moves the held link into the folder outside the project"
    elif [[ -n "$STRAND_FIXED_DIRTY" || "$STRAND_FIXED_TARGET" != "$OUT_TARGET" ]]; then
      finding "check 21 — $L the printed hand fix did not restore the project (status '$STRAND_FIXED_DIRTY'; .agents -> '$STRAND_FIXED_TARGET')"
    fi
  fi
  # ── 23. A stop after the render: the hand fix, its control, and a held link found ──
  local fixed="a link to $OUT_TARGET; held link gone"
  if [[ "$OUT_STATUS" -eq 0 && "$CRASH_STATUS" -eq 99 ]]; then
    finding "check 23 — $L the stop after the render could not be set up (a clone, or the scratch $SM_CRASH_VERSION) — see $W/mig.log"
  elif [[ "$OUT_STATUS" -eq 0 ]]; then
    if [[ "$CRASH_STATUS" -eq 0 ]]; then
      finding "check 23 — $L the update meant to stop after its render (a failing after-stage entry in $SM_CRASH_VERSION) succeeded, so no stop after the render was tested — see $CRASH_LOG"
    elif ! $CRASH_HELD; then
      finding "check 23 — $L the update that stopped after its render did not leave the link held as $SM_OUTSIDE_HELD — see $CRASH_LOG"
    elif [[ "$CRASH_LEFT" != absent ]]; then
      finding "check 23 — $L the update that stopped after its render left .agents as $CRASH_LEFT, not absent: /.agents is in _skip_if_exists, so Copier must leave it out of the diff it applies and never put it back (DESIGN.md D76, D85) — see $CRASH_LOG"
    elif [[ "$CRASH_FIXED" != "$fixed" ]]; then
      finding "check 23 — $L the hand fix, run step by step where the stop left .agents absent, did not put the held link back: $CRASH_FIXED — see $CRASH_LOG"
    elif [[ "$CRASH_STANDING" != "a link to $OUT_TARGET" ]]; then
      finding "check 23 — $L git reset --hard on the stopped project left .agents as ${CRASH_STANDING:-nothing}, not the committed link, so the hand fix with .agents standing was not tested — see $CRASH_LOG"
    elif [[ "$CRASH_STANDING_FIXED" != "$fixed" ]]; then
      finding "check 23 — $L the hand fix, run step by step with .agents standing again after git reset --hard, did not put the held link back: $CRASH_STANDING_FIXED — see $CRASH_LOG"
    elif [[ -n "$CRASH_FIXED_DIRTY" || "$CRASH_FIXED_TARGET" != "$OUT_TARGET" ]]; then
      finding "check 23 — $L discarding the stopped update after the hand fix did not leave the project clean (status '$CRASH_FIXED_DIRTY'; .agents -> '$CRASH_FIXED_TARGET')"
    elif ! $CRASH_CONTROL_WROTE; then
      finding "check 23 — $L the control no longer shows the hazard: the bare '$SM_OUTSIDE_FIX', run while .agents stands again after git reset --hard, did not write the held link into the folder outside the project"
    fi
    [[ "$CRASH_SUMS_AFTER" == "$CRASH_SUMS_BEFORE" ]] \
      || finding "check 23 — $L the stop after the render, or the hand fix, wrote into the folder outside the project that .agents links to"
    if ! $CRASH_FOUND_HELD; then
      finding "check 23 — $L with a held link committed beside an identical .agents, the next update's hold stage did not say so and ask for 'rm $SM_OUTSIDE_HELD' — see $W/crash-found.log"
    elif [[ -n "$CRASH_FOUND_MOVED" ]]; then
      finding "check 23 — $L with a held link committed beside an identical .agents, the next update moved something: $CRASH_FOUND_MOVED"
    fi
  fi
  if [[ "$AGAIN_STATUS" -ne 0 || -n "$AGAIN_DIRTY" ]]; then
    finding "check 15 — $L a second update with no template change was not a no-op (exit $AGAIN_STATUS; $(printf '%s\n' "$AGAIN_DIRTY" | grep -c . || true) path(s) changed)"
  fi
}

self_test() {
  local tmp h
  bold "▸ $SCRIPT_NAME --self-test"; log ""
  copier_init
  tmp="$(sm_mktemp)"
  # shellcheck disable=SC2064
  trap "rm -rf '$tmp'" RETURN
  h="$tmp/held"
  sm_fixture_template "$tmp/fixture" >/dev/null
  mkdir -p "$tmp/w"
  run_flow "$tmp/fixture" author-nonfiction "$tmp/w"
  st_baseline "real updates of the fixture template"

  COPY_STATUS=1;   probe "check 1 fires when the render fails" "check 1"; COPY_STATUS=0
  UPDATE_STATUS=1; probe "check 2 fires when the update fails" "check 2"; UPDATE_STATUS=0
  cp "$PROJ/.claude/MEMORY.md" "$h"; grep -vF "$MEMORY_MARK" "$h" > "$PROJ/.claude/MEMORY.md"
  probe "check 3 fires when the MEMORY entry is lost" "check 3"; cp "$h" "$PROJ/.claude/MEMORY.md"
  cp "$PROJ/$TOKENS" "$h"; grep -vF "$TOKENS_MARK" "$h" > "$PROJ/$TOKENS"
  probe "check 4 fires when the tokens.css edit is lost" "check 4"; cp "$h" "$PROJ/$TOKENS"
  mkdir -p "$PROJ/${DELETED[0]}"; probe "check 5 fires when an example comes back" "check 5"; rm -rf "${PROJ:?}/${DELETED[0]}"
  mv "$PROJ/$PUBLISH_LOG" "$h"; probe "check 6 fires when publish-log.md is not recreated" "check 6"; mv "$h" "$PROJ/$PUBLISH_LOG"
  cp "$PROJ/$OWN_PIECE" "$h"; printf 'tidied\n' >> "$PROJ/$OWN_PIECE"; probe "check 7 fires when the author's piece changes" "check 7"; cp "$h" "$PROJ/$OWN_PIECE"
  cp "$PROJ/$TARGET_REL" "$h"; grep -vF "$TEMPLATE_MARK" "$h" > "$PROJ/$TARGET_REL"
  probe "check 8 fires when the template change does not arrive" "check 8"; cp "$h" "$PROJ/$TARGET_REL"
  printf 'x\n' > "$PROJ/README.md.rej"; probe "check 9 fires on a rejected hunk" "check 9"; rm -f "$PROJ/README.md.rej"
  SWITCH_STATUS=0; probe "check 10 fires when a BRAND_KIND change is accepted" "check 10"; SWITCH_STATUS=1
  cp "$SWITCH_LOG" "$h"; grep -vF "$SM_KIND_REFUSAL" "$h" > "$SWITCH_LOG" || true
  probe "check 10 fires when the update failed for another reason" "check 10 — [author-nonfiction] the BRAND_KIND change failed"; cp "$h" "$SWITCH_LOG"
  SWITCH_DIRTY=" M README.md"; probe "check 11 fires when the refused update touched a file" "check 11"; SWITCH_DIRTY=""
  SWITCH_RECORDED=business; probe "check 11 fires when the answers record the new BRAND_KIND" "check 11"; SWITCH_RECORDED=author-nonfiction
  cp "$UPDATE_LOG" "$h"; grep -vF "Before you answer" "$h" > "$UPDATE_LOG" || true
  probe "check 12 fires when the removal warning is not printed" "check 12 — [author-nonfiction] copier update printed no removal warning"; cp "$h" "$UPDATE_LOG"
  sed -i 's/facebook/f-book/g' "$UPDATE_LOG"
  probe "check 12 fires when the warning leaves a platform out" "check 12 — [author-nonfiction] the removal warning does not name facebook"; cp "$h" "$UPDATE_LOG"
  grep -vF "If this update stops" "$h" > "$UPDATE_LOG" || true
  probe "check 22 fires when the crash pointer is not printed" "check 22 — [author-nonfiction] _message_before_update does not end with the crash pointer (none"; cp "$h" "$UPDATE_LOG"
  sed -i "/command to use\.\$/a\\A line after the pointer." "$UPDATE_LOG"
  probe "check 22 fires when the message does not end with the pointer" "check 22 — [author-nonfiction] _message_before_update does not end with the crash pointer"; cp "$h" "$UPDATE_LOG"
  REMOVE_STATUS=1; probe "check 13 fires when taking a platform away fails" "check 13 — [author-nonfiction] the update taking"; REMOVE_STATUS=0
  REMOVED="$REMOVED production/src/audiobook/CONTEXT.md"
  probe "check 13 fires when taking a platform away deletes something else" "check 13 — [author-nonfiction] taking podcast away deleted"; REMOVED="${REMOVED% *}"
  REMOVE_CONFLICTS="README.md.rej"; probe "check 13 fires when taking a platform away leaves a conflict" "check 13"; REMOVE_CONFLICTS=""
  mv "$PROJ/$FEED_DIR/harbour-lane-talks.toml" "$h"
  probe "check 13 fires when taking podcast away also deletes the author's show register" "check 13 — [author-nonfiction] taking podcast away deleted the author's $FEED_DIR/harbour-lane-talks.toml"
  mv "$h" "$PROJ/$FEED_DIR/harbour-lane-talks.toml"
  cp "$PROJ/$FEED_DIR/harbour-lane-talks.feed.xml" "$h"; printf '<!-- rewritten -->\n' >> "$PROJ/$FEED_DIR/harbour-lane-talks.feed.xml"
  probe "check 13 fires when taking podcast away changes the author's saved feed" "check 13 — [author-nonfiction] taking podcast away changed the author's $FEED_DIR/harbour-lane-talks.feed.xml"
  cp "$h" "$PROJ/$FEED_DIR/harbour-lane-talks.feed.xml"
  printf 'x\n' > "$PROJ/$DELETED_SHARED"; probe "check 14 fires when a deleted shared file comes back" "check 14 — [author-nonfiction] the shared $DELETED_SHARED"; rm -f "$PROJ/$DELETED_SHARED"
  cp "$PROJ/$EDITED_SHARED" "$h"; grep -vF "$SHARED_MARK" "$h" > "$PROJ/$EDITED_SHARED"
  probe "check 14 fires when the edit to a shared file is lost" "check 14 — [author-nonfiction] the author's edit"; cp "$h" "$PROJ/$EDITED_SHARED"
  rm "$PROJ/.agents/skills"; ln -s "$SM_AGENTS_SKILLS_LINK" "$PROJ/.agents/skills"
  probe "check 14 fires when an author's skills link target is replaced" "check 14 — [author-nonfiction] the author's shared agent path .agents/skills"
  rm "$PROJ/.agents/skills"; ln -s ../author-agent-tree "$PROJ/.agents/skills"
  printf '{"mcpServers": {}}\n' > "$PROJ/.claude/mcp_config.json"
  probe "check 14 fires when the retired .claude/mcp_config.json reappears" "check 14 — [author-nonfiction] the author's shared agent path .claude/mcp_config.json"
  rm -f "$PROJ/.claude/mcp_config.json"
  printf '# Recreated entrypoint\n' > "$PROJ/GEMINI.md"
  probe "check 14 fires when a deleted agent entrypoint is recreated" "check 14 — [author-nonfiction] the author's shared agent path GEMINI.md"
  rm "$PROJ/GEMINI.md"
  cp "$PROJ/.codex/config.toml" "$h"; printf '# Replaced settings\n' > "$PROJ/.codex/config.toml"
  probe "check 14 fires when authored Codex settings are replaced" "check 14 — [author-nonfiction] the author's shared agent path .codex/config.toml"
  cp "$h" "$PROJ/.codex/config.toml"
  local agent_root="${AGENT_COPY_ROOT[directory]}"
  cp "$agent_root/AGENTS.md" "$h"; printf '# Overwritten instructions\n' > "$agent_root/AGENTS.md"
  probe "check 16 fires when copy overwrites an existing agent entrypoint" "check 16 — [author-nonfiction] copy changed the author's agent directory path AGENTS.md"
  cp "$h" "$agent_root/AGENTS.md"
  agent_root="${AGENT_COPY_ROOT[link]}"
  rm "$agent_root/.agents"; ln -s .claude "$agent_root/.agents"
  probe "check 16 fires when copy replaces an existing alias" "check 16 — [author-nonfiction] copy changed the author's agent link path .agents"
  rm "$agent_root/.agents"; ln -s .owner-agents "$agent_root/.agents"
  ln -s ../.claude/skills "$agent_root/.owner-agents/skills"
  probe "check 16 fires when copy writes through an existing .agents link" "check 16 — [author-nonfiction] copy wrote .owner-agents/skills into the author's existing agent link"
  rm "$agent_root/.owner-agents/skills"
  agent_root="${AGENT_COPY_ROOT[legacy]}"
  printf '{"mcpServers": {}}\n' > "$agent_root/.claude/mcp_config.json"
  probe "check 16 fires when copy writes .claude/mcp_config.json through the 0.4.1 link" "check 16 — [author-nonfiction] copy wrote .claude/mcp_config.json into the author's existing agent legacy"
  rm -f "$agent_root/.claude/mcp_config.json"
  agent_root="${AGENT_COPY_ROOT[skills-link]}"
  ln -s ../.claude/skills/run-media-workflow "$agent_root/.owner-skills/media"
  probe "check 16 fires when copy writes through an existing .agents/skills link" "check 16 — [author-nonfiction] copy wrote .owner-skills/media into the author's existing agent skills-link"
  rm "$agent_root/.owner-skills/media"
  AGENT_COPY_ARGS[skills-link]='--exclude /.agents'
  probe "check 16 fires when a skills link elsewhere is given an exclude" "check 16 — [author-nonfiction] the pre-copy check gave '--exclude /.agents' for the existing agent skills-link"
  AGENT_COPY_ARGS[skills-link]=''
  AGENT_COPY_ARGS[skills-dir]='--exclude /.agents'
  probe "check 16 fires when a real skills folder excludes the whole .agents" "check 16 — [author-nonfiction] the pre-copy check gave '--exclude /.agents' for the existing agent skills-dir"
  AGENT_COPY_ARGS[skills-dir]='--exclude /.agents/skills'
  MIG_STATUS=1; probe "check 17 fires when the update across v0.4.2 fails" "check 17 — [author-nonfiction] the update across"; MIG_STATUS=0
  mv "$MIG_PROJ/.agents" "$tmp/mig-held"; ln -s .claude "$MIG_PROJ/.agents"
  probe "check 17 fires when the 0.4.1 link survives the update" "check 17 — [author-nonfiction] the migration left .agents as a link"
  rm "$MIG_PROJ/.agents"; mv "$tmp/mig-held" "$MIG_PROJ/.agents"
  cp "$MIG_PROJ/.agents/mcp_config.json" "$h"; printf '{"mcpServers": {}}\n' > "$MIG_PROJ/.agents/mcp_config.json"
  probe "check 17 fires when the author's MCP file is not the one moved" "check 17 — [author-nonfiction] .agents/mcp_config.json is missing or is not"
  cp "$h" "$MIG_PROJ/.agents/mcp_config.json"
  cp "$MIG_LOG" "$h"; sed -i 's/Review and commit: git add -A \.agents .*/Review and commit: git add -A .agents \&\& git status/' "$MIG_LOG"
  probe "check 17 fires when the commit hint leaves out the moved file" "check 17 — [author-nonfiction] the commit hint does not name the moved"
  cp "$h" "$MIG_LOG"
  local gh_held="$MIG_GH_OUT"
  MIG_GH_OUT="${gh_held//https:\/\/github.com\//gh:}"
  probe "check 17 fires when the 'run again' line keeps the gh: shorthand" "check 17 — [author-nonfiction] the 'run again' line passes Copier's gh: shorthand"
  MIG_GH_OUT="${gh_held//git add -A .agents /git add -A .agents .claude/mcp_config.json }"
  probe "check 17 fires when the commit hint names a file that never existed" "check 17 — [author-nonfiction] the commit hint names .claude/mcp_config.json"
  MIG_GH_OUT="$gh_held"
  MIG_AGAIN_DIFF=2; probe "check 18 fires when a second run changes the project" "check 18 — [author-nonfiction] the migration run again changed 2"; MIG_AGAIN_DIFF=0
  MIG_UPD_AGAIN_RAN=true; probe "check 18 fires when a second update reruns the migration" "check 18 — [author-nonfiction] a second update"; MIG_UPD_AGAIN_RAN=false
  MIG_SHAPE_DIFF[otherlink]=".agents"; probe "check 19 fires when the migration touches a link elsewhere" "check 19 — [author-nonfiction] the migration changed a otherlink"; MIG_SHAPE_DIFF[otherlink]=""
  MIG_SHAPE_SAID[textfile]=0; probe "check 19 fires when a skipped shape is not reported" "check 19 — [author-nonfiction] the migration left a textfile .agents alone but did not report it"; MIG_SHAPE_SAID[textfile]=1
  OUT_STATUS=1; probe "check 20 fires when the update over an outside link fails" "check 20 — [author-nonfiction] the update across"; OUT_STATUS=0
  local out_target="$OUT_AFTER_TARGET"
  OUT_AFTER_TARGET="not a link"; probe "check 20 fires when the outside link is not restored" "check 20 — [author-nonfiction] the outside .agents link was not restored"; OUT_AFTER_TARGET="$out_target"
  OUT_HELD_LEFT=true; probe "check 20 fires when the held link is left behind" "check 20 — [author-nonfiction] the update left $SM_OUTSIDE_HELD"; OUT_HELD_LEFT=false
  OUT_DIRTY="D .agents"; probe "check 20 fires when Git sees the link changed" "check 20 — [author-nonfiction] Git sees the outside link changed"; OUT_DIRTY=""
  cp "$OUT_LOG" "$h"; grep -vF 'restored .agents' "$h" > "$OUT_LOG" || true
  probe "check 20 fires when the restore is not printed" "check 20 — [author-nonfiction] the update did not print"; cp "$h" "$OUT_LOG"
  local out_sums="$OUT_SUMS_AFTER"
  OUT_SUMS_AFTER="$OUT_SUMS_AFTER"$'\n''mcp_config.json\tx'; probe "check 20 fires on a write into the outside folder" "check 20 — [author-nonfiction] an update wrote into the folder outside"; OUT_SUMS_AFTER="$out_sums"
  STRAND_HELD=false; probe "check 21 fires when a stopped update does not leave the link held" "check 21 — [author-nonfiction] the update that stopped did not leave"; STRAND_HELD=true
  cp "$STRAND_LOG" "$h"; grep -vF "$SM_OUTSIDE_FIX" "$h" > "$STRAND_LOG" || true
  probe "check 21 fires when a stranded hold does not print its fix" "check 21 — [author-nonfiction] the update that stopped with the link held did not print"; cp "$h" "$STRAND_LOG"
  STRAND_FIXED_DIRTY="?? $SM_OUTSIDE_HELD"; probe "check 21 fires when the printed fix leaves the project dirty" "check 21 — [author-nonfiction] the printed hand fix"; STRAND_FIXED_DIRTY=""
  sed -i 's/agents-outside-link: //' "$STRAND_LOG"
  probe "check 21 fires when the fix's first step does not come from the hold stage" "check 21 — [author-nonfiction] the hold stage did not print the hand fix's first step"; cp "$h" "$STRAND_LOG"
  printf '  If the update stops before it ends, run: %s\n' "$SM_OUTSIDE_FIX" >> "$STRAND_LOG"
  probe "check 21 fires when the message prints the bare mv again" "check 21 — [author-nonfiction] the update printed the bare"; cp "$h" "$STRAND_LOG"
  local crash_status="$CRASH_STATUS" crash_fixed="$CRASH_FIXED" crash_sums="$CRASH_SUMS_AFTER"
  local crash_left="$CRASH_LEFT" crash_standing="$CRASH_STANDING" crash_standing_fixed="$CRASH_STANDING_FIXED"
  CRASH_STATUS=0; probe "check 23 fires when the update meant to stop after its render succeeds" "check 23 — [author-nonfiction] the update meant to stop after its render"; CRASH_STATUS="$crash_status"
  CRASH_HELD=false; probe "check 23 fires when the stop after the render leaves no held link" "check 23 — [author-nonfiction] the update that stopped after its render did not leave"; CRASH_HELD=true
  CRASH_LEFT="a link to $OUT_TARGET"; probe "check 23 fires when the stop puts .agents back" "check 23 — [author-nonfiction] the update that stopped after its render left .agents as a link to"; CRASH_LEFT="$crash_left"
  CRASH_FIXED="a link to $OUT_TARGET; held link left"; probe "check 23 fires when the hand fix leaves the held link" "check 23 — [author-nonfiction] the hand fix, run step by step where the stop left"; CRASH_FIXED="$crash_fixed"
  CRASH_STANDING="absent"; probe "check 23 fires when .agents does not stand again for the second state" "check 23 — [author-nonfiction] git reset --hard on the stopped project left .agents as absent"; CRASH_STANDING="$crash_standing"
  CRASH_STANDING_FIXED="a link to $OUT_TARGET; held link gone (wrote outside)"; probe "check 23 fires when the hand fix writes outside with .agents standing" "check 23 — [author-nonfiction] the hand fix, run step by step with .agents standing"; CRASH_STANDING_FIXED="$crash_standing_fixed"
  CRASH_FIXED_DIRTY="?? $SM_OUTSIDE_HELD"; probe "check 23 fires when the discard leaves the project dirty" "check 23 — [author-nonfiction] discarding the stopped update"; CRASH_FIXED_DIRTY=""
  CRASH_CONTROL_WROTE=false; probe "check 23 fires when the control no longer shows the hazard" "check 23 — [author-nonfiction] the control no longer shows"; CRASH_CONTROL_WROTE=true
  CRASH_SUMS_AFTER="$CRASH_SUMS_AFTER"$'\n'"$SM_OUTSIDE_HELD"$'\t''x'; probe "check 23 fires on a write into the outside folder" "check 23 — [author-nonfiction] the stop after the render, or the hand fix, wrote"; CRASH_SUMS_AFTER="$crash_sums"
  CRASH_FOUND_HELD=false; probe "check 23 fires when a held link beside .agents is not reported" "check 23 — [author-nonfiction] with a held link committed beside an identical .agents, the next update's hold stage"; CRASH_FOUND_HELD=true
  CRASH_FOUND_MOVED=".agents"; probe "check 23 fires when a held link beside .agents makes the update move something" "check 23 — [author-nonfiction] with a held link committed beside an identical .agents, the next update moved"; CRASH_FOUND_MOVED=""
  AGAIN_DIRTY=" M README.md"; probe "check 15 fires when a second update changes a file" "check 15"; AGAIN_DIRTY=""
  probe_clean "the fixture's updates keep every promise again once every mutation is undone"
  st_finish "an update that keeps its promises from one that breaks them"
}

if $SELF_TEST; then
  self_test
  exit $?
fi

[[ -f "$SM_ROOT/copier.yml" ]] || die "no copier.yml at $SM_ROOT"
for k in $KINDS; do [[ " $SM_KINDS " == *" $k "* ]] || die "unknown BRAND_KIND: $k"; done
copier_init
bold "▸ $SCRIPT_NAME"
STATUS=0
for kind in $KINDS; do
  work="$(sm_mktemp)"
  run_flow "$SM_ROOT" "$kind" "$work"
  run_checks
  if [[ ${#FINDINGS[@]} -eq 0 ]]; then
    log "  ✓ $kind — edits kept, examples still gone, publish-log.md recreated, own piece untouched, $TARGET_REL updated; shared files left alone; BRAND_KIND change refused untouched; warning printed; $REMOVE_PLATFORM taken away with exactly its $(wc -w <<< "$REMOVE_WANT") file(s)${FIXTURE_SUMS[*]:+, the show register and saved feed kept}; a second update a no-op; a stop after the render undone by the hand fix, with .agents absent and standing again"
    sm_rmtree "$work"
  else
    bold "✗ $kind — ${#FINDINGS[@]} finding(s) (work kept in $work; Copier's output in $work/flow.log):"
    print_findings
    # On a CI runner the work directory is gone once the job ends, so show Copier's output here.
    if [[ "${GITHUB_ACTIONS:-}" == true ]]; then
      echo "::group::Copier output for $kind (last 80 lines of flow.log)"
      tail -n 80 "$work/flow.log" 2>/dev/null || true
      echo "::endgroup::"
    fi
    STATUS=1
  fi
done
log ""
[[ "$STATUS" -eq 0 ]] && { bold "✓ copier update keeps every ownership promise."; exit 0; }
log "  Each promise rests on one copier.yml line: _skip_if_exists for seeds, the copy-only"
log "  _exclude gates for examples and the shared files (DESIGN.md Sections 3.1–3.6), BRAND_KIND's"
log "  validator with _external_data (D14), the gated _exclude lines and _message_before_update (D16)."
exit 1
