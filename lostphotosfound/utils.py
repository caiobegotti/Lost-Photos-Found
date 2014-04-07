#!/usr/bin/env python
# -*- coding: utf-8 -*-
# same license, author and
# credits of the main script

import os

from chardet import detect
from email.header import decode_header

def _app_folder():
    """
    Internal function to return the app folder in user's home in a multi-OS way
    """
    directory = os.path.expanduser('~/.LostPhotosFound')
    if not os.path.isdir(directory):
        os.makedirs(directory, 0700)
    return directory

def _charset_decoder(header):
    """
    Internal function to decode header charsets of subject, from, filenam etc

    @param header: the result of a decode_header() in the mail object
    """

    fallback_header = []
    # make it a humand-readable string
    try:
        header = decode_header(header)
    except UnicodeEncodeError:
        forced = (header.encode('utf-8'), 'utf-8')
        fallback_header.append(forced)
        header = fallback_header

    # string in [0], charset in [1]
    if header[0][1] is None:
        guessed = detect(header[0][0])['encoding']
        if guessed is not None:
            header = header[0][0].decode(guessed).encode('utf-8')
    else:
        header = header[0][0].decode(header[0][1]).encode('utf-8')
    print 'LOG: [decoded header] %s' % repr(header)

    return header
