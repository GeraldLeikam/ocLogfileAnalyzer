from modules.ocRecordObject import ocRecord
from PyQt5.Qt import QFont
from PyQt5.Qt import QFontMetrics

def setUITitle(uiElement, title):
    uiElement.setWindowTitle(title)

def getLengthInPixels(fontFamily='Ubuntu', fontSize=10, txt=None):
    if txt is not None:
        #fontMetrics = QFontMetrics(QFont(fontFamily, fontSize))
        #return fontMetrics.width(txt)
        return QFontMetrics(QFont(fontFamily, fontSize)).width(txt)


def readFile(file):
    try:
        with open(file, 'r') as reader:
            return reader.read().split('\n')
    except:
        print('can not read file: ' + file)
        return None

def createRecordList(data):
    dataList = []
    idCount = 0
    for line in data:
        dataRecord = ocRecord(line)
        dataRecord.setRecordID(idCount)
        dataList.append(dataRecord)
        idCount += 1
    return dataList

def filter(data, filterCriterias):
    dataList = data
    for filter in filterCriterias:
        if filterCriterias[filter] is not None and len(filterCriterias[filter]) > 0:
            tempData = []
            print('filter -> ' + filter)
            for row in range(0 , len(dataList)):
                for criteria in filterCriterias[filter]:
                    if dataList[row].__getattribute__(filter).lower() == criteria.lower():
                        tempData.append(dataList[row])
            dataList = tempData
    return dataList