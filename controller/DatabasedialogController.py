from PySide import QtGui
from PySide.QtGui import QDialog
from gui import DatabaseDialog


class DatabaseDialogController(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.form = DatabaseDialog.Ui_Form()
        self.form.setupUi(self)

        self.form.okOrCancel.button(QtGui.QDialogButtonBox.Ok).clicked.connect(self.ok)
        self.form.okOrCancel.button(QtGui.QDialogButtonBox.Cancel).clicked.connect(self.cancel)

    def setElections(self, elections):
        self.form.elections.clear()
        self.form.elections.addItems(elections)

    def getElection(self):
        return self.form.elections.currentText()

    def cancel(self):
        self.form.elections.setEditText(None)
        self.reject()

    def ok(self):
        self.accept()