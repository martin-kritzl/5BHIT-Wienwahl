from PySide.QtGui import QApplication, QAction
from UndoRedo import EditCommand


class PasteAction(QAction):
    """ Creates a PasteAction for a single cell
    short cut: Ctrl-V
    Trigger: paste_clipboard_to_cell
    function: Create a EditCommand with the content of the clipboard;
    push the cmd to the undo stack
    """
    def __init__(self, table_view, undoStack):
        self.table_view = table_view
        self.model = table_view.model()
        self.undoStack = undoStack


    def paste_clipboard_to_cell(self):
        if len(self.table_view.selectionModel().selectedIndexes()) > 0:
            # get index of the selected cell
            sys_clip = QApplication.clipboard()
            value = str(sys_clip.text())
            index = self.table_view.selectionModel().selectedIndexes()[0]
            cmd = EditCommand(self.model, index)
            cmd.newValue(value)
            self.undoStack.push(cmd)

    def setModelData(self, editor, model, index):
        """
        put the new edit on the stack. The push method will start the redo()
        :param editor: editor of the item
        :param model: model of the QTableView
        :param index: index of edited field
        :return: None
        """
        newValue = editor.text()
        self.edit.newValue(newValue)
        self.undoStack.push(self.edit)