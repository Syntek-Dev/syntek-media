# Generated narration

Chapter text chunks land here from `python3 toolkit/media.py audiobook text`, as `<piece>.chNN.pNN.txt`, with each chapter's sidecar `<piece>.chNN.chunks.toml` listing its chunks in order and the pause after each, and so do their ElevenLabs takes, renamed at once by `take add` to `<piece>.chNN.pNN.tN.mp3`.
Everything here except this file is ignored by `production/src/.gitignore`: chapter text is never copied into a tracked file, and audio never enters Git.
A take cannot be made again: regenerating spends credits and gives a different take.
The mastered chapter is what is approved and archived; a take is archived with `python3 toolkit/media.py footage add FILE --kind generated --location LABEL` only where the author wants it kept, so keep the takes until their chapter's master is archived.
