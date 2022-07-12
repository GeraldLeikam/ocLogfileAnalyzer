from PyQt5.QtWidgets import QLabel
from modules.functionsString import StringFunctions

class LabelFunctions:

    def __init__(self, ui):
        self.String = StringFunctions(font=ui.font())
        self.ui = ui

    def setText(self, labelName, text, resizeWidth=False, resizeHeight=False):
        self.ui.findChild(QLabel, labelName).setText(text)
        if resizeWidth:
            self.setWidth(labelName=labelName, width=self.String.pixelWidth(txt=text))
        if resizeHeight:
            self.setHeight(labelName=labelName, height=self.String.pixelHeight(txt=text))

    def setWidth(self, labelName, width):
        self.ui.findChild(QLabel, labelName).resize(width, self.ui.findChild(QLabel, labelName).height())

    def setHeight(self, labelName, height):
        self.ui.findChild(QLabel, labelName).resize(self.ui.findChild(QLabel, labelName).width(), height)