from PySide import QtGui
from CSVHandler import CSVHandler
from DatabaseHandler import DatabaseHandler
from WienwahlModel import WienwahlModel, TableModel, Accessor, ConnectionType
import WienwahlView
import DatabaseDialog
import os

__author__ = 'mkritzl'

import sys
from PySide.QtGui import *


class MyController(QMainWindow):
    def __init__(self, parent=None):

        super().__init__(parent)

        self.form = WienwahlView.Ui_MainWindow()
        self.form.setupUi(self)

        self.dialog = DatabaseDialog.Ui_Form()
        self.dialogWindow = QDialog()
        self.dialog.setupUi(self.dialogWindow)

        self.model = WienwahlModel()
        self.csvHandler = CSVHandler()
        self.databaseHandler = DatabaseHandler('mysql+pymysql://wienwahl:wienwahl@localhost/wienwahl?charset=utf8')




        self.form.newFile.triggered.connect(self.newFile)
        self.form.openFile.triggered.connect(self.openFile)
        self.form.saveFile.triggered.connect(self.saveFile)
        self.form.saveAsFile.triggered.connect(self.saveAsFile)
        self.form.openDatabase.triggered.connect(self.databaseDialog)
        self.form.copyCreateScript.triggered.connect(self.copyCreateScript)
        self.form.closeWindow.triggered.connect(self.closeWindow)
        self.form.helpWindow.triggered.connect(self.helpWindow)
        self.form.tabs.currentChanged.connect(self.tabChanged)
        self.form.tabs.tabCloseRequested.connect(self.closeTab)
        self.form.addRow.triggered.connect(self.addRow)

        self.dialog.okOrCancel.button(QtGui.QDialogButtonBox.Ok).clicked.connect(self.openDatabase)
        self.dialog.okOrCancel.button(QtGui.QDialogButtonBox.Cancel).clicked.connect(self.closeDatabaseDialog)

    def openFileDialog(self):
        """
        Opens a file dialog and sets the label to the chosen path
        """

        path, _ = QFileDialog.getOpenFileName(self, "Open File", os.getcwd())
        return path


    def newFileDialog(self):
        path, _ = QFileDialog.getSaveFileName(self, "Save File", os.getcwd())
        return path

    def closeDatabaseDialog(self):
        self.dialogWindow.hide()


    def newFile(self):
        tab = self.appendTab(None)

        table_model = TableModel(tab, [], None)
        self.appendTable(table_model, tab)

        self.model.setCurrentTableAndAdd(table_model)
        self.formatTable(self.appendTable(table_model, tab))
        self.model.getCurrentTable().setEdited(False)

    def formatTable(self, table):
        # set font
        font = QFont("Courier New", 14)
        table.setFont(font)
        # set column width to fit contents (set font first!)
        table.resizeColumnsToContents()
        # enable sorting
        if self.model.getCurrentTable().getContent():
            table.setSortingEnabled(True)


    def appendTab(self, accessor):
        tab = QtGui.QWidget()
        tab.setObjectName("tab"+str(self.model.getTableCount()))
        if accessor:
            tab.setToolTip(accessor.getAccessString())
            self.form.tabs.addTab(tab, accessor.getName())
        else:
            tab.setToolTip("New")
            self.form.tabs.addTab(tab, "New")
        self.form.tabs.setCurrentIndex(self.form.tabs.count()-1)
        return tab

    def appendTable(self, table_model, parent):
        table_view = QTableView()
        table_view.setObjectName("table"+str(self.model.getTableCount()))
        table_view.setModel(table_model)

        layout = QVBoxLayout(self)
        layout.addWidget(table_view)
        parent.setLayout(layout)

        return table_view

    def generateNewTab(self, content, accessor):
            tab = self.appendTab(accessor)

            table_model = TableModel(tab, content, accessor)

            self.model.setCurrentTableAndAdd(table_model)
            self.formatTable(self.appendTable(table_model, tab))
            self.model.getCurrentTable().setEdited(False)

    def openFile(self):
        path = self.openFileDialog()
        if path is not "":
            accessor = Accessor(path, ConnectionType.csv)
            self.generateNewTab(self.csvHandler.getContentAsArray(accessor.getAccessString()), accessor)

    def databaseDialog(self):
        self.dialog.elections.clear()
        self.dialog.elections.addItems(self.databaseHandler.getElections())
        self.dialogWindow.show()

    def saveToDatabase(self):
        self.dialogWindow.hide()

    def openDatabase(self):
        access = self.dialog.elections.currentText()
        if access is not "":
            accessor = Accessor(access, ConnectionType.database)
            self.generateNewTab(self.databaseHandler.getConentAsArray(accessor.getAccessString()), accessor)

        self.closeDatabaseDialog()


    def saveFile(self):
        if self.model.getTableCount()>0:
            if self.model.getCurrentTable().getAccessor():
                self.csvHandler.setContent(self.model.getCurrentTable().getAccessor().getAccessString(), self.model.getCurrentTable().getData())
            else:
                self.saveAsFile()

    def saveAsFile(self):
        if self.model.getTableCount()>0:
            path = self.newFileDialog()
            self.csvHandler.setContent(path, self.model.getCurrentTable().getData())

            accessor = Accessor(path, ConnectionType.csv)
            self.model.getCurrentTable().setAccessor(Accessor(path, ConnectionType.csv))
            self.model.getCurrentTable().setEdited(False)

            self.form.tabs.setTabText(self.model.getCurrentIndex(), accessor.getName())
            self.form.tabs.setTabToolTip(self.model.getCurrentIndex(), accessor.getName())



    def get_zero_column_selected_indexes(self, table_view=None):
        if not table_view:
            return
        selected_indexes = table_view.selectedIndexes()
        if not selected_indexes:
            return
        return [index for index in selected_indexes if not index.column()]

    def get_selection(self):
        zero_column_selected_indexes = self.get_zero_column_selected_indexes(self.form["table"+self.model.getCurrentIndex()])
        if not zero_column_selected_indexes:
            return self.table_model.rowCount(self), 1
        first_zero_column_selected_index = zero_column_selected_indexes[0]
        zero_column_selected_indexes = self.get_zero_column_selected_indexes(self.view.tableView)

        if not first_zero_column_selected_index or not first_zero_column_selected_index.isValid():
            return False
        startingrow = first_zero_column_selected_index.row()

        return startingrow, len(zero_column_selected_indexes)


    def addRow(self):
        table = self.model.getCurrentTable()
        if table:
            table.insertRow(table.rowCount(table))

    def removeRows(self):
        start, amount = self.get_selection()
        self.model.getCurrentTable().removeRows(start, amount)

    def copyCreateScript(self):
        pass

    def closeWindow(self):
        pass

    def helpWindow(self):
        pass

    def tabChanged(self):
        self.model.setCurrentIndex(self.form.tabs.currentIndex())

    def closeTab(self, index):
        if not self.model.getTables()[index].isEdited():
            self.removeTab(index)
        else:
            quit_msg = "The file is not saved. Are you sure you want to close the file?"
            reply = QtGui.QMessageBox.question(self, 'Message', quit_msg, QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)

            if reply == QtGui.QMessageBox.Save:
                self.saveFile()
                self.removeTab(index)
            elif reply == QtGui.QMessageBox.Yes:
                self.removeTab(index)

    def removeTab(self, index):
        widget = self.form.tabs.widget(index)
        if widget is not None:
            widget.deleteLater()
        self.form.tabs.removeTab(index)
        self.model.deleteTable(index)




if __name__ == "__main__":
    app = QApplication(sys.argv)
    c = MyController()
    c.show()
    sys.exit(app.exec_())