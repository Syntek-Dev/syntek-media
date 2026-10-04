# Rendered deliverables

The toolkit writes every publishing render here: each platform deliverable as
`<piece>[--cNN].<platform>-<format>[.burned].<ext>`, a feed episode's audio as
`<piece>.podcast-feed-audio.mp3`, each thumbnail or cover as `<html-stem>.<platform>-<format>.png`,
each image `media.py image` encodes as `<stem>.<platform>-<format>.<ext>`, a GIF preview as
`<piece>[--cNN].newsletter-preview-gif.gif`, an episode's chapters as `<piece>.chapters.json`, and
the upload copy of a podcast feed as `<show>.feed.xml`. Everything in this folder except this file
is ignored by `publishing/src/.gitignore`, and all of it is regenerable from the master, the
captions, the thumbnail layouts and the show registers. Never edit a render by hand, and never
force one into Git.
