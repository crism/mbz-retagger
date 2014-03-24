#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
update audio files with MusicBrainz metadata

Provides a retagging service that uses a MusicBrainz client, then
interprets the received information in the same way that the Picard
tagger does, adding or (rarely) deleting information in the audio file
to bring it up to date.

Copyright © 2014 Christopher R. Maden.

This code may be freely copied, distributed, and reused without
restriction.  It would be nice if you gave me credit.  There is no
warranty; it might destroy all your data.  In fact, it probably will.
"""

__author__ = u"Christopher R. Maden <crism@maden.org>"
__date__ = u"24 March 2014"
__version__ = 0.1

from mbz_client import MBzClient

class MBzRetagger( object ):
    """
    Provide a retagging service.  Spin up a MusicBrainz client; keep
    the testing status persistently (don’t actually save changes if
    test is True).
    """
    def __init__( self, test=False, contact=None ):
        """
        Set up the service.  Remember the testing status.  Contact is
        an e-mail address passed to MusicBrainz in the User-Agent
        header.
        """
        self._test = test

        # Initialize the MusicBrainz client.
        self._mbzclient = MBzClient( contact=contact )

        return

    def retag( self, audio_file ):
        """
        Given a mutagen audio file structure, ensure it has a
        MusicBrainz track ID.  If not, skip it; if so, query
        MusicBrainz for metadata, and update the file accordingly.

        Raises MBzRetaggerMultipleTIDs if the audio file has multiple
        track IDs associated with it.
        """
        # Currently only works with FLAC and Ogg Vorbis files; mutagen
        # gives completely different results for MP3s, and we need to
        # map those separately.

        # Don’t update the file on disc unless we’ve actually made a
        # change.
        file_changed = False

        # Get the MusicBrainz track ID.
        tid = audio_file.get( "musicbrainz_trackid" )

        # If there’s no track ID, there’s nothing for us to do.
        if not tid:
            return

        # The track ID is a list; if it has more than 1, we don’t
        # really know what to do.
        if len( tid ) > 1:
            raise MBzRetaggerMultipleTIDs(
                "Track has multiple track IDs: %s" %
                audio_file.filename )

        # Query MusicBrainz for the latest metadata.  The client may
        # raise an exception, which we simply pass through.
        mbz_info = self._mbzclient.get_track( tid[0] )

        # Map the data to tags.

        # track title:
        mbz_title = unicode( mbz_info["recording"]["title"] )
        if audio_file.get( "title" )[0] != mbz_title:
            audio_file.update( { "title" : mbz_title } )
            file_changed = True

        # primary artist(s); order matters:
        mbz_artists = u""
        mbz_artist_ids = []
        mbz_artist_sorts = u""
        for mbz_artist in mbz_info["recording"]["artist-credit"]:
            # Watch for “feat.” and other joiner text.
            if isinstance( mbz_artist, dict ):
                mbz_artists += unicode( mbz_artist["artist"]["name"] )
                mbz_artist_sorts += \
                    unicode( mbz_artist["artist"]["sort-name"] )
                mbz_artist_ids.append(
                    unicode( mbz_artist["artist"]["id"] ) )
            else:
                mbz_artists += unicode( mbz_artist )
                mbz_artist_sorts += unicode( mbz_artist )
        if audio_file.get( "artist" ) != [ mbz_artists ]:
            audio_file.update( { "artist" : mbz_artists } )
            file_changed = True
        if audio_file.get( "musicbrainz_artistid" ) != mbz_artist_ids:
            audio_file.update(
                { "musicbrainz_artistid" : mbz_artist_ids } )
            file_changed = True
        if audio_file.get( "artistsort" ) != [ mbz_artist_sorts ]:
            audio_file.update( { "artistsort" : mbz_artist_sorts } )
            file_changed = True

        # Get the MusicBrainz disc ID.  (A track or recording may be
        # present on multiple releases or discs; we want to know in
        # which context this file was originally tagged.)
        #did = audio_file.get( "musicbrainz_discid" )

        # I think we need to get the disc data too... maybe cache it,
        # since it’s likely we’ll visit multiple tracks from the same
        # album.  TODO!

        # Save the file if we’re not in test mode.
        if not self._test and file_changed:
            audio_file.save()
        elif file_changed:
            print audio_file

        return

class MBzRetaggerMultipleTIDs( Exception ):
    """
    Raised when an audio file has multiple MusicBrainz track IDs.
    """
    pass
