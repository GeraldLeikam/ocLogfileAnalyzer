import json

def convertDataStrinListFromJson(dataStringList):
    succeed = []
    failed = []
    for dataString in dataStringList:
        dataString = convertDataStringFromJson(dataString=dataString)
        if type(dataString) == dict:

            succeed.append(splitDateTimeField(dataString=dataString))
        else:
            failed.append(dataString)
    return {'succeeded': succeed, 'failed': failed}

def splitDateTimeField(dataString):
    data = {}
    for key in dataString.keys():
        if key == 'time':
            tempData = dataString[key].split('T')
            data['date'] = tempData[0]
            data['time'] = tempData[1]

        else:
            data[key] = dataString[key]
    return data

def convertDataStringFromJson(dataString):
    try:
        return json.loads(dataString)
    except:
        return dataString

