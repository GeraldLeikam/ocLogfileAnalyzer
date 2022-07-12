from PyQt5.QtWidgets import QTableWidget

class ColumnFunctions:

    def __init__(self, ui):
        self.ui = ui

    def hide(self, tableName, column):
        self.ui.findChild(QTableWidget, tableName).setColumnHidden(column, True)

    def show(self, tableName, column):
        self.ui.findChild(QTableWidget, tableName).setColumnHidden(column, False)

    def setCount(self, tableName, count):
        self.ui.findChild(QTableWidget, tableName).setColumnCount(count)

    def setHeaderItem(self, tableName, column, headerItem):
        self.ui.findChild(QTableWidget, tableName).setHorizontalHeaderItem(column, headerItem)

    def getHeaderItemText(self, tableName, column):
        return self.ui.findChild(QTableWidget, tableName).horizontalHeaderItem(column).text()

    def getCount(self, tableName):
        return self.ui.findChild(QTableWidget, tableName).columnCount()

    def setWidth(self, tableName, column, width):
        self.ui.findChild(QTableWidget, tableName).setColumnWidth(column, width)
