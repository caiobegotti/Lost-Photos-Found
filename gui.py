#!/usr/bin/env python
# -*- coding: utf-8 -*-
# same license, author and
# credits of the main script

import sys
import os

from PyQt4 import QtCore
from PyQt4 import QtGui

from lostphotosfound.config import Config

app = QtCore.QCoreApplication(sys.argv)

def monitoredChange():
    print 'ACK'

config = Config()
userfolder = config.get('gmail', 'username')
filepath = os.path.expanduser('~/LostPhotosFound/') + userfolder
monitoredPath = [filepath]

fswatcher = QtCore.QFileSystemWatcher(monitoredPath)
fswatcher.directoryChanged.connect(monitoredChange)

sys.exit(app.exec_())
