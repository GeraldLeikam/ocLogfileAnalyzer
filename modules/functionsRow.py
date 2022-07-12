from PyQt5.QtWidgets import QTableWidget

class RowFunctions:

    def __init__(self, ui):
        self.ui = ui

    def setCount(self, tableName, count):
        self.ui.findChild(QTableWidget, tableName).setRowCount(count)

    def getCount(self, tableName):
        return self.ui.findChild(QTableWidget, tableName).rowCount()

    def add(self, tableName, row, items):
        self.ui.findChild(QTableWidget, tableName).setRowCount(row + 1)
        for item in items:
            self.ui.findChild(QTableWidget, tableName).setItem(row, items.index(item), item)
