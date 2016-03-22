# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui/DatabaseDialog.ui'
#
# Created: Tue Mar 22 23:06:09 2016
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(400, 300)
        self.gridLayoutWidget = QtGui.QWidget(Form)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(0, 0, 401, 301))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtGui.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.elections = QtGui.QComboBox(self.gridLayoutWidget)
        self.elections.setEditable(True)
        self.elections.setObjectName("elections")
        self.gridLayout.addWidget(self.elections, 1, 0, 1, 1)
        self.label = QtGui.QLabel(self.gridLayoutWidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.okOrCancel = QtGui.QDialogButtonBox(self.gridLayoutWidget)
        self.okOrCancel.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.okOrCancel.setObjectName("okOrCancel")
        self.gridLayout.addWidget(self.okOrCancel, 2, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Form", "Which date does the election have?", None, QtGui.QApplication.UnicodeUTF8))

