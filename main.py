#!/usr/bin/env python3
from PyQt5.QtWidgets import QApplication
import sys
from modules.ui import Ui

class Application:

    resultStorage = []

    def __init__(self):
        self.createApp()
        self.execApp()

    def createApp(self):
        self.app = QApplication(sys.argv)
        path = __file__.strip(__file__.split('/')[len(__file__.split('/')) - 1])
        self.window = Ui(uiTemplate=f'{path}ui/main.ui')

    def execApp(self):
        sys.exit(self.app.exec_())

if __name__ == '__main__':
    Application()
    """
    path = __file__.strip(__file__.split('/')[len(__file__.split('/'))-1]) # absolute path
    app = QtWidgets.QApplication(sys.argv)
    try:
        window = Ui(uiTemplate=f'{path}ui/main.ui')
    except:
        path = f'{path}/ocLogfileAnalyzer' # absolute path for appImage
        window = Ui(uiTemplate=f'{path}/ui/main.ui')
    sys.exit(app.exec_())
    """


