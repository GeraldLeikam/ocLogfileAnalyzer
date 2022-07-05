from json import loads
from modules.QItems import TableItem

class ocRecord():

    originalString = None
    ID = None
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
        self.originalString = jsonString
        self.parseJsonString(jsonString=jsonString)

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

    def getTableItemObject(self, attribute):
        columnHeader = attribute
        if attribute == 'remoteAddr':
            columnHeader = 'remote Address'
        if attribute == 'reqId':
            columnHeader = 'Request ID'
        return TableItem(txt=getattr(self, attribute), tableColumn=columnHeader)

    def setRecordID(self, ID):
        self.ID = str(ID)

if __name__ == '__main__':
    pass