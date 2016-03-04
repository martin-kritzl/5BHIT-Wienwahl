from enum import Enum
import operator
from PySide.QtCore import *

__author__ = 'mkritzl'

class WienwahlModel(object):
    tables = []
    currentIndexOfTab = 0

    def getTables(self):
        return self.tables

    def setTables(self, tables):
        self.tables = tables

    def addTable(self, table):
        self.tables.append(table)

    def deleteTable(self, index):
        return self.tables.pop(index)

    def getTable(self, index):
        return self.tables[index]

    def getCurrentTable(self):
        if len(self.tables) != 0:
            return self.tables[self.currentIndexOfTab]
        else:
            return None

    def getCurrentIndex(self):
        return self.currentIndexOfTab

    def setCurrentIndex(self, index):
        self.currentIndexOfTab = index

    def setCurrentTable(self, table):
        self.currentIndexOfTab = self.tables.index(table)

    def setCurrentTableAndAdd(self, table):
        self.addTable(table)
        self.setCurrentTable(table)

    def getTableCount(self):
        return len(self.tables)


class TableModel(QAbstractTableModel):
    """
    https://blog.rburchell.com/2010/02/pyside-tutorial-model-view-programming_22.html
    """
    content = []
    header = []
    accessor = None
    edited = False

    def __init__(self, parent,  data, accessor, *args):
        QAbstractTableModel.__init__(self, parent, *args)
        if data:
            self.content = data[1:len(data)]
            self.header = data[0]

        self.accessor = accessor

    def getAccessor(self):
        return self.accessor

    def setAccessor(self, accessor):
        self.accessor = accessor

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

    def setContent(self, content):
        self.content = content

    def getContent(self):
        return self.content

    def getData(self):
        return [self.header] + self.content

    def setHeader(self, header):
        self.header = header

    def rowCount(self, parent):
        return len(self.content)

    def columnCount(self, parent):
        return len(self.header)

    def data(self, index, role):
        if not index.isValid():
            return None
        elif role != Qt.DisplayRole:
            return None
        try:
            return self.content[index.row()][index.column()]
        except:
            return None


    def insertRow(self, row, parent=None, count=1):
        self.beginInsertRows(QModelIndex(), row, row + count - 1)
        self.content.insert(row, [None] * self.columnCount(None))
        self.endInsertRows()
        self.setEdited(True)

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.header[col]
        return None

    def removeRows(self, row, count, parent=QModelIndex):
        self.beginRemoveRows(QModelIndex(), row, row+count-1)
        for i in range(count):
            del self.content[row:row+count]
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


class Accessor(object):

    def __init__(self, access, type):
        self.access = access
        self.type = type

    def getConnectionType(self):
        return self.type

    def getName(self):
        return self.access[self.access.rfind("/")+1:len(self.access)]

    def getAccessString(self):
        return self.access

class ConnectionType(Enum):
    database = 1
    csv = 2


