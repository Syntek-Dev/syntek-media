---
name: repurpose
description: >-
  Plan the cut-downs of one long piece: read its script or approved transcript and its master, find
  the moments that stand alone, and write one cut-down plan for the platforms this project posts to,
  each cut with the lines it carries, its In and Out on the master, the hook in its opening line,
  its framing and its caption width; a silent loop for a web page is a cut too. Refuses a batch of
  near-identical cuts, proposes first, and writes only the cuts the author agrees. Use when the
  author says 'cut this talk into shorts', 'what clips can we get out of the episode?', 'plan the
  cut-downs', 'make reels from the explainer', 'a loop for the homepage' or 'turn the trailer into
  teasers'. Not rendering the cuts (`cut-for-platform`). Not timing or burning captions
  (`captions`). Not a social media plan or a content calendar (the social-media-documents skill
  (syntek-author), where present).
---

# Skill: Repurpose (<%BRAND_NAME%>)

Locale: en_GB · <%TIMEZONE%> · dates DD/MM/YYYY.

A long piece holds a few moments that work on their own: a complete thought, a line that hooks in
its first breath, a picture that survives a vertical crop. This skill finds them and writes them
down as a cut-down plan, so that every cut is chosen once, by the author, before anything is
rendered. **A cut-down is a different moment, never the same moment again**: a batch of
near-identical clips reads to a platform as mass-produced and to a viewer as padding, so this
skill offers fewer, distinct cuts and says why.

The plan is a proposal until <%OWNER_FIRST_NAME%> agrees it. Nothing is cut here: rendering
belongs to `cut-for-platform`, captions to `captions`, and when and where a cut is posted to
`prepare-post`.

## Governing procedures (route here — do not restate at length)

- `publishing/workflows/01-plan-the-cut-downs/` — this skill is that procedure in skill form. Run
  its `STEPS.md` with `CHECKLIST.md` open.
- If the layer's `workflows/local/` holds a folder with the same `NN-name` as the procedure above,
  follow that procedure instead: the author's local procedure replaces the template's
  (`run-media-workflow`, step 2).
- `publishing/docs/reference/cut-downs.md` — the plan's columns, finding the moments, framing and
  safe zones, and the rule against near-identical batches.
- `publishing/docs/reference/platform-specs.md` — how `toolkit/data/platforms.toml` is read:
  `verify`, `chosen`, absent keys and the brand's overrides.
- `production/docs/reference/recorded-pieces.md` — a recorded piece's transcript, its beat anchors
  and the caption chain that times it to the master.
- `publishing/src/cut-downs/CLAUDE.md` — the plan's format and name.
- `.claude/rules/syntek-media/01-layout-and-routing.md` Section 1 — the platforms this project
  posts to; Section 5 — the piece.
- `.claude/rules/syntek-media/03-production-ethics.md` Sections 1 and 7 — who decides what, and
  never fabricate.
- The guide in `scripts/docs/reference/` for each kind of piece this project makes (short video
  above all), named here in prose because each ships only with its kind.

The mode file adds this brand kind's long pieces, what makes a moment stand alone in them, and the
cuts this kind never makes.

## Steps

> **Mode.** Before step 1, read the brand-kind mode file beside this one — exactly one of `BUSINESS.md`, `FICTION.md`, `NONFICTION.md` ships in this folder. The mode owns the domain (paths, unit, extra reads, domain rules, examples); this file owns the procedure. Where they disagree, the procedure wins and the disagreement is reported to the author.

1. **Fix the piece and its master.** Confirm the piece by its folder in `scripts/src/pieces/` and
   read its `brief.md`: `kind`, `origin`, `status`, `deliverables` and `parent`. Probe the master,
   `production/src/renders/<piece>/<piece>.master.mp4` (`.wav` for an audio master), with
   `python3 toolkit/media.py probe`. If `publishing/src/cut-downs/<piece>.md` exists, this is a
   revision: read it, and never overwrite it without the author's word. Without a master the plan
   can still name lines, hooks and framing, but every In and Out stays empty and no cut can be
   agreed; say so.
   *Complete when:* the piece, its origin, its master (or its absence) and any existing plan are
   named. For a scene, read and probe the native master list, default first.

2. **Read the words and their timing.** For a scripted piece, read `script.md` and the
   storyboard's Vertical framing column; for a recorded piece, read the approved `transcript.md`.
   Then open the captions timed to the master, `publishing/src/captions/<piece>.en-GB.srt`. On the
   ladder they are usually made after the cuts, so where they do not exist yet, take the master's
   timing as step 4 of `publishing/workflows/01-plan-the-cut-downs/` does. For a recorded piece,
   carry its recording-timed captions to the master first, because a beat anchor is a time on the
   recording, never on the master:
   `python3 toolkit/media.py captions retime publishing/src/captions/<piece>.<FID>.en-GB.srt --edl production/src/edits/<piece>.toml --source <FID> -o publishing/src/captions/<piece>.en-GB.srt`.
   For a scripted piece, read the edit decision list, `production/src/edits/<piece>.toml`: each
   clip's place on the master's timeline and, for a voiced piece, the `vo:<piece>` row's `at`, from
   which each approved segment of `production/src/voiceover/<piece>.toml` follows the last by its
   probed length and its `pause_after`.
   *Complete when:* every spoken line can be cited as `beat.line`, and the master's timing is open,
   from its captions or its edit decision list.

3. **Read the platforms and their limits.** List the platforms this project posts to
   (`.claude/rules/syntek-media/01-layout-and-routing.md` Section 1) and, from each profile in
   `brand/src/platforms/`, the deliverables it uses. Print each candidate deliverable with
   `python3 toolkit/media.py presets <platform>.<format>`: its `aspect`, `max_seconds` (and
   `min_seconds` where it has one), `safe_zone`, `caption_formats` and every key in its `verify`
   list. Read each platform's guide in `publishing/docs/reference/`. Never take a limit from
   memory.
   *Complete when:* every deliverable a cut could serve is listed with its limits, and every
   `verify` key among them is named.

4. **Find the moments that stand alone.** Read the piece through and list candidate moments: a
   complete thought that needs no setup and leaves no promise unpaid, a hook in its opening line,
   and a length inside the deliverable's `max_seconds`. Each candidate names its lines
   (`3.2–3.9`), why it stands alone, and its hook in the speaker's own words. A cut starts and ends
   on a whole sentence, and never cuts a claim off from its condition or its source. **A silent
   loop** for a web page (`website.hero_loop`, where the project has the website platform) is a
   cut with no words: a moment of picture within its `max_seconds`, its Lines `—`, so the rule of
   whole sentences does not bind it. Apply the mode file's additions.
   *Complete when:* every candidate has its lines, its reason and its hook.

5. **Refuse near-identical batches.** Compare the candidates with each other. Two cuts that share
   most of their lines, or the same lines reframed, are one cut: keep the stronger and say why.
   One cut may serve every deliverable of its aspect; several near-identical cuts for one platform
   are what `publishing/docs/reference/cut-downs.md` warns against. When the author asks for more
   cuts than the piece has distinct moments, say so plainly and offer the distinct ones. A silent
   loop is outside this rule: it may share frames with a cut it was taken from, which its note
   names. A GIF preview is never a cut: it is `thumbnail-brief`'s.
   *Complete when:* no two candidates are near-identical, and every merge or drop has its reason.

6. **Set In, Out and the frame.** Take each cut's In and Out from the master-timed cues of its
   first and last lines, or, without them, from the edit decision list's timing of the clips or
   segments that carry those lines, as `HH:MM:SS.mmm`; check a time read from the edit decision
   list on a still of the master before proposing it, and check each cut's length against every
   deliverable it serves. Set the frame per aspect, `centre`, `crop x=<px>` or `pad`: from the storyboard where
   it has one; otherwise from a still of the master
   (`python3 toolkit/media.py frame <master> --at <HH:MM:SS.mmm>`), keeping the speaker or subject
   and any on-screen title inside the safe zone. Note the caption width the cut's aspect needs, and
   whether one deliverable needs its own caption file. A scene uses Frame `native` and the
   matching aspect's master; list every master, default first, and request any missing native
   aspect through `production/workflows/10-animate-a-scene/`, never crop or pad another scene master. An audio master's cut goes onto a video
   platform under a still: name the still.
   *Complete when:* every cut has its In, Out, frame and caption width, and its length fits every
   deliverable it serves.

7. **Propose the plan.** Present it in the plan's own shape: the table
   `| Cut | Deliverables | Lines | In | Out | Frame | Hook | Status |` and a note per cut (its
   opening words, on-screen title, caption width, whether it needs its own thumbnail, and why the
   moment stands alone). List separately, as questions and never as cuts, any moment the mode file
   keeps out. Ask the author to agree all, none or by cut, and wait.
   *Complete when:* the author has the proposal and the questions, and has answered.

8. **Write the agreed plan.** Write `publishing/src/cut-downs/<piece>.md` in the format its
   folder's `CLAUDE.md` gives, one sentence per line in the notes: each cut the author agreed is
   `approved`, each one they are still weighing is `planned`, and the frontmatter's `approved` is
   dated only on the author's word for the whole plan. Never add a cut-down to the brief's
   `deliverables`: cut-downs live only in this plan.
   *Complete when:* the plan holds exactly the cuts the author agreed, at the statuses they chose,
   and nothing was overwritten unasked.

9. **Hand back.** Report the plan's path, its cuts with their deliverables, every `verify` key a
   cut relies on, and the next moves: each cut's captions, made before the cut where they can be
   so the cutting pass burns them in (`publishing/workflows/03-caption-a-piece/`); the cuts
   themselves (`publishing/workflows/02-cut-for-a-platform/`); and a thumbnail for each cut whose
   note says it needs one (`thumbnail-brief`).
   *Complete when:* the author has the report, and nothing was rendered, scheduled or posted.

## Anti-patterns

- **The same moment, five times.** Near-identical cuts are refused, not batched; one cut serves
  every deliverable of its aspect.
- **Times from the recording.** A transcript's beat anchor is a time on the recording; a cut's In
  and Out are times on the master.
- **A cut that needs its setup.** A moment that only works after the minute before it does not
  stand alone; start earlier, or leave it out.
- **Cutting a claim off its condition.** A sentence that changes meaning when its qualifier is
  trimmed stays whole, or is not cut.
- **Cut-downs in the brief.** The brief lists full-length deliverables; cut-downs live only in the
  plan.
- **A limit from memory.** Every length, aspect and safe zone comes from `media.py presets`, with
  its `verify` keys named.
- **Rendering from a proposal.** Nothing goes to `cut-for-platform` until the author has agreed
  the cut.
- **Planning the calendar.** When a cut is posted is `prepare-post`'s to package; the social plan
  is syntek-author's, where its social-media family is present.

## Cross-references

- `cut-for-platform` — renders each agreed cut from the plan and moves its status on.
- `captions` — the master-timed captions this plan reads, and each cut's own captions.
- `thumbnail-brief` — a thumbnail for each cut whose note says it needs its own.
- `prepare-post` — the post package and the schedule row for each cut.
- `write-script` — the script whose `beat.line` citations the plan's Lines column uses.
- `publishing/src/cut-downs/` — the plans, one per piece.
- `toolkit/data/platforms.toml` — the deliverables and their limits, read through
  `python3 toolkit/media.py presets`.
- The social-media-documents skill (syntek-author), where present — the social media plan and the
  content calendar; a media cut may fill a slot there, and never replaces it.
