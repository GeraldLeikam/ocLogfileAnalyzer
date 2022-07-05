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

    def getStringLength(self):
        if self.txt == '':
            return len(self.tableColumn)
        else:
            if len(self.txt) > len(self.tableColumn):
                return len(self.txt)
            else:
                return len(self.tableColumn)

    def getItemLengthSizeInPixel(self):
        fontMetrics = QFontMetrics(self.font)
        if self.txt == '' or self.txt == None:
            return fontMetrics.width(self.tableColumn)
        else:
            if len(self.txt) > len(self.tableColumn):
                return fontMetrics.width(self.txt)
            else:
                return fontMetrics.width(self.tableColumn)