#!/usr/bin/env python3
from PyQt5 import QtWidgets
import sys
import os
from modules.ui import Ui

def find(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)

print(find('main.ui', '/'))

class Main:

    def __init__(self):
        appImagePath = 'usr/bin'
        self.app = QtWidgets.QApplication(sys.argv)
        self.window = Ui(uiTemplate=f'{appImagePath}/ui/main.ui')

        sys.exit(self.app.exec_())



