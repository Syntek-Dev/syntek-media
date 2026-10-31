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
#                    author deleted stays deleted (Section 3.2). The shared paths are a third:
#                    copy only, never on update, never recreated (D11, D80, Section 3.6), and they
#                    need BOTH their copier.yml lines — without the update gate a file the author
#                    deleted comes back from media's copy inside syntek-author's project
#                    (Section 10). And the author-owned folders ship their pair and nothing else
#                    (Section 3.3), because anything else in them is the template writing into
#                    the author's space — and the output folders ship their README.md alone,
#                    which only a `!` negation listed above every gated _exclude line can
#                    promise, because Copier obeys the last pattern that matches (D19, Section 3.5).
#                    Most of the shared paths are now the family's bytes too (D80): vendored from
#                    one syntek-author tag and never edited here, so a project that takes both
#                    templates holds one set of bytes whichever comes first. The root
#                    family-shared.json records them in the family's format, and checks 21–27
#                    hold the files, the four blocks and the renders to that record (since
#                    0.6.0 forty-three files from syntek-author's v0.8.0, D81, D84).
#
#                    Thirty-two checks:
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
#                      8. Each shared path (fifty since 0.6.0: D11, D80, D84) has its
#                         update-gated _exclude line ("_copier_operation == 'update'"), and so
#                         does each of the two client folders syntek-author gates whole (.codex
#                         and .gemini, which take no _skip_if_exists line: D80); nothing else
#                         carries that gate, a family skill's folder included (its MEDIA-*.md
#                         mode files are template-owned), nor /how-to or a folder under it (its
#                         three syntek-media/ folders hold media's template-owned files, D84).
#                      9. A Markdown register or brand seed lacks the seeded-stub banner. Index
#                         pairs carry none: a pair is navigation.
#                     10. In a render, .mcp.json is not the family's file: its SHA-256 is not
#                         the one family-shared.json records for it, which declares
#                         code-review-graph and scrapling, pinned, and never ElevenLabs, which
#                         stays user-scoped (DESIGN.md D21, D80). template/'s own copy is
#                         check 25's, so the source tree is not read here.
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
#                         autoCompactEnabled false and, since 0.6.0, idleCompaction false (D81);
#                         exactly the three denies, the guide's Edit(/how-to/**) (D84) and the
#                         family's embed_graph_tool deny, in that order, the six allows, the nine
#                         ElevenLabs asks, the two voice remix run asks (D82) and the family's
#                         eight MCP asks, those eight in the family's order (D80); a hooks key
#                         equal, as parsed JSON, to syntek-author's v0.8.0 seed's hooks object
#                         (the four handoff-hook entries, SessionStart compact among them, then
#                         the data-root guard and the guide guard: D80, D81, D84); and no
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
#                     20. copier.yml's _migrations does not open with D76's outside-link pair
#                         (D11's second, transient exception): first an entry with no version:
#                         running migrations/agents-outside-link.py hold at _stage 'before', then
#                         one running it with restore at _stage 'after', so the link is held
#                         before the render and restored before every other after-stage
#                         migration; or, since 0.6.0, it does not close with the one entry of
#                         the family 'update' block, unversioned, running
#                         migrations/family-update.py update at _stage 'after' (D81: D11's
#                         third exception, which must see what every earlier entry left); or an
#                         entry between them carries no version:. One finding per fault: the
#                         update entry missing or not last is one, and each other unversioned
#                         entry one more. Where _migrations is missing altogether, check 19
#                         claims it and this check stays quiet.
#                     21. migrations/agents-outside-link.py is not syntek-author's family-shared
#                         script as media vendored it (DESIGN.md D85, D80; syntek-author D48): its
#                         SHA-256 is not the one this repository's family-shared.json records for
#                         it (since D80, read from that entry, never a constant here); or Git's
#                         index does not hold it at the entry's mode, 100755 for "mode": "755"
#                         (read with git ls-files -s). Only where this repository is not a Git
#                         work tree is the file's executable bit read instead; a .git that Git
#                         will not read (an ownership mismatch before safe.directory is set,
#                         say) stops the run with exit 2, never a fallback. The script is
#                         never edited here: one changed byte and media's updates print a hand
#                         fix that its README, its bridge and syntek-author's script do not. A
#                         missing script is check 19's; a manifest without a usable entry for it
#                         is check 23's or 24's, and this check stays quiet.
#                     22. copier.yml's family-shared migrations block (D85; syntek-author D48)
#                         is not the family's byte for byte: the marker lines
#                         '# BEGIN family-shared migrations (D48)' and
#                         '# END family-shared migrations (D48)' do not each occur exactly once,
#                         or the lines strictly between them do not have the SHA-256 this
#                         repository's family-shared.json records for its 'migrations' block
#                         (since D80; quiet where the manifest holds no usable entry, checks 23
#                         and 24). The block is how the
#                         vendored script runs: with Copier's own interpreter, hold first,
#                         restore before every other after-stage entry. Where _migrations is
#                         missing (check 19) or does not open with the outside-link pair
#                         (check 20), those claim it and this check stays quiet. An extra
#                         unversioned entry inside the block is two faults, so two findings:
#                         check 20's for the entry, this check's for the bytes.
#                     23. family-shared.json, at this repository's root, is missing, is not JSON,
#                         or does not hold format 1, owner syntek-media and the release Git
#                         allows: 'v' + VERSION on the commit that tag names and on a commit
#                         whose VERSION no tag has yet (the release commit), 'unreleased' once
#                         that tag is an ancestor of HEAD, either where Git cannot tell (the
#                         family's rule, syntek-author D48). Checks 21, 22 and 24–27 then stay
#                         quiet: there is no record to hold anything to.
#                     24. Its files are not exactly _common.sh's SM_FAMILY_SHARED — each
#                         destination path (the family's, <template> kept), source, kind and
#                         scope, in byte order of the path — or its blocks are not exactly the
#                         questions, migrations and, since 0.6.0, update blocks of copier.yml,
#                         then rules-web-tools of rules 06 with its destination, in that order,
#                         the manifest's, with the family's marker lines (D81).
#                     25. A listed file (the outside-link script apart: check 21's) is not a
#                         file, or its size and SHA-256 differ from its entry, or its mode does
#                         ("mode": "755" for an executable; read from Git's index where the
#                         index holds the file, from the executable bit otherwise); or the
#                         listed link, .agents/skills, is the D76 link that check 18 holds it to
#                         but the record names another target (a link that is not the D76 link
#                         is check 18's alone).
#                     26. A listed block (the migrations block apart: check 22's) does not hold
#                         each of its marker lines exactly once, BEGIN first, in its file, or the
#                         lines strictly between them differ in size or SHA-256 from its entry.
#                     27. In a render, a token-free family file other than .mcp.json (check
#                         10's) is not byte for byte what family-shared.json records, or a file
#                         recorded at mode 755 (the two session hooks and, since 0.6.0, the
#                         guide guard, D84) is not executable. Copier
#                         renders every file: a delimiter that reached one of them would change
#                         it here. .codex/config.toml, .gemini/settings.json and opencode.json
#                         carry the seven shared keys and are rendered by design, so they are
#                         not read; nor is template/ (check 25's), nor the .agents/skills link
#                         (shipped-brands.sh check 13's).
#                     28. The data-root map, .claude/syntek-media-dataroot.json, is not exactly
#                         {"format": 1, "folders": []}: media files nothing on the data root
#                         since 0.5.0 (D80), and a folder it claimed could equal or overlap one of
#                         syntek-author's, which refuses every data command touching it.
#                     29. In a standalone render, `python3 .claude/syntek-media-permissions.py
#                         --check` exits other than 0 or 1, or finds missing a rule that is not
#                         one of media's own seed rules (the ElevenLabs and voice remix run
#                         asks, the two Edit denies, the six allows: DESIGN.md D13; never the
#                         guide's Edit(/how-to/**), a family rule, D84): the vendored
#                         client files carry the family's eight asks and its deny already (D80),
#                         so only media's own reach them by hand, through the --write line of
#                         _message_after_copy; or, in a scratch copy of the render, --write
#                         fails or leaves --check exiting other than 0. A render that ticks no
#                         client has nothing to check (exit 0). The script needs Python 3.14
#                         since its v0.6.0 bytes (D81) and exits 2 below it, which _common.sh's
#                         pin refuses before anything runs.
#                     30. copier.yml's _tasks does not end with syntek-author's copy-only
#                         baseline task, line for line as _common.sh's SM_BASELINE_TASK
#                         transcribes it from the tag (family-update.py baseline through
#                         _copier_python; D81, on the model of syntek-author's family-shared.sh
#                         check 14), or the entry before it is not D84's copy-time warning (a
#                         copy-only task testing .copier-answers.syntek-author.yml and
#                         how-to/src/TEMPLATE-GUIDE/syntek-author/01-overview.md at run time), or
#                         media's three tasks (the repository, the hooks' mode, the LFS
#                         tripwire) do not come first. One finding per fault: a changed baseline
#                         line still marks the baseline's place.
#                     31. migrations/family-refresh.json, media's own refresh data (D81, D84),
#                         is missing, is not JSON, or does not hold "format": 1 and "template":
#                         "syntek-media", without which every lane of the update script is off;
#                         or its refresh is not exactly the twenty-seven family-shared files
#                         (SM_REFRESH_PATHS), or its restore not exactly ["how-to"]; or a hook
#                         entry under settings names no shared hook in .claude/hooks/ that
#                         SM_FAMILY_SHARED lists and family-shared.json records at mode 755, so
#                         the data-root guard, which names none, is never listed (syntek-author's
#                         family-shared.sh check 15); or a listed hook, rule or top-level value
#                         is not one D81 lists (SM_REFRESH_HOOKS, _DENY, _ASK, _TOP: never the six
#                         allows, never "model"), or one D81 lists is missing; or a listed entry
#                         D81 does not list is not in the seed either (an entry is offered only
#                         where the new render holds it); or its mcp lane is not the two servers
#                         and the five files at their keys, never .claude/mcp_config.json (D76).
#                         A listed entry D81 lists that the seed lacks is check 12's finding,
#                         never this one's. A one-way door: an entry 0.6.0 lists reaches every
#                         project and cannot be withdrawn.
#                     32. copier.yml's _migrations does not declare 'version: v0.6.0' exactly
#                         once, running '"<% _copier_python %>"
#                         "<% _copier_conf.src_path %>/migrations/v0.6.0-how-to.py"' at _stage
#                         'after', after the v0.4.2 entry and before the family 'update' block's
#                         BEGIN marker (D84: media's report-only crossing script, on the Python
#                         that runs Copier, as D85 amends it; the update script after it must see
#                         what the report saw). Quiet on the order where check 20 already reports
#                         the update entry out of place, and on v0.4.2's side where that entry is
#                         missing (check 19's); a missing script is check 19's too.
#
#                    Checks 1–4, 8, 16–26 and 30–32 read copier.yml, template/, migrations/,
#                    rules 06 and family-shared.json (static, once; checks 21 and 25 also read Git's
#                    index). Checks 5–7, 9, 11–15 and 28 read every tree given — template/ by
#                    default, or renders — and skip a seed the tree does not ship; checks 10,
#                    27 and 29 read the renders only.
#
#                    --write-manifest rewrites family-shared.json from the vendored files and
#                    blocks, in the family's format (the step after vendoring a new tag), then
#                    runs the checks. It is the only writer of that file.
#
#                    Over-author scope (DESIGN.md Section 7): on a <kind>--over-author tree,
#                    whose <tree>.owned lists the files media's copy added, checks 5, 6, 10, 12,
#                    13 and 29 are skipped (the shared files are syntek-author's; coexist-test.sh
#                    check 12 proves them unchanged), and the rest read media-owned paths only:
#                    the family files syntek-author wrote first are its own there.
#
#                    Numbers are stable identifiers. Append, never renumber.
#
#                    What it CANNOT check: that a writing rule in a seed is generic rather than
#                    one brand's preference. "No entries" is decidable; "no personal
#                    preferences" is not — scrub.sh catches the names, a reviewer the rest.
#                    Nor that family-shared.json is still the family's: checks 21–27 hold media
#                    to its own record, and coexist-test.sh check 22 holds that record, entry by
#                    entry, to the syntek-author tree it runs against (in CI, the tag
#                    SYNTEK_AUTHOR_TAG pins). Nor that a vendored file says something true of
#                    media: its text is syntek-author's, reviewed at adoption. Checks 21 and 25
#                    read the mode the index holds, which a plain `git commit` records; `git
#                    commit -a` records the working tree's bit instead, and a file the index does
#                    not hold yet is read by its bit, which `git add` on a file system without
#                    executable bits (core.fileMode false) does not keep: only CI's run on the
#                    pushed commit then reads it.
#
# SELF-TEST. --self-test writes a fixture repository at runtime with every seed in shape and a
#            stand-in for every family file and block, writes its manifest with the writer,
#            proves it clean, then applies one mutation per check and asserts exactly one
#            finding each; then proves the render checks on a render-shaped copy, and the
#            over-author scope on a tree with a .owned list.
#
# Requirements: bash 4+, grep, awk, python3 3.14 or later (checks 10, 12, 13 and 21–29;
#               _common.sh refuses an older one, and check 29 runs the vendored permissions
#               script, which needs it), sha256sum or shasum (checks 21 and 22), git (checks 21
#               and 25, and the self-test). No network.
#
# Usage: shipped-seeds.sh [--root DIR] [--write-manifest] [--quiet] [--self-test] [--help]
#                         [<tree>...]
#
# Exit codes:  0 = every seed is wired and empty, every pair-only folder clean, every family
#                  file and block as family-shared.json records it
#              1 = finding(s), or the self-test no longer separates
#              2 = script error (bad arguments, no copier.yml, no python3, no sha256 tool, no git,
#                  a .git that Git will not read, or --write-manifest with a family file
#                  missing or a block's markers wrong)

set -euo pipefail
SCRIPT_NAME="shipped-seeds.sh"
# shellcheck source=_common.sh
source "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/_common.sh"

SELF_TEST=false
WRITE_MANIFEST=false
TARGETS=()

usage() {
  cat <<'EOF'
shipped-seeds.sh — Verify the seeds ship empty, wired, and only where they belong

Usage: shipped-seeds.sh [--root DIR] [--write-manifest] [--quiet] [--self-test] [--help] [<tree>...]

  <tree>            A render to check as well (checks 5–7, 9–15 and 27–29); template/ is
                    always checked
  --root DIR        The template repository (default: this repository)
  --write-manifest  Rewrite family-shared.json from the vendored files and blocks, then check
  --quiet           Print findings only
  --self-test       Prove the checks still fire against a fixture written at runtime
  --help            Show this message

A <tree>.owned file beside a tree (written by generate-all.sh) marks an over-author tree and
narrows the checks to media's paths.
Exit codes: 0 = clean  1 = finding(s), or the self-test no longer separates
            2 = script error
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --root)      [[ $# -gt 1 ]] || die "--root needs a value"; SM_ROOT="$(cd "$2" && pwd)" || die "no such directory: $2"; shift 2 ;;
    --write-manifest) WRITE_MANIFEST=true; shift ;;
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
  for s in $SM_SHARED_DIRS; do
    [[ -n "${update_gated[$s]:-}" ]] || finding "check 8 — the client folder $s/ has no update-gated _exclude line ($SM_SHARED_GATE) — an update that crosses 0.5.0 would leave an empty $s/ in a project that never had one (DESIGN.md D80)"
  done
  for s in "${!update_gated[@]}"; do
    is_shared "$s" && continue
    [[ " $SM_SHARED_DIRS " == *" $s "* ]] && continue
    finding "check 8 — /$s carries the shared files' update gate ($SM_SHARED_GATE) but is not a shared path (DESIGN.md D11, D80): it would never reach a project by update"
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

  # ── 20. D76's outside-link pair opens _migrations, D81's update entry closes it, and every
  #        entry between them is versioned ──
  local pair_ok=false upd_ok=true
  local -a howto_findings=()
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
    # The family 'update' entry (D81): unversioned, after the render, and last. Only the last
    # entry may be it; one found anywhere else is that one fault, and nothing more.
    local last=$((n - 1)) upd_at=-1
    for ((i = 2; i < n; i++)); do
      [[ "${cmd[$i]}" == *"/$SM_FAMILY_UPDATE_SCRIPT\" update "* ]] && upd_at=$i
    done
    if [[ "$n" -lt 3 || "$upd_at" -ne "$last" || "${ver[$last]}" != - || "${whn[$last]}" != *"_stage == 'after'"* ]]; then
      upd_ok=false
      finding "check 20 — _migrations does not close with the family 'update' block's one entry, unversioned, running $SM_FAMILY_UPDATE_SCRIPT update at _stage 'after' $( [[ "$upd_at" -ge 0 && "$upd_at" -ne "$last" ]] && printf '(it is entry %d of %d)' "$((upd_at + 1))" "$n" || printf '(none is last)'): it must run last, after every versioned entry, so it sees what each left (DESIGN.md D81, D11)"
    fi
    for ((i = 2; i < last; i++)); do
      [[ "${ver[$i]}" != - ]] && continue
      [[ "$i" -eq "$upd_at" ]] && continue
      finding "check 20 — an unversioned _migrations entry runs $(grep -oE 'migrations/[^" ]+' <<< "${cmd[$i]}" || printf '%s' "${cmd[$i]}"): only D76's outside-link pair, first, and D81's family update entry, last, are keyed to no release (DESIGN.md D76, D81; .claude/CLAUDE.md Section 7.7)"
    done
    # 32's reading, reported after 30 and 31: D84's crossing entry, where it stands.
    local h=-1 d76=-1 hn=0
    for ((i = 0; i < n; i++)); do
      [[ "${ver[$i]}" == "$SM_D76_VERSION" ]] && d76=$i
      if [[ "${ver[$i]}" == "$SM_HOWTO_VERSION" ]]; then h=$i; hn=$((hn + 1)); fi
    done
    if [[ "$hn" -ne 1 ]]; then
      howto_findings+=("check 32 — _migrations declares 'version: $SM_HOWTO_VERSION' $hn time(s), not once: D84's report-only crossing script, $SM_HOWTO_MIGRATION, runs once, on the update that crosses 0.6.0 (DESIGN.md D84)")
    else
      [[ "${cmd[$h]}" == "'\"<% _copier_python %>\" \"<% _copier_conf.src_path %>/$SM_HOWTO_MIGRATION\"'" \
          && "${whn[$h]}" == *"_stage == 'after'"* ]] \
        || howto_findings+=("check 32 — the $SM_HOWTO_VERSION entry does not run '\"<% _copier_python %>\" \"<% _copier_conf.src_path %>/$SM_HOWTO_MIGRATION\"' at _stage 'after': the crossing script runs on the Python that runs Copier, as the family entries do, after the render (DESIGN.md D84, D85)")
      # Its place: after v0.4.2's entry (whose absence is check 19's) and before the 'update'
      # block (whose misplacement is check 20's, which then claims the fault).
      if [[ "$d76" -ge 0 && "$h" -lt "$d76" ]] || { $upd_ok && [[ "$h" -gt "$upd_at" ]]; }; then
        howto_findings+=("check 32 — the $SM_HOWTO_VERSION entry is _migrations entry $((h + 1)) of $n, not after the $SM_D76_VERSION entry and before the family 'update' block: releases run in order, and the update script must see what the crossing report saw (DESIGN.md D84, D81)")
      fi
    fi
  fi

  # ── 23–26 first: the manifest, read once; it also gives checks 21 and 22 their values ──
  # family-shared.json is the record (D80): checks 21 and 22 read its entries for the
  # outside-link script and the migrations block, never a constant here. A .git that Git will
  # not read stops the run before anything is read (exit 2, never a fallback).
  local fam rc=0 line n text out_sha="" out_mode="" mig_sha="" errf why
  local -a fam_findings=()
  errf="$(mktemp)"
  fam="$(sm_family_py check "$SM_ROOT" 2>"$errf")" || rc=$?
  why="$(cat "$errf" 2>/dev/null)"; rm -f "$errf"
  [[ "$rc" -eq 3 ]] && die "check 21 cannot read Git's index: $why"
  [[ "$rc" -eq 0 ]] || die "the family-shared.json reader failed (exit $rc): $why"
  while IFS= read -r line; do
    [[ -z "$line" ]] && continue
    case "$line" in
      E$'\t'outside$'\t'*)    out_sha="$(cut -f3 <<< "$line")"; out_mode="$(cut -f4 <<< "$line")" ;;
      E$'\t'migrations$'\t'*) mig_sha="$(cut -f3 <<< "$line")" ;;
      *) n="${line%%$'\t'*}"; text="${line#*$'\t'}"; fam_findings+=("check $n — $text") ;;
    esac
  done <<< "$fam"

  # ── 21. The vendored outside-link script is the family's, byte for byte (D85, D80) ──
  # The bytes are read from disk; the mode from Git's index, which a plain `git commit` records,
  # and from the executable bit only where SM_ROOT is in no Git work tree and holds no .git.
  # Quiet where the manifest holds no usable entry for it (checks 23 and 24 say why).
  local ol="$SM_ROOT/$SM_OUTSIDE_MIGRATION" got mode
  if [[ -f "$ol" && -n "$out_sha" ]]; then
    got="$(sm_sha256 < "$ol")"
    [[ "$got" == "$out_sha" ]] \
      || finding "check 21 — $SM_OUTSIDE_MIGRATION has SHA-256 ${got:0:12}…, not ${out_sha:0:12}…, the value family-shared.json records for it (vendored from syntek-author $SM_FAMILY_RELEASE): it is vendored byte for byte and never edited here (DESIGN.md D85, D80; syntek-author D48)"
    if [[ "$(git -C "$SM_ROOT" rev-parse --is-inside-work-tree 2>/dev/null)" == true ]]; then
      mode="$(git -C "$SM_ROOT" ls-files -s -- "$SM_OUTSIDE_MIGRATION" 2>/dev/null | awk 'NR == 1 { print $1 }')"
      [[ "$mode" == "$out_mode" ]] \
        || finding "check 21 — Git's index holds $SM_OUTSIDE_MIGRATION at mode ${mode:-none (it is not in the index)}, not $out_mode, the mode family-shared.json records for it (git update-index --chmod=+x; DESIGN.md D85)"
    elif [[ -e "$SM_ROOT/.git" || -L "$SM_ROOT/.git" ]]; then
      die "check 21 cannot read Git's index: $SM_ROOT/.git stands, but Git will not read it (an ownership mismatch? see git config safe.directory)"
    elif [[ "$out_mode" == 100755 ]]; then
      [[ -x "$ol" ]] \
        || finding "check 21 — $SM_OUTSIDE_MIGRATION is not executable (outside a Git work tree, the executable bit stands for Git's 100755, the mode family-shared.json records for it; DESIGN.md D85)"
    fi
  fi

  # ── 22. The family-shared migrations block is the family's, byte for byte (D85) ──
  # Where _migrations is missing (check 19) or does not open with the pair (check 20), those
  # claim it and this check stays quiet. An extra unversioned entry inside the block is two
  # faults: check 20 names the entry, this check the bytes.
  local nb ne blk
  nb="$(grep -cxF "$SM_FAMILY_MIGRATIONS_BEGIN" "$COPIER" || true)"
  ne="$(grep -cxF "$SM_FAMILY_MIGRATIONS_END" "$COPIER" || true)"
  if ! $pair_ok || [[ -z "$mig_sha" ]]; then
    :
  elif [[ "$nb" -ne 1 || "$ne" -ne 1 ]]; then
    finding "check 22 — copier.yml carries $nb '$SM_FAMILY_MIGRATIONS_BEGIN' and $ne '$SM_FAMILY_MIGRATIONS_END' line(s), not one of each: the family-shared migrations block is taken whole (DESIGN.md D85; syntek-author D48)"
  else
    blk="$(awk -v b="$SM_FAMILY_MIGRATIONS_BEGIN" -v e="$SM_FAMILY_MIGRATIONS_END" '$0 == e { on = 0 } on { print } $0 == b { on = 1 }' "$COPIER" | sm_sha256)"
    [[ "$blk" == "$mig_sha" ]] \
      || finding "check 22 — the lines between copier.yml's family-shared migrations markers have SHA-256 ${blk:0:12}…, not ${mig_sha:0:12}…, the value family-shared.json records for the block (vendored from syntek-author $SM_FAMILY_RELEASE): it is taken byte for byte and never edited here (DESIGN.md D85, D80; syntek-author D48)"
  fi

  # ── 23–26. The manifest and what it records (D80): reported here, in number order ──
  for line in "${fam_findings[@]}"; do finding "$line"; done

  # ── 30 and 31. D81's offers: the baseline task last, and the refresh data ──
  offers_checks

  # ── 32. D84's crossing entry: v0.6.0, through _copier_python, after v0.4.2, before 'update' ──
  for line in "${howto_findings[@]}"; do finding "$line"; done
}

# 30. _tasks: media's three, then D84's copy-time warning, then syntek-author's baseline task,
# line for line as _common.sh transcribes it from the tag (D81, D84). One finding per fault:
# the baseline task changed or missing, or not last; the warning missing from its place; the
# three media tasks not first.
tasks_entries() { # $1 = copier.yml → one entry per record, its non-comment lines joined by \n, NUL-ended
  awk '
    /^_tasks:/ { on = 1; next }
    on && /^[A-Za-z_]/ { exit }
    !on { next }
    /^[[:space:]]*#/ || /^[[:space:]]*$/ { next }
    /^  - / { if (n++) printf "%s%c", buf, 0; buf = $0; next }
    { buf = buf "\n" $0 }
    END { if (n) printf "%s%c", buf, 0 }' "$1"
}

offers_checks() {
  local -a ent=()
  local e i n base=-1 warn
  while IFS= read -r -d '' e; do ent+=("$e"); done < <(tasks_entries "$COPIER")
  n=${#ent[@]}
  for ((i = 0; i < n; i++)); do [[ "${ent[$i]}" == "$SM_BASELINE_TASK" ]] && base=$i; done
  if [[ "$base" -lt 0 ]]; then
    finding "check 30 — _tasks holds no entry equal, line for line, to syntek-author's baseline task as _common.sh transcribes it from $SM_FAMILY_RELEASE ($SM_UPDATE_MIGRATION baseline through _copier_python, copy only): it is taken byte for byte and never edited here (DESIGN.md D81; syntek-author D51, D52)"
  elif [[ "$base" -ne $((n - 1)) ]]; then
    finding "check 30 — syntek-author's baseline task is _tasks entry $((base + 1)) of $n, not the last: it must run after every other task, on the repository task 1 made and the files the copy kept (DESIGN.md D81)"
  fi
  # A changed baseline line is still the baseline's place: the warning is the entry before it.
  local at=$base
  if [[ "$at" -lt 0 ]]; then
    at=$n
    for ((i = 0; i < n; i++)); do [[ "${ent[$i]}" == *"/$SM_UPDATE_MIGRATION\" baseline"* ]] && at=$i; done
  fi
  warn=$((at - 1))
  if [[ "$warn" -lt 0 || "${ent[$warn]}" != *"$SM_AUTHOR_ANSWERS"* || "${ent[$warn]}" != *"$SM_AUTHOR_GUIDE_START"* \
      || "${ent[$warn]}" != *"_copier_operation == 'copy'"* ]]; then
    finding "check 30 — the _tasks entry before the baseline task is not D84's copy-time warning, a copy-only task that tests $SM_AUTHOR_ANSWERS and $SM_AUTHOR_GUIDE_START at run time (DESIGN.md D84, D81)"
  elif [[ "$warn" -ne 3 || "${ent[0]}" != *"git init"* || "${ent[1]}" != *"chmod +x .claude/hooks"* || "${ent[2]}" != *"filter.lfs"* ]]; then
    finding "check 30 — _tasks does not open with media's three tasks (the repository, the hooks' mode, the LFS tripwire) before D84's warning and the baseline task (DESIGN.md Section 3.5, D81)"
  fi

  # 31. migrations/family-refresh.json, media's own refresh data (D81, D84).
  local line
  while IFS= read -r line; do
    if [[ -n "$line" ]]; then finding "check 31 — $SM_REFRESH_DATA $line"; fi
  done < <(SR_PATHS="$SM_REFRESH_PATHS" SR_RESTORE="$SM_REFRESH_RESTORE" SR_TEMPLATE="$SM_REFRESH_TEMPLATE" \
    SR_TOP="$(printf '%s\n' "${SM_REFRESH_TOP[@]}")" SR_DENY="$(printf '%s\n' "${SM_REFRESH_DENY[@]}")" \
    SR_ASK="$(printf '%s\n' "${SM_REFRESH_ASK[@]}")" SR_HOOKS="$SM_REFRESH_HOOKS" \
    SR_SERVERS="$SM_REFRESH_MCP_SERVERS" SR_FILES="$SM_REFRESH_MCP_FILES" SR_FAMILY="$SM_FAMILY_SHARED" \
    python3 -I - "$SM_ROOT/$SM_REFRESH_DATA" "$TPL/.claude/settings.json" "$SM_ROOT/$SM_FAMILY_MANIFEST" <<'PYREFRESH'
import json, os, re, sys
E = os.environ
path, seed_path, man_path = sys.argv[1:4]
out = []
def say(text):
    out.append(text)
def done():
    print("\n".join(out))
    sys.exit(0)
try:
    data = json.load(open(path, encoding="utf-8"))
except FileNotFoundError:
    say("is missing: without it every lane of the update script is off, and nothing is refreshed, offered or restored (DESIGN.md D81)")
    done()
except (OSError, ValueError) as err:
    say(f"is not JSON ({err.__class__.__name__}): every lane of the update script is then off (DESIGN.md D81)")
    done()
if not isinstance(data, dict) or data.get("format") != 1 or type(data.get("format")) is not int or data.get("template") != E["SR_TEMPLATE"]:
    say(f"does not hold \"format\": 1 and \"template\": \"{E['SR_TEMPLATE']}\": the update script reads it as no refresh data, so every lane is off (DESIGN.md D81; syntek-author D48)")
    done()
want_paths = E["SR_PATHS"].split()
if data.get("refresh") != want_paths:
    have = data.get("refresh") if isinstance(data.get("refresh"), list) else []
    miss = [p for p in want_paths if p not in have]
    extra = [str(p) for p in have if p not in want_paths]
    say(f"refresh is not exactly the twenty-seven family-shared files syntek-author lists, in its order (missing: {', '.join(miss) or 'none'}; "
        f"extra: {', '.join(extra) or 'none'}): a listed file reaches every project and cannot be withdrawn (DESIGN.md D81, D84)")
if data.get("restore") != [E["SR_RESTORE"]]:
    say(f"restore is {json.dumps(data.get('restore'))}, not [\"{E['SR_RESTORE']}\"]: the update restores the read-only guide folder and nothing else (DESIGN.md D84)")
# The seed's own lists are check 12's and its parse check 13's: an entry D81 lists that the seed
# lacks is check 12's finding, so this check reports only a listed entry D81 does not list.
try:
    seed = json.load(open(seed_path, encoding="utf-8"))
except (OSError, ValueError):
    seed = None
seed_ok = isinstance(seed, dict)
seed = seed if seed_ok else {}
shipped = set()
for line in E["SR_FAMILY"].splitlines():
    f = line.split()
    if f and len(f) == 2 and f[0].startswith(".claude/hooks/") and f[0].endswith(".sh"):
        shipped.add(f[0])
try:
    man = json.load(open(man_path, encoding="utf-8"))
    modes = {e.get("path"): e.get("mode") for e in man.get("files", []) if isinstance(e, dict)}
except (OSError, ValueError, AttributeError):
    modes = None   # check 23's
settings = data.get("settings") if isinstance(data.get("settings"), dict) else {}
# Hooks: each listed entry names a shipped hook at mode 755, stands in the seed, and is one D81 lists.
want_hooks = json.loads(E["SR_HOOKS"])
seed_hooks = seed.get("hooks") if isinstance(seed.get("hooks"), dict) else {}
hooks = settings.get("hooks") if isinstance(settings.get("hooks"), dict) else {}
for event, entries in sorted(hooks.items()):
    for entry in entries if isinstance(entries, list) else []:
        cmds = [h.get("command", "") for h in entry.get("hooks", []) if isinstance(h, dict)] if isinstance(entry, dict) else []
        scripts = sorted({m for c in cmds for m in re.findall(r"\.claude/hooks/[A-Za-z0-9._-]+\.sh", c)})
        label = f"{event} {entry.get('matcher', '(no matcher)') if isinstance(entry, dict) else '?'}"
        bad = [s for s in scripts if s not in shipped or (modes is not None and modes.get(s) != "755")]
        if not scripts or bad:
            say(f"lists the hook entry {label}, which names no shared hook in .claude/hooks/ that ships at mode 755 "
                f"({', '.join(bad) or 'it names no script there'}): the data-root guard is never listed, so it reaches new copies only "
                "(DESIGN.md D81; syntek-author's family-shared.sh check 15)")
        elif entry in (want_hooks.get(event) or []):
            pass   # wanted: where the seed lacks it, check 12 says so
        elif seed_ok and entry not in (seed_hooks.get(event) or []):
            say(f"lists the hook entry {label}, which the seed's hooks do not hold as written: an entry is offered only where the new render holds it (DESIGN.md D13, D81)")
        else:
            say(f"lists the hook entry {label}, which D81 does not list (DESIGN.md D81)")
for event, entries in sorted(want_hooks.items()):
    for entry in entries:
        if entry not in (hooks.get(event) or []):
            say(f"does not list the hook entry {event} {entry.get('matcher', '(no matcher)')}, which D81 offers (DESIGN.md D81, D84)")
# Permission rules: deny and ask only, each in the seed, exactly D81's.
perms = settings.get("permissions") if isinstance(settings.get("permissions"), dict) else {}
seed_perms = seed.get("permissions") if isinstance(seed.get("permissions"), dict) else {}
for kind in sorted(perms):
    if kind not in ("deny", "ask"):
        say(f"lists permissions.{kind}, which D81 never offers (the six allows are given by hand; DESIGN.md D13, D81)")
for kind, env in (("deny", "SR_DENY"), ("ask", "SR_ASK")):
    want = [w for w in E[env].splitlines() if w]
    have = perms.get(kind) if isinstance(perms.get(kind), list) else []
    for rule in have:
        if rule in want:
            continue   # wanted: where the seed lacks it, check 12 says so
        if seed_ok and rule not in (seed_perms.get(kind) or []):
            say(f"lists the {kind} rule {rule}, which the seed does not hold: an entry is offered only where the new render holds it (DESIGN.md D13, D81)")
        else:
            say(f"lists the {kind} rule {rule}, which D81 does not list (DESIGN.md D81)")
    for rule in want:
        if rule not in have:
            say(f"does not list the {kind} rule {rule}, which D81 offers (DESIGN.md D13, D81)")
    # D13's order, each rule once (VEND-14): the order of _common.sh's lists, which check 12
    # holds the seed to, so a fault in the seed itself stays check 12's alone.
    if set(have) == set(want) and have != want:
        say(f"lists its {kind} rules out of D13's order, or one twice: they are listed once each, in the seed's order (DESIGN.md D13, D81)")
# Top-level values: exactly the seed's two, never "model".
want_top = {}
for kv in [t for t in E["SR_TOP"].splitlines() if t]:
    k, v = kv.split("=", 1)
    want_top[k] = json.loads(v)
for k in sorted(settings):
    if k in ("hooks", "permissions"):
        continue
    if k not in want_top:
        why = "the model is the owner's to choose" if k == "model" else "only the two compaction values are listed"
        say(f"lists the top-level value {k}, which D81 never offers ({why}; DESIGN.md D81)")
    elif settings[k] != want_top[k]:
        say(f"lists {k} as {json.dumps(settings[k])}, not {json.dumps(want_top[k])}, the value the seed holds (DESIGN.md D13, D81)")
for k in want_top:
    if k not in settings:
        say(f"does not list the top-level value {k}, which D81 offers (DESIGN.md D81)")
# The MCP lane: the two servers, the five files at their keys, never .claude/mcp_config.json.
mcp = data.get("mcp") if isinstance(data.get("mcp"), dict) else {}
servers = E["SR_SERVERS"].split()
if mcp.get("servers") != servers:
    say(f"mcp.servers is {json.dumps(mcp.get('servers'))}, not {json.dumps(servers)} (DESIGN.md D81)")
want_files = {}
for line in E["SR_FILES"].splitlines():
    if line.strip():
        f, keys = line.split("\t")
        want_files[f] = keys.split(".")
files = mcp.get("files") if isinstance(mcp.get("files"), dict) else {}
for f in sorted(files):
    if f == ".claude/mcp_config.json":
        say("mcp.files names .claude/mcp_config.json, the retired Antigravity path that ships no more: the servers go to .agents/mcp_config.json (DESIGN.md D76, D81)")
    elif f not in want_files:
        say(f"mcp.files names {f}, which D81 does not list (DESIGN.md D81)")
    elif files[f] != want_files[f]:
        say(f"mcp.files gives {f} the key {json.dumps(files[f])}, not {json.dumps(want_files[f])} (DESIGN.md D81)")
for f in want_files:
    if f not in files:
        say(f"mcp.files does not name {f}, which D81 lists (DESIGN.md D81)")
for k in sorted(data):
    if k not in ("format", "template", "refresh", "restore", "settings", "mcp"):
        say(f"holds the key {k}, which syntek-author D48's format does not (DESIGN.md D81)")
done()
PYREFRESH
  )
}

json_check() { # $1 = mode (settings|parse), $2 = file → prints one problem per line
  SM_DENY="$(printf '%s\n' "${SM_SETTINGS_DENY[@]}" "${SM_SETTINGS_FAMILY_DENY[@]}")" \
  SM_ALLOW="$(printf '%s\n' "${SM_SETTINGS_ALLOW[@]}")" \
  SM_ASK="$(printf '%s\n' "${SM_SETTINGS_ASK[@]}" "${SM_SETTINGS_FAMILY_ASK[@]}")" \
  SM_FAMILY_ASK="$(printf '%s\n' "${SM_SETTINGS_FAMILY_ASK[@]}")" \
  SM_HOOKS="$SM_SETTINGS_HOOKS" SM_BANNED="$SM_SETTINGS_BANNED_KEYS" \
  SM_TOP="$(printf '%s\n' "${SM_SETTINGS_TOP[@]}")" \
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
if not isinstance(data, dict):
    print("is not a JSON object"); sys.exit(0)
if data.get("model") != "opus":
    print(f"model is {data.get('model')!r}, not 'opus'")
for kv in [t for t in os.environ["SM_TOP"].split("\n") if t]:
    key, val = kv.split("=", 1)
    if data.get(key, "absent") != json.loads(val):
        print(f"{key} is not {val} — hand off, never compact (DESIGN.md D13, D35, D81)")
if data.get("hooks") != json.loads(os.environ["SM_HOOKS"]):
    print("hooks are not exactly syntek-author's v0.8.0 seed's hooks object — the four handoff-hook entries (UserPromptSubmit, "
          "PreCompact auto and manual, SessionStart compact), then the data-root guard and the guide guard — as parsed JSON "
          "(DESIGN.md D13, D35, D80, D81, D84)")
for k in data:
    if k in os.environ["SM_BANNED"].split() or k.startswith("disable"):
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
family = [w for w in os.environ["SM_FAMILY_ASK"].split("\n") if w]
order = [h for h in perms.get("ask") or [] if h in family]
if sorted(order) == sorted(family) and order != family:
    print("asks the family's eight MCP tools out of the family's order (Scrapling's six, then code-review-graph's two; DESIGN.md D13, D80)")
wdeny = [w for w in os.environ["SM_DENY"].split("\n") if w]
hdeny = [h for h in perms.get("deny") or [] if h in wdeny]
if sorted(hdeny) == sorted(wdeny) and hdeny != wdeny:
    print("denies its rules out of D13's order: media's three, then the guide's Edit(/how-to/**), then the family's "
          "embed_graph_tool deny (DESIGN.md D13, D84)")
PY
}

# 29. The vendored client files hold the family's rules, so in a fresh render the permissions
# script finds missing only media's own seed rules, which the after-copy --write line carries;
# and --write, run in a scratch copy, leaves nothing missing.
SM_PERMISSIONS_PY=".claude/syntek-media-permissions.py"
permissions_checks() { # on TREE
  local out rc line rule scratch r
  local -A mine=()
  sm_py_older "$(sm_py_version python3 || printf '0.0')" \
    && die "check 29 needs python3 $SM_PYTHON_MIN or later, which the vendored permissions script needs since its v0.6.0 bytes (DESIGN.md D81)"
  # Media's own seed rules: the guide's Edit(/how-to/**) is syntek-author's (D84; syntek-author
  # D56), which the vendored opencode.json already holds as how-to/*, so it is never one of them.
  for r in "${SM_SETTINGS_ASK[@]}" "${SM_SETTINGS_DENY[@]}" "${SM_SETTINGS_ALLOW[@]}"; do
    [[ "$r" == "Edit(/how-to/"* ]] && continue
    mine["$r"]=1
  done
  rc=0; out="$(cd "$TREE" && env -u SYNTEK_DATA_ROOT python3 "$SM_PERMISSIONS_PY" --check 2>&1)" || rc=$?
  if [[ "$rc" -ne 0 && "$rc" -ne 1 ]]; then
    finding "check 29 — $SM_PERMISSIONS_PY --check exits $rc in a fresh render: $(grep -v '^[[:space:]]*$' <<< "$out" | tail -1 | cut -c1-160)"
    return 0
  fi
  while IFS= read -r line; do
    rule="${line#*✗ }"; rule="${rule%% -> *}"
    [[ -n "${mine[$rule]:-}" ]] && continue
    finding "check 29 — $SM_PERMISSIONS_PY --check finds $rule missing in a fresh render: the vendored client files should already hold every family rule, and --write carries media's own seed rules only (DESIGN.md D13, D80)"
  done < <(grep -F '✗ ' <<< "$out" | grep -F ' -> ' || true)
  [[ "$rc" -eq 0 ]] && return 0
  scratch="$(sm_mktemp)"
  cp -a "$TREE/." "$scratch/"
  if ! (cd "$scratch" && env -u SYNTEK_DATA_ROOT python3 "$SM_PERMISSIONS_PY" --write >/dev/null 2>&1); then
    finding "check 29 — $SM_PERMISSIONS_PY --write fails in a copy of a fresh render, so the after-copy line cannot carry media's own rules (DESIGN.md D13, D80)"
  else
    rc=0; out="$(cd "$scratch" && env -u SYNTEK_DATA_ROOT python3 "$SM_PERMISSIONS_PY" --check 2>&1)" || rc=$?
    [[ "$rc" -eq 0 ]] || finding "check 29 — after $SM_PERMISSIONS_PY --write, --check still exits $rc in a copy of a fresh render: $(grep -v '^[[:space:]]*$' <<< "$out" | tail -1 | cut -c1-160)"
  fi
  rm -rf "$scratch"
  return 0
}

tree_checks() { # on TREE
  local f s h line rel d ok base g sub n
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

  # ── 10 and 27. A render's family files are the manifest's bytes (D21, D80) ──
  # Renders only: template/'s own copies are check 25's. Over syntek-author, check 10 is skipped
  # and check 27 reads media-owned paths: the family files syntek-author wrote first are its own.
  if [[ "$TREE" != "$TPL" ]]; then
    local own=""
    $SM_OWNED_MODE && own="$TREE.owned"
    while IFS= read -r line; do
      [[ -z "$line" ]] && continue
      n="${line%%$'\t'*}"
      [[ "$n" == 10 ]] && $SM_OWNED_MODE && continue
      finding "check $n — ${line#*$'\t'}"
    done < <(sm_family_py tree "$SM_ROOT" "$TREE" "$own")
  fi

  # ── 28. The data-root map is empty (D80) ────────────────────────────────────
  f="$TREE/$SM_DATAROOT_MAP"
  if [[ -f "$f" ]] && is_owned_file "$SM_DATAROOT_MAP"; then
    python3 - "$f" <<'PYMAP' || finding "check 28 — $SM_DATAROOT_MAP is not exactly {\"format\": 1, \"folders\": []}: media files nothing on the data root since 0.5.0, and a folder it claimed could overlap one of syntek-author's, which refuses every data command there (DESIGN.md D80)"
import json, sys
try:
    data = json.load(open(sys.argv[1], encoding="utf-8"))
except Exception:
    sys.exit(1)
sys.exit(0 if data == {"format": 1, "folders": []} and type(data["format"]) is int else 1)
PYMAP
  fi

  # ── 29. Only media's own seed rules wait for --write (D13, D80) ──────────────
  # Renders only, standalone only: over syntek-author the settings and client files are its.
  if [[ "$TREE" != "$TPL" ]] && ! $SM_OWNED_MODE && [[ -f "$TREE/$SM_PERMISSIONS_PY" ]]; then
    permissions_checks
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
    for s in $SM_SHARED $SM_SHARED_DIRS; do printf '  - "<: if _copier_operation == %supdate%s :>/%s<: endif :>"\n' "$q" "$q" "$s"; done
    for s in $SM_SHARED_RETIRED; do printf '  - /%s\n' "$s"; done
    printf '  - "<: if not (%syoutube%s in PLATFORMS) :>/brand/src/platforms/youtube.md<: endif :>"\n' "$q" "$q"
    for s in $SM_EXAMPLES; do printf '  - "<: if %s :>/%s<: endif :>"\n' "$SM_EXAMPLE_GATE" "$s"; done
    printf '_skip_if_exists:\n'
    for s in $SM_SHARED $SM_SEEDS; do printf '  - /%s\n' "$s"; done
    printf 'BRAND_NAME:\n  type: str\n'
    # A stand-in for the family-shared questions block (D80): its own markers, its own bytes.
    printf '# BEGIN family-shared questions (D48)\nAGENT_CLIENTS:\n  type: str\n  multiselect: true\n# END family-shared questions (D48)\n'
    printf '_migrations:\n'
    sm_family_migrations_block
    printf '  - version: %s\n    command: python3 "<%% _copier_conf.src_path %%>/%s"\n    when: "<%% _stage == %safter%s %%>"\n' "$SM_D76_VERSION" "$SM_D76_MIGRATION" "$q" "$q"
    # D84's crossing entry (check 32), after v0.4.2's and before the family update block.
    printf '  - version: %s\n    command: %s"<%% _copier_python %%>" "<%% _copier_conf.src_path %%>/%s"%s\n    when: "<%% _stage == %safter%s %%>"\n' \
      "$SM_HOWTO_VERSION" "$q" "$SM_HOWTO_MIGRATION" "$q" "$q" "$q"
    # The family update block (D81), byte for byte the tag's, closing _migrations.
    sm_family_update_block
    # _tasks (D81, D84): stand-ins for media's three, D84's copy-time warning, then the
    # baseline task exactly as _common.sh transcribes it.
    printf '_tasks:\n  - command: "[ -d .git ] || git init --initial-branch=main"\n    when: "<%% _copier_operation == %scopy%s %%>"\n' "$q" "$q"
    printf '  - command: "chmod +x .claude/hooks/*.sh 2>/dev/null || true"\n    when: "<%% _copier_operation == %scopy%s %%>"\n' "$q" "$q"
    printf '  - command: "git config --get filter.lfs.process || git config filter.lfs.required true"\n    when: "<%% _copier_operation == %scopy%s %%>"\n' "$q" "$q"
    printf '  - command: >-\n      [ ! -f %s ] || [ -f %s ] || echo %sa fixture warning%s\n    when: "<%% _copier_operation == %scopy%s %%>"\n' \
      "$SM_AUTHOR_ANSWERS" "$SM_AUTHOR_GUIDE_START" "$q" "$q" "$q" "$q"
    printf '%s\n' "$SM_BASELINE_TASK"
  } > "$r/copier.yml"
  # The refresh data (D81), from the lists check 31 holds the real one to.
  SR_PATHS="$SM_REFRESH_PATHS" SR_TOP="$(printf '%s\n' "${SM_REFRESH_TOP[@]}")" SR_HOOKS="$SM_REFRESH_HOOKS" \
  SR_DENY="$(printf '%s\n' "${SM_REFRESH_DENY[@]}")" SR_ASK="$(printf '%s\n' "${SM_REFRESH_ASK[@]}")" \
  SR_SERVERS="$SM_REFRESH_MCP_SERVERS" SR_FILES="$SM_REFRESH_MCP_FILES" \
  python3 -I - "$r/$SM_REFRESH_DATA" "$SM_REFRESH_TEMPLATE" "$SM_REFRESH_RESTORE" <<'PYFIX'
import json, os, sys
E = os.environ
top = {kv.split("=", 1)[0]: json.loads(kv.split("=", 1)[1]) for kv in E["SR_TOP"].splitlines() if kv}
files = {l.split("\t")[0]: l.split("\t")[1].split(".") for l in E["SR_FILES"].splitlines() if l.strip()}
data = {"format": 1, "template": sys.argv[2], "refresh": E["SR_PATHS"].split(), "restore": [sys.argv[3]],
        "settings": dict(top, hooks=json.loads(E["SR_HOOKS"]),
                         permissions={"deny": E["SR_DENY"].splitlines(), "ask": E["SR_ASK"].splitlines()}),
        "mcp": {"servers": E["SR_SERVERS"].split(), "files": files}}
os.makedirs(os.path.dirname(sys.argv[1]), exist_ok=True)
open(sys.argv[1], "w").write(json.dumps(data, indent=2) + "\n")
PYFIX
  for s in $SM_SHARED $SM_SEEDS; do
    [[ "$s" == .agents || "$s" == .agents/skills ]] && continue
    mkdir -p "$(dirname "$t/$s")"; printf '# %s\n' "${s##*/}" > "$t/$s"
  done
  ln -s "$SM_AGENTS_SKILLS_LINK" "$t/.agents/skills"
  mkdir -p "$r/migrations"; printf 'print("fixture migration")\n' > "$r/$SM_D76_MIGRATION"
  printf 'print("fixture outside-link migration")\n' > "$r/$SM_OUTSIDE_MIGRATION"
  printf 'print("fixture crossing report")\n' > "$r/$SM_HOWTO_MIGRATION"
  chmod 755 "$r/$SM_OUTSIDE_MIGRATION"
  # The permissions script's stand-in is a stub check 29 can drive (STUB_PERM_* below): by
  # default it finds two of media's own seed rules missing until --write has run.
  mkdir -p "$t/.claude"
  cat > "$t/$SM_PERMISSIONS_PY" <<'PYSTUB'
import os, sys
from pathlib import Path
mark = Path(__file__).resolve().parent / "stub-permissions-written"
if "--write" in sys.argv:
    mark.write_text("written\n")
    sys.exit(int(os.environ.get("STUB_PERM_WRITE_EXIT", "0")))
if mark.exists() and not os.environ.get("STUB_PERM_STILL"):
    print("every expressible rule is in place")
    sys.exit(0)
missing = [m for m in os.environ.get("STUB_PERM_MISSING", "mcp__elevenlabs__text_to_speech|Edit(**/renders/**)").split("|") if m]
for m in missing:
    print("  \u2717 %s -> a rule is missing" % m)
sys.exit(int(os.environ.get("STUB_PERM_EXIT", "1" if missing else "0")))
PYSTUB
  # A stand-in for every family-shared file the shared paths above did not write (D80), the two
  # session hooks executable as the family's are, and rules 06 with its family block.
  local fpath fsrc _scope
  while read -r fpath fsrc _scope; do
    [[ -z "$fpath" || -e "$r/$fsrc" || -L "$r/$fsrc" ]] && continue
    mkdir -p "$(dirname "$r/$fsrc")"; printf '# %s — a family stand-in\n' "$fpath" > "$r/$fsrc"
  done <<< "$SM_FAMILY_SHARED"
  chmod 755 "$t/.claude/hooks/context-threshold-handoff.sh" "$t/.claude/hooks/pre-compact-handoff.sh" \
    "$t/.claude/hooks/how-to-read-only.sh" "$r/$SM_FAMILY_UPDATE_SCRIPT"
  mkdir -p "$t/.claude/rules/syntek-media"
  printf '# 06-global-rules.md\n\n## 13. Web and code tools\n\n<!-- BEGIN family-shared rules: web and code tools -->\n- Use the plainest tool.\n<!-- END family-shared rules: web and code tools -->\n' \
    > "$t/.claude/rules/syntek-media/06-global-rules.md"
  printf '{"format": 1, "folders": []}\n' > "$t/$SM_DATAROOT_MAP"
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
    printf '{\n  "model": "opus",\n  "autoCompactEnabled": false,\n  "idleCompaction": false,\n  "permissions": {\n'
    printf '    "deny": [%s],\n' "$(for s in "${SM_SETTINGS_DENY[@]}" "${SM_SETTINGS_FAMILY_DENY[@]}"; do printf '"%s", ' "$s"; done | sed 's/, $//')"
    printf '    "allow": [%s],\n' "$(for s in "${SM_SETTINGS_ALLOW[@]}"; do printf '"%s", ' "$s"; done | sed 's/, $//')"
    printf '    "ask": [%s]\n' "$(for s in "${SM_SETTINGS_ASK[@]}" "${SM_SETTINGS_FAMILY_ASK[@]}"; do printf '"%s", ' "$s"; done | sed 's/, $//')"
    printf '  },\n  "hooks": %s\n}\n' "$SM_SETTINGS_HOOKS"
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
  local tmp real_root="$SM_ROOT" real_tpl="$TPL" real_copier="$COPIER" t f m
  bold "▸ $SCRIPT_NAME --self-test"; log ""
  command -v python3 >/dev/null 2>&1 || die "python3 is not installed"
  tmp="$(sm_mktemp)"
  # shellcheck disable=SC2064
  trap "rm -rf '$tmp'" RETURN
  # The fixture is in no Git work tree until check 21's probes make it one: the ceiling stops
  # Git from finding a repository above the temporary folder.
  local -x GIT_CEILING_DIRECTORIES
  GIT_CEILING_DIRECTORIES="$(dirname "$tmp")"
  write_fixture "$tmp"
  SM_ROOT="$tmp"; TPL="$tmp/template"; COPIER="$tmp/copier.yml"; TREE="$TPL"; SM_SETS_FOR=""
  # The manifest is the writer's record of the fixture's own stand-ins, as --write-manifest
  # writes the real one from the vendored bytes: checks 21–27 hold the fixture to it.
  sm_family_py write "$tmp" || die "the family-shared.json writer failed on the fixture"
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
  grep -vF "/.gemini<: endif" "$tmp/c" > "$COPIER"; SM_SETS_FOR=""
  probe "check 8 fires when a client folder loses its update gate (D80)" "check 8 — the client folder .gemini/ has no update-gated _exclude line"
  awk -v q="'" '/^_skip_if_exists:/ { print "  - \"<: if _copier_operation == " q "update" q " :>/.claude/skills/grilling<: endif :>\"" } { print }' "$tmp/c" > "$COPIER"; SM_SETS_FOR=""
  probe "check 8 fires when a family skill's folder, not its SKILL.md, takes the shared gate (D80)" "check 8 — /.claude/skills/grilling carries the shared files' update gate"
  awk -v q="'" '/^_skip_if_exists:/ { print "  - \"<: if _copier_operation == " q "update" q " :>/how-to<: endif :>\"" } { print }' "$tmp/c" > "$COPIER"; SM_SETS_FOR=""
  probe "check 8 fires when /how-to takes the shared gate, not its family files one by one (D84)" "check 8 — /how-to carries the shared files' update gate"
  grep -vF "/how-to/src/TEMPLATE-GUIDE/the-data-root.md<: endif" "$tmp/c" > "$COPIER"; SM_SETS_FOR=""
  probe "check 8 fires when one of the guide's family files loses its update gate (D84)" "check 8 — the shared file how-to/src/TEMPLATE-GUIDE/the-data-root.md"
  cp "$tmp/c" "$COPIER"; SM_SETS_FOR=""

  f=publishing/src/schedule.md; cp "$t/$f" "$tmp/h"
  sed -i '/seeded stub/d' "$t/$f";                             probe "check 9 fires when a register loses its banner" "check 9 — $f"; cp "$tmp/h" "$t/$f"
  f=brand/src/platforms/tiktok.md; cp "$t/$f" "$tmp/h"
  sed -i '/seeded stub/d' "$t/$f";                             probe "check 9 fires when a platform profile loses its banner" "check 9 — $f"; cp "$tmp/h" "$t/$f"
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
  sed -i 's/"timeout":10}]}],"PreToolUse"/"timeout":30}]}],"PreToolUse"/' "$t/.claude/settings.json"; probe "check 12 fires when a family hook registration drifts (D80)" "check 12 — .claude/settings.json hooks are not exactly syntek-author's v0.8.0 seed's hooks object"; cp "$tmp/h" "$t/.claude/settings.json"
  sed -i 's/"idleCompaction": false/"idleCompaction": true/' "$t/.claude/settings.json"; probe "check 12 fires when idle compaction is switched on (D81)" "check 12 — .claude/settings.json idleCompaction is not false"; cp "$tmp/h" "$t/.claude/settings.json"
  sed -i 's#"Edit(/how-to/\*\*)", ##' "$t/.claude/settings.json"; probe "check 12 fires when the guide's deny is lost (D84)" "check 12 — .claude/settings.json does not deny Edit(/how-to/**)"; cp "$tmp/h" "$t/.claude/settings.json"
  sed -i 's#"Edit(/how-to/\*\*)", "mcp__code-review-graph__embed_graph_tool"#"mcp__code-review-graph__embed_graph_tool", "Edit(/how-to/**)"#' "$t/.claude/settings.json"
  probe "check 12 fires when the guide's deny leaves D13's order (D84)" "check 12 — .claude/settings.json denies its rules out of D13's order"; cp "$tmp/h" "$t/.claude/settings.json"
  python3 -c 'import json,sys; p=sys.argv[1]; d=json.load(open(p)); del d["hooks"]["SessionStart"]; json.dump(d,open(p,"w"))' "$t/.claude/settings.json"
  probe "check 12 fires when the SessionStart compact entry is lost (D81)" "check 12 — .claude/settings.json hooks are not exactly"; cp "$tmp/h" "$t/.claude/settings.json"
  sed -i 's/"mcp__scrapling__stealthy_fetch", "mcp__scrapling__bulk_stealthy_fetch"/"mcp__scrapling__bulk_stealthy_fetch", "mcp__scrapling__stealthy_fetch"/' "$t/.claude/settings.json"
  probe "check 12 fires when the family's asks leave the family's order (D80)" "check 12 — .claude/settings.json asks the family's eight MCP tools out of the family's order"; cp "$tmp/h" "$t/.claude/settings.json"
  sed -i 's/, "mcp__code-review-graph__embed_graph_tool"//' "$t/.claude/settings.json"; probe "check 12 fires when the embed_graph_tool deny is lost (D80)" "check 12 — .claude/settings.json does not deny mcp__code-review-graph__embed_graph_tool"; cp "$tmp/h" "$t/.claude/settings.json"
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
  # The v0.4.2 entry alone goes: the update block below it stays, which check 26 holds whole.
  awk -v v="  - version: $SM_D76_VERSION" '$0 == v { skip = 3 } skip { skip--; next } { print }' "$tmp/c" > "$COPIER"
  probe "check 19 fires when the D76 migration is not declared" "check 19 — _migrations has no $SM_D76_VERSION entry"
  cp "$tmp/c" "$COPIER"; mv "$tmp/$SM_D76_MIGRATION" "$tmp/mig-held"
  probe "check 19 fires when a migration's script is missing" "check 19 — a migration runs $SM_D76_MIGRATION"
  mv "$tmp/mig-held" "$tmp/$SM_D76_MIGRATION"
  # 20: the outside-link pair first, and no other unversioned entry.
  sed -i "0,/_stage == 'before'/s//_stage == 'after'/" "$COPIER"; SM_SETS_FOR=""
  probe "check 20 fires when the outside-link hold does not run before the render" "check 20 — _migrations does not open with D76's outside-link pair"
  cp "$tmp/c" "$COPIER"; SM_SETS_FOR=""
  awk -v e="$(printf '  - command: python3 "<%% _copier_conf.src_path %%>/%s"\n    when: "<%% _stage == %safter%s %%>"' "$SM_D76_MIGRATION" "'" "'")" \
    '$0 == "# BEGIN family-shared update (D48)" { print e } { print }' "$tmp/c" > "$COPIER"; SM_SETS_FOR=""
  probe "check 20 fires on an unversioned entry between the pair and the update entry" "check 20 — an unversioned _migrations entry runs $SM_D76_MIGRATION"
  printf '  - version: v9.9.9\n    command: python3 "<%% _copier_conf.src_path %%>/%s"\n    when: "<%% _stage == %safter%s %%>"\n' "$SM_D76_MIGRATION" "'" "'" > "$tmp/extra"
  awk -v x="$tmp/extra" '/^_tasks:/ { while ((getline l < x) > 0) print l } { print }' "$tmp/c" > "$COPIER"; SM_SETS_FOR=""
  probe "check 20 fires when the family update entry is not last (D81)" "check 20 — _migrations does not close with the family 'update' block's one entry"
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
  probe_clean "in a Git work tree, check 21 reads the index's 100755, not the working tree's 644"
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

  # 23–26: the manifest (D80). Each probe edits the record or one vendored byte, then restores.
  m="$tmp/$SM_FAMILY_MANIFEST"; cp "$m" "$tmp/manifest.held"
  rm -f "$m";                                                 probe "check 23 fires when family-shared.json is missing" "check 23 — family-shared.json is missing"; cp "$tmp/manifest.held" "$m"
  sed -i 's/"owner": "syntek-media"/"owner": "syntek-author"/' "$m"; probe "check 23 fires on another template's owner" "check 23 — family-shared.json must hold format 1, owner syntek-media"; cp "$tmp/manifest.held" "$m"
  sed -i 's/"release": "[^"]*"/"release": "v9.9.9"/' "$m";  probe "check 23 fires on a release Git does not allow" "check 23 — family-shared.json must hold"; cp "$tmp/manifest.held" "$m"
  sed -i '\#"path": ".gemini/CLAUDE.md"#d' "$m";              probe "check 24 fires when the record drops a vendored file" "check 24 — family-shared.json files are not the vendored set"; cp "$tmp/manifest.held" "$m"
  python3 -c 'import json,sys; m=json.load(open(sys.argv[1])); m["blocks"].reverse(); json.dump(m,open(sys.argv[1],"w"))' "$m"
  probe "check 24 fires when the blocks leave the family's order" "check 24 — family-shared.json blocks are not exactly"; cp "$tmp/manifest.held" "$m"
  f="$t/.claude/skills/wayfinder/SKILL.md"; cp "$f" "$tmp/h"
  printf 'x\n' >> "$f";                                       probe "check 25 fires when one vendored byte changes" "check 25 — template/.claude/skills/wayfinder/SKILL.md has SHA-256"; cp "$tmp/h" "$f"
  chmod 644 "$t/.claude/hooks/pre-compact-handoff.sh";         probe "check 25 fires when a session hook loses its executable bit" "check 25 — template/.claude/hooks/pre-compact-handoff.sh is at mode 644, not 755"
  chmod 755 "$t/.claude/hooks/pre-compact-handoff.sh"
  chmod 644 "$t/.claude/hooks/how-to-read-only.sh";            probe "check 25 fires when the guide guard loses its executable bit (D84)" "check 25 — template/.claude/hooks/how-to-read-only.sh is at mode 644, not 755"
  chmod 755 "$t/.claude/hooks/how-to-read-only.sh"
  chmod 644 "$tmp/$SM_FAMILY_UPDATE_SCRIPT";                   probe "check 25 fires when the vendored update script loses its executable bit (D81)" "check 25 — $SM_FAMILY_UPDATE_SCRIPT is at mode 644, not 755"
  chmod 755 "$tmp/$SM_FAMILY_UPDATE_SCRIPT"
  sed -i 's#"target": "../.claude/skills"#"target": "../.claude/skillz"#' "$m"; probe "check 25 fires when the record names another target for the D76 link" "check 25 — template/.agents/skills is the link"; cp "$tmp/manifest.held" "$m"
  cp "$COPIER" "$tmp/c"
  sed -i 's/^  multiselect: true$/  multiselect: false/' "$COPIER"; SM_SETS_FOR=""
  probe "check 26 fires when one byte of the questions block changes" "check 26 — the lines between copier.yml's family-shared questions markers"
  cp "$tmp/c" "$COPIER"; SM_SETS_FOR=""
  sed -i 's/^  # each file this update did not deliver/  # Each file this update did not deliver/' "$COPIER"; SM_SETS_FOR=""
  probe "check 26 fires when one byte of the update block changes (D81)" "check 26 — the lines between copier.yml's family-shared update markers"
  cp "$tmp/c" "$COPIER"; SM_SETS_FOR=""
  f="$t/.claude/rules/syntek-media/06-global-rules.md"; cp "$f" "$tmp/h"
  sed -i '/^<!-- END family-shared rules/d' "$f";             probe "check 26 fires when rules 06 loses the block's END marker" "check 26 — template/.claude/rules/syntek-media/06-global-rules.md holds"; cp "$tmp/h" "$f"
  rm -f "$m"; sm_family_py write "$tmp" || die "the writer failed"
  probe_clean "--write-manifest writes the record the checks hold the fixture to"
  cp "$tmp/manifest.held" "$m"
  printf '{"format": 1, "folders": [{"path": "production/src/footage/raw"}]}\n' > "$t/$SM_DATAROOT_MAP"
  probe "check 28 fires when the data-root map claims a folder" "check 28 — $SM_DATAROOT_MAP is not exactly"; printf '{"format": 1, "folders": []}\n' > "$t/$SM_DATAROOT_MAP"

  # 30: the baseline task last, line for line, after D84's warning (D81, D84).
  cp "$COPIER" "$tmp/c"
  printf '  - command: "true"\n    when: "<%% _copier_operation == %scopy%s %%>"\n' "'" "'" >> "$COPIER"; SM_SETS_FOR=""
  probe "check 30 fires when the baseline task is not last (D81)" "check 30 — syntek-author's baseline task is _tasks entry 5 of 6, not the last"
  sed 's/ baseline --src / baseline  --src /' "$tmp/c" > "$COPIER"; SM_SETS_FOR=""
  probe "check 30 fires when a byte of the baseline task changes (D81)" "check 30 — _tasks holds no entry equal, line for line, to syntek-author's baseline task"
  awk '/^  - command: >-$/ { skip = 2; next } skip { skip--; next } { print }' "$tmp/c" > "$COPIER"; SM_SETS_FOR=""
  probe "check 30 fires when D84's copy-time warning is missing (D84)" "check 30 — the _tasks entry before the baseline task is not D84's copy-time warning"
  cp "$tmp/c" "$COPIER"; SM_SETS_FOR=""
  # 31: the refresh data (D81, D84), one fault each.
  f="$tmp/$SM_REFRESH_DATA"; cp "$f" "$tmp/refresh.held"
  rr() { python3 -I -c "import json,sys; p=sys.argv[1]; d=json.load(open(p)); $1; json.dump(d, open(p, 'w'), indent=2)" "$f"; }
  rr 'd["format"] = 2';                                    probe "check 31 fires when the refresh data is not format 1" "check 31 — $SM_REFRESH_DATA does not hold \"format\": 1"; cp "$tmp/refresh.held" "$f"
  rr 'd["refresh"].remove(".claude/skills/wayfinder/SKILL.md")'; probe "check 31 fires when a refresh path is dropped" "check 31 — $SM_REFRESH_DATA refresh is not exactly the twenty-seven"; cp "$tmp/refresh.held" "$f"
  rr 'd["restore"] = ["how-to", "handoffs"]';              probe "check 31 fires when restore names more than how-to (D84)" "check 31 — $SM_REFRESH_DATA restore is"; cp "$tmp/refresh.held" "$f"
  rr 'd["settings"]["hooks"]["PreToolUse"].insert(0, [e for e in json.load(open(sys.argv[1].replace("migrations/family-refresh.json", "template/.claude/settings.json")))["hooks"]["PreToolUse"] if "dataroot" in json.dumps(e)][0])'
  probe "check 31 fires when the data-root guard is listed (D81)" "check 31 — $SM_REFRESH_DATA lists the hook entry PreToolUse Edit|Write|MultiEdit|NotebookEdit|Grep|Glob, which names no shared hook"; cp "$tmp/refresh.held" "$f"
  rr 'd["settings"]["permissions"]["deny"].append("Edit(**/drafts/**)")'; probe "check 31 fires when a listed rule is not in the seed (D81)" "check 31 — $SM_REFRESH_DATA lists the deny rule Edit(**/drafts/**), which the seed does not hold"; cp "$tmp/refresh.held" "$f"
  rr 'd["mcp"]["files"][".claude/mcp_config.json"] = ["mcpServers"]'; probe "check 31 fires when the mcp lane names .claude/mcp_config.json (D76)" "check 31 — $SM_REFRESH_DATA mcp.files names .claude/mcp_config.json"; cp "$tmp/refresh.held" "$f"
  rr 'd["settings"]["permissions"]["ask"].append(d["settings"]["permissions"]["ask"].pop(0))'
  probe "check 31 fires when the asks are out of the seed's order (VEND-14)" "check 31 — $SM_REFRESH_DATA lists its ask rules out of D13's order"; cp "$tmp/refresh.held" "$f"
  rr 'd["settings"]["model"] = "opus"';                    probe "check 31 fires when the refresh data lists the model (D81)" "check 31 — $SM_REFRESH_DATA lists the top-level value model"; cp "$tmp/refresh.held" "$f"
  unset -f rr
  probe_clean "the baseline task last and the refresh data in shape"

  # 32: D84's crossing entry, one fault each; misplaced after the update block, it is check 20's.
  cp "$COPIER" "$tmp/c"
  local he
  he="$(printf '  - version: %s\n    command: %s"<%% _copier_python %%>" "<%% _copier_conf.src_path %%>/%s"%s\n    when: "<%% _stage == %safter%s %%>"' \
    "$SM_HOWTO_VERSION" "'" "$SM_HOWTO_MIGRATION" "'" "'" "'")"
  hmove() { # $1 = the line the entry goes before (an exact match)
    awk -v v="  - version: $SM_HOWTO_VERSION" -v at="$1" -v e="$he" \
      '$0 == v { skip = 3 } skip { skip--; next } $0 == at { print e } { print }' "$tmp/c" > "$COPIER"; SM_SETS_FOR=""
  }
  hmove "  - version: $SM_D76_VERSION"
  probe "check 32 fires when the v0.6.0 entry comes before v0.4.2's (D84)" "check 32 — the $SM_HOWTO_VERSION entry is _migrations entry 3 of 5, not after the $SM_D76_VERSION entry"
  hmove "_tasks:"
  probe "check 32 stays quiet, and check 20 claims it, when the v0.6.0 entry follows the update block" "check 20 — _migrations does not close with the family 'update' block's one entry"
  sed "s#^    command: '\"<% _copier_python %>\" \"<% _copier_conf.src_path %>/$SM_HOWTO_MIGRATION\"'\$#    command: python3 \"<% _copier_conf.src_path %>/$SM_HOWTO_MIGRATION\"#" "$tmp/c" > "$COPIER"; SM_SETS_FOR=""
  probe "check 32 fires when the v0.6.0 entry runs python3, not _copier_python (D84, D85)" "check 32 — the $SM_HOWTO_VERSION entry does not run"
  hmove "no such line"
  probe "check 32 fires when the v0.6.0 entry is not declared (D84)" "check 32 — _migrations declares 'version: $SM_HOWTO_VERSION' 0 time(s)"
  cp "$tmp/c" "$COPIER"; SM_SETS_FOR=""; unset -f hmove
  probe_clean "the v0.6.0 crossing entry after v0.4.2's and before the update block"

  # 10 and 27: a render of the fixture, whose family files must keep the recorded bytes.
  local rt="$tmp/render"; cp -a "$t" "$rt"; TREE="$rt"; load_owned "$TREE"
  probe_clean "a render whose family files are the recorded bytes"
  printf '{"mcpServers": {"elevenlabs": {}}}\n' > "$rt/.mcp.json"
  probe "check 10 fires when a render's .mcp.json is not the family's (an ElevenLabs server in it)" "check 10 — .mcp.json has SHA-256"
  cp "$t/.mcp.json" "$rt/.mcp.json"
  printf 'x\n' >> "$rt/.claude/skills/grilling/SKILL.md"
  probe "check 27 fires when a render changes a token-free family file" "check 27 — .claude/skills/grilling/SKILL.md has SHA-256"
  cp "$t/.claude/skills/grilling/SKILL.md" "$rt/.claude/skills/grilling/SKILL.md"
  chmod 644 "$rt/.claude/hooks/context-threshold-handoff.sh"
  probe "check 27 fires when a render's session hook is not executable" "check 27 — .claude/hooks/context-threshold-handoff.sh is not executable in the render"
  chmod 755 "$rt/.claude/hooks/context-threshold-handoff.sh"
  chmod 644 "$rt/.claude/hooks/how-to-read-only.sh"
  probe "check 27 fires when a render's guide guard is not executable (D84)" "check 27 — .claude/hooks/how-to-read-only.sh is not executable in the render"
  chmod 755 "$rt/.claude/hooks/how-to-read-only.sh"
  printf 'x\n' >> "$rt/.codex/config.toml"
  probe_clean "a render of a family file that carries the shared keys is not compared byte for byte"
  STUB_PERM_MISSING='mcp__elevenlabs__voice_clone|mcp__scrapling__fetch' \
    probe "check 29 fires when the permissions script finds a family rule missing in a render" "check 29 — $SM_PERMISSIONS_PY --check finds mcp__scrapling__fetch missing"
  STUB_PERM_MISSING='Edit(**/renders/**)|Edit(/how-to/**)' \
    probe "check 29 fires when the guide's deny, a family rule, is missing in a render (D84)" "check 29 — $SM_PERMISSIONS_PY --check finds Edit(/how-to/**) missing"
  STUB_PERM_STILL=1 \
    probe "check 29 fires when --write leaves a rule missing" "check 29 — after $SM_PERMISSIONS_PY --write, --check still exits 1"
  STUB_PERM_EXIT=2 \
    probe "check 29 fires when the permissions script cannot run in a render" "check 29 — $SM_PERMISSIONS_PY --check exits 2"
  STUB_PERM_WRITE_EXIT=1 \
    probe "check 29 fires when --write fails in a copy of the render" "check 29 — $SM_PERMISSIONS_PY --write fails"
  rm -rf "$rt"; TREE="$TPL"; load_owned "$TREE"

  # The over-author scope, on a render-shaped copy (the source's family files are check 25's):
  # the shared files are syntek-author's, so checks 5, 6, 10, 12 and 13 do not read them, nor
  # check 27 the family files it wrote first; media's own seeds are still held to their contract.
  local oa="$tmp/oa"; cp -a "$t" "$oa"; TREE="$oa"
  while IFS= read -r f; do is_shared "$f" || printf '%s\n' "$f"; done < <(tree_files "$oa") > "$oa.owned"
  load_owned "$oa"
  printf '{"mcpServers": {"drive": {}}}\n' > "$oa/.mcp.json"
  printf 'x\n' >> "$oa/.claude/skills/handoff/SKILL.md"
  printf -- '- **01/01/2027** — **syntek-author owns this file.** Kept.\n' >> "$oa/.claude/MEMORY.md"
  printf '{ not json\n' > "$oa/.claude/settings.json"
  probe_clean "over syntek-author, its .mcp.json, MEMORY.md, settings.json and family files are not media's to audit"
  f=publishing/src/publish-log.md
  printf '| 01/01/2027 | youtube | youtube.short | 003 | x | on | burned | — |\n' >> "$oa/$f"
  probe "check 7 still fires on a media seed, over syntek-author" "check 7 — $f"
  rm -rf "$oa" "$oa.owned"; TREE="$TPL"; SM_OWNED_MODE=false; SM_OWNED=()

  SM_ROOT="$real_root"; TPL="$real_tpl"; COPIER="$real_copier"; SM_SETS_FOR=""
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
command -v git >/dev/null 2>&1 || die "git is not installed (checks 21 and 25 read the vendored files' modes from Git's index)"

if $WRITE_MANIFEST; then
  rc=0
  sm_family_py write "$SM_ROOT" || rc=$?
  [[ "$rc" -eq 0 ]] || die "family-shared.json was not written (exit $rc): vendor every file and block from syntek-author $SM_FAMILY_RELEASE first"
  log "  wrote $SM_FAMILY_MANIFEST from the vendored files and blocks (syntek-author $SM_FAMILY_RELEASE); now checking"
fi

bold "▸ $SCRIPT_NAME"
STATUS=0
for target in "$TPL" "${TARGETS[@]}"; do
  [[ -d "$target" ]] || die "not a directory: $target"
  TREE="$(cd "$target" && pwd)"
  load_owned "$TREE"
  run_checks
  scope="standalone"; $SM_OWNED_MODE && scope="over syntek-author: media-owned paths; checks 5, 6, 10, 12, 13, 29 skipped"
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
  bold "✓ Every seed is wired and ships empty; every shared file is copy-only; every author-owned folder ships its pair only; every family file and block is as family-shared.json records it."
  exit 0
fi
log "  A polluted seed is a one-way door: no update can retract it (SB rule 21). The wiring lives in"
log "  copier.yml's _skip_if_exists and _exclude (DESIGN.md Sections 3.1–3.6)."
exit 1
