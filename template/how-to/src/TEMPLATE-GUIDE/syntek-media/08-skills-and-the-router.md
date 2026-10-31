# Skills and the router — the skills, the router, the mode files and the model tiers

A skill is a written procedure that a session follows for one kind of job, such as writing a script or cutting a piece for a platform.
You rarely need a skill's name: say what you want in plain words, and the skill for that job runs.
This chapter lists syntek-media's skills, the router that finds work no skill claims, the mode files that fit each skill to your brand, and which model does which work.

## Reaching a skill

You can name a skill by typing a slash and its name, such as `/write-script`.
You can describe the job instead, such as 'cut this for every platform', and the skill whose job it is runs.
You can also ask 'what's next?' or 'pick up the trailer', and the router finds the procedure that fits.
The phrases below are examples, never passwords: any wording that describes the job will do.
Every skill lives in its own folder under `.claude/skills/`, and its `SKILL.md` is its whole manual.

## Media's skills

These skills carry a piece from its script to its post, and you decide at every gate.

| Skill | What it does | Say something like |
|---|---|---|
| `write-script` | Turns a brief into a spoken script, timed, with a hook, beats and a call to action | 'write the script for the new short' |
| `storyboard` | Gives every spoken line a picture and every shot a source, and opens a rights row for anything that needs clearing | 'storyboard the explainer' |
| `voiceover` | Makes a voiceover with ElevenLabs, one segment at a time, after telling you what it will cost | 'record the voiceover for the trailer' |
| `captions` | Writes and checks captions and transcripts, burned in or alongside | 'caption the talk' |
| `cut-for-platform` | Assembles the master and cuts and encodes each deliverable through the toolkit, then checks each one | 'cut this for every platform' |
| `repurpose` | Plans the cut-downs of one long piece, one for each platform you publish to | 'plan the clips from the talk' |
| `thumbnail-brief` | Briefs and renders a piece's thumbnails, covers and other images | 'brief the thumbnail' |
| `prepare-post` | Prepares each post's package and its schedule row, and never posts | 'get the post ready' |
| `run-media-workflow` | Finds the procedure for media work no other skill claims | 'what's next on the trailer?' |

Where the project makes audiobooks, a further skill narrates one, chapter by chapter, by the route each channel accepts.
`.claude/rules/syntek-media/02-skills.md` lists every skill this project ships, with what each does.
A skill that is not listed there does not ship here on purpose, and a session says so rather than improvising one.

## The router

`run-media-workflow` is the router for media work that no other skill claims.
It first checks the Workflow aliases of syntek-author's project settings file, 00-project.md, where that file is present.
Then it looks in each media layer's `workflows/local/`, so that a procedure of yours is found before the template's.
Then it reads the workflow index of each of the four layers, and resolves the request to one procedure.
To find what is next, it reads the briefs' status and gate dates, the newest handoff and the project's memory.
It loads that procedure whole, with its checklist open, obeys its gates, and works in order.
It favours a finished, approved deliverable over more scaffolding, because only that brings a piece nearer.
It never routes the guide's own procedures under `how-to/workflows/syntek-media/`.
A session runs one of those as its folder says, step by step with its checklist open.
Writing work, a blog post's or a newsletter's own words included, goes to the writing router of syntek-author, where present.

## Mode files

Your answer to `BRAND_KIND` chose one mode file for each skill that has one.
In a business project it is `BUSINESS.md`, in fiction `FICTION.md`, and in non-fiction `NONFICTION.md`.
The skill's `SKILL.md` holds the procedure, the same in every brand kind, and the mode file beside it holds the domain: its paths, its examples and its rules for that kind of brand.
Where the two disagree, the procedure wins, and the session tells you.
`run-media-workflow`, `captions` and `cut-for-platform` work the same in every brand kind, so they have none.
Beside a working-practice skill, described below, media's mode file carries a `MEDIA-` prefix, such as `MEDIA-FICTION.md`, so that it never collides with another template's.
For media work a session reads that file and no other: an upper-case file beside it from another template applies only to that template's work.

## The working-practice skills

Every template of the family ships the same working-practice skills, byte for byte, so a project with two templates keeps one copy.

- The `grilling` skill, where present, is an interview in rounds, each question with a recommended answer, that sharpens a brief or a plan before anything is made.
- The `grill-with-docs` skill, where present, grills the same way and records each decision where it belongs; design work opens with it.
- The `grill-me` skill, where present, grills and records nothing.
- The `wayfinder` skill, where present, charts work too big for one sitting, such as a series or a launch, into a map of decisions.
- The `handoff` skill, where present, writes a handoff at the end of a session instead of compacting it.
- The `to-questionnaire` skill, where present, turns a decision only someone else can answer into a questionnaire, and never sends it.
- The `wait-what` skill, where present, explains the last reply again, conclusion first.

They are copy-only, so a project updated from an older release may lack one until an update or a copy adds it.
Never edit one: an edit freezes it, so it never receives the family's later fixes.

## Companions from syntek-author

Where syntek-author is applied, some of its skills help with media work, and syntek-media never ships them.
The spelling skill (syntek-author), where present, and the grammar skill (syntek-author), where present, report on scripts, transcripts, captions and post copy.
The comprehension skill (syntek-author), where present, reads a script as your audience test.
The fact-check skill (syntek-author), where present, checks every factual claim in a script, a transcript or a post.
Each reports, and changes only what you accept.
Where a companion is absent, a session says which one is missing and what it would have checked, and never recreates it.

## The model tiers

Every job belongs to one of two tiers, which name the work rather than a model.

- **Substantive work** always uses Opus: anything a viewer or listener will read or hear, every edit decision, every rights or disclosure judgement, grilling and review.
- **Mechanical work** uses the model you answered in `MODEL_MECHANICAL`: renders, encodes, probes, file moves and checklist ticks.
- When in doubt, the work is substantive.
- If Opus is unavailable, substantive work falls back to Sonnet until it returns, and never lower.
- Haiku is never used on this project.

The tier of each step is printed beside it, as `· _opus_` or `· _sonnet_` on a checklist item and as `model:` at the top of a guide or a procedure.
`how-to/src/TEMPLATE-GUIDE/agent-clients-and-mcp.md` explains how the other coding agents run these tiers.

## When a skill does the wrong thing

Say so, in plain words, and the session stops and asks.
A skill that keeps doing something you never want is changed in the project's own rules, never in the skill itself.
Record it in syntek-author's project settings file, 00-project.md, under Overrides, where that file is present, naming the skill and the step.
Otherwise record it in `.claude/CLAUDE.md` under the heading 'Project-specific rules'.
`how-to/src/TEMPLATE-GUIDE/syntek-media/10-customising.md` explains overrides in full.

## Where the rules live

- `.claude/rules/syntek-media/02-skills.md` Sections 1 to 3: skills only, the mode files, and every media skill.
- `.claude/rules/syntek-media/02-skills.md` Sections 4 and 5: the working-practice skills, the companions, and how a skill may be changed.
- `.claude/rules/syntek-media/05-model-allocation.md` Sections 1 to 4: the two tiers, how files name them, why, and the other coding agents.
- `.claude/rules/syntek-media/01-layout-and-routing.md` Section 7: the routing frontmatter that names a step's skill and model.

## Next

- Making your first piece with these skills → `how-to/src/TEMPLATE-GUIDE/syntek-media/09-your-first-piece.md`
- Making a skill behave your way → `how-to/src/TEMPLATE-GUIDE/syntek-media/10-customising.md`
- The other coding agents and their models → `how-to/src/TEMPLATE-GUIDE/agent-clients-and-mcp.md`
