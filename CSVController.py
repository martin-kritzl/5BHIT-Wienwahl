import sys
import CSVView, CSVModel
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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    c = MyController()
    c.show()
    sys.exit(app.exec_())