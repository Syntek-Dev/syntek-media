---
piece: 000-example-piece
version: 1
approved: <%DATE%>
<: if BRAND_KIND == 'business' :>words: 68
estimated_seconds: 28.1
---

# One line before every meeting — script

<!-- WORKED EXAMPLE: the approved script of the example piece, spoken on camera, so there is no VO line and no voiceover to generate.
     The frontmatter holds what `python3 toolkit/media.py script time` reports at the brief's 150 words a minute: 28.1 seconds against a target of 30.
     The captions in publishing/src/captions/ carry these spoken words exactly, without the braces. -->

## 1. Hook (target 00:05)

TEXT: One line before every meeting
ON: {straight to camera} Every meeting you call needs one line before it starts.

## 2. The line (target 00:10)

ON: Put the decision you need in the first line of the invite.
ON: Not the topic, the decision.
ON: {pause 0.5} 'Agree the price list', not 'Pricing catch-up'.

## 3. Why it works (target 00:09)

ON: People arrive knowing what they're there to decide.
ON: If you can't write it, skip the meeting.
ON: {pause 0.4} Send an email instead.

## 4. Call to action (target 00:06)

ON: {warmly} Try it on your next invite.
ON: Then come back and tell us what changed.
<: elif BRAND_KIND == 'author-fiction' :>words: 60
estimated_seconds: 27.8
---

# Count the stones — script

<!-- WORKED EXAMPLE: the approved script of the example piece, spoken on camera, so there is no VO line and no voiceover to generate.
     The frontmatter holds what `python3 toolkit/media.py script time` reports at the brief's 140 words a minute: 27.8 seconds against a target of 30.
     The captions in publishing/src/captions/ carry these spoken words exactly, without the braces. -->

## 1. Hook (target 00:05)

TEXT: Count the stones
ON: {low} Count the stones, and the river lets you pass.

## 2. The count (target 00:10)

ON: Tam taught Maren the count.
ON: Three stones to the post, four to the willow.
ON: {pause 0.5} Tonight she has to cross the ford in the dark.

## 3. The crossing (target 00:09)

ON: She counts to the post.
ON: {pause 0.6} She counts to the willow.
ON: {pause 1.0} Then something upstream moves.

## 4. Call to action (target 00:06)

ON: That night is where my novel begins.
ON: Follow to see the cover first.
<: else :>words: 65
estimated_seconds: 28.8
---

# The second visit — script

<!-- WORKED EXAMPLE: the approved script of the example piece, spoken on camera, so there is no VO line and no voiceover to generate.
     The frontmatter holds what `python3 toolkit/media.py script time` reports at the brief's 140 words a minute: 28.8 seconds against a target of 30.
     The captions in publishing/src/captions/ carry these spoken words exactly, without the braces. -->

## 1. Hook (target 00:05)

TEXT: The second visit
ON: Making a newcomer welcome once is the easy part.

## 2. The test (target 00:10)

ON: The real test of a welcome is the second visit.
ON: {pause 0.4} Does anyone remember their name?
ON: Does anyone notice that they came back at all?

## 3. The claim (target 00:09)

ON: A welcome isn't finished at the door.
ON: It's finished when they're expected back.
ON: {pause 0.5} That holds for any group.

## 4. Call to action (target 00:06)

ON: It's the heart of my next book.
ON: Follow for the rest of the argument.
<: endif :>