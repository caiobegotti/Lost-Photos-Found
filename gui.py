#!/usr/bin/env python
# -*- coding: utf-8 -*-
# same license, author and
# credits of the main script

#@button.clicked.connect
#def myCallback():

import sys

from PyQt4 import QtCore, QtGui, Qt, QtDeclarative

app = QtGui.QApplication(sys.argv)

view = QtDeclarative.QDeclarativeView()
view.setSource(QtCore.QUrl('ui.qml'))
#view.setWindowFlags(QtCore.Qt.FramelessWindowHint)
view.setResizeMode(QtDeclarative.QDeclarativeView.SizeRootObjectToView)
view.setGeometry(100, 100, 400, 240)
view.show()
sys.exit(app.exec_()) 

