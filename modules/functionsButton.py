from PyQt5.QtWidgets import QPushButton

class ButtonFunctions:

    def __init__(self, ui):
        self.ui = ui

    def deactivate(self, buttonName=None):
        if buttonName is not None:
            self.ui.findChild(QPushButton, buttonName).setDisabled(True)

    def activate(self, buttonName=None):
        if buttonName is not None:
            self.ui.findChild(QPushButton, buttonName).setEnabled(True)

    def addClickedConnection(self, buttonName, connectFunction):
        self.ui.findChild(QPushButton, buttonName).clicked.connect(connectFunction)