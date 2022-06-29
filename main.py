from PyQt5 import QtWidgets
import sys
from modules.dataFromJson import convertDataStrinListFromJson
from modules.ui import Ui

class Main:

    def __init__(self):
        self.app = QtWidgets.QApplication(sys.argv)
        self.window = Ui(uiTemplate='./ui/main.ui')

        sys.exit(self.app.exec_())


Main()