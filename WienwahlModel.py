import operator
from PySide import QtCore
from PySide.QtGui import *
from PySide.QtCore import *

__author__ = 'mkritzl'

from PySide.QtGui import *

class WienwahlModel(object):
    pass


class TableModel(QAbstractTableModel):
    content = None
    header = None
    currentFile = None

    def __init__(self, parent, content, header, *args):
        QAbstractTableModel.__init__(self, parent, *args)
        self.content = content
        self.header = header

    def setData(self, data):
        self.setHeader(data[0])
        self.setContent(data[1:len(data)])

    def setContent(self, content):
        self.content = content

    def getData(self):
        return self.header + self.content

    def setHeader(self, header):
        self.header = header

    def rowCount(self, parent):
        return len(self.content)

    def columnCount(self, parent):
        return len(self.content[0])

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

