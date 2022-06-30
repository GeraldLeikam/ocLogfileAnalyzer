#!/usr/bin/env python3
from PyQt5 import QtWidgets
import sys
import os
from modules.ui import Ui

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    try:
        window = Ui(uiTemplate=f'./ui/main.ui')
    except:
        window = Ui(uiTemplate=f'{os.getcwd()}/bin/ocLogfileAnalyzer/ui/main.ui') #used for appImage
    sys.exit(app.exec_())



