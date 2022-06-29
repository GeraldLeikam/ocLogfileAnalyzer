#!/usr/bin/env python3
from PyQt5 import QtWidgets
import sys
import os
from modules.ui import Ui

class Main:

    def __init__(self):
        appImagePath = 'usr/bin'
        self.app = QtWidgets.QApplication(sys.argv)
        self.window = Ui(uiTemplate=f'{appImagePath}/ui/main.ui')

        sys.exit(self.app.exec_())


Main()
