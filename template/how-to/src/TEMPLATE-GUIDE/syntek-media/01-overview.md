# Overview — what syntek-media adds, and how this guide is laid out

This project carries syntek-media, a template that adds audio and video production to a project: its folders, its rules, a set of AI skills and a toolkit that renders.
This chapter says what it gives you, what it never does, and how to find your way round this guide.

## What syntek-media adds

syntek-media turns a folder of plain text files into a place where video and audio are planned, scripted, voiced, cut, captioned and made ready to publish.
Git records every version of those files, and Claude Code, an AI assistant that works inside the folder, is your production partner.
The work lives in four production layers, the top-level folders where it is made.

- `brand/` holds the look and the spoken voice of the brand, and one profile for each place you publish.
- `scripts/` holds the pieces, each with its brief, its script or transcript, its storyboard and its shot list.
- `production/` holds the source media, the voiceover, the edit decision lists, the cards, the rights and the credits.
- `publishing/` holds the cut-down plans, the captions, the thumbnails, the post packages, the schedule and the publish log.

A supporting layer, `toolkit/`, holds the code every render runs through.
The rules that tell Claude how all of this works are in `.claude/rules/syntek-media/`, and they load at the start of every session.
`how-to/src/TEMPLATE-GUIDE/syntek-media/07-a-tour-of-the-project.md` takes you round each folder.

## The three brand kinds

The template makes one of three kinds of brand, and the answer `BRAND_KIND` chose it once, when the template was applied.

- `business` is for a business's social video, recorded talks and explainers.
- `author-fiction` is for a novelist's book trailers, audiobook and author socials.
- `author-nonfiction` is for a non-fiction author's talks, podcast, audiobook and author socials.

The brand kind decides which mode files the skills read, the notes that fit a skill's steps to your kind of brand.
It never changes: an update refuses a different answer, and a different brand kind is a new project.
The platforms you publish to and the kinds of media you make add to the brand kind, and you can change those later.
`how-to/src/TEMPLATE-GUIDE/syntek-media/05-the-answers.md` lists every answer and what it gave you.

## The piece and its ladder

A piece is one deliverable work, such as a short, an explainer, a talk, a trailer, a podcast episode, an audiobook or a voiceover.
Each piece has its own numbered folder under `scripts/src/pieces/`, and its brief records its plan and where it stands.
A piece climbs a ladder of steps, from an idea to a published work, and passes a gate at each step.
The gates are called M1 to M7, and `scripts/docs/reference/the-piece-ladder.md` says what each one checks.
A gate passes only when its checks are met and you say so, and the brief records the date.
`how-to/src/TEMPLATE-GUIDE/syntek-media/09-your-first-piece.md` follows a piece up every step.

## A toolkit, not an editor

There is no editing app here, and no timeline to drag clips along.
A cut is written down as a plain-text edit decision list, and `toolkit/media.py` drives ffmpeg to render it.
Thumbnails and cards are web pages styled by the brand's design tokens, and `toolkit/card.py` turns them into images.
Every render can be made again from the files Git tracks, so a master or a deliverable is never edited by hand.
To change one, change its source and render it again.
The toolkit checks what it renders and reports it, and you watch or listen before anything counts as done.

## What it never does

- It never decides for you: Claude drafts, proposes, renders and checks, and you decide what a piece says and when it goes out.
- It never spends credits unasked: a call to a paid voice service is made only when you asked for that audio, after Claude has stated what it will cost.
- It never invents a statistic, a quotation, a testimonial, a platform rule or a price; where one is missing, it leaves a visible gap for you to fill.
- It never publishes or sends anything for you: it builds the package and the schedule row, and you post.
- It never lets a session compact on its own, which is the AI summarising its own conversation to make room, because a summary loses the reasons behind decisions.
- When a session grows long, Claude writes a handoff, a short note of where the work stands, and stops, so the next session starts afresh from it.

## A companion, not a dependency

syntek-media is made to sit beside syntek-author, the family's template for the written side of a project, such as a book or a library of business documents.
Over a syntek-author project, its writing skills check a script's spelling, grammar and flow, and its project settings file can change how media's rules apply.
syntek-media never needs it.
On its own, the project works with less: a skill that would use a writing companion says which one is missing, such as the spelling skill (syntek-author), where present.
The working-practice skills, such as the `handoff` and `grill-with-docs` skills, where present, ship with both templates, byte for byte the same.
`how-to/src/TEMPLATE-GUIDE/syntek-media/12-beside-syntek-author.md` explains a project that carries both.

## How this guide is laid out

The guide is the `how-to/` folder, and it holds three kinds of file.

- Chapters, like this one, explain how the project works, in plain English.
- Guides, in `how-to/docs/syntek-media/`, explain one practice each, such as updating, and name the procedure that carries it out.
- Procedures, in `how-to/workflows/syntek-media/`, give the steps and every command, for you or a session to follow.

This template's chapters are in `how-to/src/TEMPLATE-GUIDE/syntek-media/`.
The shared chapters, which every template of the family carries, sit one folder up, in `how-to/src/TEMPLATE-GUIDE/`, and cover updating, the coding agents and the data root.
The reading order, by what you want to do, is in `how-to/src/TEMPLATE-GUIDE/syntek-media/CONTEXT.md`.
The guide is read-only: read it, and never edit it.
Every full update of the template puts its files back as the template wrote them, and what you had stays in Git.
To work differently from something it says, `how-to/src/TEMPLATE-GUIDE/syntek-media/10-customising.md` shows where your own way is recorded.

## Where the rules live

- `.claude/rules/syntek-media/01-layout-and-routing.md` Sections 1 to 3: the brand brief, the layers and what each kind of layer is for.
- `.claude/rules/syntek-media/03-production-ethics.md` Section 1: who decides what.
- `.claude/rules/syntek-media/03-production-ethics.md` Section 3: the piece ladder and its gates.
- `.claude/rules/syntek-media/03-production-ethics.md` Section 4: never spending credits unasked.
- `.claude/rules/syntek-media/06-global-rules.md` Section 3: the guide is read-only, and no rule or guide is rewritten without your word.

## Next

- Finding your way round the folders → `how-to/src/TEMPLATE-GUIDE/syntek-media/07-a-tour-of-the-project.md`
- Taking a first piece from a brief to a publication → `how-to/src/TEMPLATE-GUIDE/syntek-media/09-your-first-piece.md`
- The tools to install before you start → `how-to/src/TEMPLATE-GUIDE/syntek-media/02-prerequisites.md`
- Adding syntek-media to a syntek-author project → `how-to/src/TEMPLATE-GUIDE/syntek-media/03-applying-over-syntek-author.md`
- A project that carries both templates → `how-to/src/TEMPLATE-GUIDE/syntek-media/12-beside-syntek-author.md`
