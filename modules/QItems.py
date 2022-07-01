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

    def __init__(self, txt='', fontFamily='Ubuntu', fontSize=10, setBold=False, color=QColor(0, 0, 0), fontSet=None, alignment=0, tableField=None):
        super().__init__()
        self.tableField = tableField
        self.txt = txt
        self.stringLength = len(txt)
        self.fontFamily = fontFamily
        self.fontSize = fontSize
        self.setTextAlignment(alignment)
        if fontSet is not None:
            self.font = fontSet
        else:
            self.font = QFont(self.fontFamily, self.fontSize)
        self.font.setBold(setBold)
        #fontMetrics = QFontMetrics(self.font)

        self.setForeground(color)
        self.setFont(self.font)
        self.setText(self.txt)

        #self.itemWidth = fontMetrics.width(self.txt)
        #self.itemHeight = fontMetrics.height()

    def getItemLengthSizeInPixel(self):
        fontMetrics = QFontMetrics(self.font)
        if self.txt == '':
            return fontMetrics.width(self.tableField)
        else:
            return fontMetrics.width(self.txt)
