from modules.QItems import TableItem
from PyQt5.Qt import QColor
from PyQt5.Qt import QFont

class LogLineObject:

    fontFamily = 'Ubuntu'
    fontSize = 10,

    def __init__(
            self,
            requestID=None,
            level=None,
            date=None,
            time=None,
            remoteAddress=None,
            user=None,
            app=None,
            method=None,
            url=None,
            message=None):

        self.requestID = TableItem(txt=requestID, fontSet=QFont(self.fontFamily, self.fontSize))
        self.level = TableItem(txt=level, fontSet=QFont(self.fontFamily, self.fontSize))
        self.date = TableItem(txt=date, fontSet=QFont(self.fontFamily, self.fontSize))
        self.time = TableItem(txt=time, fontSet=QFont(self.fontFamily, self.fontSize))
        self.remoteAddress = TableItem(txt=remoteAddress, fontSet=QFont(self.fontFamily, self.fontSize))
        self.user = TableItem(txt=user, fontSet=QFont(self.fontFamily, self.fontSize))
        self.app = TableItem(txt=app, fontSet=QFont(self.fontFamily, self.fontSize))
        self.method = TableItem(txt=method, fontSet=QFont(self.fontFamily, self.fontSize))
        self.url = TableItem(txt=url, fontSet=QFont(self.fontFamily, self.fontSize))
        self.message = TableItem(txt=message, fontSet=QFont(self.fontFamily, self.fontSize))

        def compareValues(self, value1, value2):
            pass