#!/usr/bin/env python3
from PyQt5.QtWidgets import QApplication
import sys
from modules.ui import Ui

class Application:

    resultStorage = []

    def __init__(self, uiPath):
        self.getPath()
        #self.createApp(uiPath=uiPath)
        #self.execApp()

    def createApp(self, uiPath):
        self.app = QApplication(sys.argv)
        path = __file__.strip(__file__.split('/')[len(__file__.split('/')) - 1])
        self.window = Ui(uiTemplate=f'{path}ui/main.ui')

    def getPath(self):
        path = __file__.strip(__file__.split('/')[len(__file__.split('/')) - 1])
        print(path)

    def execApp(self):
        sys.exit(self.app.exec_())

if __name__ == '__main__':
    Application(uiPath=None)



