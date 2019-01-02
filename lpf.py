#!/usr/bin/env python3
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
    parser.add_argument('--no-index', help='ignore retrieved e-mail index', action='store_true')
    parser.add_argument('-F', '--folders', help='create folders for e-mail senders', action='store_true')
    parser.add_argument('-L', '--label', type=str, help='fetch messages from a different gmail label')
    parser.add_argument('-S', '--search', type=str, help='specify additional search criteria')
    args = parser.parse_args()

    config = Config()
    host = config.get('host')
    username = config.get('username')
    password = config.get('password')
    search = args.search
    label = args.label
    use_index = not args.no_index
    use_folders = args.folders

    imap = Server(
        host, username, password, search=search, label=label,
        use_index=use_index, use_folders=use_folders,
        debug=os.getenv('DEBUG', False))
    imap.lostphotosfound()

    print("All done, see directory ~/LostPhotosFound for all the treasure we found for you :-)")
    sys.exit()
