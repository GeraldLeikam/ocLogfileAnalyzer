from PyQt5.QtWidgets import QComboBox

class ComboBoxFunctions:

    def __init__(self, ui):
        self.ui = ui

    def clear(self, comboBoxName):
        self.ui.findChild(QComboBox, comboBoxName).clear()

    def addItems(self, comboBoxName, items):
        self.ui.findChild(QComboBox, comboBoxName).addItems(items)

    def getSelectedItemText(self, comboBoxName):
        return self.ui.findChild(QComboBox, comboBoxName).currentText()

    def getItemText(self, comboBoxName, itemIndex):
        return self.ui.findChild(QComboBox, comboBoxName).itemText(itemIndex)

    def setPreSelectedItem(self, comboBoxName, itemIndex):
        self.ui.findChild(QComboBox, comboBoxName).setCurrentText(self.getItemText(comboBoxName=comboBoxName, itemIndex=itemIndex))