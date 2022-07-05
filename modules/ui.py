from PyQt5 import QtWidgets
from PyQt5 import QtCore
from modules.QItems import TableItem
from PyQt5.QtWidgets import QFileDialog
from os.path import expanduser
from PyQt5.uic import loadUi
from modules.uiFunctions import setUITitle
from modules.uiFunctions import readFile
from modules.uiFunctions import createRecordList
from modules.uiFunctions import filter
from modules.uiFunctions import getLengthInPixels
from threading import Thread

class Ui(QtWidgets.QMainWindow):

    parsedData = None
    title = 'oC 10 Logfile Analyzer'

    columnHeaders = [
        TableItem(txt='ID', tableColumn='ID'),
        TableItem(txt='Request ID', tableColumn='Request ID'),
        TableItem(txt='Level', tableColumn='Level'),
        TableItem(txt='Date', tableColumn='Date'),
        TableItem(txt='Time', tableColumn='Time'),
        TableItem(txt='Remote Address', tableColumn='Remote Address'),
        TableItem(txt='User', tableColumn='User'),
        TableItem(txt='App', tableColumn='App'),
        TableItem(txt='Method', tableColumn='Method'),
        TableItem(txt='URL', tableColumn='URL'),
        TableItem(txt='Message', tableColumn='Message'),
    ]

    def __init__(self, uiTemplate):
        super(Ui, self).__init__() # Call the inherited classes __init__ method
        loadUi(uiTemplate, self) # Load the .ui file
        setUITitle(uiElement=self, title=f'{self.title}')
        self.setGUIObjects()
        self.configureTableWidget()
        self.setLabelText(labelName='rowsCompleteCountLabel', text=f'rows complete: 0')
        self.setLabelText(labelName='rowsAffectedCountLabel', text=f'rows affected by filter: 0')

        self.show()

    def setGUIObjects(self):
        self.dataTable = self.findChild(QtWidgets.QTableWidget, 'dataTable')

        self.uiFilterListViews = {
            'reqId': self.findChild(QtWidgets.QListView, 'requestIdListView'),
            'level': self.findChild(QtWidgets.QListView, 'levelListView'),
            'user': self.findChild(QtWidgets.QListView, 'userListView'),
            'app': self.findChild(QtWidgets.QListView, 'appsListView'),
            'method': self.findChild(QtWidgets.QListView, 'methodListView'),
        }
        self.uiFilterLineEdits = {
            'reqId': self.findChild(QtWidgets.QLineEdit, 'reqIdLineEdit'),
            'user': self.findChild(QtWidgets.QLineEdit, 'userLineEdit'),
            'app': self.findChild(QtWidgets.QLineEdit, 'appLineEdit')
        }
        self.uiFilterComboBoxes = {
            'level': self.findChild(QtWidgets.QComboBox, 'levelComboBox'),
            'method': self.findChild(QtWidgets.QComboBox, 'methodComboBox')
        }
        self.uiFilterAddButtons = {
            'reqId': self.findChild(QtWidgets.QPushButton, 'requestIdAddButton'),
            'level': self.findChild(QtWidgets.QPushButton, 'levelAddButton'),
            'user': self.findChild(QtWidgets.QPushButton, 'userAddButton'),
            'app': self.findChild(QtWidgets.QPushButton, 'appAddButton'),
            'method': self.findChild(QtWidgets.QPushButton, 'methodAddButton'),
        }
        self.uiFilterRemoveButtons = {
            'reqId': self.findChild(QtWidgets.QPushButton, 'requestIdRemoveButton'),
            'level': self.findChild(QtWidgets.QPushButton, 'levelRemoveButton'),
            'user': self.findChild(QtWidgets.QPushButton, 'userRemoveButton'),
            'app': self.findChild(QtWidgets.QPushButton, 'appRemoveButton'),
            'method': self.findChild(QtWidgets.QPushButton, 'methodRemoveButton')
        }
        self.uiLabels = {
            'rowsCompleteCountLabel': self.findChild(QtWidgets.QLabel, 'rowsCompleteCountLabel'),
            'rowsAffectedCountLabel': self.findChild(QtWidgets.QLabel, 'rowsAffectedCountLabel')
        }
        self.openButton = self.findChild(QtWidgets.QPushButton, 'openButton')

        self.filterButton = self.findChild(QtWidgets.QPushButton, 'filterButton')
        self.filterButton.setDisabled(True)

        self.openButton.clicked.connect(self.openButtonFunction)

        self.uiFilterAddButtons['reqId'].clicked.connect(lambda: self.addButtonFunction(filter='reqId'))
        self.uiFilterAddButtons['level'].clicked.connect(lambda: self.addButtonFunction(filter='level'))
        self.uiFilterAddButtons['user'].clicked.connect(lambda: self.addButtonFunction(filter='user'))
        self.uiFilterAddButtons['app'].clicked.connect(lambda: self.addButtonFunction(filter='app'))
        self.uiFilterAddButtons['method'].clicked.connect(lambda: self.addButtonFunction(filter='method'))

        self.uiFilterRemoveButtons['reqId'].clicked.connect(lambda: self.removeButtonFunction(filter='reqId'))
        self.uiFilterRemoveButtons['level'].clicked.connect(lambda: self.removeButtonFunction(filter='level'))
        self.uiFilterRemoveButtons['user'].clicked.connect(lambda: self.removeButtonFunction(filter='user'))
        self.uiFilterRemoveButtons['app'].clicked.connect(lambda: self.removeButtonFunction(filter='app'))
        self.uiFilterRemoveButtons['method'].clicked.connect(lambda: self.removeButtonFunction(filter='method'))

        self.uiFilterLineEdits['reqId'].installEventFilter(self)
        self.uiFilterLineEdits['user'].installEventFilter(self)
        self.uiFilterLineEdits['app'].installEventFilter(self)

        self.filterButton.clicked.connect(self.filterButtonFunction)

    def setLabelText(self, labelName, text):
        self.uiLabels[labelName].setText(text)
        self.uiLabels[labelName].resize(getLengthInPixels(txt=text), self.uiLabels[labelName].height())

    def configureTableWidget(self):
        self.dataTable.clearContents()
        self.dataTable.setColumnCount(len(self.columnHeaders))
        for column in range(0, len(self.columnHeaders)):
            self.dataTable.setHorizontalHeaderItem(column, self.columnHeaders[column])
            self.dataTable.setColumnWidth(column, self.columnHeaders[column].getItemLengthSizeInPixel() + 20)
        self.dataTable.setColumnHidden(0, True)

    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.KeyPress:
            if event.key() == QtCore.Qt.Key_Return or event.key() == QtCore.Qt.Key_Enter:
                if 'LineEdit' in obj.objectName():
                    self.addButtonFunction(filter=obj.objectName().replace('LineEdit', ''))
        return super().eventFilter(obj, event)

    def openButtonFunction(self):
        self.filterButton.setDisabled(True)
        file = QFileDialog.getOpenFileName(self, 'Select LogFile to load', expanduser('~'))[0]
        if file != '':
            setUITitle(self, f'{self.title} - {file}')
            data = readFile(file=file)
            self.dataGood = []
            self.dataFailed = []
            if data is not None:
                for data in createRecordList(data):
                    if data.parseSuccess:
                        self.dataGood.append(data)
                    else:
                        self.dataFailed.append(data)
            self.setLevelFilterItems()
            self.setMethodFilterItems()
            self.setLabelText(labelName='rowsCompleteCountLabel', text=f'rows complete: {len(self.dataGood)}')
            Thread(target=self.loadData, args=(self.dataGood, )).start()

    def setLevelFilterItems(self):
        levels = []
        for line in self.dataGood:
            if line.level not in levels:
                levels.append(line.level)
                levels.sort()
        self.uiFilterComboBoxes['level'].clear()
        self.uiFilterComboBoxes['level'].addItems(levels)

    def setMethodFilterItems(self):
        methods = []
        for line in self.dataGood:
            if line.method not in methods:
                methods.append(line.method)
                methods.sort()
        self.uiFilterComboBoxes['method'].clear()
        self.uiFilterComboBoxes['method'].addItems(methods)

    def addButtonFunction(self, filter=None):
        filterCriteria = None
        if filter in self.uiFilterLineEdits.keys():
            filterCriteria = self.uiFilterLineEdits[filter].text()
            self.uiFilterLineEdits[filter].clear()
        if filter in self.uiFilterComboBoxes.keys():
            filterCriteria = self.uiFilterComboBoxes[filter].currentText()
            self.uiFilterComboBoxes[filter].setCurrentText(self.uiFilterComboBoxes[filter].itemText(0))
        if filterCriteria != '':
            found = False
            for i in range(0, self.uiFilterListViews[filter].count()):
                if self.uiFilterListViews[filter].item(i).text().lower() == filterCriteria.lower():
                    found = True
                    break
            if found == False:
                self.uiFilterListViews[filter].addItem(filterCriteria)
            self.uiFilterListViews[filter].item(0).setSelected(True)

    def removeButtonFunction(self, filter=None):
        index = self.uiFilterListViews[filter].currentIndex().row()
        if index == -1:
            index = 0
        self.uiFilterListViews[filter].takeItem(index)
        if self.uiFilterListViews[filter].count() > 0:
            self.uiFilterListViews[filter].item(0).setSelected(True)

    def filterButtonFunction(self):
        self.filterButton.setDisabled(True)
        if self.dataGood != None:
            dataList = self.dataGood
            filterCriterias = {
                'reqId': [],
                'level': [],
                'date': [],
                'time': [],
                'remoteAddr': [],
                'user': [],
                'app': [],
                'method': [],
                'url': [],
                'message': []
            }

            for listView in self.uiFilterListViews:
                if self.uiFilterListViews[listView] != None:
                    for row in range(0, self.uiFilterListViews[listView].count()):
                        filterCriterias[listView].append(self.uiFilterListViews[listView].item(row).text())
            goFiltering = False
            for criteria in filterCriterias:
                if len(filterCriterias[criteria]) > 0:
                    goFiltering = True
                    break
            if goFiltering:
                dataList = filter(data=self.dataGood, filterCriterias=filterCriterias)
                self.setLabelText(labelName='rowsAffectedCountLabel', text=f'rows affected by filter: {len(dataList)}')
            else:
                self.setLabelText(labelName='rowsAffectedCountLabel', text=f'rows affected by filter: 0')
            Thread(target=self.loadData, args=(dataList,)).start()


    def loadData(self, dataList):
        self.configureTableWidget()
        tableColumns = {
            'ID': 0,
            'reqId': 0,
            'level': 0,
            'date': 0,
            'time': 0,
            'remoteAddr': 0,
            'user': 0,
            'app': 0,
            'method': 0,
            'url': 0,
            'message': 0
        }
        self.dataTable.setRowCount(len(dataList))
        for row in range(0, len(dataList)):
            record = dataList[row]
            for column in range(0, len(tableColumns)):
                item = record.getTableItemObject(attribute=list(tableColumns)[column])
                self.dataTable.setItem(row, column, item)
                if item.getStringLength() > tableColumns[list(tableColumns)[column]]:
                    tableColumns[list(tableColumns)[column]] = item.getStringLength()
                    self.dataTable.setColumnWidth(column, item.getItemLengthSizeInPixel() + 20)
        self.filterButton.setEnabled(True)
