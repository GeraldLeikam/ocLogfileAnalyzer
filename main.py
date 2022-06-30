#!/usr/bin/env python3
from PyQt5 import QtWidgets
import sys
import os
from modules.ui import Ui

if __name__ == '__main__':
    path = __file__.strip(__file__.split('/')[len(__file__.split('/'))-1])
    app = QtWidgets.QApplication(sys.argv)
    try:
        window = Ui(uiTemplate=f'{path}/ui/main.ui')
    except:
        print(path)
        window = Ui(uiTemplate=f'{os.getcwd()}/bin/ocLogfileAnalyzer/ui/main.ui') #used for appImage
    sys.exit(app.exec_())



