#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
connect to the MusicBrainz XML API

This is a wrapper for the musicbrainzngs library intended for repeat
use; it ensures no more than one request is made per second, as
politely requested by MusicBrainz.

Copyright © 2014 Christopher R. Maden.

This code may be freely copied, distributed, and reused without
restriction.  It would be nice if you gave me credit.  There is no
warranty; it might destroy all your data.  In fact, it probably will.
"""

__author__ = u"Christopher R. Maden <crism@maden.org>"
__date__ = u"19 March 2014"
__version__ = 0.1

import musicbrainzngs
from time import sleep, time

class MBzClient( object ):
    """
    Broker requests to the MusicBrainz XML API via the musicbrainzngs
    library; keep track of the time each request finishes, and don’t
    allow a new request to start until a full second has passed.
    """
    def __init__( self, contact=None ):
        """
        Spin up the client; set the timestamp to 0, as the first
        request should always be allowed to proceed.
        """
        self._time = 0

        # Set the User-Agent header for the client.
        musicbrainzngs.musicbrainz.set_useragent(
            "mbz-retagger MBzClient",
            "%0.1f" % __version__,
            contact=contact
        )

        return

    def get_track( self, track_id ):
        """
        Fetch the metadata for a track based on the specified ID.
        """
        # Time management should be generalized, but for now, tracks
        # are all we care about, so we’ll put that off.

        # Wait until it’s been at least a second.
        self.wait()

        # Get the stuff.

        # Of the valid includes, we skip:
        #  • aliases (aliases for the artist — not interesting for
        #    track-level metadata)
        #  • annotation (free text, sometimes used for additional
        #    credits — hypothetically interesting, but not a good
        #    candidate for file embedding)
        #  • ... and, actually, all the rest for now, for simplicity,
        #    but we will add them back. TODO!
        audio_data = musicbrainzngs.musicbrainz.\
            get_recording_by_id( track_id,
                                 includes=[ #"area-rels", # maybe
                                            #"artist-credits",
                                            #"artist-rels",
                                            "artists",
                                            #"discids", # maybe
                                            #"isrcs", # maybe
                                            #"label-rels", maybe
                                            #"media", # maybe
                                            #"place-rels",
                                            #"recording-rels",
                                            #"release-group-rels",
                                            #"release-rels",
                                            #"releases", # no!(?)
                                            #"tags", # later
                                            #"url-rels",
                                            #"work-rels" # yes, recursive
                                          ] )

        # Note the time we finished the request.
        self.set_time()

        return audio_data

    def set_time( self ):
        """
        Note the time of an event, so that we can space requests out
        appropriately.
        """
        self._time = time()
        return

    def wait( self ):
        """
        Make sure it’s been at least 1 s since the last request.
        """
        now = time()
        if now - self._time < 1.0:
            sleep( 1.0 + now - self._time )

        return
