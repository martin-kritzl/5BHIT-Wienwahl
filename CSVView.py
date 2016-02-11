# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'CSVView.ui'
#
# Created: Tue Jan 12 14:50:13 2016
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(854, 735)
        self.textarea = QtGui.QTextBrowser(Form)
        self.textarea.setGeometry(QtCore.QRect(0, 0, 851, 731))
        self.textarea.setObjectName("textarea")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))

