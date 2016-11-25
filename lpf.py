#!/usr/bin/env python
# -*- coding: utf-8 -*-

__license__   = 'GPLv2'
__author__    = 'Caio Begotti'
__email__     = 'caio1982@gmail.com'
__credits__   = ['Claudio Matsuoka', 'Alexandre Possebom']

# Lost-Photos-Found, recover all your images buried deep in Gmail!

import os
import sys
import argparse

from lostphotosfound.server import Server
from lostphotosfound.config import Config

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('--no-index', help='ignore retrieved email index', action='store_true')
    parser.add_argument('-F', '--folders', help='create folders for email senders', action='store_true')
    parser.add_argument('-S', '--search', type=str, help='specify additional search criteria')
    args = parser.parse_args()

    config = Config()
    host = config.get('host')
    username = config.get('username')
    password = config.get('password')
    search = args.search
    use_index = not args.no_index
    use_folders = args.folders

    imap = Server(host, username, password, search=search, debug=os.getenv('DEBUG', False),
                  use_index=use_index, use_folders=use_folders)
    imap.lostphotosfound()

    print 'All done, see directory ~/LostPhotosFound for all the treasure we found for you :-)'
    sys.exit()
