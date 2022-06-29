#!/usr/bin/env python3
from PyQt5 import QtWidgets
import sys
import os
from modules.ui import Ui


def find_all(name, path):
    result = []
    for root, dirs, files in os.walk(path):
        if name in files:
            result.append(os.path.join(root, name))
    return result

for line in find_all('main.ui', '/'):
    print(line)

print('================================================================')
print(os.getcwd())

class Main:

    def __init__(self):
        appImagePath = '/tmp/.mount_PythonFsLV00/usr/bin'
        self.app = QtWidgets.QApplication(sys.argv)
        self.window = Ui(uiTemplate=f'{appImagePath}/ui/main.ui')

        sys.exit(self.app.exec_())



