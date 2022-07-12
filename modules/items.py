from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.Qt import QColor
from PyQt5.Qt import QFont
from PyQt5.Qt import QFontMetrics


"""
Alignments
0:left 
1:left 
2:right 
3:right 
4:centre
"""

class TabelColumnHeaderItem(QTableWidgetItem):

    text = None

    def __init__(self, txt=None, font=None):
        super().__init__()
        self.text = txt
        self.setText(self.text)
        self.setFont(font)
        self.setTextAlignment(0)

    def getTextLength(self):
        if self.text is not None:
            return len(self.text)
        else:
            return 0

    def getText(self):
        return self.text

    def updateText(self, text=None):
        if text is not None:
            self.setText(text)

class TableItem(QTableWidgetItem):

    def __init__(self, txt='', fontFamily='Ubuntu', fontSize=10, setBold=False, color=QColor(0, 0, 0), alignment=0, tableColumn=None):
        super().__init__()
        self.tableColumn = tableColumn
        self.txt = txt
        self.fontFamily = fontFamily
        self.fontSize = fontSize
        self.setTextAlignment(alignment)

        self.font = QFont(self.fontFamily, self.fontSize)
        self.font.setBold(setBold)

        self.setForeground(color)
        self.setFont(self.font)
        self.setText(self.txt)
