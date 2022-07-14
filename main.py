#!/usr/bin/env python3
from PyQt5.QtWidgets import QApplication
import sys
from modules.ui import Ui

class Application:

    def __init__(self):
        self.getPath()
        self.createApp()
        self.execApp()

    def createApp(self):
        self.app = QApplication(sys.argv)
        self.window = Ui(uiTemplate=f'{self.getPath()}ui/main.ui')

    def getPath(self):
        path = __file__.strip(__file__.split('/')[len(__file__.split('/')) - 1])
        if '/tmp/' in path:
            path = f'{path[:-1]}ocLogfileAnalyzer/'
        return path

    def execApp(self):
        sys.exit(self.app.exec_())

if __name__ == '__main__':
    Application()



