# Rendered deliverables

The toolkit writes each piece's publishing renders into a folder named for it, `<piece>/`, which
it makes when it first writes there: each platform deliverable as
`<piece>[--cNN].<platform>-<format>[.burned].<ext>`, a feed episode's audio as
`<piece>.podcast-feed-audio.mp3`, each thumbnail or cover as `<html-stem>.<platform>-<format>.png`,
each image `media.py image` encodes as `<stem>.<platform>-<format>.<ext>`, a GIF preview as
`<piece>[--cNN].newsletter-preview-gif.gif`, and an episode's chapters as `<piece>.chapters.json`.
At this folder's top sits only what no piece owns: an image encoded from a source whose name
carries no piece key, such as a show's cover, and the upload copy of a podcast feed,
`<show>.feed.xml`. A render an earlier release left at this folder's top stays where it is,
ignored, until you delete it; a feed episode's audio left there is moved into its piece's folder,
or encoded again, before its tags are written. Everything in this folder except this file is
ignored by `publishing/src/.gitignore`, every piece's folder included, and all of it is
regenerable from the master, the captions, the thumbnail layouts and the show registers. A folder
inside this one carries no README and no pair. Never edit a render by hand, never force one into
Git, and never put a tracked file in a folder here.
