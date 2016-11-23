#!/usr/bin/env python
# -*- coding: utf-8 -*-

__license__   = 'GPLv2'
__author__    = 'Caio Begotti'
__email__     = 'caio1982@gmail.com'
__credits__   = ['Claudio Matsuoka', 'Alexandre Possebom']

# Lost-Photos-Found, recover all your images buried deep in Gmail!

import os
import sys

from lostphotosfound.server import Server
from lostphotosfound.config import Config

if __name__ == "__main__":
    config = Config()
    host = config.get('host')
    username = config.get('username')
    password = config.get('password')

    imap = Server(host, username, password, debug=os.getenv('DEBUG', False))
    imap.lostphotosfound()

    print 'All done, see directory ~/LostPhotosFound for all the treasure we found for you :-)'
    sys.exit()
