from PyQt5.QtWidgets import QTableWidgetItem
from json import loads
import hashlib
from time import time

class ocRecord():

    originalString = None
    recordId = None
    reqId = None
    level = None
    date = None
    time = None
    remoteAddr = None
    user = None
    app = None
    method = None
    url = None
    message = None
    parseSuccess = False

    def __init__(self, jsonString):

        self.originalString = jsonString.strip('\n')
        self.parseJsonString(jsonString=jsonString)
        self.setRecordID()

    def parseJsonString(self, jsonString):
        try:
            jsonString = loads(jsonString)
            for key in jsonString:
                setattr(self, key, str(jsonString[key]))
            self.date, self.time = self.time.split('T')
            self.parseSuccess = True
        except Exception as e:
            print(e)

    def getStringLength(self, attribute):
        return len(getattr(self, attribute))

    def getString(self, attribute):
        return getattr(self, attribute)

    def getTableItemObject(self, attribute):
        item = QTableWidgetItem()
        item.setText(getattr(self, attribute))
        return item


    def setRecordID(self, recordId=None):
        if recordId != None:
            self.recordId = str(recordId)
        else:
            idString = f'{time()}{self.originalString}{self.reqId}{self.level}{self.date}{self.time}{self.remoteAddr}{self.user}{self.app}{self.method}{self.url}{self.message}'
            self.recordId = idString = hashlib.md5(idString.encode('utf-8')).hexdigest()


if __name__ == '__main__':
    pass
