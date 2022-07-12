from PyQt5.QtWidgets import QFileDialog
from os.path import expanduser

class FileDialogFunctions:

    def __init__(self, ui):
        self.ui = ui

    def getSingleFileFileDialog(self):
        return QFileDialog.getOpenFileName(self.ui, 'Select LogFile to load', expanduser('~'))[0]

    def getSaveFileDialog(self):
        return QFileDialog.getSaveFileName(self.ui, 'Select LogFile to save', expanduser('~'))[0]
