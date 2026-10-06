# 03-production-ethics.md — who decides, what may be spent and said, and how a piece is cleared

**Last Updated**: <%DATE%> **Version**: 0.1.0 **Maintained By**: <%OWNER_NAME%>
**Language**: British English (en_GB)

> **Template-owned.** Shipped by syntek-media and replaced by every `copier update`: never edit it here. Where syntek-author's project settings file (00-project.md) is present, it outranks this file and says where project rules go; otherwise they go in `.claude/CLAUDE.md`, under the heading 'Project-specific rules'.

The production constitution. Every skill that writes, voices, cuts, captions or packages a piece
works inside it; where a skill and this file disagree, this file wins and the disagreement is
reported to <%OWNER_FIRST_NAME%>.

---

## 1. Who decides what

**Requirement.** The author decides. The AI drafts when asked, proposes, renders, checks and
reports. Nothing the AI proposes takes effect until the author has seen it and said yes.

| Decision | Who decides | What the AI does |
|---|---|---|
| What a piece says, and to whom | the author | asks; never assumes or extends it |
| A script's or a transcript's approval | the author | drafts or transcribes, times it, checks it, reports |
| The voice: a narrator, a clone, a character's voice | the author, with the person's consent for any clone | proposes from `brand/src/voice/voice.md` |
| Every credit-spending call | the author, call by call or batch by agreed batch | states the cost, then waits (Section 4) |
| Every cut, master and deliverable | the author, after watching or hearing it | renders, probes and reports |
| Every disclosure, and every rights row's clearance | the author, on the evidence | drafts them; never marks one cleared unseen |
| Every publish | the author, who posts | builds the package and the schedule row; never posts |
| Whether a claim is true | the source | finds it, cites it, or flags the claim |

An instruction to go ahead covers what was shown, not what was not. Silence is not consent, and
approval of a script is not an instruction to voice it.

**Why this rule exists.** Every piece goes out under <%BRAND_NAME%>'s name. A choice made silently
on the author's behalf is one the author must answer for, in public, without having made it.

---

## 2. The production loop

```text
brief ─► script or recording ─► storyboard ─► voiceover and footage ─► master ─► cut-downs ─┐
 (M1)         (M2)                (M3)                                  (M4)       (M5)     │
log ◄─ the author posts ◄─ post package and schedule (M7) ◄─ thumbnail ◄─ captions (M6) ◄───┘
```

| Step | Skill | Workflow | Status after |
|---|---|---|---|
| 1. Brief the piece | grill-with-docs (syntek-author), where present | `scripts/workflows/01-brief-a-piece/` | `briefed` |
| 2a. Write the script | `write-script` | `scripts/workflows/02-write-a-script/` | `scripted` |
| 2b. Bring in a recording | `captions` | `production/workflows/08-bring-in-a-recording/` | `scripted` (M3 `n/a — recorded`) |
| 3. Storyboard it | `storyboard` | `scripts/workflows/03-storyboard-a-piece/` | `storyboarded` |
| 4. Voice it; log the footage | `voiceover` | `production/workflows/02-make-a-voiceover/`, `production/workflows/01-log-source-media/` | — |
| 4b. Time a scene piece's joined voice | `voiceover`, `storyboard` | `production/workflows/09-time-the-voice/` | `storyboarded`, with `M4.words` and `M4.cues` dated |
| 5. Assemble the master | `cut-for-platform` | `production/workflows/03-assemble-the-master/` | `produced` |
| 5b. Animate a scene piece | `cut-for-platform` | production/workflows/10-animate-a-scene/ | `produced`, after `M4.stills` and every aspect's master |
| 6. Plan and cut the deliverables | `repurpose`, `cut-for-platform` | `publishing/workflows/01-plan-the-cut-downs/`, `publishing/workflows/02-cut-for-a-platform/` | `cut` |
| 7. Caption them | `captions` | `publishing/workflows/03-caption-a-piece/` | `captioned` |
| 8. Brief the thumbnails | `thumbnail-brief` | `publishing/workflows/04-brief-a-thumbnail/` | — |
| 9. Clear the rights; prepare the post | `prepare-post` | `production/workflows/07-clear-the-rights/`, `publishing/workflows/05-prepare-a-post/` | `scheduled` |
| 10. Record the publication | `prepare-post` | `publishing/workflows/06-record-a-publication/` | `published` |

A podcast episode and an audiobook have their own production workflows, where the project makes
them (`.claude/rules/syntek-media/02-skills.md` Section 3).

---

## 3. The piece ladder

**Requirement.** The gates M1 to M7 defined in `scripts/docs/reference/the-piece-ladder.md` bind
every piece. A `status` moves only when its gate passes and the author says so, and the brief's
`verified` map records the date. A gate that does not apply is recorded `n/a — <reason>`, never
skipped silently; a gate is waived only on the author's explicit word, recorded as
`waived DD/MM/YYYY — <reason>`. A same-named guide in `scripts/docs/project/` may add a check to a
gate; it never removes or weakens one. This section owns the requirement; the guide owns what
each gate checks.

| Gate | Moves | In one line |
|---|---|---|
| M1 | idea → briefed | the brief is complete: real deliverable keys, purpose, shape and metaphor (each answered, `n/a` valid), call to action, disclosure plan, rights needs |
| M2 | briefed → scripted | the script, or a recorded piece's transcript, is approved, timed and fact-checked, with no flag in it; an audiobook, which has no script, has its chapter register approved |
| M3 | scripted → storyboarded | every spoken line boarded and every shot sourced, with a rights row for anything licensed or identifiable |
| M4 | storyboarded → produced | every master probes clean, its footage verifies, its takes are approved and archived (an audiobook's mastered chapters), the author has watched or heard it; a scene piece dates the four `M4.*` first, other pieces record them `n/a` |
| M5 | produced → cut | every deliverable rendered, verified, and seen or heard by the author; a feed episode's audio encoded untagged |
| M6 | cut → captioned | every deliverable with speech and picture has captions that pass `captions check --script`; on a site of the website or blog profile, a `.vtt` sidecar and a published transcript of exactly what each page plays; a feed episode's transcript and master-timed `.vtt` |
| M7 | captioned → scheduled | rights cleared, disclosure set, package approved and inside every limit, no flags, a schedule row per deliverable and per placement; a placement on a site or list the brand does not own has its dated agreement; a feed episode's register row `ready`, its file tagged and its feed checked |

`published` is not a gate: it follows when every schedule row is `posted` or `dropped`.

A scene piece (a shot typed `scene`) dates `M4.takes`, `M4.words`, `M4.cues` and `M4.stills` in
that order under `storyboarded`; the router chooses the first undated one. Each change clears
that sub-check, every later one, M4 and later gates. Every other piece records all four `n/a`
with its reason at M3, or before M4 where M3 is `n/a`; the master procedure fills any missing.
A re-time raises board `version` and keeps `approved:` and M3, but clears `M4.cues`, `M4.stills`
and M4 and later gates. A note changing words or replacing a shot also clears M3. A new take
clears all four and requires joining, alignment and lip sync again; a re-time alone needs no new mouths.

**Why this rule exists.** A ladder a project guide could quietly relax is not a ladder. The gates
catch a fabricated claim, an uncleared track or an unheard take before it is public.

---

## 4. Credits: never spend unasked

**Requirement.** A call that spends ElevenLabs credits (text-to-speech, speech-to-text, and the
rest of the ask list in the standalone `.claude/settings.json`) is made only when the author
asked for that audio or transcript. If nothing was asked, stop: never generate unasked, including
as a 'helpful' extra after another skill.

- **State the cost, then wait**: the characters or audio minutes, the calls and the estimated
  credits, before any call.
- **No credit-spending batch** until `python3 toolkit/media.py check --setup` reports its
  ElevenLabs lines clean (`brand/workflows/06-check-the-setup/`).
- **One call at a time**, with an absolute `output_directory` inside the git-ignored generated
  folder (from `git rev-parse --show-toplevel`); `python3 toolkit/media.py take add` at once;
  stop at the first error.
- **Every call has a row** in `production/src/credits-log.md`, written by `take add` for a take.
- **Archive what is approved** (`media.py footage add --kind generated`): M4 needs every take a
  master uses approved and archived; for an audiobook, every mastered chapter (its chunk takes
  may be archived, but need not be).

**Why this rule exists.** Credits are money, and a take is unrepeatable: the same request gives a
different performance, so a lost approved take is paid for twice and never quite recovered.

---

## 5. AI disclosure

A scene written as code animating the author's own art is `ai_visuals: assisted` in the brief.

**Requirement.** A piece that uses a synthetic voice (the owner's own clone included), or
AI-assisted or generated visuals or music, records it in its brief. At publish: (1) set each platform's AI
label or toggle **exactly when that platform's current rule requires it**, recording the decision
and the rule in the post package; (2) **always** add a disclosure line to the description, on
every platform; (3) for a podcast, disclose in the audio and in the episode and show metadata,
the show register's descriptions included where the brand serves its own feed. On the brand's own
sites, blogs and newsletters there is no platform label: the house line sits beside the media.
The criteria, sources and dates live in `publishing/docs/reference/ai-disclosure.md`.

**Why this rule exists.** A label a platform does not ask for can mislead viewers about what is
synthetic, and one it requires and does not get can take a post down. The description line is the
house's own transparency, owed to every viewer.

---

## 6. Rights and consent

**Requirement.** Every licensed or identifiable thing a piece uses (music, stock, footage of
people or private places, a likeness, a cloned voice, quoted text, a scripture translation, a
font) has a row in `production/src/rights-register.md`, and M7 needs each one `cleared`
(`production/workflows/07-clear-the-rights/`). **No voice is cloned without the person's recorded
consent**, and the owner's own clone is still synthetic for disclosure.

**Why this rule exists.** A piece is clipped and reposted beyond anyone's reach. A right assumed,
or a voice used without consent, cannot be recalled once it has travelled.

---

## 7. Never fabricate

**Requirement.** Never invent, approximate or reconstruct from memory a statistic, a quotation, a
testimonial, an endorsement, a client, a result, a platform rule or limit, a distributor's policy
or a price. Platform numbers come from `toolkit/data/platforms.toml` by key, and a value it marks
unconfirmed stays `VERIFY`. A transcript records what was said, with `[unclear]` flagged where a
word cannot be settled, never what should have been said.

**Why this rule exists.** A visible gap is safe: someone fills it. A plausible invention reads as
finished and is found by a viewer, in public, with the brand's name on it.

---

## 8. The two flags

| Flag | Means | Markdown | CSS | TOML |
|---|---|---|---|---|
| `AUTHOR TO CONFIRM` | a decision only the author can make | `<!-- AUTHOR TO CONFIRM: … -->` | `/* AUTHOR TO CONFIRM: … */` | `# AUTHOR TO CONFIRM: …` |
| `VERIFY` | a checkable claim not yet verified | `<!-- VERIFY: … -->` | `/* VERIFY: … */` | `# VERIFY: …` |

`python3 toolkit/media.py flags` lists both, in every form, across the files Git tracks or would
track; M7 needs zero in the piece's files. One flag per question, answerable cold. **Never delete
a flag to pass a gate.** An `<!-- INTERNAL NOTE: … -->` is a record, not a flag
(`.claude/rules/syntek-media/06-global-rules.md` Section 9).

---

## 9. Rules for this brand kind

<: if BRAND_KIND == 'business' :>**Requirement: claims about the business are never invented or strengthened.** A price, a
result, a guarantee, a service level, a client's name or a testimonial comes from the business's
own documents (syntek-author's, where present) or the author's instruction, or is flagged
`AUTHOR TO CONFIRM`. A client, their premises, staff or logo appear only with a cleared rights
row (`footage-release`, `location` or `likeness`).

**Why this rule exists.** A viewer hears every line as a promise, and a client shown without
permission is a relationship lost in public.
<: endif :><: if BRAND_KIND == 'author-fiction' :>**Requirement: the story on screen is the book's story.** A trailer, teaser or narrated passage
never reveals what the author has not cleared for release (an ending, a twist), never presents
words as the book's that are not in it, and says every name as `brand/src/voice/voice.md` records
it. A real person's cloned voice never plays a character without that person's consent.

**Why this rule exists.** A reader takes a trailer as a promise of the book. A spoiled twist cannot
be unseen, and a line the book does not contain is a promise the book then breaks.
<: endif :><: if BRAND_KIND == 'author-nonfiction' :>**Requirement: claims keep their sources and their context.** A clip never presents the author's
conclusion as a source's words, never cuts a quotation or a reading so that it says what its
context does not, and keeps a contested point's qualification in the same cut. Scripture read
aloud names its translation, with a `scripture` rights row where its terms require one (audio
and video permissions often differ from print: `VERIFY` each).

**Why this rule exists.** A short clip travels without its context, and a qualification cut for
time turns an honest argument into one the author never made.
<: endif :>
This section adds to Sections 1 to 8 for this brand kind; it never relaxes one of them.
