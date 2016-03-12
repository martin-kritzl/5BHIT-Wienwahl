from threading import Thread
import os

from PySide import QtGui
from datetime import datetime
from command.command import EditCommand, InsertRowsCommand, RemoveRowsCommand, DuplicateRowCommand
from command.delegate import ItemDelegate
from controller.DatabasedialogController import DatabaseDialogController

from csvhandler.CSVHandler import CSVHandler
from command.CopyPaste import PasteAction
from database.DatabaseHandler import DatabaseHandler
from model.WienwahlModel import WienwahlModel, TableModel, Accessor, ConnectionType
from gui import WienwahlView

__author__ = 'mkritzl'

import sys
from PySide.QtGui import *


class MyController(QMainWindow):
    def __init__(self, parent=None):

        super().__init__(parent)

        self.form = WienwahlView.Ui_MainWindow()
        self.form.setupUi(self)

        self.dialogWindow = DatabaseDialogController()

        self.model = WienwahlModel()
        self.csvHandler = CSVHandler()
        self.databaseHandler = DatabaseHandler('mysql+pymysql://wienwahl:wienwahl@localhost/wienwahl?charset=utf8')

        self.databaseStep = None
        self.undoStack = QUndoStack()


        self.form.newFile.triggered.connect(self.newFile)
        self.form.openFile.triggered.connect(self.openFile)
        self.form.saveFile.triggered.connect(self.saveResourceThread)
        self.form.saveAsFile.triggered.connect(self.saveAsFile)
        self.form.saveAsDatabase.triggered.connect(self.saveAsDatabase)
        self.form.openDatabase.triggered.connect(self.openDatabase)
        self.form.copy.triggered.connect(self.copy)
        self.form.cut.triggered.connect(self.cut)
        self.form.paste.triggered.connect(self.paste)
        self.form.undo.triggered.connect(self.undo)
        self.form.redo.triggered.connect(self.redo)
        self.form.closeWindow.triggered.connect(self.closeWindow)
        self.form.helpWindow.triggered.connect(self.helpWindow)
        self.form.tabs.currentChanged.connect(self.tabChanged)
        self.form.tabs.tabCloseRequested.connect(self.closeTab)
        self.form.addRow.triggered.connect(self.addRow)
        self.form.duplicateRow.triggered.connect(self.duplicateRow)
        self.form.removeRow.triggered.connect(self.removeRows)

        self.form.prediction.triggered.connect(self.prediction)
        self.form.createPrediction.triggered.connect(self.createPrediction)

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
        table_view.setItemDelegate(ItemDelegate(self.undoStack))

        layout = QVBoxLayout(self)
        layout.addWidget(table_view)
        parent.setLayout(layout)

        return table_view

    def generateNewTab(self, content, accessor):
            tab = self.appendTab(accessor)

            table_model = TableModel(tab, content, accessor)

            self.model.setCurrentTableAndAdd(table_model)
            table_view = self.appendTable(table_model, tab)
            self.formatTable(table_view)
            self.model.getCurrentTable().setView(table_view)
            self.model.getCurrentTable().setEdited(False)

    def openFile(self):
        path = self.openFileDialog()
        if path is not "":
            accessor = Accessor(path, ConnectionType.csv)
            self.generateNewTab(self.csvHandler.getContentAsArray(accessor.getAccessString()), accessor)

    def databaseDialog(self):
        self.dialogWindow.setElections(self.databaseHandler.getElections())
        self.dialogWindow.show()
        if self.dialogWindow.exec_():
            self.dialogWindow.hide()
            return self.dialogWindow.getElection()

    def handleDatabase(self):
        pass

    def openDatabase(self):
        access = self.databaseDialog()
        if access:
            accessor = Accessor(access, ConnectionType.database)
            self.generateNewTab(self.databaseHandler.getVotesAsArray(accessor.getAccessString()), accessor)

        self.closeDatabaseDialog()

    def saveAsResourceThread(self, type):
        self.saveAsResource(type)

    def saveResourceThread(self):
        self.saveResource()

    def setSavingStatus(self):
        print("Set saving status")
        if self.model.allSaved():
            self.form.statusbar.showMessage('saved')
        else:
            self.form.statusbar.showMessage('saving...')


    def saveResource(self, accessor=None):
        if not accessor:
            accessor = self.model.getCurrentTable().getAccessor()
        self.model.getCurrentTable().setSaved(False)
        # self.setSavingStatus()
        handler = None
        if self.model.getTableCount()>0:

            if accessor.getConnectionType()==ConnectionType.csv:
                handler = self.csvHandler
            elif accessor.getConnectionType()==ConnectionType.database:
                handler = self.databaseHandler

            handler.setContent(accessor.getAccessString(), self.model.getCurrentTable().getData())
            self.model.getCurrentTable().setEdited(False)


        self.model.getCurrentTable().setSaved(True)
        # self.setSavingStatus()


    def saveAsDatabase(self):
        self.saveAsResourceThread(ConnectionType.database)

    def saveAsFile(self):
        self.saveAsResourceThread(ConnectionType.csv)

    def saveAsResource(self, type=ConnectionType.csv):
        accessor = None
        if self.model.getTableCount()>0:
            if type==ConnectionType.csv:
                accessor = Accessor(self.newFileDialog(), ConnectionType.csv)
            elif type==ConnectionType.database:
                accessor = Accessor(self.databaseDialog(), ConnectionType.database)

            thread = Thread(target=self.saveResource, args=(accessor, ))
            thread.start()

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
        zero_column_selected_indexes = self.get_zero_column_selected_indexes(self.model.getCurrentTable().getView())
        if not zero_column_selected_indexes:
            return self.model.getCurrentTable().rowCount(self), 1
        first_zero_column_selected_index = zero_column_selected_indexes[0]
        zero_column_selected_indexes = self.get_zero_column_selected_indexes(self.model.getCurrentTable().getView())

        if not first_zero_column_selected_index or not first_zero_column_selected_index.isValid():
            return False
        startingrow = first_zero_column_selected_index.row()

        return startingrow, len(zero_column_selected_indexes)


    def addRow(self):
        table = self.model.getCurrentTable()
        if table:
            start, amount = self.get_selection()
            self.undoStack.push(InsertRowsCommand(self.model.getCurrentTable(), start, 1))
            self.editedSomething()

    def duplicateRow(self):
        if len(self.model.getCurrentTable().getContent()) == 0:
            return
        start, amount = self.get_selection()
        self.undoStack.push(DuplicateRowCommand(self.model.getCurrentTable(), start))
        self.editedSomething()

    def removeRows(self):
        if len(self.model.getCurrentTable().getContent()) == 0:
            return
        start, amount = self.get_selection()
        self.undoStack.push(RemoveRowsCommand(self.model.getCurrentTable(), start, amount))
        self.editedSomething()

    def cut(self):
        selectedIndexes = self.model.getCurrentTable().getView().selectionModel().selectedIndexes()
        if len(selectedIndexes) == 0:
            return

        sys_clip = QApplication.clipboard()
        selection = selectedIndexes[0]
        selected_text = str(self.model.getCurrentTable().data(selection))
        sys_clip.setText(selected_text)

        cmd = EditCommand(self.model.getCurrentTable(), selection)
        cmd.newValue("")
        self.undoStack.push(cmd)
        self.editedSomething()

    def copy(self):
        selectedIndexes = self.model.getCurrentTable().getView().selectionModel().selectedIndexes()
        if len(selectedIndexes) == 0:
            return

        sys_clip = QApplication.clipboard()
        selection = selectedIndexes[0]
        selected_text = str(self.model.getCurrentTable().data(selection))
        sys_clip.setText(selected_text)


    def paste(self):
        selectedIndexes = self.model.getCurrentTable().getView().selectionModel().selectedIndexes()
        if len(selectedIndexes) == 0:
            return

        sys_clip = QApplication.clipboard()
        value = str(sys_clip.text())
        index = selectedIndexes[0]
        cmd = EditCommand(self.model.getCurrentTable(), index)
        cmd.newValue(value)
        self.undoStack.push(cmd)
        self.editedSomething()

    def editedSomething(self):
        self.model.getCurrentTable().getView().reset()
        self.model.getCurrentTable().setEdited(True)

    def undo(self):
        self.undoStack.undo()
        self.model.getCurrentTable().getView().reset()

    def redo(self):
        self.undoStack.redo()
        self.model.getCurrentTable().getView().reset()

    def closeWindow(self):
        pass

    def helpWindow(self):
        pass

    def prediction(self,date=None):
        if not date:
            if self.model.getCurrentTable() and self.model.getCurrentTable().getAccessor() and self.model.getCurrentTable().getAccessor().getConnectionType()==ConnectionType.database:
                date = self.model.getCurrentTable().getAccessor().getAccessString()
            else:
                date = self.databaseDialog()
        if date:
            accessor = Accessor(date, ConnectionType.prediction)
            self.generateNewTab(self.databaseHandler.getPredictionsAsArray(accessor.getAccessString()), accessor)

    def createPrediction(self):
        if self.model.getCurrentTable() and self.model.getCurrentTable().getAccessor():
            date = self.model.getCurrentTable().getAccessor().getAccessString()
        else:
            date = datetime.now().strftime("%Y-%m-%d")
        self.prediction(self.databaseHandler.createPrediction(date))

    def tabChanged(self):
        self.model.setCurrentIndex(self.form.tabs.currentIndex())

    def closeTab(self, index):
        if not self.model.getTables()[index].isEdited():
            self.removeTab(index)
        else:
            quit_msg = "The file is not saved. Are you sure you want to close the file?"
            reply = QtGui.QMessageBox.question(self, 'Message', quit_msg, QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)

            if reply == QtGui.QMessageBox.Save:
                self.saveRessource()
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