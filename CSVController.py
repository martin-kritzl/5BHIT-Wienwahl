import sys
import collections
from itertools import islice
import CSVView, CSVModel
from PySide.QtCore import *
from PySide.QtGui import *
import csv


class MyController(QWidget):
    def __init__(self, parent=None):

        super().__init__(parent)
        self.form = CSVView.Ui_Form()
        self.form.setupUi(self)
        self.model = CSVModel.CSVModel()
        self.readCSV()
        self.form.textarea.setText(self.model.csv_text)

    def readCSV(self):
        with open('data.csv', newline='') as csvfile:
            file = csv.reader(csvfile, delimiter=';')
            for row in file:
                self.model.csv_text = self.model.csv_text + ';'.join(row) + '\r\n'


class CSVHandler(object):

    def __init__(self, file):
        self.file = file

    def getContentAsArray(self):
        with open(self.file, newline='') as csvfile:
            rows = []
            file = csv.reader(csvfile, delimiter=';')
            for row in file:
                rows.append(row)
            return rows

    def getContentAsString(self):
        output = ""
        rows = self.getContentAsArray()
        for row in rows:
            output = output + ';'.join(row) + '\r\n'

        return output

    def getLineAsArray(self, linenumber):
        linenumber = linenumber - 1
        with open(self.file, newline='') as csvfile:
            file = csv.reader(csvfile, delimiter=';')
            if linenumber is None:
                collections.deque(file, maxlen=0)
            else:
                next(islice(file, linenumber, linenumber), None)

            return next(file)

    def getLineAsString(self, linenumber):
        linenumber = linenumber - 1
        with open(self.file, newline='') as csvfile:
            file = csv.reader(csvfile, delimiter=';')
            if linenumber is None:
                collections.deque(file, maxlen=0)
            else:
                next(islice(file, linenumber, linenumber), None)


            tmp = next(file)
            return ';'.join(tmp)

    def clearFile(self, fromFile, toFile):
        with open(fromFile, newline='') as csvSource, open(toFile, "w", newline='') as csvDest:
            reader = csv.reader(csvSource, delimiter=';')
            writer = csv.writer(csvDest, delimiter=';')

            for row in reader:
                writer.writerow(row[0:len(row)-1])

    def setContent(self, content):
        with open(self.file, "w", newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=';')
            csvfile.truncate()

            if isinstance(content, list):
                for row in content:
                    writer.writerow(row)
            elif type(content) is str:
                writer.writerow(content.split(";"))

    def appendLine(self, row):
        with open(self.file, "a", newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=';')

            if isinstance(row, list):
                writer.writerow(row)
            elif type(row) is str:
                writer.writerow(row.split(";"))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    c = MyController()
    c.show()
    sys.exit(app.exec_())