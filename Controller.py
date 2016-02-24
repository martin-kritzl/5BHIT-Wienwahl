from PySide import QtGui
from CSVHandler import CSVHandler
from WienwahlModel import WienwahlModel, TableModel, Accessor
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
        self.model = WienwahlModel()
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
        tab = self.appendTab("New")

        table_model = TableModel(tab, [], None)
        self.appendTable(table_model, tab)

        self.model.setCurrentTableAndAdd(table_model)
        self.formatTable(self.appendTable(table_model, tab))

    def formatTable(self, table):
        # set font
        font = QFont("Courier New", 14)
        table.setFont(font)
        # set column width to fit contents (set font first!)
        table.resizeColumnsToContents()
        # enable sorting
        if self.model.getCurrentTable().getContent():
            table.setSortingEnabled(True)

    def appendTab(self, displayName):
        tab = QtGui.QWidget()
        tab.setObjectName("tab"+str(self.model.getTableCount()))
        self.form.tabs.addTab(tab, displayName)
        return tab

    def appendTable(self, table_model, parent):
        table_view = QTableView()
        table_view.setModel(table_model)

        layout = QVBoxLayout(self)
        layout.addWidget(table_view)
        parent.setLayout(layout)

        return table_view

    def openFile(self):
        path = self.openFileDialog()
        accessor = Accessor(path)
        tab = self.appendTab(accessor.getName())

        table_model = TableModel(tab, self.csvHandler.getContentAsArray(path), accessor)

        self.model.setCurrentTableAndAdd(table_model)
        self.formatTable(self.appendTable(table_model, tab))

    def saveFile(self):
        if self.model.getCurrentTable().getAccessor():
            self.csvHandler.setContent(self.model.getCurrentTable().getAccessor().getAccessString(), self.model.getCurrentTable().getData())
        else:
            self.saveAsFile()

    def saveAsFile(self):
        self.model.setCurrentFileAndAdd(self.openFileDialog())
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