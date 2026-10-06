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
#                  Sixteen checks per brand kind:
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
#                       D73 extends this to all seven agent paths, preserving an edited
#                       alias target and native configuration as well as deleted entrypoints.
#                   15. A second update with no template change leaves `git status
#                       --porcelain` empty.
#
#                   16. Copies over existing agent entrypoints, configuration, a real .agents
#                       directory and a differently targeted alias preserve every prior byte
#                       and link target and explain manual setup (D73).
#                       A real directory uses D73's pre-copy --exclude /.agents procedure.
#
#                  Copier prints a MissingFileWarning on a fresh copy and on every update (the
#                  previous answers are read through _external_data, D14). It is expected and
#                  never a finding: only exit statuses, messages and files are judged.
#
#                  Numbers are stable identifiers. Append, never renumber.
#
#                  What it CANNOT check: an upgrade from a released version (there is none
#                  before 0.1.0; the first release that moves a folder writes its migration and
#                  adds its flow here), or a project applied over syntek-author, which is
#                  coexist-test.sh's.
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
declare -A FIXTURE_SUMS=() AGENT_EXPECTED=() AGENT_COPY_ROOT=() AGENT_COPY_STATUS=() AGENT_COPY_SUMS=()

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
  REMOVE_WANT=""; FIXTURE_SUMS=(); AGENT_EXPECTED=(); AGENT_COPY_ROOT=(); AGENT_COPY_STATUS=(); AGENT_COPY_SUMS=()
  : > "$UPDATE_LOG"; : > "$SWITCH_LOG"
  sm_snapshot "$src" "$tpl" >>"$log" 2>&1 || die "could not snapshot $src"

  sm_render "$tpl" "$PROJ" "$KIND" >>"$log" 2>&1 || COPY_STATUS=$?
  [[ "$COPY_STATUS" -eq 0 ]] || return 0
  [[ -d "$PROJ/.git" ]] || sm_git "$PROJ" init -q
  sm_commit_all "$PROJ" 'generated'

  # D73: fresh copies must preserve both an existing real alias directory and another link.
  local shape target path digest
  local -a copy_args
  for shape in directory link; do
    target="$W/agent-copy-$shape"; AGENT_COPY_ROOT["$shape"]="$target"
    mkdir -p "$target/.claude" "$target/.codex"
    for path in AGENTS.md GEMINI.md .codex/config.toml .codex/CONTEXT.md .codex/CLAUDE.md .claude/mcp_config.json; do
      printf '# Existing author configuration: preserve it.\n' > "$target/$path"
    done
    if [[ "$shape" == directory ]]; then
      mkdir "$target/.agents"; printf 'Owner skill tree.\n' > "$target/.agents/keep.md"
    else
      mkdir "$target/.owner-agents"; printf 'Owner skill tree.\n' > "$target/.owner-agents/keep.md"
      ln -s .owner-agents "$target/.agents"
    fi
    while IFS=$'\t' read -r path digest; do
      AGENT_COPY_SUMS["$shape:$path"]="$digest"
    done < <(hash_tree "$target")
    AGENT_COPY_STATUS["$shape"]=0
    # D73's documented pre-copy check: Copier cannot skip a link landing on a real directory.
    copy_args=()
    if [[ -d "$target/.agents" && ! -L "$target/.agents" ]]; then
      copy_args+=(--exclude /.agents)
    fi
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
  for e in AGENTS.md GEMINI.md .agents .codex/config.toml .codex/CONTEXT.md .codex/CLAUDE.md .claude/mcp_config.json; do
    case "$e" in
      GEMINI.md|.codex/CONTEXT.md|.claude/mcp_config.json) rm -f "$PROJ/$e" ;;
      .agents) rm -f "$PROJ/$e"; ln -s ../author-agent-tree "$PROJ/$e" ;;
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
  return 0
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
  done
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
  rm "$PROJ/.agents"; ln -s .claude "$PROJ/.agents"
  probe "check 14 fires when an author alias target is replaced" "check 14 — [author-nonfiction] the author's shared agent path .agents"
  rm "$PROJ/.agents"; ln -s ../author-agent-tree "$PROJ/.agents"
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
    log "  ✓ $kind — edits kept, examples still gone, publish-log.md recreated, own piece untouched, $TARGET_REL updated; shared files left alone; BRAND_KIND change refused untouched; warning printed; $REMOVE_PLATFORM taken away with exactly its $(wc -w <<< "$REMOVE_WANT") file(s)${FIXTURE_SUMS[*]:+, the show register and saved feed kept}; a second update a no-op"
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
