from PySide.QtCore import Qt
from PySide.QtGui import QUndoCommand


class EditCommand(QUndoCommand):
    """
    Edit the selected cell
    :var __model: QTableModel: Model for command
    :var __index: QModelIndex: selected cell
    :var __oldValue: string: value before redo command executed
    :var __newValue: string: value before undo command executed
    """

    def __init__(self, model, index):
        """
        :param model: QTableModel
        :param index: QModelIndex
        :return: None
        """
        QUndoCommand.__init__(self)
        self.__newValue = None
        self.__model = model
        self.__index = index
        self.__oldValue = None

    def redo(self):
        self.__oldValue = self.__model.data(self.__index)
        self.__model.setData(self.__index, self.__newValue)

    def undo(self):
        self.__newValue = self.__model.data(self.__index)
        self.__model.setData(self.__index, self.__oldValue)

    def setText(self, *args, **kwargs):
        super().setText(*args, **kwargs)

    def newValue(self, newValue):
        self.__newValue = newValue

class InsertRowsCommand(QUndoCommand):
    def __init__(self, model, index, amount):
        QUndoCommand.__init__(self)
        self.__model = model
        self.__index = index
        self.__amount = amount

    def redo(self):
        self.__model.insertRows(self.__index, self.__amount)

    def undo(self):
        self.__model.removeRows(self.__index, self.__amount)

class DuplicateRowCommand(QUndoCommand):
    def __init__(self, model, index):
        QUndoCommand.__init__(self)
        self.__model = model
        self.__index = index
        self.__last_row = list(model.getContent()[index])

    def redo(self):
        self.__model.getContent().insert(self.__index+1, self.__last_row)

    def undo(self):
        self.__model.getContent().pop(self.__index+1)


class RemoveRowsCommand(QUndoCommand):
    def __init__(self, model, index, amount):
        QUndoCommand.__init__(self)
        self.__model = model
        self.__index = index
        self.__amount = amount
        self.__oldList = None

    def redo(self):
        self.__oldList = list(self.__model.getContent())
        self.__model.removeRows(self.__index, self.__amount)

    def undo(self):
        self.__model.setVotes(self.__oldList)
