# Platforms and media kinds — adding or removing a platform or a media kind

The platforms the brand posts to and the kinds of media it makes are two list answers, `PLATFORMS` and `MEDIA_KINDS`, recorded in `.copier-answers.syntek-media.yml`.
Each answer decides which files the project has, so a change goes through an update, and a removal deletes files.
This chapter says what arrives when you add one, what goes when you remove one, and what to edit by hand afterwards.

## How a list answer changes

- Never edit `.copier-answers.syntek-media.yml` by hand.
- A changed list goes through an update, as `how-to/workflows/syntek-media/02-change-the-answers/` says, and that procedure gives the full command.
- A list answer replaces the whole list, so name every platform or media kind you keep as well as the one you add.
- One you leave out of the new list is removed, with its files.
- `BRAND_KIND` never changes: the update refuses it, because a different brand kind is a new project.
- The brand brief in `.claude/rules/syntek-media/01-layout-and-routing.md` Section 1 is rendered from your answers, so the new lists arrive there on their own.

## Platforms and media kinds are separate answers

- A platform is somewhere the brand publishes, and a media kind is a kind of piece the brand makes.
- The brand's own website, blog and newsletter are platforms too, each with a profile and a guide of its own.
- A podcast is both, as two separate answers.
- The podcast platform is the brand's own feed and its profile, and the podcast media kind is the making of episodes.
- So a project can make episodes it posts only to a video platform, or publish a feed without the episode workflow, and each half is added or removed on its own.
- A coding agent is not a platform: adding one is a different change, in `how-to/workflows/syntek-media/06-enable-a-coding-agent-client/`.

## Adding a platform

- A new platform brings its profile, a seed named for the platform in `brand/src/platforms/`, empty for you to fill in.
- It also brings the platform's guide, among the publishing layer's reference guides.
- The podcast platform also brings the podcast folder in the publishing layer's source, the feed publishing workflow and the feed guide.
- Its limits are already in `toolkit/data/platforms.toml`, which every project carries whatever its platforms.
- Then fill in the profile through `brand/workflows/04-set-up-a-platform/`.
- That workflow records the account, the deliverables you use, the cadence, the tone, the call to action and the hashtag sets.
- In a business project with syntek-author's social-media documents, those documents own the written side, and the profile holds only the delivery facts.

## Adding a media kind

- A new media kind brings its guide, among the scripts layer's reference guides, and anything that serves only it.
- The podcast media kind also brings the guide for podcast episodes and the workflow that masters an episode.
- The audiobook media kind also brings the audiobook skill, the audiobook folder in the production layer's source, the workflows that narrate and master an audiobook, and the narration guide.
- The voiceover media kind adds only the guide for standalone voiceovers, because the `voiceover` skill and `production/workflows/02-make-a-voiceover/` ship in every project.
- A new kind's workflows are listed in their layer's workflow index, where `run-media-workflow` finds them.

## Removing one

- Removing a platform or a media kind deletes every file it generated, the seeds you have filled in included.
- A removed platform takes its profile with it, whatever you wrote there.
- Before its questions, the update prints the files each removal deletes, so read that list first.
- Copy out anything you need from those files and commit, then answer the questions.
- Git history keeps the last committed copy of each deleted file.
- The files you made yourself stay: your pieces, your register rows, your edit lists and your posts.
- The podcast platform's show registers and saved feeds stay, and so do the audiobook's chapter registers.
- `brand/src/platforms/overrides.toml` stays too, whatever platforms the project posts to.
- A brief, a cut-down plan or a schedule row that names a removed platform is yours, and stays as you wrote it until you change it.

## Hand edits after a change

- Some files that describe your options are written once and never updated, so after a change you edit them by hand.
- In a standalone project those are `README.md`, `CONTEXT.md` and the 'Project' section of `.claude/CLAUDE.md`.
- Over syntek-author, those files are syntek-author's, and need no edit for media.
- After a removal, delete the removed platform's tables from `brand/src/platforms/overrides.toml`.
- After an addition, fill in the new platform's profile with `brand/workflows/04-set-up-a-platform/`, while the brand brief in the media rules updates itself.

## Limits live in the platform data

- Every platform limit, such as a length, a size or a caption width, lives in `toolkit/data/platforms.toml`, never in a guide or a chapter.
- Each table there records the date it was checked and where its figures came from, and every update refreshes the file.
- `python3 toolkit/media.py presets` prints every table, with each override it applies.
- When a platform's own words differ from the data, the confirmed difference is an override in `brand/src/platforms/overrides.toml`, never an edit of the data file.
- An override is recorded through `brand/workflows/04-set-up-a-platform/` or `publishing/workflows/07-refresh-the-platform-specs/`, with the platform's words, their source and the date checked.
- An override is a confirmed fact, never a preference: the brand's own choices belong in its profile.

## Where the rules live

- `.claude/rules/syntek-media/06-global-rules.md` Section 11: answers change through Copier, and what a removal deletes.
- `.claude/rules/syntek-media/01-layout-and-routing.md` Section 1: the brand brief, platforms and media kinds included.
- `.claude/rules/syntek-media/04-toolkit-pipeline.md` Section 3: platform numbers live in the platform data, and a confirmed difference is an override.
- `how-to/workflows/syntek-media/02-change-the-answers/`: every step and command for changing a list.

## Next

- Changing the list through an update → `how-to/workflows/syntek-media/02-change-the-answers/`
- Filling in a new platform's profile → `brand/workflows/04-set-up-a-platform/`
- Every answer the template keeps → `how-to/src/TEMPLATE-GUIDE/syntek-media/05-the-answers.md`
