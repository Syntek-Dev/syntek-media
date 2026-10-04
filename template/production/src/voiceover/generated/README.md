# Generated voiceover

ElevenLabs takes land here, one call at a time, and `python3 toolkit/media.py take add` renames each at once to `<piece>.sNN.tN.mp3` (`.pcm` for a raw format) and logs it in the piece's segment register and the credits log.
Everything here except this file is ignored by `production/src/.gitignore`; never force a take into Git.
A take cannot be made again: regenerating spends credits and gives a different take.
Archive every approved take with `python3 toolkit/media.py footage add FILE --kind generated --location LABEL` before a master depends on it, and record its footage ID in the register's `archived`.
