#!/usr/bin/env python3
from PyQt5 import QtWidgets
import sys
import os
from modules.ui import Ui

print(os.getcwd())

class Main:

    def __init__(self):
        self.app = QtWidgets.QApplication(sys.argv)
        try:
            self.window = Ui(uiTemplate=f'./ui/main.ui')
        except:
            self.window = Ui(uiTemplate=f'{os.getcwd()}/bin/ocLogfileAnalyzer/ui/main.ui')
        sys.exit(self.app.exec_())

Main()




