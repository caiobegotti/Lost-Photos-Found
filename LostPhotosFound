#!/usr/bin/env python
# -*- coding: utf-8 -*-

__license__   = 'GPLv2'
__author__    = 'Caio Begotti'
__email__     = 'caio1982@gmail.com'
__credits__   = ['Claudio Matsuoka', 'Alexandre Possebom']

"""LostPhotosFound, Linux version of the LostPhotos application for Mac/Windows"""

import sys

# the server class and the app method
from lib.server import _charset_decoder
from lib.server import Server

# config class and its methods
from lib.config import _app_folder
from lib.config import Config

if __name__ == "__main__":
    config = Config()
    host = config.get('gmail', 'host')
    username = config.get('gmail', 'username')
    password = config.get('gmail', 'password')

    imap = Server(host,
                  username,
                  password,
                  debug=False)
    imap.lostphotosfound()
    imap.close()

    print 'All done!'
    sys.exit()
