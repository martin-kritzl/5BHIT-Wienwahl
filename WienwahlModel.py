import operator
from PySide import QtCore, QtGui
from PySide.QtGui import *
from PySide.QtCore import *

__author__ = 'mkritzl'

from PySide.QtGui import *

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
        tmp = self.currentIndexOfTab
        return self.tables[self.currentIndexOfTab]

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

    def __init__(self, parent,  data, accessor, *args):
        QAbstractTableModel.__init__(self, parent, *args)
        if data:
            self.content = data[1:len(data)]
            self.header = data[0]

        # self.header = ["abc", "def"]
        # self.content = [[QtGui.QTableWidgetItem("ghi"), QtGui.QTableWidgetItem("jkl")]]

        self.accessor = accessor

    def getAccessor(self):
        return self.accessor

    def flags(self, index):
        return Qt.ItemIsSelectable | Qt.ItemIsEditable | Qt.ItemIsEnabled

    # def setData(self, data):
    #     self.setHeader(data[0])
    #     self.setContent(data[1:len(data)])

    def setData(self, index, value, role = Qt.EditRole):
        if role == Qt.EditRole:
            self.content[index.row()][index.column()] = value
            QObject.emit(self, SIGNAL("dataChanged(const QModelIndex&, const QModelIndex &)"), index, index)
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
        return self.content[index.row()][index.column()]

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.header[col]
        return None

    def sort(self, col, order):
        """sort table by given column number col"""
        self.emit(SIGNAL("layoutAboutToBeChanged()"))
        self.content = sorted(self.content,key=operator.itemgetter(col))
        if order == Qt.DescendingOrder:
            self.content.reverse()
        self.emit(SIGNAL("layoutChanged()"))


class Accessor(object):

    def __init__(self, access):
        self.access = access

    def getName(self):
        return self.access[self.access.rfind("/")+1:len(self.access)]

    def getAccessString(self):
        return self.access

