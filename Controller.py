from CSVHandler import CSVHandler
from WienwahlModel import WienwahlModel, TableModel
import WienwahlView
import os
from PySide.QtGui import *
from PySide.QtCore import *

__author__ = 'mkritzl'

import sys
from PySide.QtGui import *


class MyController(QMainWindow):
    def __init__(self, parent=None):

        super().__init__(parent)
        self.form = WienwahlView.Ui_MainWindow()
        self.form.setupUi(self)
        self.model = TableModel()
        self.currentFile = None
        self.csvHandler = CSVHandler()

        self.form.newFile.triggered.connect(self.newFile)
        self.form.openFile.triggered.connect(self.openFile)
        self.form.saveFile.triggered.connect(self.saveFile)
        self.form.saveAsFile.triggered.connect(self.saveAsFile)
        self.form.copyCreateScript.triggered.connect(self.copyCreateScript)
        self.form.closeWindow.triggered.connect(self.closeWindow)
        self.form.helpWindow.triggered.connect(self.helpWindow)

    def openFileDialog(self):
        """
        Opens a file dialog and sets the label to the chosen path
        """

        path, _ = QFileDialog.getOpenFileName(self, "Open File", os.getcwd())
        return path

    def newFile(self):
        pass

    def openFile(self):
        self.currentFile = self.openFileDialog()
        self.model.setData(self.csvHandler.getContentAsArray())

    def saveFile(self):
        if self.currentFile:
            pass
        else:
            self.saveAsFile()

    def saveAsFile(self):
        self.currentFile = self.openFileDialog()
        self.csvHandler.setContent(self.model.getData())

    def copyCreateScript(self):
        pass

    def closeWindow(self):
        pass

    def helpWindow(self):
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    c = MyController()
    c.show()
    sys.exit(app.exec_())