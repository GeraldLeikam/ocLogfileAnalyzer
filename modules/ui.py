from PyQt5 import QtWidgets
from modules.QItems import TableItem
from PyQt5.QtWidgets import QFileDialog
from os.path import expanduser
from PyQt5.uic import loadUi
from modules.uiFunctions import setUITitle
from modules.uiFunctions import readFile
from modules.uiFunctions import createRecordList
from modules.uiFunctions import filter

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
        self.show()

    def setGUIObjects(self):
        self.dataTable = self.findChild(QtWidgets.QTableWidget, 'dataTable')

        self.uiFilterListViews = {
            'reqId': self.findChild(QtWidgets.QListView, 'requestIdListView'),
            'level': self.findChild(QtWidgets.QListView, 'levelListView'),
            'date': None,
            'time': None,
            'remoteAddr': None,
            'user': self.findChild(QtWidgets.QListView, 'userListView'),
            'app': self.findChild(QtWidgets.QListView, 'appsListView'),
            'method': self.findChild(QtWidgets.QListView, 'methodListView'),
            'url': None,
            'message': None
        }
        self.uiFilterTextEdits = {
            'reqId': self.findChild(QtWidgets.QTextEdit, 'requestIdTextEdit'),
            'date': None,
            'time': None,
            'remoteAddr': None,
            'user': self.findChild(QtWidgets.QTextEdit, 'userTextEdit'),
            'app': self.findChild(QtWidgets.QTextEdit, 'appTextEdit'),
            'url': None,
            'message': None
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

        self.openButton = self.findChild(QtWidgets.QPushButton, 'openButton')

        self.filterButton = self.findChild(QtWidgets.QPushButton, 'filterButton')

        self.rowsCountLabel = self.findChild(QtWidgets.QLabel, 'rowsCountLabel')

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

        self.filterButton.clicked.connect(self.filterButtonFunction)

    def configureTableWidget(self):

        self.dataTable.setColumnCount(len(self.columnHeaders))
        for column in range(0, len(self.columnHeaders)):
            self.dataTable.setHorizontalHeaderItem(column, self.columnHeaders[column])
            self.dataTable.setColumnWidth(column, self.columnHeaders[column].getItemLengthSizeInPixel() + 20)
        self.dataTable.setColumnHidden(0, True)

    def openButtonFunction(self):
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
            self.loadData(dataList=self.dataGood)

    def addButtonFunction(self, filter=None):
        if filter in self.uiFilterTextEdits.keys():
            filterCriteria = self.uiFilterTextEdits[filter].toPlainText()
            self.uiFilterTextEdits[filter].setText('')
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
        if self.dataGood != None:

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

            self.loadData(filter(data=self.dataGood, filterCriterias=filterCriterias))

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

        self.rowsCountLabel.setText(f'Rows: {len(dataList)}')


