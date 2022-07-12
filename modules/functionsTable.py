from PyQt5.QtWidgets import QTableWidget
from PyQt5.Qt import QItemSelectionModel
from modules.functionsColumn import ColumnFunctions
from modules.functionsRow import RowFunctions

class TableFunctions:

    def __init__(self, ui):
        self.Column = ColumnFunctions(ui=ui)
        self.Row = RowFunctions(ui=ui)
        self.ui = ui

    def clear(self, tableName):
        self.ui.findChild(QTableWidget, tableName).clearContents()
        self.Row.setCount(tableName=tableName, count=0)

    def getSelectedItems(self, tableName):
        return self.ui.findChild(QTableWidget, tableName).selectedIndexes()

    def getItemText(self, tableName, row, column):
        return self.ui.findChild(QTableWidget, tableName).item(row, column).text()

    def deselectRow(self, tableName, row):
        self.ui.findChild(QTableWidget, tableName).selectionModel().clearSelection()
