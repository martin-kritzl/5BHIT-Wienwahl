import operator
from PySide.QtCore import *
from PySide.QtGui import QUndoStack

__author__ = 'mkritzl'

class TableModel(QAbstractTableModel):
    """
    https://blog.rburchell.com/2010/02/pyside-tutorial-model-view-programming_22.html
    """
    content = []
    header = []
    accessor = None
    edited = False
    undoStack = QUndoStack()

    def __init__(self, parent, *args):
        QAbstractTableModel.__init__(self, parent, *args)

    def getAccessor(self):
        return self.accessor

    def setAccessor(self, accessor):
        self.accessor = accessor

    def getUndoStack(self):
        return self.undoStack

    def setUndoStack(self, undoStack):
        self.undoStack = undoStack

    def setEdited(self, edited):
        self.edited = edited

    def isEdited(self):
        return self.edited

    def flags(self, index):
        return Qt.ItemIsSelectable | Qt.ItemIsEditable | Qt.ItemIsEnabled

    def setData(self, index, value, role = Qt.EditRole):
        if role == Qt.EditRole:
            self.content[index.row()][index.column()] = value
            QObject.emit(self, SIGNAL("dataChanged(const QModelIndex&, const QModelIndex &)"), index, index)
            self.setEdited(True)
            return True
        return False

    def setHeaderAndContent(self, data):
        if data:
            self.emit(SIGNAL("layoutToBeChanged()"))
            self.content = data[1:len(data)]
            self.header = data[0]
            self.emit(SIGNAL("layoutChanged()"))

    def setContent(self, content):
        self.emit(SIGNAL("layoutToBeChanged()"))
        self.content = content
        self.emit(SIGNAL("layoutChanged()"))

    def getContent(self):
        return self.content

    def getData(self):
        return [self.header] + self.content

    def getHeader(self):
        return self.header

    def setHeader(self, header):
        self.emit(SIGNAL("layoutToBeChanged()"))
        self.header = header
        self.emit(SIGNAL("layoutChanged()"))

    def rowCount(self, parent):
        return len(self.content)

    def columnCount(self, parent):
        return len(self.header)

    def data(self, index, role = Qt.DisplayRole):
        if not index.isValid():
            return None
        elif role != Qt.DisplayRole:
            return None
        try:
            return self.content[index.row()][index.column()]
        except:
            return None


    def insertRows(self, row, parent=None, count=1):
        self.beginInsertRows(QModelIndex(), row, row + count - 1)
        self.content.insert(row, [None] * self.columnCount(None))
        self.endInsertRows()
        self.setEdited(True)

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.header[col]
        return None

    def removeRows(self, position, rows=1, index=QModelIndex()):
        self.beginRemoveRows(QModelIndex(), position, position + rows - 1)
        self.content = self.content[:position] + self.content[position + rows:]
        self.endRemoveRows()
        return True

    def sort(self, col, order):
        """sort table by given column number col"""
        self.emit(SIGNAL("layoutAboutToBeChanged()"))
        self.content = sorted(self.content,key=operator.itemgetter(col))
        if order == Qt.DescendingOrder:
            self.content.reverse()
        self.emit(SIGNAL("layoutChanged()"))
        self.setEdited(True)
