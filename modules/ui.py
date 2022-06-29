from PyQt5 import QtWidgets
from modules.QItems import TableItem
from modules.dataFromJson import convertDataStrinListFromJson
from PyQt5.QtWidgets import QFileDialog
from os.path import expanduser
from PyQt5.uic import loadUi



class Ui(QtWidgets.QMainWindow):

    parsedData = None
    title = 'oC 10 Logfile Analyzer'

    def __init__(self, uiTemplate):
        super(Ui, self).__init__() # Call the inherited classes __init__ method
        loadUi(uiTemplate, self) # Load the .ui file
        self.setWindowTitle(f'{self.title}')
        self.tableHeaders = [
            TableItem(txt='Request ID'),
            TableItem(txt='Level'),
            TableItem(txt='Date'),
            TableItem(txt='Time'),
            TableItem(txt='Remote Address'),
            TableItem(txt='User'),
            TableItem(txt='App'),
            TableItem(txt='Method'),
            TableItem(txt='Url'),
            TableItem(txt='Message'),
        ]
        self.setGUIObjects()
        self.show()

    def setGUIObjects(self):
        self.dataTable = self.findChild(QtWidgets.QTableWidget, 'dataTable')
        self.setDataTableHeaders()

        self.openButton = self.findChild(QtWidgets.QPushButton, 'openButton')

        self.requestIdTextEdit = self.findChild(QtWidgets.QTextEdit, 'requestIdTextEdit')
        self.requestIdListView = self.findChild(QtWidgets.QListView, 'requestIdListView')
        self.requestIdAddButton = self.findChild(QtWidgets.QPushButton, 'requestIdAddButton')
        self.requestIdRemoveButton = self.findChild(QtWidgets.QPushButton, 'requestIdRemoveButton')

        self.levelAddButton = self.findChild(QtWidgets.QPushButton, 'levelAddButton')
        self.levelRemoveButton = self.findChild(QtWidgets.QPushButton, 'levelRemoveButton')
        self.levelComboBox = self.findChild(QtWidgets.QComboBox, 'levelComboBox')
        self.levelListView = self.findChild(QtWidgets.QListView, 'levelListView')

        self.userAddButton = self.findChild(QtWidgets.QPushButton, 'userAddButton')
        self.userRemoveButton = self.findChild(QtWidgets.QPushButton, 'userRemoveButton')
        self.userTextEdit = self.findChild(QtWidgets.QTextEdit, 'userTextEdit')
        self.userListView = self.findChild(QtWidgets.QListView, 'userListView')

        self.appAddButton = self.findChild(QtWidgets.QPushButton, 'appAddButton')
        self.appRemoveButton = self.findChild(QtWidgets.QPushButton, 'appRemoveButton')
        self.appAddTextEdit = self.findChild(QtWidgets.QTextEdit, 'appAddTextEdit')
        self.appsListView = self.findChild(QtWidgets.QListView, 'appsListView')

        self.methodAddButton = self.findChild(QtWidgets.QPushButton, 'methodAddButton')
        self.methodRemoveButton = self.findChild(QtWidgets.QPushButton, 'methodRemoveButton')
        self.methodComboBox = self.findChild(QtWidgets.QComboBox, 'methodComboBox')
        self.methodListView = self.findChild(QtWidgets.QListView, 'methodListView')

        self.filterButton = self.findChild(QtWidgets.QPushButton, 'filterButton')

        self.rowsCountLabel = self.findChild(QtWidgets.QLabel, 'rowsCountLabel')

        self.openButton.clicked.connect(self.openButtonFunction)
        self.requestIdAddButton.clicked.connect(self.requestIdAddButtonFunction)
        self.requestIdRemoveButton.clicked.connect(self.requestIdRemoveButtonFunction)
        self.levelAddButton.clicked.connect(self.levelAddButtonFunction)
        self.levelRemoveButton.clicked.connect(self.levelRemoveButtonFunction)
        self.userAddButton.clicked.connect(self.userAddButtonFunction)
        self.userRemoveButton.clicked.connect(self.userRemoveButtonFunction)
        self.appAddButton.clicked.connect(self.appAddButtonFunction)
        self.appRemoveButton.clicked.connect(self.appRemoveButtonFunction)
        self.methodAddButton.clicked.connect(self.methodAddButtonFunction)
        self.methodRemoveButton.clicked.connect(self.methodRemoveButtonFunction)
        self.filterButton.clicked.connect(self.filterButtonFunction)

    def openButtonFunction(self):
        fileName = QFileDialog.getOpenFileName(self, 'Select LogFile to load', expanduser('~'))[0]
        if fileName != '':
            self.setWindowTitle(f'{self.title} - {fileName}')
            fileData = self.readFile(fileName=fileName)
            self.parsedData = self.parseData(data=fileData)

            self.loadData(self.parsedData['succeeded'])

    def requestIdAddButtonFunction(self):
        requestID = self.requestIdTextEdit.toPlainText()
        if requestID != '':
            found = False
            for i in range(0, self.requestIdListView.count()):
                if self.requestIdListView.item(i).text().lower() == requestID.lower():
                    found = True
                    break
            if found != True:
                self.requestIdListView.addItem(requestID)
        self.requestIdTextEdit.setText('')

    def requestIdRemoveButtonFunction(self):
        index = self.requestIdListView.currentRow()
        self.requestIdListView.takeItem(index)

    def levelAddButtonFunction(self):
        level = self.levelComboBox.currentText()
        found = False
        for i in range(0, self.levelListView.count()):
            if self.levelListView.item(i).text().lower() == level.lower():
                found = True
                break
        if found != True:
            self.levelListView.addItem(level)
        self.levelComboBox.setCurrentText('0')

    def levelRemoveButtonFunction(self):
        index = self.levelListView.currentRow()
        self.levelListView.takeItem(index)

    def userAddButtonFunction(self):
        userName = self.userTextEdit.toPlainText()
        if userName != '':
            found = False
            for i in range(0, self.userListView.count()):
                if self.userListView.item(i).text().lower() == userName.lower():
                    found = True
                    break
            if found != True:
                self.userListView.addItem(userName)
        self.userTextEdit.setText('')

    def userRemoveButtonFunction(self):
        index = self.userListView.currentRow()
        self.userListView.takeItem(index)

    def appAddButtonFunction(self):
        appName = self.appAddTextEdit.toPlainText()
        if appName != '':
            found = False
            for i in range(0, self.appsListView.count()):
                if self.appsListView.item(i).text().lower() == appName.lower():
                    found = True
                    break
            if found != True:
                self.appsListView.addItem(appName)
        self.appAddTextEdit.setText('')

    def appRemoveButtonFunction(self):
        index = self.appsListView.currentRow()
        self.appsListView.takeItem(index)

    def methodAddButtonFunction(self):
        method = self.methodComboBox.currentText()
        found = False
        for i in range(0, self.methodListView.count()):
            if self.methodListView.item(i).text().lower() == method.lower():
                found = True
                break
        if found != True:
            self.methodListView.addItem(method)
        self.methodComboBox.setCurrentText('POST')

    def methodRemoveButtonFunction(self):
        index = self.methodListView.currentRow()
        self.methodListView.takeItem(index)

    def filterButtonFunction(self):
        if self.parsedData != None:
            dataList = self.parsedData['succeeded']

            requestIdToFilter = []
            for i in range(0, self.requestIdListView.count()):
                requestIdToFilter.append(self.requestIdListView.item(i).text())

            levelToFilter = []
            for i in range(0, self.levelListView.count()):
                levelToFilter.append(self.levelListView.item(i).text())

            userToFilter = []
            for i in range(0, self.userListView.count()):
                userToFilter.append(self.userListView.item(i).text())

            appsToFilter = []
            for i in range(0, self.appsListView.count()):
                appsToFilter.append(self.appsListView.item(i).text())

            methodsToFilter = []
            for i in range(0, self.methodListView.count()):
                methodsToFilter.append(self.methodListView.item(i).text())

            templist = []
            if len(userToFilter) > 0:
                for data in dataList:
                    for user in userToFilter:
                        if str(data['user']).lower() == str(user).lower():
                            templist.append(data)
                dataList = templist

            templist =[]
            if len(requestIdToFilter) > 0:
                for data in dataList:
                    for id in requestIdToFilter:
                        if str(data['reqId']).lower() == str(id).lower():
                            templist.append(data)
                dataList = templist

            templist = []
            if len(levelToFilter) > 0:
                for data in dataList:
                    for level in levelToFilter:
                        if str(data['level']).lower() == str(level).lower():
                            templist.append(data)
                dataList = templist

            tempList = []
            if len(appsToFilter) > 0:
                for data in dataList:
                    for appName in appsToFilter:
                        if data['app'].lower() == appName.lower():
                            tempList.append(data)
                dataList = tempList

            tempList = []
            if len(methodsToFilter) > 0:
                for data in dataList:
                    for method in methodsToFilter:
                        if data['method'].lower() == method.lower():
                            tempList.append(data)
                dataList = tempList

            self.loadData(dataList)


    def readFile(self, fileName):
        try:
            with open(fileName, 'r') as reader:
                return reader.read().split('\n')
        except:
            print('can not read file: ' + fileName)
            return None

    def parseData(self, data):
        try:
            return convertDataStrinListFromJson(data)
        except:
            print('cannot parse data from json')
            return None

    def setDataTableHeaders(self):
        for i in range(0, len(self.tableHeaders)):
            self.dataTable.setHorizontalHeaderItem(i, self.tableHeaders[i])
            self.dataTable.setColumnWidth(i, self.tableHeaders[i].getItemLengthSizeInPixel() + 10)

    def loadData(self, dataList):
        self.setDataTableHeaders()

        row = 0

        requestIdColumnWidth = 0
        levelColumnWidth = 15
        dateColumnWidth = 0
        timeColumnWidth = 0
        remoteAddressColumnWidth = 0
        userColumnWidth = 0
        appColumnWidth = 0
        methodColumnWidth = 0
        urlColumnWidth = 0
        messageColumnWidth = 0

        requestIdColumnWidthObject = TableItem(tableField='Request ID',)
        dateColumnWidthObject = TableItem(tableField='Date')
        timeColumnWidthObject = TableItem(tableField='Time')
        remoteAddressColumnWidthObject = TableItem(tableField='Remote Address')
        userColumnWidthObject = TableItem(tableField='User')
        appColumnWidthObject = TableItem(tableField='App')
        methodColumnWidthObject = TableItem(tableField='Method')
        urlColumnWidthObject = TableItem(tableField='Url')
        messageColumnWidthObject = TableItem(tableField='Message')

        self.dataTable.setRowCount(len(dataList))
        for data in dataList:

            reqId = TableItem(txt=str(data['reqId']), tableField='Request Id')
            level = TableItem(txt=str(data['level']), tableField='Level')
            date = TableItem(txt=str(data['date']), tableField='Date')
            time = TableItem(txt=str(data['time']), tableField='Time')
            remoteAddr = TableItem(txt=str(data['remoteAddr']), tableField='Remote Address')
            user = TableItem(txt=str(data['user']), tableField='User')
            app = TableItem(txt=str(data['app']), tableField='App')
            method = TableItem(txt=str(data['method']), tableField='Method')
            url = TableItem(txt=str(data['url']).strip(' '), tableField='Url')
            message = TableItem(txt=str(data['message']), tableField='Message')

            self.dataTable.setItem(row, 0, reqId)
            self.dataTable.setItem(row, 1, level)
            self.dataTable.setItem(row, 2, date)
            self.dataTable.setItem(row, 3, time)
            self.dataTable.setItem(row, 4, remoteAddr)
            self.dataTable.setItem(row, 5, user)
            self.dataTable.setItem(row, 6, app)
            self.dataTable.setItem(row, 7, method)
            self.dataTable.setItem(row, 8, url)
            self.dataTable.setItem(row, 9, message)

            if reqId.stringLength > requestIdColumnWidth:
                requestIdColumnWidth = reqId.stringLength
                requestIdColumnWidthObject = reqId

            if date.stringLength > dateColumnWidth:
                dateColumnWidth = date.stringLength
                dateColumnWidthObject = date

            if time.stringLength > timeColumnWidth:
                timeColumnWidth = time.stringLength
                timeColumnWidthObject = time

            if remoteAddr.stringLength > remoteAddressColumnWidth:
                remoteAddressColumnWidth = remoteAddr.stringLength
                remoteAddressColumnWidthObject = remoteAddr

            if user.stringLength > userColumnWidth:
                userColumnWidth = user.stringLength
                userColumnWidthObject = user

            if app.stringLength > appColumnWidth:
                appColumnWidth = app.stringLength
                appColumnWidthObject = app

            if method.stringLength > methodColumnWidth:
                methodColumnWidth = method.stringLength
                methodColumnWidthObject = method

            if url.stringLength > urlColumnWidth:
                urlColumnWidth = url.stringLength
                urlColumnWidthObject = url

            if message.stringLength > messageColumnWidth:
                messageColumnWidth = message.stringLength
                messageColumnWidthObject = message

            row += 1

        self.dataTable.setColumnWidth(0, requestIdColumnWidthObject.getItemLengthSizeInPixel() + 10)  # Set the width of the reqId column
        self.dataTable.setColumnWidth(1, levelColumnWidth)  # Set the width of the level column
        self.dataTable.setColumnWidth(2, dateColumnWidthObject.getItemLengthSizeInPixel() + 10)  # Set the width of the date column
        self.dataTable.setColumnWidth(3, timeColumnWidthObject.getItemLengthSizeInPixel() + 10)  # Set the width of the time column
        self.dataTable.setColumnWidth(4, remoteAddressColumnWidthObject.getItemLengthSizeInPixel() + 10)  # Set the width of the remoteAddress column
        self.dataTable.setColumnWidth(5, userColumnWidthObject.getItemLengthSizeInPixel() + 10)  # Set the width of the user column
        self.dataTable.setColumnWidth(6, appColumnWidthObject.getItemLengthSizeInPixel() + 10)  # Set the width of the app column
        self.dataTable.setColumnWidth(7, methodColumnWidthObject.getItemLengthSizeInPixel() + 10)  # Set the width of the method column
        self.dataTable.setColumnWidth(8, urlColumnWidthObject.getItemLengthSizeInPixel() + 10)  # Set the width of the url column
        self.dataTable.setColumnWidth(9, messageColumnWidthObject.getItemLengthSizeInPixel() + 10)  # Set the width of the message column

        self.rowsCountLabel.setText(f'Rows: {len(dataList)}')


