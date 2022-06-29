import json

logfile = '../logfiles/owncloud.log'

with open(logfile, 'r') as reader:
    logdata = reader.read()

logdata = logdata.split('\n')
for logline in logdata:
    try:
        logline = json.loads(logline)
        print(logline)
    except:
        pass