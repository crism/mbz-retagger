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
__date__ = u"13 March 2014"
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
        """
        # Get the MusicBrainz track ID.
        tid = audio_file.get( "musicbrainz_trackid" )

        # If there’s no track ID, there’s nothing for us to do.
        if not tid:
            return

        # query mbz

        # map the data

        audio_file.update( { "test_tag" : "crism" } )

        # Save the file if we’re not in test mode.
        if not self._test:
            audio_file.save()

        return
