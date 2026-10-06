# AGENTS.md — syntek-media template development

Read `.claude/CLAUDE.md`, root `CONTEXT.md` and the sections of `DESIGN.md` relevant to the
change, then the affected folder's CONTEXT.md and CLAUDE.md, before editing.

This repository develops a Copier template. Everything under template/ is product text;
its manuals, rules and skills never govern development. Do not invoke a product skill or
call ElevenLabs from here. Tests use fixtures generated at runtime.

DESIGN.md wins. Change it only with the maintainer's explicit approval; ask about decisions
it does not settle. Preserve authorised work and source repositories. Follow the development
manual for tokens, formats, audits and release procedure. Development model tier labels
identify the kind of work; use the owner's configured client model.

`.agents` aliases the development .claude folder, which has no production skills.
The development .codex/config.toml disables all product skills and sets no instruction
fallback into template/. Read product files only as the source being edited.
