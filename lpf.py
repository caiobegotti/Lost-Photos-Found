#!/usr/bin/env python
# -*- coding: utf-8 -*-

__license__   = 'GPLv2'
__author__    = 'Caio Begotti'
__email__     = 'caio1982@gmail.com'
__credits__   = ['Claudio Matsuoka', 'Alexandre Possebom']

"""LostPhotosFound, Linux version of the LostPhotos application for Mac/Windows"""

import sys

from lostphotosfound.utils import _charset_decoder
from lostphotosfound.utils import _app_folder

from lostphotosfound.server import Server
from lostphotosfound.config import Config

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
