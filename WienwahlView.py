# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Overview.ui'
#
# Created: Thu Feb 11 13:12:37 2016
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(855, 599)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 855, 26))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuEdit = QtGui.QMenu(self.menubar)
        self.menuEdit.setObjectName("menuEdit")
        self.menuWindows = QtGui.QMenu(self.menubar)
        self.menuWindows.setAcceptDrops(False)
        self.menuWindows.setObjectName("menuWindows")
        self.helpWindow = QtGui.QMenu(self.menubar)
        self.helpWindow.setAcceptDrops(False)
        self.helpWindow.setObjectName("helpWindow")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.openFile = QtGui.QAction(MainWindow)
        self.openFile.setObjectName("openFile")
        self.saveFile = QtGui.QAction(MainWindow)
        self.saveFile.setObjectName("saveFile")
        self.saveAsFile = QtGui.QAction(MainWindow)
        self.saveAsFile.setObjectName("saveAsFile")
        self.newFile = QtGui.QAction(MainWindow)
        self.newFile.setObjectName("newFile")
        self.closeWindow = QtGui.QAction(MainWindow)
        self.closeWindow.setObjectName("closeWindow")
        self.copyCreateScript = QtGui.QAction(MainWindow)
        self.copyCreateScript.setObjectName("copyCreateScript")
        self.menuFile.addAction(self.openFile)
        self.menuFile.addAction(self.saveFile)
        self.menuFile.addAction(self.saveAsFile)
        self.menuFile.addAction(self.newFile)
        self.menuEdit.addAction(self.copyCreateScript)
        self.menuWindows.addAction(self.closeWindow)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuWindows.menuAction())
        self.menubar.addAction(self.helpWindow.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QObject.connect(self.closeWindow, QtCore.SIGNAL("triggered()"), MainWindow.close)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.menuFile.setStatusTip(QtGui.QApplication.translate("MainWindow", "Handle files", None, QtGui.QApplication.UnicodeUTF8))
        self.menuFile.setTitle(QtGui.QApplication.translate("MainWindow", "File", None, QtGui.QApplication.UnicodeUTF8))
        self.menuEdit.setStatusTip(QtGui.QApplication.translate("MainWindow", "Edit content", None, QtGui.QApplication.UnicodeUTF8))
        self.menuEdit.setTitle(QtGui.QApplication.translate("MainWindow", "Edit", None, QtGui.QApplication.UnicodeUTF8))
        self.menuWindows.setStatusTip(QtGui.QApplication.translate("MainWindow", "Handle the window", None, QtGui.QApplication.UnicodeUTF8))
        self.menuWindows.setTitle(QtGui.QApplication.translate("MainWindow", "Windows", None, QtGui.QApplication.UnicodeUTF8))
        self.helpWindow.setStatusTip(QtGui.QApplication.translate("MainWindow", "Show help", None, QtGui.QApplication.UnicodeUTF8))
        self.helpWindow.setTitle(QtGui.QApplication.translate("MainWindow", "Help", None, QtGui.QApplication.UnicodeUTF8))
        self.openFile.setText(QtGui.QApplication.translate("MainWindow", "Open", None, QtGui.QApplication.UnicodeUTF8))
        self.openFile.setStatusTip(QtGui.QApplication.translate("MainWindow", "Open a file", None, QtGui.QApplication.UnicodeUTF8))
        self.saveFile.setText(QtGui.QApplication.translate("MainWindow", "Save", None, QtGui.QApplication.UnicodeUTF8))
        self.saveFile.setStatusTip(QtGui.QApplication.translate("MainWindow", "Save the actual file", None, QtGui.QApplication.UnicodeUTF8))
        self.saveAsFile.setText(QtGui.QApplication.translate("MainWindow", "Save As", None, QtGui.QApplication.UnicodeUTF8))
        self.saveAsFile.setStatusTip(QtGui.QApplication.translate("MainWindow", "Save the actual file again", None, QtGui.QApplication.UnicodeUTF8))
        self.newFile.setText(QtGui.QApplication.translate("MainWindow", "New", None, QtGui.QApplication.UnicodeUTF8))
        self.newFile.setStatusTip(QtGui.QApplication.translate("MainWindow", "Create a new file", None, QtGui.QApplication.UnicodeUTF8))
        self.closeWindow.setText(QtGui.QApplication.translate("MainWindow", "Close", None, QtGui.QApplication.UnicodeUTF8))
        self.closeWindow.setStatusTip(QtGui.QApplication.translate("MainWindow", "Close the window", None, QtGui.QApplication.UnicodeUTF8))
        self.closeWindow.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+Q", None, QtGui.QApplication.UnicodeUTF8))
        self.copyCreateScript.setText(QtGui.QApplication.translate("MainWindow", "Copy", None, QtGui.QApplication.UnicodeUTF8))
        self.copyCreateScript.setStatusTip(QtGui.QApplication.translate("MainWindow", "Copy the displayed content", None, QtGui.QApplication.UnicodeUTF8))
        self.copyCreateScript.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+C", None, QtGui.QApplication.UnicodeUTF8))

