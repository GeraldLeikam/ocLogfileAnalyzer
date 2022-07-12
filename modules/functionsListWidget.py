from PyQt5.QtWidgets import QListWidget

class ListWidgetFunctions:

    def __init__(self, ui):
        self.ui = ui

    def addItem(self, listWidgetName, item):
        self.ui.findChild(QListWidget, listWidgetName).addItem(item)

    def count(self, listWidgetName):
        return self.ui.findChild(QListWidget, listWidgetName).count()

    def selectItem(self, listWidgetName, index):
        self.ui.findChild(QListWidget, listWidgetName).item(index).setSelected(True)

    def getItemText(self, listWidgetName, itemIndex):
        return self.ui.findChild(QListWidget, listWidgetName).item(itemIndex).text()

    def getItemsAsTextList(self, listWidgetName):
        data = []
        for item in range(self.count(listWidgetName=listWidgetName)):
            data.append(self.getItemText(listWidgetName=listWidgetName, itemIndex=item))
        return data


    def getSelectedItemIndex(self, listWidgetName):
        index = self.ui.findChild(QListWidget, listWidgetName).currentRow()
        if index == -1:
            index = 0
        return index

    def removeItem(self, listWidgetName, itemIndex):
        self.ui.findChild(QListWidget, listWidgetName).takeItem(itemIndex)