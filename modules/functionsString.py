from PyQt5.Qt import QFontMetrics

class StringFunctions:

    def __init__(self, font):
        self.fontMetrics = QFontMetrics(font)

    def pixelWidth(self, txt):
        return self.fontMetrics.width(txt)

    def pixelHeight(self, txt):
        return self.fontMetrics.height(txt)
