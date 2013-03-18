#!/usr/bin/env python
# -*- coding: utf-8 -*-
# same license, author and
# credits of the main script

import sys
import os

from PyQt4 import QtCore
from PyQt4 import QtGui

from lostphotosfound.config import Config

app = QtGui.QApplication(sys.argv)

def monitoredChange(path):
    filelist = os.listdir(filepath)
    filelist = filter(lambda x: not os.path.isdir(x), filelist)
    newest = max(filelist, key=lambda x: os.path.getmtime(filepath + '/' + x))
    newest = filepath + '/' + newest
    pic.setPixmap(QtGui.QPixmap(newest))
    print 'ACK'

config = Config()
userfolder = config.get('gmail', 'username')
filepath = os.path.expanduser('~/LostPhotosFound/') + userfolder

monitoredPath = [filepath]
fswatcher = QtCore.QFileSystemWatcher(monitoredPath)
fswatcher.directoryChanged.connect(monitoredChange)

window = QtGui.QMainWindow()
window.setGeometry(0, 0, 500, 500)
pic = QtGui.QLabel(window)
pic.setGeometry(0, 0, 500, 500)
pic.setScaledContents(True)
#pic.setPixmap(QtGui.QPixmap(newest))
window.show()

sys.exit(app.exec_())
