---
workflow: 05-narrate-an-audiobook
phase: produce
skills: [narrate-audiobook]
model: opus
---

# STEPS.md — narrate an audiobook

**Last Updated**: <%DATE%> **Version**: 0.1.0 **Maintained By**: <%OWNER_NAME%>
**Language**: British English (en_GB)

The ordered procedure for planning an audiobook and voicing or recording its chapters on the
author's request. Each step names the skill and guide it uses. **Run in order** (the plan is
approved, the route chosen, and the cost stated and agreed, before anything is generated) and tick
`CHECKLIST.md` as you go.

> Read the read-order files first (this folder's `CONTEXT.md` and `CLAUDE.md`). The
> `narrate-audiobook` skill is this procedure in skill form.

## 1. Confirm the request

> **Skill:** `narrate-audiobook` · **Guide:** `production/docs/reference/audiobook-narration.md`

Confirm which audiobook piece and which chapters the author wants planned, voiced or recorded.
Read the brief: `kind: audiobook`, `picture: false`, its deliverables `audiobook.<store>` keys, and
M1 dated. An audiobook has no script: this procedure writes its plan and passes its M2. If nothing
was asked, stop. _Substantive._

## 2. Choose the route per channel

> **Skill:** `narrate-audiobook` · **Guide:** `production/docs/reference/audiobook-narration.md`

For each channel, agree `human`, `ai` or `external` with the author, reading where that channel
stands in the guide (re-check a row marked `VERIFY` before relying on it). Say plainly that ACX
and Audible need a human narrator unless the author is authorised otherwise, and that INaudio's
synthetic route is ElevenLabs' own package, made outside this template. _Substantive._

## 3. Write the chapter register and the credits, and record M2

> **Skill:** `narrate-audiobook` · **Guide:** `production/docs/reference/audiobook-narration.md`

Write `production/src/audiobook/<piece>.md` in the format its folder's `CLAUDE.md` fences: its
`channels` each the store part of an `[audiobook.<store>]` key (`acx`, `spotify_authors`); one
row per chapter, its Source the chapter's file (a syntek-author unit whose status is `final`,
where present, unless the author says otherwise, or a text the author provides); and the credit
rows `ch00` and `ch99`, each `planned`. Write the credits' words with the author in
`<piece>.ch00.md` and `<piece>.ch99.md` beside it. For a chapter on the `external` route, record
in Master the export and where it is kept, and in Check `external`; nothing more is made here for
it. When the author approves the plan, date the register's `approved:`, check M2 against the
ladder guide, record `M2` with today's date and `M3: 'n/a — no picture'` in the brief's
`verified`, and set `status: scripted`. _Substantive._

## 4. Check the setup and the narrator

> **Skill:** `narrate-audiobook` · **Guide:** `production/docs/reference/elevenlabs.md`

AI route: load the `elevenlabs` tools with ToolSearch (searching 'elevenlabs'), run
`python3 toolkit/media.py check --setup` and stop on any ElevenLabs finding; read the narration
use in `brand/src/voice/voice.md`, or choose the voice with the author after
`mcp__elevenlabs__list_models`, and record it; check that the brief's `synthetic_voice` says so.
Human route: agree the recording set-up with the author: a quiet room, the same microphone for
every chapter, and room tone at head and tail. _Substantive._

## 5. Make the chapter text

> **Skill:** `narrate-audiobook` · **Guide:** `production/docs/reference/audiobook-narration.md`

AI route: run `python3 toolkit/media.py audiobook text` on the chapter's source, with `--piece`
and `--chapter`, from a syntek-author unit whose status is `final`, where present, unless the
author says otherwise, or a text the author provides. Exit 1 lists words or references with no
spoken form: agree each with the author, add it to the pronunciations in
`brand/src/voice/voice.md`, and run it again. The chunks land in
`production/src/audiobook/generated/`; never copy them into a tracked file. _Mechanical._

## 6. State the cost and wait

> **Skill:** `narrate-audiobook` · **Guide:** `production/docs/reference/elevenlabs.md`

Count the characters of every chunk exactly as it will be sent, the number of calls and the
estimated credits, and say whether the output format needs a higher tier. Give the balance from
`mcp__elevenlabs__check_subscription` if the author wants it. Wait for a yes. _Mechanical._

## 7. Generate, one call at a time

> **Skill:** `narrate-audiobook` · **Guide:** `production/docs/reference/elevenlabs.md`

For each chunk in turn, call `mcp__elevenlabs__text_to_speech` with the recorded voice, model,
settings and format, and an absolute `output_directory`: the output of
`git rev-parse --show-toplevel` followed by `/production/src/audiobook/generated`. Straight after
the call, and before the next, run `python3 toolkit/media.py take add` on the file the result
names, with `--piece`, `--chapter` and `--part`; it renames the take and writes the credits-log
row. Stop at the first error and report it. Set the chapter's row to `generated`. _Mechanical._

## 8. Log a human recording

> **Skill:** `narrate-audiobook` · **Guide:** `production/docs/reference/source-media.md`

Human route: when the author has recorded a chapter, log each file with
`python3 toolkit/media.py footage add FILE --kind audio --location LABEL`, name its footage ID in
the chapter's Takes, and set the row to `recorded`. A narrator other than the author signs a
release first, with its row in `production/src/rights-register.md`. _Mechanical._

## 9. Listen and approve

> **Skill:** `narrate-audiobook` · **Guide:** `production/docs/reference/audiobook-narration.md`

The author listens to every part. A rejected part is regenerated or re-recorded only on the
author's word, through steps 6 and 7 or step 8. An approved take may be archived with
`python3 toolkit/media.py footage add FILE --kind generated --location LABEL` where the author
wants it kept, its footage ID named in the chapter's Takes; it need not be, because the mastered
chapter is what is approved and archived (`production/workflows/06-master-an-audiobook/`).
_Substantive._

## 10. Hand back

> **Skill:** `narrate-audiobook` · **Guide:** `production/docs/reference/audiobook-narration.md`

Report the chapters voiced or recorded, their routes, the characters and credits spent, the
voice and model used, what is approved and archived, and anything the narrator got wrong. Point
to `production/workflows/06-master-an-audiobook/`. _Substantive._
