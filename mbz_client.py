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
__date__ = u"13 March 2014"
__version__ = 0.1

import musicbrainzngs

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
