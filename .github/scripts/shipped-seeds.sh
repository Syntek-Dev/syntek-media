#!/usr/bin/env bash
#
# shipped-seeds.sh — Verify the seeds ship empty, wired, and only where they belong.
#
#                    A seed (`_skip_if_exists`) is written once and never again: the author's
#                    copy is never overwritten, and a deleted one comes back on the next
#                    update. That makes a polluted seed a one-way door (SB rule 21) — an entry
#                    that ships in the template's MEMORY.md, rights register or footage
#                    manifest lands in every project and no update can retract it — so emptiness
#                    is AUDITED, not trusted (DESIGN.md Section 3.1). Seed-once examples are the
#                    opposite contract: copied on `copy`, excluded on `update`, so an example the
#                    author deleted stays deleted (Section 3.2). The nineteen shared paths are a third:
#                    copy only, never on update, never recreated (D11, Section 3.6), and they need
#                    BOTH their copier.yml lines — without the update gate a file the author
#                    deleted comes back from media's copy inside syntek-author's project
#                    (Section 10). And the author-owned folders ship their pair and nothing else
#                    (Section 3.3), because anything else in them is the template writing into
#                    the author's space — and the output folders ship their README.md alone,
#                    which only a `!` negation listed above every gated _exclude line can
#                    promise, because Copier obeys the last pattern that matches (D19, Section 3.5).
#
#                    Twenty-two checks:
#                      1. Every DESIGN.md seed and shared file is listed in copier.yml's
#                         _skip_if_exists.
#                      2. Every _skip_if_exists entry names a file under template/.
#                      3. Every seed-once example has its copy-only _exclude line, gated exactly
#                         "_copier_operation == 'update' or not SEED_EXAMPLES".
#                      4. Every seed-once example exists under template/.
#                      5. .claude/MEMORY.md carries the six H2s: Facts · Decisions · Feedback ·
#                         Status · Open questions · Sensitivities.
#                      6. .claude/MEMORY.md carries no entry (a "- **" bullet).
#                      7. A seed carries an entry: in Markdown a filled table row or a dated
#                         bullet; in TOML a table ([…] or [[…]]) or a key outside a comment. A
#                         table header with no rows is empty: the website and blog profiles'
#                         `## Sites` and the newsletter profile's `## Lists` ship that way
#                         (DESIGN.md D61, Section 6.15).
#                      8. Each of the nineteen shared paths has its update-gated _exclude line
#                         ("_copier_operation == 'update'"), and nothing else carries that gate.
#                      9. A Markdown register or brand seed lacks the seeded-stub banner. Index
#                         pairs carry none: a pair is navigation.
#                     10. .mcp.json is exactly {"mcpServers": {}} (DESIGN.md D19, D21).
#                     11. A pair-only folder holds something other than its pair, a nested
#                         .gitignore or .gitattributes, a declared seed or a seed-once example;
#                         or a sub-folder that is not itself pair-only, an example, or a
#                         README-only generated/, renders/ or raw/ folder. The show registers'
#                         folder, publishing/src/podcast/ (D59), is one: a register or a feed
#                         that a toolkit run inside template/ left there would ship. So are the
#                         tracked timing and scene folders, production/src/timing/ and
#                         production/src/scenes/ (D64): a piece's words, mouth cues, cue index or
#                         scene code left there would ship.
#                     12. .claude/settings.json breaks DESIGN.md D13: model opus,
#                         autoCompactEnabled false, no hooks key, exactly the three denies, the
#                         six allows, the nine ElevenLabs asks and the two voice remix run asks
#                         (D82) of _common.sh's lists, and no
#                         owner-specific key (effortLevel, ultracode, enabledPlugins, disable*).
#                     13. .claude/settings.json does not parse as JSON. Read only where the file
#                         is plain JSON (every render; the source while it holds no block).
#                     14. An index seed (a docs/project/ or workflows/local/ pair) lists an entry
#                         in its directory tree: a line naming anything but the pair, a
#                         workflow's four files or a placeholder (<…>, NN-…, kebab-…).
#                     15. A brand seed (tokens.css, previews/thumbnail.html, previews/card.html,
#                         voice.md, a platform profile) has no open `AUTHOR TO CONFIRM` slot:
#                         every brand fact is the author's call, so a brand seed with none left
#                         has shipped somebody's brand.
#                     16. A `!` negation in _exclude brings back anything but an output folder's
#                         own README.md (anchored, no glob, the folder a generated/, renders/ or
#                         raw/), or is listed below the first gated line, or sits inside a gated
#                         line (DESIGN.md Section 3.5, Section 10, D19). Copier obeys the last
#                         pattern that matches a path, so a negation after a shut gate brings
#                         its path back: the audiobook folder's two READMEs would ship to a brand
#                         that makes no audiobooks. shipped-brands.sh check 12 proves the renders.
#                     17. A retired shared path (D76: .claude/mcp_config.json) lacks its
#                         unconditional, anchored _exclude line, or a shared path that still
#                         ships carries one. The retired path keeps its two D11 lines (checks 1
#                         and 8) and its file under template/ (check 2): only the third line
#                         stops it shipping, on copy as on update.
#                     18. template/.agents is not a real folder holding exactly two entries:
#                         skills, the relative link ../.claude/skills, and mcp_config.json
#                         (DESIGN.md D76, Section 3.7).
#                     19. copier.yml's _migrations has no v0.4.2 entry running
#                         migrations/v0.4.2-agents-folder.py after the update, or a migration
#                         names a script that is not in migrations/ at this repository's root
#                         (D76; copier.yml's house shape).
#                     20. copier.yml's _migrations does not open with D76's outside-link pair,
#                         the only entries keyed to no release (D11's second, transient
#                         exception): first an entry with no version: running
#                         migrations/agents-outside-link.py hold at _stage 'before', then one
#                         running it with restore at _stage 'after', so the link is held before
#                         the render and restored before every other after-stage migration; or
#                         any later entry carries no version:. Where _migrations is missing
#                         altogether, check 19 claims it and this check stays quiet.
#                     21. migrations/agents-outside-link.py is not syntek-author's family-shared
#                         script as media vendored it (DESIGN.md D85; syntek-author D48): its
#                         SHA-256 is not _common.sh's SM_OUTSIDE_SHA256, the value the release
#                         tag it was vendored from (SM_OUTSIDE_RELEASE) records for it in
#                         family-shared.json; or Git's index does not hold it at mode 100755
#                         (read with git ls-files -s). Only where this repository is not a Git
#                         work tree is the file's executable bit read instead; a .git that Git
#                         will not read (an ownership mismatch before safe.directory is set,
#                         say) stops the run with exit 2, never a fallback. The script is
#                         never edited here: one changed byte and media's updates print a hand
#                         fix that its README, its bridge and syntek-author's script do not. A
#                         missing script is check 19's.
#                     22. copier.yml's family-shared migrations block (D85; syntek-author D48)
#                         is not the family's byte for byte: the marker lines
#                         '# BEGIN family-shared migrations (D48)' and
#                         '# END family-shared migrations (D48)' do not each occur exactly once,
#                         or the lines strictly between them do not have _common.sh's
#                         SM_FAMILY_MIGRATIONS_SHA256, the value the same tag's
#                         family-shared.json records for the block. The block is how the
#                         vendored script runs: with Copier's own interpreter, hold first,
#                         restore before every other after-stage entry. Where _migrations is
#                         missing (check 19) or does not open with the outside-link pair
#                         (check 20), those claim it and this check stays quiet. An extra
#                         unversioned entry inside the block is two faults, so two findings:
#                         check 20's for the entry, this check's for the bytes.
#
#                    Checks 1–4, 8 and 16–22 read copier.yml, template/ and migrations/ (static,
#                    once; check 21 also reads Git's index). Checks 5–7 and 9–15 read every tree
#                    given — template/ by default, or renders — and skip a seed the tree does
#                    not ship.
#
#                    Over-author scope (DESIGN.md Section 7): on a <kind>--over-author tree,
#                    whose <tree>.owned lists the files media's copy added, checks 5, 6, 10, 12
#                    and 13 are skipped (the shared files are syntek-author's; coexist-test.sh
#                    check 12 proves them unchanged), and the rest read media-owned paths only.
#
#                    Numbers are stable identifiers. Append, never renumber.
#
#                    What it CANNOT check: that a writing rule in a seed is generic rather than
#                    one brand's preference. "No entries" is decidable; "no personal
#                    preferences" is not — scrub.sh catches the names, a reviewer the rest.
#                    Nor that SM_OUTSIDE_SHA256 and SM_FAMILY_MIGRATIONS_SHA256 are still the
#                    family's: checks 21 and 22 hold media to the tag it last vendored from, and
#                    a later tag is re-read by hand against its family-shared.json (D85). Check
#                    21 reads the mode the index holds, which a plain `git commit` records;
#                    `git commit -a` records the working tree's bit instead, which only CI's
#                    run on the pushed commit then reads.
#
# SELF-TEST. --self-test writes a fixture repository at runtime with every seed in shape,
#            proves it clean, then applies one mutation per check and asserts exactly one
#            finding each; then proves the over-author scope on a tree with a .owned list.
#
# Requirements: bash 4+, grep, awk, python3 (checks 10, 12 and 13), sha256sum or shasum
#               (checks 21 and 22), git (check 21, and the self-test). No network.
#
# Usage: shipped-seeds.sh [--root DIR] [--quiet] [--self-test] [--help] [<tree>...]
#
# Exit codes:  0 = every seed is wired and empty, every pair-only folder clean
#              1 = finding(s), or the self-test no longer separates
#              2 = script error (bad arguments, no copier.yml, no python3, no sha256 tool, no git,
#                  or a .git that Git will not read)

set -euo pipefail
SCRIPT_NAME="shipped-seeds.sh"
# shellcheck source=_common.sh
source "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/_common.sh"

SELF_TEST=false
TARGETS=()

usage() {
  cat <<'EOF'
shipped-seeds.sh — Verify the seeds ship empty, wired, and only where they belong

Usage: shipped-seeds.sh [--root DIR] [--quiet] [--self-test] [--help] [<tree>...]

  <tree>       A render to check as well (checks 5–7, 9–15); template/ is always checked
  --root DIR   The template repository (default: this repository)
  --quiet      Print findings only
  --self-test  Prove the checks still fire against a fixture written at runtime
  --help       Show this message

A <tree>.owned file beside a tree (written by generate-all.sh) marks an over-author tree and
narrows the checks to media's paths.
Exit codes: 0 = clean  1 = finding(s), or the self-test no longer separates
            2 = script error
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --root)      [[ $# -gt 1 ]] || die "--root needs a value"; SM_ROOT="$(cd "$2" && pwd)" || die "no such directory: $2"; shift 2 ;;
    --quiet|-q)  QUIET=true; shift ;;
    --self-test) SELF_TEST=true; shift ;;
    --help|-h)   usage; exit 0 ;;
    -*)          die "unknown argument: $1" ;;
    *)           TARGETS+=("$1"); shift ;;
  esac
done

COPIER="$SM_ROOT/copier.yml"
TPL="$SM_ROOT/template"
TREE=""

# The seeds by what the checks ask of them, from the catalogue in _common.sh (DESIGN.md 3.1).
MD_SEEDS="$SM_REGISTER_SEEDS brand/src/voice/voice.md $SM_PLATFORM_SEEDS"
TOML_SEEDS="$SM_TOML_SEEDS"
INDEX_SEEDS="$SM_INDEX_SEEDS"
BRAND_SEEDS="$SM_BRAND_SEEDS"

# Block delimiters removed, fenced code and HTML comments dropped: what an entry would look like.
readable() {
  sed -E 's/<:([^:]|:[^>])*:>//g' "$1" | awk '
    /^[[:space:]]*```/ { f = !f; next }
    f { next }
    /<!--/ && !/-->/ { c = 1; next }
    c && /-->/ { c = 0; next }
    c { next }
    { gsub(/<!--.*-->/, ""); print }'
}

register_entries() { # prints one line per entry found
  readable "$1" | awk '
    function placeholder(c) {
      gsub(/^[ \t]+|[ \t]+$/, "", c)
      return (c == "" || c ~ /^(—|-|–|…|\.\.\.|TBD|_[^_]*_|\*[^*]*\*|<[^>]*>|\[AWAITING USER INPUT\])$/)
    }
    /^[[:space:]]*\|/ {
      if ($0 ~ /^[[:space:]]*\|[[:space:]:|-]+\|[[:space:]]*$/ && $0 ~ /---/) { body = 1; next }
      if (!body) next
      n = split($0, cells, "|"); filled = 0
      for (i = 2; i < n; i++) if (!placeholder(cells[i])) filled = 1
      if (filled) print "table row: " substr($0, 1, 60)
      next
    }
    { body = 0 }
    /^[-*] (\*\*)?[0-9][0-9]\/[0-9][0-9]\/[0-9][0-9][0-9][0-9]/ { print "dated entry: " substr($0, 1, 60) }'
}

# A TOML seed ships header comments only (DESIGN.md Section 3.1): any table outside a comment
# is an entry, its keys with it, and so is a key before the first table. Block delimiters are
# removed first, so a source seed is read as the lines it renders to.
toml_entries() { # $1 = file → one line per entry
  sed -E 's/<:([^:]|:[^>])*:>//g' "$1" | awk '
    /^[[:space:]]*(#|$)/ { next }
    /^[[:space:]]*\[/ { print "a " $1 " table"; t = 1; next }
    t { next }
    { l = $0; sub(/^[[:space:]]+/, "", l); print "a value: " substr(l, 1, 40) }'
}

# The names an index seed's directory tree lists, other than the pair, a workflow's four files
# and placeholders. Tree lines live in fenced code, which readable() drops, so this reads the
# fences themselves. awk alternation, not a bracket class, for the box-drawing bytes (mawk).
tree_entries() { # $1 = file → one listed name per line
  sed -E 's/<:([^:]|:[^>])*:>//g' "$1" | awk '
    /^[[:space:]]*```/ { f = !f; next }
    !f { next }
    /(├|└)── / {
      line = $0; sub(/^.*(├|└)── /, "", line); split(line, a, /[ \t]+/); n = a[1]
      if (n ~ /^(CONTEXT|CLAUDE|STEPS|CHECKLIST)\.md$/ || n ~ /</ || n ~ /^NN-/ || n ~ /^kebab-/) next
      print n
    }'
}

static_checks() {
  local s e cond path
  local -A skip=() copy_only=() update_gated=()
  while IFS= read -r s; do [[ -n "$s" && "$s" != *'<:'* ]] && skip["${s#/}"]=1; done < <(yaml_list _skip_if_exists "$COPIER")

  # ── 1 and 2. _skip_if_exists against DESIGN.md and the disk ─────────────────
  for s in $SM_SEEDS $SM_SHARED; do
    [[ -n "${skip[$s]:-}" ]] && continue
    if is_shared "$s"; then
      finding "check 1 — $s is a shared file (DESIGN.md D11) but _skip_if_exists does not list it — a copy over syntek-author's project stops with 'Interactive session required'"
    else
      finding "check 1 — $s is a seed (DESIGN.md Section 3.1) but _skip_if_exists does not list it — the next update overwrites the author's copy"
    fi
  done
  for s in "${!skip[@]}"; do
    [[ "$s" == *[*?[]* ]] && continue
    [[ -e "$TPL/$s" ]] || finding "check 2 — _skip_if_exists lists /$s, which is not under template/"
  done

  # ── 3, 4 and 8. Seed-once examples and the copy-only shared files ───────────
  while IFS=$'\t' read -r cond path; do
    cond="$(norm_expr "$cond")"
    [[ "$cond" == "$SM_EXAMPLE_GATE" ]] && copy_only["$path"]=1
    [[ "$cond" == "$SM_SHARED_GATE" ]] && update_gated["$path"]=1
  done < <(exclude_gates "$COPIER")
  for e in $SM_EXAMPLES; do
    [[ -n "${copy_only[$e]:-}" ]] || finding "check 3 — the example $e has no copy-only _exclude line ($SM_EXAMPLE_GATE) — a deleted example would come back"
    [[ -e "$TPL/$e" ]] || finding "check 4 — the example $e is not under template/"
  done
  for s in $SM_SHARED; do
    [[ -n "${update_gated[$s]:-}" ]] || finding "check 8 — the shared file $s has no update-gated _exclude line ($SM_SHARED_GATE) — an update would recreate it after the author deleted it (DESIGN.md Section 10)"
  done
  for s in "${!update_gated[@]}"; do
    is_shared "$s" || finding "check 8 — /$s carries the shared files' update gate ($SM_SHARED_GATE) but is not one of the nineteen (DESIGN.md D11): it would never reach a project by update"
  done

  # ── 16. Negations: an output folder's own README.md, above every gated line ──
  # Copier obeys the last pattern that matches a path, so a `!` line listed after a gate brings
  # its path back with the gate shut (DESIGN.md Section 3.5, Section 10, D19).
  local item n=0 first_gated=0 d
  local -a negs=()
  while IFS= read -r item; do
    n=$((n + 1))
    if [[ "$item" == *'<:'* ]]; then
      [[ "$first_gated" -eq 0 ]] && first_gated=$n
      path="$(split_gated_item "$item" | cut -f2)"
      [[ "$path" == '!'* ]] && finding "check 16 — a gated _exclude line negates ${path#!} back in; a negation is never gated, and is listed above every gated line (DESIGN.md Section 3.5)"
    elif [[ "$item" == '!'* ]]; then
      negs+=("$n"$'\t'"${item#!}")
    fi
  done < <(yaml_list _exclude "$COPIER")
  for item in "${negs[@]}"; do
    n="${item%%$'\t'*}"; path="${item#*$'\t'}"; d="${path%/README.md}"
    if [[ "$path" != /*/README.md || "$path" == *[*?[]* || " $SM_README_ONLY_DIRS " != *" ${d##*/} "* ]]; then
      finding "check 16 — _exclude negates $path back in, which is not an output folder's own README.md: only the README.md of a generated/, renders/ or raw/ folder, anchored, ever is (DESIGN.md Section 3.5, D42)"
    elif [[ "$first_gated" -gt 0 && "$n" -gt "$first_gated" ]]; then
      finding "check 16 — _exclude negates $path back in at item $n, after the first gated line (item $first_gated): a negation listed after a gate brings its path back with the gate shut — list it above every gated line (DESIGN.md Section 3.5, Section 10)"
    fi
  done

  # ── 17. A retired shared path: its two lines, its file, and a third line (D76) ──
  local -A plain=()
  while IFS= read -r item; do
    [[ "$item" == /* && "$item" != *'<:'* ]] && plain["${item#/}"]=1
  done < <(yaml_list _exclude "$COPIER")
  for s in $SM_SHARED_RETIRED; do
    [[ -n "${plain[$s]:-}" ]] || finding "check 17 — the retired shared path /$s has no unconditional _exclude line: it still ships on copy (DESIGN.md D76)"
  done
  for s in $SM_SHARED_SHIPPED; do
    [[ -n "${plain[$s]:-}" ]] && finding "check 17 — the shared path /$s carries an unconditional _exclude line: it would never ship (DESIGN.md D11, D76)"
  done

  # ── 18. The agent folder under template/ (D76) ──────────────────────────────
  local entries
  if [[ -L "$TPL/.agents" || ! -d "$TPL/.agents" ]]; then
    finding "check 18 — template/.agents is not a real folder (DESIGN.md D76)"
  else
    entries="$(find "$TPL/.agents" -mindepth 1 -maxdepth 1 -printf '%f\n' | LC_ALL=C sort | paste -sd' ' -)"
    [[ "$entries" == "mcp_config.json skills" ]] || finding "check 18 — template/.agents holds '${entries:-nothing}', not exactly mcp_config.json and skills (DESIGN.md D76)"
    [[ -L "$TPL/.agents/skills" && "$(readlink "$TPL/.agents/skills")" == "$SM_AGENTS_SKILLS_LINK" ]] \
      || finding "check 18 — template/.agents/skills is not the relative link $SM_AGENTS_SKILLS_LINK (DESIGN.md D76)"
  fi

  # ── 19. The D76 migration is declared, and every migration's script exists ──
  local mig
  mig="$(awk '/^_migrations:/ { on = 1; next } on && /^[A-Za-z_]/ { exit } on' "$COPIER")"
  if ! grep -qE "^[[:space:]]*-[[:space:]]+version:[[:space:]]+${SM_D76_VERSION}[[:space:]]*$" <<< "$mig" \
      || ! grep -qF "/$SM_D76_MIGRATION" <<< "$mig" || ! grep -qF "_stage == 'after'" <<< "$mig"; then
    finding "check 19 — _migrations has no $SM_D76_VERSION entry running $SM_D76_MIGRATION after the update (DESIGN.md D76)"
  fi
  while IFS= read -r item; do
    [[ -f "$SM_ROOT/$item" ]] || finding "check 19 — a migration runs $item, which is not in this repository (it is read from the template clone: _copier_conf.src_path)"
  done < <(grep -oE 'src_path *%>/migrations/[^" ]+' <<< "$mig" | sed -E 's#^.*%>/##')

  # ── 20. D76's outside-link pair opens _migrations; every other entry is versioned ──
  local pair_ok=false
  if [[ -n "$mig" ]]; then
    local -a ver=() cmd=() whn=()
    local n=0 i v c w
    while IFS=$'\t' read -r v c w; do
      ver+=("$v"); cmd+=("$c"); whn+=("$w"); n=$((n + 1))
    done < <(awk '
      /^[[:space:]]*#/ { next }
      /^  - / { n++; sub(/^  - /, "    ") }
      n && /^    version:/ { v[n] = $2 }
      n && /^    command:/ { c[n] = substr($0, index($0, "command:") + 9) }
      n && /^    when:/    { w[n] = substr($0, index($0, "when:") + 6) }
      END { for (i = 1; i <= n; i++) printf "%s\t%s\t%s\n", (v[i] == "" ? "-" : v[i]), c[i], w[i] }
    ' <<< "$mig")
    if [[ "$n" -lt 2 || "${ver[0]}" != - || "${ver[1]}" != - \
        || "${cmd[0]}" != *"/$SM_OUTSIDE_MIGRATION\" hold"* || "${whn[0]}" != *"_stage == 'before'"* \
        || "${cmd[1]}" != *"/$SM_OUTSIDE_MIGRATION\" restore"* || "${whn[1]}" != *"_stage == 'after'"* ]]; then
      finding "check 20 — _migrations does not open with D76's outside-link pair: an unversioned $SM_OUTSIDE_MIGRATION hold at _stage 'before', then restore at _stage 'after' (DESIGN.md D76, D11)"
    else
      pair_ok=true
    fi
    for ((i = 2; i < n; i++)); do
      [[ "${ver[$i]}" != - ]] && continue
      finding "check 20 — an unversioned _migrations entry runs $(grep -oE 'migrations/[^" ]+' <<< "${cmd[$i]}" || printf '%s' "${cmd[$i]}"): only D76's outside-link pair is keyed to no release (DESIGN.md D76; .claude/CLAUDE.md Section 9)"
    done
  fi

  # ── 21. The vendored outside-link script is the family's, byte for byte (D85) ──
  # The bytes are read from disk; the mode from Git's index, which a plain `git commit` records,
  # and from the executable bit only where SM_ROOT is in no Git work tree and holds no .git. A
  # .git that Git will not read (an ownership mismatch, say) is a script error, never a fallback.
  local ol="$SM_ROOT/$SM_OUTSIDE_MIGRATION" got mode
  if [[ -f "$ol" ]]; then
    got="$(sm_sha256 < "$ol")"
    [[ "$got" == "$SM_OUTSIDE_SHA256" ]] \
      || finding "check 21 — $SM_OUTSIDE_MIGRATION has SHA-256 ${got:0:12}…, not ${SM_OUTSIDE_SHA256:0:12}…, the value syntek-author's $SM_OUTSIDE_RELEASE records for it in family-shared.json: it is vendored byte for byte and never edited here (DESIGN.md D85; syntek-author D48)"
    if [[ "$(git -C "$SM_ROOT" rev-parse --is-inside-work-tree 2>/dev/null)" == true ]]; then
      mode="$(git -C "$SM_ROOT" ls-files -s -- "$SM_OUTSIDE_MIGRATION" 2>/dev/null | awk 'NR == 1 { print $1 }')"
      [[ "$mode" == "$SM_OUTSIDE_MODE" ]] \
        || finding "check 21 — Git's index holds $SM_OUTSIDE_MIGRATION at mode ${mode:-none (it is not in the index)}, not $SM_OUTSIDE_MODE, the mode syntek-author's $SM_OUTSIDE_RELEASE records for it (git update-index --chmod=+x; DESIGN.md D85)"
    elif [[ -e "$SM_ROOT/.git" || -L "$SM_ROOT/.git" ]]; then
      die "check 21 cannot read Git's index: $SM_ROOT/.git stands, but Git will not read it (an ownership mismatch? see git config safe.directory)"
    else
      [[ -x "$ol" ]] \
        || finding "check 21 — $SM_OUTSIDE_MIGRATION is not executable (outside a Git work tree, the executable bit stands for Git's $SM_OUTSIDE_MODE, the mode syntek-author's $SM_OUTSIDE_RELEASE records for it; DESIGN.md D85)"
    fi
  fi

  # ── 22. The family-shared migrations block is the family's, byte for byte (D85) ──
  # Where _migrations is missing (check 19) or does not open with the pair (check 20), those
  # claim it and this check stays quiet. An extra unversioned entry inside the block is two
  # faults: check 20 names the entry, this check the bytes.
  local nb ne blk
  nb="$(grep -cxF "$SM_FAMILY_MIGRATIONS_BEGIN" "$COPIER" || true)"
  ne="$(grep -cxF "$SM_FAMILY_MIGRATIONS_END" "$COPIER" || true)"
  if ! $pair_ok; then
    :
  elif [[ "$nb" -ne 1 || "$ne" -ne 1 ]]; then
    finding "check 22 — copier.yml carries $nb '$SM_FAMILY_MIGRATIONS_BEGIN' and $ne '$SM_FAMILY_MIGRATIONS_END' line(s), not one of each: the family-shared migrations block is taken whole (DESIGN.md D85; syntek-author D48)"
  else
    blk="$(awk -v b="$SM_FAMILY_MIGRATIONS_BEGIN" -v e="$SM_FAMILY_MIGRATIONS_END" '$0 == e { on = 0 } on { print } $0 == b { on = 1 }' "$COPIER" | sm_sha256)"
    [[ "$blk" == "$SM_FAMILY_MIGRATIONS_SHA256" ]] \
      || finding "check 22 — the lines between copier.yml's family-shared migrations markers have SHA-256 ${blk:0:12}…, not ${SM_FAMILY_MIGRATIONS_SHA256:0:12}…, the value syntek-author's $SM_OUTSIDE_RELEASE records for the block in family-shared.json: it is taken byte for byte and never edited here (DESIGN.md D85; syntek-author D48)"
  fi
}

json_check() { # $1 = mode (mcp|settings|parse), $2 = file → prints one problem per line
  SM_DENY="$(printf '%s\n' "${SM_SETTINGS_DENY[@]}")" \
  SM_ALLOW="$(printf '%s\n' "${SM_SETTINGS_ALLOW[@]}")" \
  SM_ASK="$(printf '%s\n' "${SM_SETTINGS_ASK[@]}")" \
  python3 - "$1" "$2" <<'PY'
import json, os, sys
mode, path = sys.argv[1], sys.argv[2]
try:
    data = json.load(open(path, encoding="utf-8"))
except Exception as exc:
    if mode == "parse":
        print(f"is not valid JSON ({exc.__class__.__name__}: {str(exc)[:60]})")
    sys.exit(0)
if mode == "parse":
    sys.exit(0)
if mode == "mcp":
    if data != {"mcpServers": {}}:
        print('is not exactly {"mcpServers": {}} — the template adds no server; ElevenLabs is user-scoped (DESIGN.md D21)')
    sys.exit(0)
if not isinstance(data, dict):
    print("is not a JSON object"); sys.exit(0)
if data.get("model") != "opus":
    print(f"model is {data.get('model')!r}, not 'opus'")
if data.get("autoCompactEnabled") is not False:
    print("autoCompactEnabled is not false — hand off, never compact (DESIGN.md D35)")
if "hooks" in data:
    print("carries a hooks key — media ships no hook (DESIGN.md D13, D35)")
for k in data:
    if k in ("effortLevel", "ultracode", "enabledPlugins") or k.startswith("disable"):
        print(f"carries the owner-specific key {k}")
perms = data.get("permissions") or {}
for kind, env in (("deny", "SM_DENY"), ("allow", "SM_ALLOW"), ("ask", "SM_ASK")):
    want = [w for w in os.environ[env].split("\n") if w]
    have = perms.get(kind) or []
    for w in want:
        if w not in have:
            print(f"does not {kind} {w}")
    for h in have:
        if h not in want:
            print(f"{kind}s {h}, which DESIGN.md D13 does not list")
PY
}

tree_checks() { # on TREE
  local f s h line rel d ok base g sub
  # ── 5 and 6. MEMORY ─────────────────────────────────────────────────────────
  f="$TREE/.claude/MEMORY.md"
  if ! $SM_OWNED_MODE && [[ -f "$f" ]]; then
    for h in "${SM_MEMORY_H2S[@]}"; do
      grep -qx "## $h" "$f" || finding "check 5 — .claude/MEMORY.md has no '## $h' heading"
    done
    while IFS= read -r line; do
      finding "check 6 — .claude/MEMORY.md carries an entry: ${line:0:60}"
    done < <(readable "$f" | grep -E '^[-*] \*\*' || true)
  fi

  # ── 7 and 9. Seeds carry no entry; Markdown seeds carry the banner ──────────
  for s in $MD_SEEDS $INDEX_SEEDS; do
    [[ -f "$TREE/$s" ]] || continue
    is_owned_file "$s" || continue
    while IFS= read -r line; do
      finding "check 7 — $s carries an entry ($line) — a seed ships empty"
    done < <(register_entries "$TREE/$s")
  done
  for s in $TOML_SEEDS; do
    [[ -f "$TREE/$s" ]] || continue
    is_owned_file "$s" || continue
    while IFS= read -r line; do
      finding "check 7 — $s carries $line — a TOML seed ships its header comments only"
    done < <(toml_entries "$TREE/$s")
  done
  for s in $MD_SEEDS; do
    [[ -f "$TREE/$s" ]] || continue
    is_owned_file "$s" || continue
    grep -qiE '^>.*seeded stub' "$TREE/$s" || finding "check 9 — $s has no seeded-stub banner"
  done

  # ── 10. .mcp.json ───────────────────────────────────────────────────────────
  if ! $SM_OWNED_MODE && [[ -f "$TREE/.mcp.json" ]]; then
    while IFS= read -r line; do finding "check 10 — .mcp.json $line"; done < <(json_check mcp "$TREE/.mcp.json")
  fi

  # ── 11. Pair-only folders ───────────────────────────────────────────────────
  while IFS= read -r -d '' f; do
    rel="${f#./}"; d="$(dirname "$rel")"; base="${rel##*/}"
    is_owned_file "$rel" || continue
    ok=false
    for g in $SM_PAIR_ONLY_GLOBS; do
      # shellcheck disable=SC2053  # glob match on purpose
      [[ "$d" == $g ]] && { ok=true; break; }
    done
    $ok || continue
    case "$base" in CONTEXT.md|CLAUDE.md|.gitignore|.gitattributes) continue ;; esac
    is_seed "$rel" && continue
    is_example "$rel" && continue
    finding "check 11 — $rel sits in $d/, an author-owned folder that ships its pair only (DESIGN.md Section 3.3)"
  done < <(cd "$TREE" && find . -name .git -prune -o -type f -print0 | sort -z)
  # A pair-only folder may hold a sub-folder that is pair-only itself, a seed-once example, or a
  # README-only generated/, renders/ or raw/ folder (DESIGN.md D42).
  while IFS= read -r -d '' d; do
    rel="${d#./}"
    [[ "$rel" == */* ]] || continue
    is_example "$rel" && continue
    sub="${rel##*/}"
    [[ " $SM_README_ONLY_DIRS " == *" $sub "* ]] && continue
    ok=false
    for g in $SM_PAIR_ONLY_GLOBS; do
      # shellcheck disable=SC2053
      [[ "$rel" == $g ]] && { ok=true; break; }
    done
    $ok && continue
    for g in $SM_PAIR_ONLY_GLOBS; do
      # shellcheck disable=SC2053
      if [[ "${rel%/*}" == $g ]]; then
        is_owned_dir "$rel" || break
        finding "check 11 — $rel/ is a sub-folder of ${rel%/*}/, which ships its pair only"
        break
      fi
    done
  done < <(cd "$TREE" && find . -name .git -prune -o -type d -print0 | sort -z)

  # ── 14. Index seeds list no entry in their tree ─────────────────────────────
  for s in $INDEX_SEEDS; do
    [[ -f "$TREE/$s" ]] || continue
    is_owned_file "$s" || continue
    while IFS= read -r line; do
      finding "check 14 — $s lists '$line' in its tree — an index seed ships with no entries, only placeholders"
    done < <(tree_entries "$TREE/$s")
  done

  # ── 15. Brand seeds keep their open slots ───────────────────────────────────
  for s in $BRAND_SEEDS; do
    [[ -f "$TREE/$s" ]] || continue
    is_owned_file "$s" || continue
    grep -q 'AUTHOR TO CONFIRM' "$TREE/$s" \
      || finding "check 15 — $s has no open AUTHOR TO CONFIRM slot — a brand seed ships the structure, and every brand fact is the author's call"
  done

  # ── 13 and 12. settings.json parses, then matches D13 ───────────────────────
  f="$TREE/.claude/settings.json"
  if ! $SM_OWNED_MODE && [[ -f "$f" ]] && ! grep -q '<:' "$f"; then
    line="$(json_check parse "$f")"
    if [[ -n "$line" ]]; then
      finding "check 13 — .claude/settings.json $line"
    else
      while IFS= read -r line; do finding "check 12 — .claude/settings.json $line"; done < <(json_check settings "$f")
    fi
  fi
}

run_checks() {
  FINDINGS=()
  build_sets "$COPIER"
  [[ "$TREE" == "$TPL" ]] && static_checks
  tree_checks
}

# ── Self-test ────────────────────────────────────────────────────────────────

write_fixture() { # $1 = repo root
  local r="$1" t="$1/template" s q="'" banner
  banner='> **This file is a seeded stub, and it is deliberately unfinished.** It ships so the skills that route here point at something real.'
  mkdir -p "$t"
  {
    printf '_exclude:\n  - .git\n  - /production/src/renders/**\n  - "!/production/src/renders/README.md"\n'
    for s in $SM_SHARED; do printf '  - "<: if _copier_operation == %supdate%s :>/%s<: endif :>"\n' "$q" "$q" "$s"; done
    for s in $SM_SHARED_RETIRED; do printf '  - /%s\n' "$s"; done
    printf '  - "<: if not (%syoutube%s in PLATFORMS) :>/brand/src/platforms/youtube.md<: endif :>"\n' "$q" "$q"
    for s in $SM_EXAMPLES; do printf '  - "<: if %s :>/%s<: endif :>"\n' "$SM_EXAMPLE_GATE" "$s"; done
    printf '_skip_if_exists:\n'
    for s in $SM_SHARED $SM_SEEDS; do printf '  - /%s\n' "$s"; done
    printf 'BRAND_NAME:\n  type: str\n'
    printf '_migrations:\n'
    sm_family_migrations_block
    printf '  - version: %s\n    command: python3 "<%% _copier_conf.src_path %%>/%s"\n    when: "<%% _stage == %safter%s %%>"\n' "$SM_D76_VERSION" "$SM_D76_MIGRATION" "$q" "$q"
  } > "$r/copier.yml"
  for s in $SM_SHARED $SM_SEEDS; do
    [[ "$s" == .agents || "$s" == .agents/skills ]] && continue
    mkdir -p "$(dirname "$t/$s")"; printf '# %s\n' "${s##*/}" > "$t/$s"
  done
  ln -s "$SM_AGENTS_SKILLS_LINK" "$t/.agents/skills"
  mkdir -p "$r/migrations"; printf 'print("fixture migration")\n' > "$r/$SM_D76_MIGRATION"
  printf 'print("fixture outside-link migration")\n' > "$r/$SM_OUTSIDE_MIGRATION"
  chmod 755 "$r/$SM_OUTSIDE_MIGRATION"
  for s in $SM_REGISTER_SEEDS; do
    printf '# %s\n\n%s\n\n## Register\n\n| ID | Notes |\n|---|---|\n' "${s##*/}" "$banner" > "$t/$s"
  done
  printf '# voice.md\n\n%s\n\n## Narrators\n\n<!-- AUTHOR TO CONFIRM: one narrator per use -->\n\n| Use | Voice |\n|---|---|\n' "$banner" > "$t/brand/src/voice/voice.md"
  for s in $SM_PLATFORM_SEEDS; do
    printf '# %s\n\n%s\n\n## Account\n\n<!-- AUTHOR TO CONFIRM: the handle -->\n\n- **Handle:** —\n' "${s##*/}" "$banner" > "$t/$s"
  done
  # The own-channel profiles hold a table of sites or lists in place of ## Account (D61): a
  # header and no rows.
  for s in website blog; do
    printf '# %s.md\n\n%s\n\n## Sites\n\n<!-- AUTHOR TO CONFIRM: one row per site -->\n\n| Site | Domain | Owner | CMS or hosting | Player | Captions | Carries | Agreement | Notes |\n|---|---|---|---|---|---|---|---|---|\n' "$s" "$banner" > "$t/brand/src/platforms/$s.md"
  done
  printf '# newsletter.md\n\n%s\n\n## Lists\n\n<!-- AUTHOR TO CONFIRM: one row per list -->\n\n| List | Sender | Service | Owner | Images hosted at | Agreement | Notes |\n|---|---|---|---|---|---|---|\n' "$banner" > "$t/brand/src/platforms/newsletter.md"
  printf '/* tokens.css */\n:root {\n  --color-bg: #ffffff; /* AUTHOR TO CONFIRM: the background */\n}\n' > "$t/brand/src/design-system/tokens.css"
  for s in thumbnail card; do
    printf '<!-- @dsCard group="Components" -->\n<!doctype html>\n<!-- AUTHOR TO CONFIRM: the layout -->\n' > "$t/brand/src/design-system/previews/$s.html"
  done
  for s in $TOML_SEEDS; do printf '# %s — header comments only.\n#\n# [[file]]\n# id = "F0001"\n' "${s##*/}" > "$t/$s"; done
  for s in $INDEX_SEEDS; do
    case "$s" in
      */CONTEXT.md) printf '# CONTEXT.md\n\n```text\n%s/\n├── CONTEXT.md\n├── CLAUDE.md\n└── <question>.md   ← one guide per question\n```\n\n| Procedure | What it does |\n|---|---|\n' "${s%/CONTEXT.md}" > "$t/$s" ;;
    esac
  done
  { printf '# MEMORY.md\n\nTo add an entry: `- **DD/MM/YYYY** — **Headline.** Body.`\n\n'
    for s in "${SM_MEMORY_H2S[@]}"; do printf '## %s\n\n_No entries yet._\n\n' "$s"; done; } > "$t/.claude/MEMORY.md"
  printf '{"mcpServers": {}}\n' > "$t/.mcp.json"
  {
    printf '{\n  "model": "opus",\n  "autoCompactEnabled": false,\n  "permissions": {\n'
    printf '    "deny": [%s],\n' "$(for s in "${SM_SETTINGS_DENY[@]}"; do printf '"%s", ' "$s"; done | sed 's/, $//')"
    printf '    "allow": [%s],\n' "$(for s in "${SM_SETTINGS_ALLOW[@]}"; do printf '"%s", ' "$s"; done | sed 's/, $//')"
    printf '    "ask": [%s]\n' "$(for s in "${SM_SETTINGS_ASK[@]}"; do printf '"%s", ' "$s"; done | sed 's/, $//')"
    printf '  }\n}\n'
  } > "$t/.claude/settings.json"
  for s in $SM_EXAMPLES; do
    case "$s" in
      */000-example-piece) mkdir -p "$t/$s"; printf '# brief\n' > "$t/$s/brief.md" ;;
      *) mkdir -p "$(dirname "$t/$s")"; printf 'example\n' > "$t/$s" ;;
    esac
  done
  # Pair-only folders with their declared extras: an LFS attributes file, README-only folders.
  mkdir -p "$t/brand/src/exports/large" "$t/production/src/footage/raw" "$t/production/src/voiceover/generated"
  printf '* filter=lfs diff=lfs merge=lfs -text\n' > "$t/brand/src/exports/large/.gitattributes"
  printf '# raw/\n' > "$t/production/src/footage/raw/README.md"
  printf '# generated/\n' > "$t/production/src/voiceover/generated/README.md"
  for d in brand/src/exports brand/src/exports/large production/src/footage production/src/voiceover production/src/timing production/src/scenes publishing/src/posts publishing/src/podcast; do
    mkdir -p "$t/$d"
    printf '# CONTEXT.md — %s/\n' "$d" > "$t/$d/CONTEXT.md"
    printf '@./CONTEXT.md\n' > "$t/$d/CLAUDE.md"
  done
}

self_test() {
  local tmp real_root="$SM_ROOT" real_tpl="$TPL" real_copier="$COPIER" real_ol_sha="$SM_OUTSIDE_SHA256" t f
  bold "▸ $SCRIPT_NAME --self-test"; log ""
  command -v python3 >/dev/null 2>&1 || die "python3 is not installed"
  tmp="$(sm_mktemp)"
  # shellcheck disable=SC2064
  trap "rm -rf '$tmp'" RETURN
  write_fixture "$tmp"
  SM_ROOT="$tmp"; TPL="$tmp/template"; COPIER="$tmp/copier.yml"; TREE="$TPL"; SM_SETS_FOR=""
  # Check 21 holds the fixture's stand-in script to its own bytes; the real run, to the family's.
  SM_OUTSIDE_SHA256="$(sm_sha256 < "$tmp/$SM_OUTSIDE_MIGRATION")"
  # The fixture is in no Git work tree until check 21's probes make it one: the ceiling stops
  # Git from finding a repository above the temporary folder.
  local -x GIT_CEILING_DIRECTORIES
  GIT_CEILING_DIRECTORIES="$(dirname "$tmp")"
  load_owned "$TREE"
  t="$TPL"
  st_baseline "a fixture with every seed and shared file in shape"

  cp "$COPIER" "$tmp/c"
  grep -vxF '  - /publishing/src/schedule.md' "$tmp/c" > "$COPIER"; SM_SETS_FOR=""
  probe "check 1 fires when a seed leaves _skip_if_exists" "check 1 — publishing/src/schedule.md is a seed"
  grep -vxF '  - /.claude/skills/CLAUDE.md' "$tmp/c" > "$COPIER"; SM_SETS_FOR=""
  probe "check 1 fires when a shared file leaves _skip_if_exists" "check 1 — .claude/skills/CLAUDE.md is a shared file"
  awk '/^_skip_if_exists:/ { print; print "  - /production/src/ghost.md"; next } { print }' "$tmp/c" > "$COPIER"; SM_SETS_FOR=""
  probe "check 2 fires on a seed that is not on disk" "check 2 — _skip_if_exists lists /production/src/ghost.md"
  grep -vF '/publishing/src/posts/000-example-piece.md<' "$tmp/c" > "$COPIER"; SM_SETS_FOR=""
  probe "check 3 fires when an example loses its copy-only line" "check 3 — the example publishing/src/posts/000-example-piece.md"
  cp "$tmp/c" "$COPIER"; SM_SETS_FOR=""
  mv "$t/production/src/edits/000-example-piece.toml" "$tmp/h"
  probe "check 4 fires when an example is missing" "check 4 — the example production/src/edits/000-example-piece.toml"
  mv "$tmp/h" "$t/production/src/edits/000-example-piece.toml"

  cp "$t/.claude/MEMORY.md" "$tmp/h"
  sed -i '/^## Sensitivities$/d' "$t/.claude/MEMORY.md";      probe "check 5 fires when a MEMORY heading is lost" "check 5"; cp "$tmp/h" "$t/.claude/MEMORY.md"
  printf -- '- **01/01/2030** — **Robin prefers stills.** Not so.\n' >> "$t/.claude/MEMORY.md"; probe "check 6 fires on a MEMORY entry" "check 6"; cp "$tmp/h" "$t/.claude/MEMORY.md"
  f=production/src/rights-register.md; cp "$t/$f" "$tmp/h"
  printf '| RR0001 | a music bed |\n' >> "$t/$f"; probe "check 7 fires on a filled register row" "check 7 — $f"; cp "$tmp/h" "$t/$f"
  f=brand/src/voice/voice.md; cp "$t/$f" "$tmp/h"
  printf '| voiceover | Ferry Voice |\n' >> "$t/$f"; probe "check 7 fires on a narrator row in the voice seed" "check 7 — $f"; cp "$tmp/h" "$t/$f"
  f=production/src/footage/manifest.toml; cp "$t/$f" "$tmp/h"
  printf '[[file]]\nid = "F0001"\n' >> "$t/$f"; probe "check 7 fires on a [[file]] table in the manifest seed" "check 7 — $f carries a [[file]] table"; cp "$tmp/h" "$t/$f"
  probe_clean "a TOML seed whose example table sits in comments is empty"
  f=brand/src/platforms/website.md; cp "$t/$f" "$tmp/h"
  printf '| harbour-lane | example.com | own | static | self-hosted | vtt | video | own | — |\n' >> "$t/$f"
  probe "check 7 fires on a site row in the website profile seed" "check 7 — $f"; cp "$tmp/h" "$t/$f"
  f=brand/src/platforms/newsletter.md; cp "$t/$f" "$tmp/h"
  printf '| harbour-notes | news@example.com | a sending service | own | example.com | own | — |\n' >> "$t/$f"
  probe "check 7 fires on a list row in the newsletter profile seed" "check 7 — $f"; cp "$tmp/h" "$t/$f"
  probe_clean "a profile whose ## Sites or ## Lists table has a header and no rows is empty"

  cp "$COPIER" "$tmp/c"
  grep -vF "/.claude/MEMORY.md<: endif" "$tmp/c" > "$COPIER"; SM_SETS_FOR=""
  probe "check 8 fires when a shared file loses its update gate" "check 8 — the shared file .claude/MEMORY.md"
  awk -v q="'" '/^_skip_if_exists:/ { print "  - \"<: if _copier_operation == " q "update" q " :>/toolkit/media.py<: endif :>\"" } { print }' "$tmp/c" > "$COPIER"; SM_SETS_FOR=""
  probe "check 8 fires when a template-owned file takes the shared gate" "check 8 — /toolkit/media.py carries the shared files' update gate"
  cp "$tmp/c" "$COPIER"; SM_SETS_FOR=""

  f=publishing/src/schedule.md; cp "$t/$f" "$tmp/h"
  sed -i '/seeded stub/d' "$t/$f";                             probe "check 9 fires when a register loses its banner" "check 9 — $f"; cp "$tmp/h" "$t/$f"
  f=brand/src/platforms/tiktok.md; cp "$t/$f" "$tmp/h"
  sed -i '/seeded stub/d' "$t/$f";                             probe "check 9 fires when a platform profile loses its banner" "check 9 — $f"; cp "$tmp/h" "$t/$f"
  printf '{"mcpServers": {"elevenlabs": {}}}\n' > "$t/.mcp.json";  probe "check 10 fires on a server in .mcp.json" "check 10"; printf '{"mcpServers": {}}\n' > "$t/.mcp.json"
  printf 'take\n' > "$t/production/src/voiceover/003-ferry.s01.t1.mp3"
  probe "check 11 fires on a file in a pair-only folder" "check 11 — production/src/voiceover/003-ferry.s01.t1.mp3"; rm -f "$t/production/src/voiceover/003-ferry.s01.t1.mp3"
  printf '[show]\nshow = "harbour-lane-talks"\n' > "$t/publishing/src/podcast/harbour-lane-talks.toml"
  probe "check 11 fires on a show register left in the podcast folder" "check 11 — publishing/src/podcast/harbour-lane-talks.toml"; rm -f "$t/publishing/src/podcast/harbour-lane-talks.toml"
  printf '{"segments": []}\n' > "$t/production/src/timing/003-ferry.words.json"
  probe "check 11 fires on a timing file left in the timing folder" "check 11 — production/src/timing/003-ferry.words.json"; rm -f "$t/production/src/timing/003-ferry.words.json"
  mkdir -p "$t/publishing/src/posts/drafts"
  probe "check 11 fires on a sub-folder in a pair-only folder" "check 11 — publishing/src/posts/drafts/"; rmdir "$t/publishing/src/posts/drafts"
  probe_clean "the LFS attributes file and the README-only raw/ and generated/ folders are declared extras"
  cp "$t/.claude/settings.json" "$tmp/h"
  sed -i 's/"autoCompactEnabled": false/"autoCompactEnabled": true/' "$t/.claude/settings.json"; probe "check 12 fires when compaction is switched on" "check 12 — .claude/settings.json autoCompactEnabled"; cp "$tmp/h" "$t/.claude/settings.json"
  sed -i 's/, "mcp__elevenlabs__voice_clone"//' "$t/.claude/settings.json"; probe "check 12 fires when a credit-spending tool is not asked" "check 12 — .claude/settings.json does not ask mcp__elevenlabs__voice_clone"; cp "$tmp/h" "$t/.claude/settings.json"
  sed -i 's/"ask": \[/"ask": ["mcp__elevenlabs__list_models", /' "$t/.claude/settings.json"; probe "check 12 fires on an ask D13 does not list" "check 12 — .claude/settings.json asks mcp__elevenlabs__list_models"; cp "$tmp/h" "$t/.claude/settings.json"
  sed -i 's/"model": "opus",/"model": "opus",\n  "hooks": {"PreCompact": []},/' "$t/.claude/settings.json"; probe "check 12 fires on a hooks key" "check 12 — .claude/settings.json carries a hooks key"; cp "$tmp/h" "$t/.claude/settings.json"
  sed -i 's/"autoCompactEnabled": false,/"autoCompactEnabled": false/' "$t/.claude/settings.json"; probe "check 13 fires when settings.json does not parse" "check 13 — .claude/settings.json is not valid JSON"; cp "$tmp/h" "$t/.claude/settings.json"
  f=scripts/workflows/local/CONTEXT.md; cp "$t/$f" "$tmp/h"
  sed -i 's/^└── <question>.md .*$/├── <question>.md\n└── 01-record-a-guest\/   ← a local procedure/' "$t/$f"
  probe "check 14 fires on a procedure listed in an index seed's tree" "check 14 — $f lists '01-record-a-guest/'"; cp "$tmp/h" "$t/$f"
  f=brand/src/design-system/tokens.css; cp "$t/$f" "$tmp/h"
  sed -i 's#/\* AUTHOR TO CONFIRM: the background \*/#/* Harbour blue */#' "$t/$f"
  probe "check 15 fires on a brand seed with every slot filled" "check 15 — $f"; cp "$tmp/h" "$t/$f"

  # 16: the fixture's one negation sits above every gated line; move it, widen it, gate it.
  cp "$COPIER" "$tmp/c"
  awk '/^  - "!\/production\/src\/renders\/README.md"$/ { held = $0; next } { print } /youtube.md<: endif :>"$/ { print held }' "$tmp/c" > "$COPIER"; SM_SETS_FOR=""
  probe "check 16 fires on a negation listed after a gated line" "check 16 — _exclude negates /production/src/renders/README.md back in at item"
  sed 's#"!/production/src/renders/README.md"#"!/production/src/renders/003-ferry/README.md"#' "$tmp/c" > "$COPIER"; SM_SETS_FOR=""
  probe "check 16 fires on a negation of a README inside a per-piece output folder" "check 16 — _exclude negates /production/src/renders/003-ferry/README.md back in, which is not an output folder's own"
  sed 's#"!/production/src/renders/README.md"#"!/production/src/cards/README.md"#' "$tmp/c" > "$COPIER"; SM_SETS_FOR=""
  probe "check 16 fires on a negation of anything but an output folder's README" "check 16 — _exclude negates /production/src/cards/README.md back in, which is not"
  awk -v q="'" '/youtube.md<: endif :>"$/ { print; print "  - \"<: if not (" q "audiobook" q " in MEDIA_KINDS) :>!/production/src/audiobook/renders/README.md<: endif :>\""; next } { print }' "$tmp/c" > "$COPIER"; SM_SETS_FOR=""
  probe "check 16 fires on a negation inside a gated line" "check 16 — a gated _exclude line negates /production/src/audiobook/renders/README.md"
  cp "$tmp/c" "$COPIER"; SM_SETS_FOR=""
  probe_clean "an output folder's own README.md, negated above every gated line, is the one negation allowed"

  # 17: the retired path's third line, and no third line on a path that still ships.
  sed -i '\#^  - /\.claude/mcp_config\.json$#{x;s/^/x/;/^x$/{x;d};x}' "$COPIER"; SM_SETS_FOR=""
  probe "check 17 fires when the retired path loses its unconditional line" "check 17 — the retired shared path /.claude/mcp_config.json"
  cp "$tmp/c" "$COPIER"
  sed -i 's#^_skip_if_exists:#  - /.agents/mcp_config.json\n_skip_if_exists:#' "$COPIER"; SM_SETS_FOR=""
  probe "check 17 fires when a shipped shared path is excluded outright" "check 17 — the shared path /.agents/mcp_config.json carries an unconditional"
  cp "$tmp/c" "$COPIER"; SM_SETS_FOR=""
  # 18: the agent folder.
  mv "$t/.agents" "$tmp/agents-held"; ln -s .claude "$t/.agents"
  probe "check 18 fires when .agents is the 0.4.1 link" "check 18 — template/.agents is not a real folder"
  rm "$t/.agents"; mv "$tmp/agents-held" "$t/.agents"
  rm "$t/.agents/skills"; ln -s ../.claude "$t/.agents/skills"
  probe "check 18 fires when the skills link targets anything else" "check 18 — template/.agents/skills is not the relative link"
  rm "$t/.agents/skills"; ln -s "$SM_AGENTS_SKILLS_LINK" "$t/.agents/skills"
  printf 'x\n' > "$t/.agents/rules.md"
  probe "check 18 fires on a third entry in the agent folder" "check 18 — template/.agents holds 'mcp_config.json rules.md skills'"
  rm -f "$t/.agents/rules.md"
  # 19: the migration entry and its script.
  awk '/^_migrations:/ { exit } { print }' "$tmp/c" > "$COPIER"
  probe "check 19 fires when the D76 migration is not declared" "check 19 — _migrations has no $SM_D76_VERSION entry"
  cp "$tmp/c" "$COPIER"; mv "$tmp/$SM_D76_MIGRATION" "$tmp/mig-held"
  probe "check 19 fires when a migration's script is missing" "check 19 — a migration runs $SM_D76_MIGRATION"
  mv "$tmp/mig-held" "$tmp/$SM_D76_MIGRATION"
  # 20: the outside-link pair first, and no other unversioned entry.
  sed -i "0,/_stage == 'before'/s//_stage == 'after'/" "$COPIER"; SM_SETS_FOR=""
  probe "check 20 fires when the outside-link hold does not run before the render" "check 20 — _migrations does not open with D76's outside-link pair"
  cp "$tmp/c" "$COPIER"; SM_SETS_FOR=""
  printf '  - command: python3 "<%% _copier_conf.src_path %%>/%s"\n    when: "<%% _stage == %safter%s %%>"\n' "$SM_D76_MIGRATION" "'" "'" >> "$COPIER"
  probe "check 20 fires on an unversioned entry beyond the pair" "check 20 — an unversioned _migrations entry runs $SM_D76_MIGRATION"
  cp "$tmp/c" "$COPIER"; SM_SETS_FOR=""
  # 21: one byte of the vendored script; then its mode, outside a Git work tree (the executable
  # bit) and inside one (the index alone: the working tree's bit is not what a commit records).
  cp "$tmp/$SM_OUTSIDE_MIGRATION" "$tmp/h"; sed -i '1s/p/q/' "$tmp/$SM_OUTSIDE_MIGRATION"
  probe "check 21 fires when one byte of the vendored outside-link script changes" "check 21 — $SM_OUTSIDE_MIGRATION has SHA-256"
  cp "$tmp/h" "$tmp/$SM_OUTSIDE_MIGRATION"
  chmod 644 "$tmp/$SM_OUTSIDE_MIGRATION"
  probe "check 21 fires outside a Git work tree when the vendored script is not executable" "check 21 — $SM_OUTSIDE_MIGRATION is not executable"
  if ! { sm_git "$tmp" init -q && sm_git "$tmp" add -- "$SM_OUTSIDE_MIGRATION" \
    && sm_git "$tmp" update-index --chmod=+x -- "$SM_OUTSIDE_MIGRATION"; }; then
    die "could not make the fixture a Git work tree"
  fi
  probe_clean "in a Git work tree, check 21 reads the index's $SM_OUTSIDE_MODE, not the working tree's 644"
  chmod 755 "$tmp/$SM_OUTSIDE_MIGRATION"
  sm_git "$tmp" update-index --chmod=-x -- "$SM_OUTSIDE_MIGRATION"
  probe "check 21 fires when Git's index holds the vendored script at 100644, though the file is executable" "check 21 — Git's index holds $SM_OUTSIDE_MIGRATION at mode 100644"
  sm_git "$tmp" update-index --force-remove -- "$SM_OUTSIDE_MIGRATION"
  probe "check 21 fires when the vendored script is not in Git's index" "check 21 — Git's index holds $SM_OUTSIDE_MIGRATION at mode none"
  rm -rf "$tmp/.git"
  # A .git that Git will not read (here, a gitfile naming no repository) stops the run with
  # exit 2: the executable bit stands in for the index only where there is no repository.
  local rc=0 err
  printf 'gitdir: %s\n' "$tmp/no-such-repository" > "$tmp/.git"
  err="$( (run_checks) 2>&1 >/dev/null )" || rc=$?
  rm -f "$tmp/.git"
  ST_PROBES=$((ST_PROBES + 1))
  if [[ $rc -eq 2 && "$err" == *"check 21 cannot read Git's index"* ]]; then
    log "  ✓ check 21 stops with exit 2 where a .git stands that Git will not read"
  else
    ST_FAILS=$((ST_FAILS + 1))
    printf '\033[31m  ✗ check 21 exited %d, not 2, where a .git stands that Git will not read: %s\033[0m\n' "$rc" "${err:-(no message)}"
  fi
  # 22: the family-shared migrations block: one byte of it, a marker gone, a marker twice.
  sed -i 's/Keep this pair first/Keep this pair First/' "$COPIER"; SM_SETS_FOR=""
  probe "check 22 fires when one byte of the family-shared migrations block changes" "check 22 — the lines between copier.yml's family-shared migrations markers have SHA-256"
  cp "$tmp/c" "$COPIER"
  sed -i '/^# END family-shared migrations (D48)$/d' "$COPIER"; SM_SETS_FOR=""
  probe "check 22 fires when the block loses its END marker" "check 22 — copier.yml carries 1 '$SM_FAMILY_MIGRATIONS_BEGIN' and 0 '$SM_FAMILY_MIGRATIONS_END'"
  cp "$tmp/c" "$COPIER"
  printf '%s\n' "$SM_FAMILY_MIGRATIONS_BEGIN" >> "$COPIER"; SM_SETS_FOR=""
  probe "check 22 fires when a marker occurs twice" "check 22 — copier.yml carries 2 '$SM_FAMILY_MIGRATIONS_BEGIN' and 1 '$SM_FAMILY_MIGRATIONS_END'"
  cp "$tmp/c" "$COPIER"; SM_SETS_FOR=""
  probe_clean "the retired path, the agent folder and the migrations in shape"

  # The over-author scope: the shared files are syntek-author's, so checks 5, 6, 10, 12 and 13
  # do not read them; media's own seeds are still held to their contract.
  while IFS= read -r f; do is_shared "$f" || printf '%s\n' "$f"; done < <(tree_files "$t") > "$t.owned"
  load_owned "$t"
  printf '{"mcpServers": {"drive": {}}}\n' > "$t/.mcp.json"
  printf -- '- **01/01/2027** — **syntek-author owns this file.** Kept.\n' >> "$t/.claude/MEMORY.md"
  printf '{ not json\n' > "$t/.claude/settings.json"
  probe_clean "over syntek-author, its .mcp.json, MEMORY.md and settings.json are not media's to audit"
  f=publishing/src/publish-log.md; cp "$t/$f" "$tmp/h"
  printf '| 01/01/2027 | youtube | youtube.short | 003 | x | on | burned | — |\n' >> "$t/$f"
  probe "check 7 still fires on a media seed, over syntek-author" "check 7 — $f"; cp "$tmp/h" "$t/$f"
  rm -f "$t.owned"; SM_OWNED_MODE=false; SM_OWNED=()

  SM_ROOT="$real_root"; TPL="$real_tpl"; COPIER="$real_copier"; SM_OUTSIDE_SHA256="$real_ol_sha"; SM_SETS_FOR=""
  st_finish "wired, empty seeds from polluted or unwired ones"
}

if $SELF_TEST; then
  self_test
  exit $?
fi

[[ -f "$COPIER" ]] || die "no copier.yml at $SM_ROOT"
[[ -d "$TPL" ]] || die "no template/ directory at $SM_ROOT"
command -v python3 >/dev/null 2>&1 || die "python3 is not installed"
command -v sha256sum >/dev/null 2>&1 || command -v shasum >/dev/null 2>&1 || die "neither sha256sum nor shasum is installed"
command -v git >/dev/null 2>&1 || die "git is not installed (check 21 reads the vendored script's mode from Git's index)"

bold "▸ $SCRIPT_NAME"
STATUS=0
for target in "$TPL" "${TARGETS[@]}"; do
  [[ -d "$target" ]] || die "not a directory: $target"
  TREE="$(cd "$target" && pwd)"
  load_owned "$TREE"
  run_checks
  scope="standalone"; $SM_OWNED_MODE && scope="over syntek-author: media-owned paths; checks 5, 6, 10, 12, 13 skipped"
  [[ "$TREE" == "$TPL" ]] && scope="the template source"
  if [[ ${#FINDINGS[@]} -eq 0 ]]; then
    log "  ✓ $TREE — seeds wired and empty, pair-only folders clean ($scope)"
  else
    bold "✗ $TREE — ${#FINDINGS[@]} finding(s) ($scope):"
    print_findings
    STATUS=1
  fi
done
log ""
if [[ "$STATUS" -eq 0 ]]; then
  bold "✓ Every seed is wired and ships empty; every shared file is copy-only; every author-owned folder ships its pair only."
  exit 0
fi
log "  A polluted seed is a one-way door: no update can retract it (SB rule 21). The wiring lives in"
log "  copier.yml's _skip_if_exists and _exclude (DESIGN.md Sections 3.1–3.6)."
exit 1
