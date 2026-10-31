@./CONTEXT.md

# CLAUDE.md — how-to/src/

Read order: `.claude/CLAUDE.md` → `.claude/MEMORY.md` → `how-to/CONTEXT.md` →
`how-to/CLAUDE.md` → this folder's `CONTEXT.md` (what the chapters are, imported above) → this
file.

## Purpose (one line)

Find the chapter that answers the question; never treat a chapter as the work.

## How to work here

- **Routing:** every chapter is under `how-to/src/TEMPLATE-GUIDE/`, whose pair says which to
  read. The work lives in the folders the project's rules in `.claude/rules/` name, never here.
- **Model:** **Opus**: choosing the chapter that owns an answer is judgement.
- **Concrete steps:** go to `how-to/src/TEMPLATE-GUIDE/` → read its `CONTEXT.md` → read the
  chapter it names → follow the chapter to the rule that decides.
- **Definition of done:** the right chapter is found, and nothing under `how-to/` changed except
  through a template's update, its recovery and the commands its report prints.

## Guardrails

- **This `src/` is not a production folder.** Never draft, revise, promote or file anything
  here, and never count a chapter as part of the work.
- **Never edit, write, move or delete a chapter, even when asked**, except through a template's
  update, its recovery and the commands its update report prints for a file here. Claude Code
  denies it, a hook refuses it, and the next update puts the file back.
- **Check a chapter only when asked.** A template's lint and flag checks read this folder only
  when they are pointed at it; a finding here is reported to the owner, never fixed here.

## Output & naming

- **Writes nothing.** Every chapter here is a template's.
- **Names:** `TEMPLATE-GUIDE/` is the one folder here; see its `CLAUDE.md` for chapter names.
