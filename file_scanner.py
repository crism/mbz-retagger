#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
iterates over files in specified list of files or directories

Provides a class for iterating over the specified files, whether given
as individual files or directories.

Copyright © 2014 Christopher R. Maden.

This code may be freely copied, distributed, and reused without
restriction.  It would be nice if you gave me credit.  There is no
warranty; it might destroy all your data.  In fact, it probably will.
"""

__author__ = u"Christopher R. Maden <crism@maden.org>"
__date__ = u"11 March 2014"
__version__ = 0.1

# TODO v0.2: Keep a log file, so if rerun on the same library
# repeatedly, will pick up where it left off.

from glob import glob
from os.path import exists, isdir

class FileScanner( object ):
    """
    Given a list of filenames, acts as an iterator over all specified
    files.  If specified filenames include directories, recursively
    descends into directories.

    Returns filenames as strings when iterated over.

    Raises IOError if filenames do not exist.
    """
    def __init__( self, files=[] ):
        """
        Set up an iteration with the specified files.  No verification
        is done at this stage.  The files should be a list of strings.
        """
        self._files = files

        # Reverse the list so that pop() works in user-logical order.
        self._files.reverse()

        return

    def __iter__( self ):
        """
        Return self for iteration purposes; all the heavy lifting is
        done in self.next().
        """
        return self

    def get_next_filename( self ):
        """
        Look at the next specified file.  If it is a simple file,
        return it; if it is a directory, expand it to its constituent
        files, adjust the queue, and recurse.
        """
        # Are we there yet?
        if len( self._files ) <= 0:
            raise StopIteration

        # Get a candidate filename.
        this_file = self._files.pop().strip()

        # Check for file existence...
        if not exists( this_file ):
            raise IOError, "File not found: %s" % this_file

        # Simple file?  Just return it.
        if not isdir( this_file ):
            return this_file

        # If the candidate is a directory, alter the queue with the
        # contents of the directory, then recurse.
        this_file = this_file.rstrip("/")

        # This reversal stuff is not strictly necessary, since the
        # user will probably never know, but my OCD would be annoyed
        # if the contents of a directory were done in reverse order,
        # too.
        filelist = glob( this_file + "/*" )
        filelist.reverse()
        self._files.extend( filelist )
        return self.get_next_filename()

    def next( self ):
        """
        Implement iteration by calling get_next_filename() to
        ... well, y’know.
        """
        return self.get_next_filename()

if __name__ == '__main__':
    pass
