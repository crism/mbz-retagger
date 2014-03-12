#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
iterates over files returning structured audio metadata

Provides a class for iterating over the specified files, whether given
as individual files or directories.  For each file, attempts to open
them and observe their metadata; skips files that fail to open as
audio files.

Copyright © 2014 Christopher R. Maden.

This code may be freely copied, distributed, and reused without
restriction.  It would be nice if you gave me credit.  There is no
warranty; it might destroy all your data.  In fact, it probably will.
"""

__author__ = u"Christopher R. Maden <crism@maden.org>"
__date__ = u"11 March 2014"
__version__ = 0.1

from file_scanner import FileScanner
import mutagen

class AudioFileScanner( FileScanner ):
    """
    Given a list of filenames, acts as an iterator over all specified
    files.  If specified filenames include directories, recursively
    descends into directories.

    Attempts to open each file using the mutagen library.  Skips
    unsuccessful files.

    Returns files as instances of mutagen.FileType or some subtype
    thereof.

    Raises IOError if filenames do not exist.
    """
    def next( self ):
        """
        Let FileScanner identify the next filename to process.
        Attempt to open it with mutagen; return the resulting object
        if successful.
        """
        audio_filename = self.get_next_filename()
        audio_file = mutagen.File( audio_filename )

        # mutagen will return None if it doesn’t know what to do with
        # it.
        if audio_file is None:
            return self.next()

        return audio_file
