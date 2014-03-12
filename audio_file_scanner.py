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

class AudioFileScanner( FileScanner ):
    pass
