@./CONTEXT.md

# CLAUDE.md — handoffs/

Read order: `.claude/CLAUDE.md` → `.claude/MEMORY.md` → this folder's `CONTEXT.md`
(what a handoff carries, imported above) → this file.

## Purpose (one line)

Hold the session bridges that let a fresh session resume the work without re-deriving it.

## How to work here

- **Routing:** the `handoff` skill owns this folder and its format; any session that is ending
  runs it. The hooks in `.claude/hooks/` steer here: `context-threshold-handoff.sh` as the
  context window fills, `pre-compact-handoff.sh` when compaction is attempted.
- **Model:** **Opus**: deciding what is load-bearing enough to carry is judgement, and getting it
  wrong costs the next session an hour of re-derivation.
- **Concrete steps:** record durable knowledge in its real home first → write the handoff with
  every part the skill names → print its path → **stop the turn**, so the author or owner can
  run `/clear` and resume from the file.
- **Definition of done:** the file exists as `handoffs/HANDOFF-<DESCRIPTOR>-DD-MM-YYYY.md` (or
  where and as the project's rules say), carries every part, anchors each in-flight item with
  `path:line`, references every artefact by path, contains nothing confidential, its path has
  been printed, and the turn has ended.

## Guardrails

- **Write it, print the path, then stop.** A handoff followed by more work is stale before it is
  read.
- **`path:line` anchors on every in-flight item.** 'The draft is partly done' is not a
  handoff; a path and a line, with what is done and what is not, is.
- **Reference; never paste.** A handoff that quotes half a passage has recreated the context it
  was meant to replace.
- **Never paste confidential material.** These files are committed. Credentials, personal contact
  details and private correspondence are named and located, never reproduced.
- **Not a memory store.** If a fact will matter next month, record it in `.claude/MEMORY.md` or a
  folder file, and link to it from the handoff.
- **Never edit an old handoff** to bring it up to date: write a new one and prune the old.
- **Prune once the work has resumed and landed.** A stale handoff read as current is worse than
  none.

## Output & naming

- **Hand-written:** Markdown only, one file per handed-over session, named
  `HANDOFF-<DESCRIPTOR>-DD-MM-YYYY.md`: the descriptor in capitals naming the work, the date as
  DD-MM-YYYY.
- **Not here:** decisions, facts, prose, evidence or decision maps; each has a home elsewhere.
