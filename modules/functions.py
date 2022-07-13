from PyQt5.Qt import QFontMetrics
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QListWidget
from PyQt5.QtWidgets import QTableWidget
from PyQt5.QtWidgets import QTableWidgetItem

from os.path import exists
from os.path import expanduser

from threading import Thread
from modules.ocRecordObject import ocRecord

class Functions():

    ui = None

    def __init__(self, ui=None):
        self.ui = ui
        self.App = self.App(parent=self)
        self.File = self.File(parent=self)
        self.String = self.String(parent=self)
        self.Qt = self.Qt(parent=self)


    class App:

        fileData = None
        filteringInProgress = False
        tableColumns = [
            'recordId',
            'reqId',
            'level',
            'date',
            'time',
            'remoteAddr',
            'user',
            'app',
            'method',
            'url',
            'message'
        ]

        def __init__(self, parent):
            self.Functions = parent

        def connectButtons(self):
            self.Functions.Qt.Button.addClickedConnection(buttonName='openFileButton', connectFunction=lambda x: Thread(target=self.openFileButtonFunction).start())
            self.Functions.Qt.Button.addClickedConnection(buttonName='reqIdAddButton', connectFunction=lambda x: self.addFilterCriteria('reqId'))
            self.Functions.Qt.Button.addClickedConnection(buttonName='levelAddButton', connectFunction=lambda x: self.addFilterCriteria('level'))
            self.Functions.Qt.Button.addClickedConnection(buttonName='userAddButton', connectFunction=lambda x: self.addFilterCriteria('user'))
            self.Functions.Qt.Button.addClickedConnection(buttonName='appAddButton', connectFunction=lambda x: self.addFilterCriteria('app'))
            self.Functions.Qt.Button.addClickedConnection(buttonName='methodAddButton', connectFunction=lambda x: self.addFilterCriteria('method'))
            self.Functions.Qt.Button.addClickedConnection(buttonName='reqIdRemoveButton', connectFunction=lambda x: self.removeFilterCriteria('reqId'))
            self.Functions.Qt.Button.addClickedConnection(buttonName='levelRemoveButton', connectFunction=lambda x: self.removeFilterCriteria('level'))
            self.Functions.Qt.Button.addClickedConnection(buttonName='userRemoveButton', connectFunction=lambda x: self.removeFilterCriteria('user'))
            self.Functions.Qt.Button.addClickedConnection(buttonName='appRemoveButton', connectFunction=lambda x: self.removeFilterCriteria('app'))
            self.Functions.Qt.Button.addClickedConnection(buttonName='methodRemoveButton', connectFunction=lambda x: self.removeFilterCriteria('method'))
            self.Functions.Qt.Button.addClickedConnection(buttonName='filterButton', connectFunction=lambda x: Thread(target=self.filter).start())
            self.Functions.Qt.Button.addClickedConnection(buttonName='exportButton', connectFunction=lambda x: Thread( target=self.exportRecords).start())

        def connectEventFilters(self):
            self.Functions.Qt.LineEdit.installEventFilter(lineEditName='reqIdLineEdit')
            self.Functions.Qt.LineEdit.installEventFilter(lineEditName='userLineEdit')
            self.Functions.Qt.LineEdit.installEventFilter(lineEditName='appLineEdit')

        def configDataTable(self, tableName):
            self.Functions.Qt.Table.Column.setCount(tableName=tableName, count=len(self.tableColumns))
            for i in range(0, len(self.tableColumns)):
                item = QTableWidgetItem()
                item.setFont(self.Functions.ui.font())
                item.setText(self.tableColumns[i])
                item.setTextAlignment(0)
                self.Functions.Qt.Table.Column.setHeaderItem(tableName=tableName, column=i, headerItem=item)
            self.Functions.Qt.Table.Column.hide(tableName=tableName, column=0)

        def createRecordList(self, jsonStringList):
            dataList = []
            for line in jsonStringList:
                dataList.append(ocRecord(line))
            return dataList

        def openFileButtonFunction(self):
            fileName = self.Functions.Qt.FileDialog.getOpenSingleFileFileDialog()
            if fileName != '' and fileName != None:
                Thread(target=self.Functions.Qt.ComboBox.clear, args=('levelComboBox',)).start()
                Thread(target=self.Functions.Qt.ComboBox.clear, args=('methodComboBox',)).start()
                Thread(target=self.Functions.Qt.Table.clear, args=('dataTable',)).start()
                self.Functions.Qt.Label.setText(labelName='statusLabel', text=f'status: reading file', resizeWidth=True)
                result = self.Functions.File.readLines(file=fileName)
                self.Functions.Qt.Label.setText(labelName='statusLabel', text=f'status: parsing data', resizeWidth=True)
                self.fileData = self.createRecordList(jsonStringList=result)
                Thread(target=self.setComboBoxFilterItems,args=(['levelComboBox', 'methodComboBox'], self.fileData, ['level', 'method'])).start()
                self.loadDataIntoTable(tableName='dataTable', data=self.fileData)
                self.Functions.Qt.Label.setText(labelName='statusLabel', text=f'status: data loaded ...  100%', resizeWidth=True)
                self.Functions.Qt.Label.setText(labelName='rowsCompleteCountLabel', text=f'rows complete: {len(self.fileData)}', resizeWidth=True)
                self.Functions.Qt.Button.activate(buttonName='filterButton')

        def setComboBoxFilterItems(self, comboBoxNames, data, attributes):
            filterItems = {}
            for attribute in attributes:
                filterItems[attribute] = []
            for record in data:
                for attribute in attributes:
                    if record.__getattribute__(attribute) not in filterItems[attribute]:
                        filterItems[attribute].append(record.__getattribute__(attribute))
            for comboBoxName in comboBoxNames:
                for attribute in attributes:
                    if attribute in comboBoxName:
                        filterItems[attribute].sort()
                        self.Functions.Qt.ComboBox.addItems(comboBoxName=comboBoxName, items=filterItems[attribute])

        def loadDataIntoTable(self, tableName, data):
            columns = []
            columnsLength = {}
            for i in range(self.Functions.Qt.Table.Column.count(tableName=tableName)):
                columns.append(self.Functions.Qt.Table.Column.getHeaderItemText(tableName=tableName, column=i))
                columnsLength[self.Functions.Qt.Table.Column.getHeaderItemText(tableName=tableName, column=i)] = 0
            for row in range(0, len(data)):
                items = []
                for column in columns:
                    items.append(data[row].getTableItemObject(attribute=column))
                    if len(data[row].__getattribute__(column)) > columnsLength[column]:
                        columnsLength[column] = len(data[row].__getattribute__(column))
                        self.Functions.Qt.Table.Column.setWidth(tableName=tableName, column=columns.index(column), width=self.Functions.String.pixelWidth(txt=data[row].__getattribute__(column)) + 20)
                self.Functions.Qt.Table.Row.add(tableName=tableName, row=row, items=items)
                self.Functions.Qt.Label.setText(labelName='statusLabel', text=f'status: loading data ...  {int(((100 / len(data)) * row))}%', resizeWidth=True)

        def addFilterCriteria(self, filterFiledName):
            try:
                criteria = self.Functions.Qt.LineEdit.getText(lineEditName=f'{filterFiledName}LineEdit')
            except:
                criteria = self.Functions.Qt.ComboBox.getSelectedItemText(comboBoxName=f'{filterFiledName}ComboBox')
            if criteria != '':
                itemFound = False
                for i in range(0, self.Functions.Qt.ListWidget.count(listWidgetName=f'{filterFiledName}ListWidget')):
                    if criteria.lower() == self.Functions.Qt.ListWidget.getItemText(listWidgetName=f'{filterFiledName}ListWidget', itemIndex=i):
                        itemFound = True
                        break
                if itemFound == False:
                    self.Functions.Qt.ListWidget.addItem(listWidgetName=f'{filterFiledName}ListWidget', item=criteria)
                    try:
                        self.Functions.Qt.LineEdit.clear(lineEditName=f'{filterFiledName}LineEdit')
                    except:
                        self.Functions.Qt.ComboBox.setPreSelectedItem(comboBoxName=f'{filterFiledName}ComboBox', itemIndex=0)
                self.Functions.Qt.ListWidget.selectItem(listWidgetName=f'{filterFiledName}ListWidget', index=0)

        def removeFilterCriteria(self, filterFiledName):
            if self.Functions.Qt.ListWidget.count(listWidgetName=f'{filterFiledName}ListWidget') > 0:
                index = self.Functions.Qt.ListWidget.getSelectedItemIndex(listWidgetName=f'{filterFiledName}ListWidget')
                self.Functions.Qt.ListWidget.removeItem(listWidgetName=f'{filterFiledName}ListWidget', itemIndex=index)
                if self.Functions.Qt.ListWidget.count(listWidgetName=f'{filterFiledName}ListWidget') > 0:
                    self.Functions.Qt.ListWidget.selectItem(listWidgetName=f'{filterFiledName}ListWidget', index=0)

        def filter(self):
            self.filteringInProgress = True
            self.deactivateButtonsWhileFiltering()
            data = self.fileData
            filterCriterias = self.collectFilterCriteria()
            Thread(target=self.Functions.Qt.Table.clear, args=('dataTable',)).start()
            for filter in filterCriterias:
                if len(filterCriterias[filter]) > 0:
                    tempData = []
                    for record in data:
                        for criteria in filterCriterias[filter]:
                            if record.__getattribute__(filter).lower() == criteria.lower():
                                tempData.append(record)
                    data = tempData
            self.loadDataIntoTable(tableName='dataTable', data=data)
            self.activateButtonsAfterFiltering()
            self.filteringInProgress = False

        def deactivateButtonsWhileFiltering(self):
            buttons = [
                'openFileButton',
                'reqIdAddButton',
                'levelAddButton',
                'userAddButton',
                'appAddButton',
                'methodAddButton',
                'reqIdRemoveButton',
                'levelRemoveButton',
                'userRemoveButton',
                'appRemoveButton',
                'methodRemoveButton',
                'filterButton',
                'exportButton']
            for button in buttons:
                self.Functions.Qt.Button.deactivate(buttonName=button)

        def activateButtonsAfterFiltering(self):
            buttons = [
                'openFileButton',
                'reqIdAddButton',
                'levelAddButton',
                'userAddButton',
                'appAddButton',
                'methodAddButton',
                'reqIdRemoveButton',
                'levelRemoveButton',
                'userRemoveButton',
                'appRemoveButton',
                'methodRemoveButton',
                'filterButton',
                'exportButton']
            for button in buttons:
                self.Functions.Qt.Button.activate(buttonName=button)

        def collectFilterCriteria(self):
            filterCriterias = {}
            for column in self.tableColumns:
                try:
                    filterCriterias[column] = self.Functions.Qt.ListWidget.getItemsAsTextList(listWidgetName=f'{column}ListWidget')
                except:
                    pass
            return filterCriterias

        def exportRecords(self):
            data = self.remmoveDuplicates(self.Functions.Qt.Table.getSelectedItems(tableName='dataTable'))
            if len(data) > 0:
                recordStrings = []
                for index in data:
                    for record in self.fileData:
                        if record.recordId.lower() == self.Functions.Qt.Table.getItemText(tableName='dataTable', row=index,column=0).lower():
                            recordStrings.append(record.originalString)
                fileName = self.Functions.Qt.FileDialog.getSaveFileDialog()
                if fileName != '':
                    with open(fileName, 'w') as writer:
                        for record in recordStrings:
                            writer.write(record + '\n')

        def remmoveDuplicates(self, data):
            tempData = []
            for item in data:
                if item.row() not in tempData:
                    tempData.append(item.row())
            return tempData

    class File:

        def __init__(self, parent):
            self.Functions = parent

        def exists(self, file):
            return exists(file)

        def read(self, file, mode='r'):
            if self.exists(file=file):
                with open(file, mode) as reader:
                    return reader.read()

        def readLines(self, file, mode='r'):
            if self.exists(file=file):
                with open(file, mode) as reader:
                    return reader.readlines()

    class String:

        def __init__(self, parent):
            self.Functions = parent
            self.fontMetrics = QFontMetrics(self.Functions.ui.font())

        def pixelWidth(self, txt):
            return self.fontMetrics.width(txt)

        def pixelHeight(self, txt):
            return self.fontMetrics.height(txt)

    class Qt:

        def __init__(self, parent):
            self.Functions = parent
            self.Button = self.Button(parent=self)
            self.ComboBox = self.ComboBox(parent=self)
            self.FileDialog = self.FileDialog(parent=self)
            self.Label = self.Label(parent=self)
            self.LineEdit = self.LineEdit(parent=self)
            self.ListWidget = self.ListWidget(parent=self)
            self.Table = self.Table(parent=self)

        def getObject(self, objectType, objectName):
            return self.Functions.ui.findChild(objectType, objectName)

        class Button:

            def __init__(self, parent):
                self.Qt = parent

            def deactivate(self, buttonName):
                self.Qt.getObject(objectType=QPushButton, objectName=buttonName).setDisabled(True)

            def activate(self, buttonName=None):
                self.Qt.getObject(objectType=QPushButton, objectName=buttonName).setEnabled(True)

            def addClickedConnection(self, buttonName, connectFunction):
                self.Qt.getObject(objectType=QPushButton, objectName=buttonName).clicked.connect(connectFunction)

        class ComboBox:

            def __init__(self, parent):
                self.Qt = parent

            def clear(self, comboBoxName):
                self.Qt.getObject(objectType=QComboBox, objectName=comboBoxName).clear()

            def addItems(self, comboBoxName, items):
                self.Qt.getObject(objectType=QComboBox, objectName=comboBoxName).addItems(items)

            def getSelectedItemText(self, comboBoxName):
                return self.Qt.getObject(objectType=QComboBox, objectName=comboBoxName).currentText()

            def getItemText(self, comboBoxName, itemIndex):
                return self.Qt.getObject(objectType=QComboBox, objectName=comboBoxName).itemText(itemIndex)

            def setPreSelectedItem(self, comboBoxName, itemIndex):
                self.Qt.getObject(objectType=QComboBox, objectName=comboBoxName).setCurrentText(
                    self.getItemText(comboBoxName=comboBoxName, itemIndex=itemIndex))

        class FileDialog:

            def __init__(self, parent):
                self.Qt = parent

            def getOpenSingleFileFileDialog(self):
                return QFileDialog.getOpenFileName(self.Qt.Functions.ui, 'Select LogFile to load', expanduser('~'))[0]

            def getSaveFileDialog(self):
                return QFileDialog.getSaveFileName(self.Qt.Functions.ui, 'Select LogFile to save', expanduser('~'))[0]

        class Label:

            def __init__(self, parent):
                self.Qt = parent

            def setText(self, labelName, text, resizeWidth=False, resizeHeight=False):
                self.Qt.getObject(objectType=QLabel, objectName=labelName).setText(text)
                if resizeWidth:
                    self.setWidth(labelName=labelName, width=self.Qt.Functions.String.pixelWidth(txt=text))
                if resizeHeight:
                    self.setHeight(labelName=labelName, height=self.Qt.Functions.String.pixelHeight(txt=text))

            def getWidth(self, labelName):
                return self.Qt.getObject(objectType=QLabel, objectName=labelName).width()

            def getHeight(self, labelName):
                return self.Qt.getObject(objectType=QLabel, objectName=labelName).height()

            def setWidth(self, labelName, width):
                self.Qt.getObject(objectType=QLabel, objectName=labelName).resize(width, self.getHeight(labelName=labelName))

            def setHeight(self, labelName, height):
                self.Qt.getObject(objectType=QLabel, objectName=labelName).resize(self.getWidth(labelName=labelName), height)

        class LineEdit:

            def __init__(self, parent):
                self.Qt = parent

            def getText(self, lineEditName):
                return self.Qt.getObject(objectType=QLineEdit, objectName=lineEditName).text()

            def clear(self, lineEditName):
                self.Qt.getObject(objectType=QLineEdit, objectName=lineEditName).clear()

            def installEventFilter(self, lineEditName):
                self.Qt.getObject(objectType=QLineEdit, objectName=lineEditName).installEventFilter(self.Qt.Functions.ui)

        class ListWidget:

            def __init__(self, parent):
                self.Qt = parent

            def addItem(self, listWidgetName, item):
                self.Qt.getObject(objectType=QListWidget, objectName=listWidgetName).addItem(item)

            def count(self, listWidgetName):
                return self.Qt.getObject(objectType=QListWidget, objectName=listWidgetName).count()

            def selectItem(self, listWidgetName, index):
                self.Qt.getObject(objectType=QListWidget, objectName=listWidgetName).item(index).setSelected(True)

            def getItemText(self, listWidgetName, itemIndex):
                return self.Qt.getObject(objectType=QListWidget, objectName=listWidgetName).item(itemIndex).text()

            def getItemsAsTextList(self, listWidgetName):
                data = []
                for item in range(self.count(listWidgetName=listWidgetName)):
                    data.append(self.getItemText(listWidgetName=listWidgetName, itemIndex=item))
                return data

            def getSelectedItemIndex(self, listWidgetName):
                index = self.Qt.getObject(objectType=QListWidget, objectName=listWidgetName).currentRow()
                if index == -1:
                    index = 0
                return index

            def removeItem(self, listWidgetName, itemIndex):
                self.Qt.getObject(objectType=QListWidget, objectName=listWidgetName).takeItem(itemIndex)

        class Table:

            def __init__(self, parent):
                self.Qt = parent
                self.Column = self.Column(parent=self)
                self.Row = self.Row(parent=self)

            def clear(self, tableName):
                self.Qt.getObject(objectType=QTableWidget, objectName=tableName).clearContents()
                self.Row.setCount(tableName=tableName, count=0)

            def getSelectedItems(self, tableName):
                return self.Qt.getObject(objectType=QTableWidget, objectName=tableName).selectedIndexes()

            def getItemText(self, tableName, row, column):
                return self.Qt.getObject(objectType=QTableWidget, objectName=tableName).item(row, column).text()

            class Column:

                def __init__(self, parent):
                    self.Table = parent

                def hide(self, tableName, column):
                    self.Table.Qt.getObject(objectType=QTableWidget, objectName=tableName).setColumnHidden(column, True)

                def show(self, tableName, column):
                    self.Table.Qt.getObject(objectType=QTableWidget, objectName=tableName).setColumnHidden(column, False)

                def setCount(self, tableName, count):
                    self.Table.Qt.getObject(objectType=QTableWidget, objectName=tableName).setColumnCount(count)

                def setHeaderItem(self, tableName, column, headerItem):
                    self.Table.Qt.getObject(objectType=QTableWidget, objectName=tableName).setHorizontalHeaderItem(column, headerItem)

                def getHeaderItemText(self, tableName, column):
                    return self.Table.Qt.getObject(objectType=QTableWidget, objectName=tableName).horizontalHeaderItem(column).text()

                def count(self, tableName):
                    return self.Table.Qt.getObject(objectType=QTableWidget, objectName=tableName).columnCount()

                def setWidth(self, tableName, column, width):
                    self.Table.Qt.getObject(objectType=QTableWidget, objectName=tableName).setColumnWidth(column, width)

            class Row:

                def __init__(self, parent):
                    self.Table = parent

                def setCount(self, tableName, count):
                    self.Table.Qt.getObject(objectType=QTableWidget, objectName=tableName).setRowCount(count)

                def count(self, tableName):
                    return self.Table.Qt.getObject(objectType=QTableWidget, objectName=tableName).rowCount()

                def add(self, tableName, row, items):
                    self.setCount(tableName=tableName, count=(row + 1))
                    table = self.Table.Qt.getObject(objectType=QTableWidget, objectName=tableName)
                    for item in items:
                        table.setItem(row, items.index(item), item)