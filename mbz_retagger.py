#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
MusicBrainz Retagger, updates metadata in audio files

Reads audio files specified on the command line, then checks
MusicBrainz for updated data.  If new information is present, updates
the tags and resaves the file in place.

To comply with MusicBrainz’s request, queries are made at one per
second, so run this in the background.

Copyright © 2014 Christopher R. Maden.

This code may be freely copied, distributed, and reused without
restriction.  It would be nice if you gave me credit.  There is no
warranty; it might destroy all your data.  In fact, it probably will.
"""

__author__ = u"Christopher R. Maden <crism@maden.org>"
__date__ = u"13 March 2014"
__title__ = u"MusicBrainz Retagger"
__version__ = 0.1

# TODO v0.2: Keep a log file, so if rerun on the same library
# repeatedly, will pick up where it left off.

import argparse
from audio_file_scanner import AudioFileScanner
from os.path import expanduser
from retagger import MBzRetagger

def main():
    """
    Do the heavy lifting.  Parse the user options, spin up a file
    scanner, and spin up a MusicBrainz client.  Then iterate over the
    files, updating each one with fresh MusicBrainz goodness!
    """
    # Parse user options.
    parser = argparse.ArgumentParser(
        description="updates metadata in audio files",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument( "-v", "--version", action="version",
                         version="%s %0.1f" %
                             (__title__, __version__) )
    parser.add_argument( "-t", "--test", action="store_true",
                         help="do not actually write changes out")
    parser.add_argument( "-u", "--user",
                         help="email address to pass to MusicBrainz" )
    parser.add_argument( "files", nargs="+",
                         help="audio files or directories to read" )
    args = parser.parse_args()

    # Initialize the file scanner.
    file_scanner = AudioFileScanner( args.files )

    # Initialize the MusicBrainz retagger.
    retagger = MBzRetagger( args.test, contact=args.user )

    # Iterate over the audio files, retagging each one.
    for audio_file in file_scanner:
        retagger.retag( audio_file )

if __name__ == "__main__":
    main()
    exit( 0 )
