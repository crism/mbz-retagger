mbz-retagger
============

Updates audio files with new metadata from MusicBrainz.

Requires `mutagen` and `musicbrainzngs` libraries.

Requires Python 2, as `mutagen` does not yet support Python 3.

The executable script is `mbz_retagger.py`.  Run `mbz_retagger.py -h`
for help.

Limitations
-----------

Currently only updates title and artist info.

Currently only supports FLAC and Ogg Vorbis formats.

There is a failure mode in that, in some situations, a MusicBrainz
recording ID may come to represent a completely different recording.
In that case, the retagger will corrupt the metadata based on the
recording ID stored in the file.

TODO
----

Add disc (i.e., album) details.

Add abstraction to transparently support MP3.

Reverse engineer Picard mappings to support all metadata supported by
Picard.

Add logging to support scanning of large libraries that picks up where
it left off, if interrupted.

Develop a heuristic for detecting changed recording IDs.
