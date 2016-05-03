import os
from command.command import EditCommand, InsertRowsCommand, RemoveRowsCommand, DuplicateRowCommand
from command.delegate import ItemDelegate

from csvhandler.CSVHandler import CSVHandler
from model.WienwahlModel import TableModel
from gui import WienwahlView

__author__ = 'mkritzl'

import sys
from PySide.QtGui import *


class MyController(QMainWindow):
    def __init__(self, parent=None):

        super().__init__(parent)

        self.form = WienwahlView.Ui_MainWindow()
        self.form.setupUi(self)


        self.model = TableModel(self)
        self.handler = CSVHandler()

        self.form.tableView.setModel(self.model)
        self.form.tableView.setItemDelegate(ItemDelegate(self.model.getUndoStack(), self.changedTableModel))

        self.handler = CSVHandler()

        self.form.newFile.triggered.connect(self.newFile)
        self.form.openFile.triggered.connect(self.openFile)
        self.form.saveFile.triggered.connect(self.saveFile)
        self.form.saveAsFile.triggered.connect(self.saveAsFile)

        self.form.copy.triggered.connect(self.copy)
        self.form.cut.triggered.connect(self.cut)
        self.form.paste.triggered.connect(self.paste)
        self.form.undo.triggered.connect(self.undo)
        self.form.redo.triggered.connect(self.redo)

        self.form.addRow.triggered.connect(self.addRow)
        self.form.duplicateRow.triggered.connect(self.duplicateRow)
        self.form.removeRow.triggered.connect(self.removeRows)

        self.formatTable()

    def openFileDialog(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open File", os.getcwd())
        return path

    def newFileDialog(self):
        path, _ = QFileDialog.getSaveFileName(self, "Save File", os.getcwd())
        return path

    def newFile(self):
        self.model=TableModel(self)
        self.model.setHeader(["T","WV","WK","BZ","SPR","WBER","ABG","UNG","SPOE","FPOE","OEVP","GRUE","NEOS","WWW","ANDAS","GFW","SLP","WIFF","M","FREIE"])
        self.model.setEdited(False)
        self.editedSomething()

    def formatTable(self):
        font = QFont("Courier New", 14)
        self.form.tableView.setFont(font)
        self.form.tableView.resizeColumnsToContents()
        if self.model.getContent():
            self.form.tableView.setSortingEnabled(True)

    def openFile(self):
        path = self.openFileDialog()
        if path is not "":
            self.model.setHeaderAndContent(self.handler.getContentAsArray(path))
            self.model.setAccessor(path)
            self.editedSomething()

    def saveFile(self):
        self.save(False)

    def saveAsFile(self):
        self.save(True)

    def save(self, new):
        if new==True:
            accessor = self.newFileDialog()
            if accessor:
                self.handler.setContent(accessor, self.model.getData())
        else:
            accessor = self.model.getAccessor()
            if accessor:
                self.handler.setContent(accessor, self.model.getData())

    def get_selected_rows(self):
        indexes = self.form.tableView.selectionModel().selectedIndexes()
        if indexes:
            return indexes[0].row(), len(indexes)
        else:
            return None, None

    def changedTableModel(self, cmds, name):
        self.model.getUndoStack().beginMacro(name)
        for cmd in cmds:
            self.model.getUndoStack().push(cmd)
        self.model.getUndoStack().endMacro()
        self.editedSomething()

    def addRow(self):
        table = self.model
        if table:
            start, amount = self.get_selected_rows()
            if amount:
                self.changedTableModel([InsertRowsCommand(self.model, start, 1)], "Added table")

    def duplicateRow(self):
        table = self.model
        if len(table.getContent()) == 0:
            return
        start, amount = self.get_selected_rows()
        if amount:
            self.changedTableModel([DuplicateRowCommand(table, start)], "Duplicated row")

    def removeRows(self):
        table = self.model
        if len(table.getContent()) == 0:
            return
        start, amount = self.get_selected_rows()
        if amount:
            self.changedTableModel([RemoveRowsCommand(table, start, amount)], "Removed row(s)")

    def cut(self):
        selectedIndexes = self.form.tableView.selectionModel().selectedIndexes()
        if len(selectedIndexes) == 0:
            return

        self.setClipboard()

        cmd = EditCommand(self.model, selectedIndexes[0])
        cmd.newValue("")
        self.changedTableModel([cmd], "Cutted Text")

    def setClipboard(self):
        sys_clip = QApplication.clipboard()
        selection = self.form.tableView.selectionModel().selectedIndexes()[0]
        selected_text = str(self.model.data(selection))
        sys_clip.setText(selected_text)

    def copy(self):
        selectedIndexes = self.form.tableView.selectionModel().selectedIndexes()
        if len(selectedIndexes) == 0:
            return

        self.setClipboard()


    def paste(self):
        selectedIndexes = self.form.tableView.selectionModel().selectedIndexes()
        if len(selectedIndexes) == 0:
            return

        sys_clip = QApplication.clipboard()
        value = str(sys_clip.text())
        index = selectedIndexes[0]
        cmd = EditCommand(self.model, index)
        cmd.newValue(value)

        self.changedTableModel([cmd], "Pasted Text")

    def editedSomething(self):
        self.form.tableView.reset()
        self.model.setEdited(True)
        self.setUndoRedoMenu()
        self.formatTable()

    def undo(self):
        self.model.getUndoStack().undo()
        self.editedSomething()

    def redo(self):
        self.model.getUndoStack().redo()
        self.editedSomething()

    def setUndoRedoMenu(self):
        undo = "Undo"
        redo = "Redo"
        undoText = self.model.getUndoStack().undoText()
        redoText = self.model.getUndoStack().redoText()
        if undoText:
            undo+= " (" + undoText + ")"
        if redoText:
            redo+= " (" + redoText + ")"

        self.form.undo.setText(undo)
        self.form.redo.setText(redo)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    c = MyController()
    c.show()
    sys.exit(app.exec_())