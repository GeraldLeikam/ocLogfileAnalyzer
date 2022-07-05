#!/usr/bin/env python3
from PyQt5 import QtWidgets
import sys
from modules.ui import Ui

if __name__ == '__main__':
    path = __file__.strip(__file__.split('/')[len(__file__.split('/'))-1]) # absolute path
    app = QtWidgets.QApplication(sys.argv)
    try:
        window = Ui(uiTemplate=f'{path}ui/main.ui')
    except:
        path = f'{path}/ocLogfileAnalyzer' # absolute path for appImage
        window = Ui(uiTemplate=f'{path}/ui/main.ui')
    sys.exit(app.exec_())



