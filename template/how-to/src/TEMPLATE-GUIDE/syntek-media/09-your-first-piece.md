# Your first piece — from a brief to a recorded publication

A piece is one deliverable work, such as a short, an explainer, a talk or a trailer, and it climbs a ladder of gates from an idea to a publication you have recorded.
This chapter walks that climb once, step by step, and names the workflow that carries out each step by its full folder path.
It names the gates and never restates them: what each gate checks is in `scripts/docs/reference/the-piece-ladder.md`.

## Before you start

- Finish the copy first, as `how-to/workflows/syntek-media/01-finish-a-copy/` says, so that the toolkit runs without a prompt and nothing spends credits unasked.
- Check your tools with `python3 toolkit/media.py check --setup`, or run `brand/workflows/06-check-the-setup/`, and clear what it reports before the first call that spends credits.
- A piece reads the brand's own files, so set them up early: `brand/workflows/01-set-up-the-brand-kit/` for the look, `brand/workflows/05-write-the-spoken-voice/` for the voice, and `brand/workflows/04-set-up-a-platform/` for each platform you post to.
- Read the worked example, where it was kept: it shows the files of a finished piece in your brand kind.
- The worked example is never entered in the piece register, and no workflow counts it as one of your pieces.

## How a piece moves

- Each piece has a folder of its own under `scripts/src/pieces/`, named with a three-digit number and a short title, and the number is never reused.
- The piece's brief holds its `status` and, in `verified`, the date each gate passed.
- The status moves one gate at a time, from M1 to M7, and only when the gate passes and you say so.
- A gate that does not apply is recorded as not applicable, with its reason, and never skipped in silence.
- A gate is waived only on your own word, and the waiver is recorded with its date and its reason.
- A project guide of your own may add a check to a gate, but it never removes or weakens one.
- Ask Claude what comes next at any point, and `run-media-workflow` offers the workflow for the piece's next gate.
- Every workflow runs from its `STEPS.md`, with its `CHECKLIST.md` open, and stops for you at each decision.

## Brief it (M1)

- `scripts/workflows/01-brief-a-piece/` takes the piece's number, opens its folder and writes its brief.
- It asks you for the purpose, the audience, the hook, the kind, the deliverables, the key points, the call to action, the disclosure plan and the rights needs.
- The `grill-with-docs` skill, where present, asks those questions in rounds, each with a recommended answer.
- A question the repository can already answer is never put to you.
- The workflow adds the piece's row to `scripts/src/piece-register.md`, which records numbers and kinds, never a status.
- M1 passes when you agree the brief, and the piece is then briefed.

## Script it and board it (M2 and M3)

- A scripted piece goes to `scripts/workflows/02-write-a-script/`, where the `write-script` skill writes a spoken script from the brief and times it.
- The script is written one spoken sentence per line, so that each line is voiced, timed and captioned as one unit.
- The spelling skill (syntek-author), where present, and the other writing companions report on the script, and a fix is applied only when you accept it.
- A recorded piece, such as a talk or an interview, comes in through `production/workflows/08-bring-in-a-recording/` instead.
- That workflow logs the recording and makes its transcript, which stands in for the script wherever a script is read.
- An audiobook has no script: its chapter register is approved instead, in the audiobook narration workflow, where the project makes audiobooks.
- M2 passes when you approve the script or the transcript, and the piece is then scripted.

Then the piece is boarded, unless it has no picture to board.

- `scripts/workflows/03-storyboard-a-piece/` runs the `storyboard` skill, which gives every spoken line a picture and every shot a source.
- It opens a row in `production/src/rights-register.md` for anything licensed or identifiable that a shot uses.
- A recorded piece records this gate as not applicable, and so does a piece with no picture.
- M3 passes when you agree the board, and the piece is then storyboarded.

## Produce it (M4)

- Footage you bring in is listed through `production/workflows/01-log-source-media/`, and the file itself is kept outside Git.
- A voiceover is made through `production/workflows/02-make-a-voiceover/`, where the `voiceover` skill works one sentence or beat at a time.
- Before any call that spends credits, the skill states what the call will cost and waits for your word.
- You listen to every take, and every take you approve is archived as source media.
- A piece with characters can have their voices designed first, through `production/workflows/11-design-character-voices/`.
- A scene piece times its joined voice through `production/workflows/09-time-the-voice/` and is animated through `production/workflows/10-animate-a-scene/`.
- Every other piece is assembled through `production/workflows/03-assemble-the-master/`, where the `cut-for-platform` skill renders and probes the master.
- The rights are cleared through `production/workflows/07-clear-the-rights/`, which can run once the board lists what the piece uses, and must be done before M7.
- A podcast episode and an audiobook have production workflows of their own, where the project makes them, and the project's workflow indexes list them.
- M4 passes when every master probes clean and you have watched or heard it, and the piece is then produced.

## Cut, caption and post it (M5 to M7)

- `publishing/workflows/01-plan-the-cut-downs/` runs the `repurpose` skill, which proposes the cuts for each platform from the master and lets you choose.
- `publishing/workflows/02-cut-for-a-platform/` runs the `cut-for-platform` skill, which renders and checks every deliverable for you to watch.
- M5 passes when you have seen or heard every deliverable, and the piece is then cut.
- `publishing/workflows/03-caption-a-piece/` runs the `captions` skill, which makes each deliverable's captions and checks them against the script.
- M6 passes when every deliverable with speech and picture has captions that pass their check, and the piece is then captioned.

Then the posts are prepared, and you publish them.

- `publishing/workflows/04-brief-a-thumbnail/` runs the `thumbnail-brief` skill, which briefs and renders the thumbnails and the other images the posts need.
- `publishing/workflows/05-prepare-a-post/` runs the `prepare-post` skill, which writes the post package and the schedule row for each deliverable.
- The package carries the title, the description, the disclosure, the captions, the thumbnail and the rights, each inside its platform's limits.
- M7 passes when the rights are cleared, the disclosure is set and you approve the package, and the piece is then scheduled.
- You post each deliverable yourself: nothing in the project posts, uploads or sends anything for you.
- `publishing/workflows/06-record-a-publication/` then writes the row in `publishing/src/publish-log.md` from what you report.
- Where the project publishes its own podcast feed, the feed has a publishing workflow of its own.
- The piece is published once every one of its schedule rows is posted or dropped.

## When a piece changes after a gate

- A material change to something a gate checked clears that gate and every later one, and the status steps back to the earliest cleared gate.
- A corrected typing slip clears nothing.
- Changing the words of a script after M2, or replacing a shot after M3, sends the piece back through the gates that checked them.
- A new take of a voiceover clears what was made from the old one, so the master is made and checked again.
- Before any change, the workflow says which gates it would clear, and waits for your word.
- The ladder guide lists, case by case, what each change clears.

## Where the files go

- The piece's own words and plans are tracked in Git: its brief, its script or transcript, its storyboard and its shot list, in its folder.
- Its edit list, cards, captions, cut-down plan, thumbnails and posts sit in the production and publishing layers, under names that begin with the piece's name.
- Renders and generated audio go to output folders that Git ignores, and each of those folders carries only a `README.md` that Git tracks.
- `python3 toolkit/media.py where` followed by the piece's name lists the piece's tracked files and names its output folders, saying whether each exists.
- Claude never lists or searches an output folder, and opens a file there only by the path a register or a command has given.
- Approved takes and footage are kept outside Git and listed in `production/src/footage/manifest.toml`.

## Where the rules live

- `.claude/rules/syntek-media/03-production-ethics.md` Section 2: the production loop, with each step's skill and workflow.
- `.claude/rules/syntek-media/03-production-ethics.md` Section 3: the piece ladder, and how a gate is recorded, waived or marked not applicable.
- `.claude/rules/syntek-media/03-production-ethics.md` Section 4: never spending credits unasked.
- `.claude/rules/syntek-media/01-layout-and-routing.md` Section 5: the piece, its folder and the register.
- `scripts/docs/reference/the-piece-ladder.md`: what each gate checks.

## Next

- The skills each step runs, and the router that finds the next step → `how-to/src/TEMPLATE-GUIDE/syntek-media/08-skills-and-the-router.md`
- Working your own way without breaking an update → `how-to/src/TEMPLATE-GUIDE/syntek-media/10-customising.md`
- What each gate checks, item by item → `scripts/docs/reference/the-piece-ladder.md`
