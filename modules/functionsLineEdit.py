from PyQt5.QtWidgets import QLineEdit

class LineEditFunctions:

    def __init__(self, ui):
        self.ui = ui

    def getText(self, lineEditName):
        return self.ui.findChild(QLineEdit, lineEditName).text()

    def clear(self, lineEditName):
        self.ui.findChild(QLineEdit, lineEditName).clear()