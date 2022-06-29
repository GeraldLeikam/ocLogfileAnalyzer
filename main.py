#!/usr/bin/env python3
from PyQt5 import QtWidgets
import sys
import os
from modules.ui import Ui

class Main:

    def __init__(self):
        c_dir = os.getcwd()
        print(c_dir)
        self.app = QtWidgets.QApplication(sys.argv)
        self.window = Ui(uiTemplate=f'{c_dir}/ui/main.ui')

        sys.exit(self.app.exec_())


Main()
