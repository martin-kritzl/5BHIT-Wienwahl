from PySide.QtGui import QStyledItemDelegate, QUndoStack, QTextEdit, QLineEdit
from command.command import EditCommand


class ItemDelegate(QStyledItemDelegate):

    def __init__(self, undoStack, changedTableFunction, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.undoStack = undoStack
        self.changedTableFunction = changedTableFunction
        self.edit = None

    def setModelData(self, editor, model, index):
        newValue = editor.text()
        self.edit.newValue(newValue)
        self.changedTableFunction([self.edit], "Edited table")

    def editorEvent(self, event, model, option, index):
        self.edit = EditCommand(model, index)

    def createEditor(self, parent, option, index):
        return QLineEdit(parent)

