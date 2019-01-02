#!/usr/bin/env python
# -*- coding: utf-8 -*-
# same license, author and
# credits of the main script

import chardet
import os

from email.header import decode_header


def _app_folder():
    """
    Internal function to return the app folder in user's home in a multi-OS way
    """
    directory = os.path.expanduser('~/.LostPhotosFound')
    if not os.path.isdir(directory):
        os.makedirs(directory, 0o700)
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

    data = header[0][0]

    # Ensure data is bytes, not string
    if isinstance(data, str):
        data = data.encode("utf-8")

    # Don't trust given encoding, it may be bogus
    guessed = chardet.detect(data)
    if guessed is not None and "encoding" in guessed and guessed["encoding"] is not None:
        header = data.decode(guessed["encoding"])
    else:
        header = _sanitize_bytes(data)

    print("LOG: [decoded header] {}".format(repr(header)))

    return header


def _sanitize_bytes(data: bytes) -> str:
    return bytes(filter(lambda x: x >= 20 and x < 172, data)).decode("utf-8")
