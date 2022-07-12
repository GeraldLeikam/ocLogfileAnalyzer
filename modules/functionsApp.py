from modules.ocRecordObject import ocRecord
from PyQt5.QtWidgets import QTableWidgetItem
from threading import Thread

class AppFunctions:

    fileData = None
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
    filteringInProgress = False

    def __init__(self, functions):
        self.Functions = functions

    def openFileButtonFunction(self):
        fileName = self.Functions.FileDialog.getSingleFileFileDialog()
        if fileName != '' and fileName != None:
            Thread(target=self.Functions.ComboBox.clear, args=('levelComboBox',)).start()
            Thread(target=self.Functions.ComboBox.clear, args=('methodComboBox',)).start()
            Thread(target=self.Functions.Table.clear, args=('dataTable',)).start()
            self.Functions.Label.setText(labelName='statusLabel', text=f'status: reading file', resizeWidth=True)
            result = self.Functions.File.readLines(file=fileName)
            self.Functions.Label.setText(labelName='statusLabel', text=f'status: parsing data', resizeWidth=True)
            self.fileData = self.createRecordList(jsonStringList=result)
            Thread(target=self.setComboBoxFilterItems, args=(['levelComboBox', 'methodComboBox'], self.fileData, ['level', 'method'])).start()
            self.loadDataIntoTable(tableName='dataTable', data=self.fileData)
            self.Functions.Label.setText(labelName='statusLabel', text=f'status: data loaded ...  100%', resizeWidth=True)
            self.Functions.Label.setText(labelName='rowsCompleteCountLabel', text=f'rows complete: {len(self.fileData)}', resizeWidth=True)
            self.Functions.Button.activate(buttonName='filterButton')

    def createRecordList(self, jsonStringList):
        dataList = []
        for line in jsonStringList:
            dataList.append(ocRecord(line))
        return dataList

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
                    self.Functions.ComboBox.addItems(comboBoxName=comboBoxName, items=filterItems[attribute])

    def loadDataIntoTable(self, tableName, data):
        columns = []
        columnsLength = {}
        for i in range(self.Functions.Table.Column.getCount(tableName=tableName)):
            columns.append(self.Functions.Table.Column.getHeaderItemText(tableName=tableName, column=i))
            columnsLength[self.Functions.Table.Column.getHeaderItemText(tableName=tableName, column=i)] = 0
        for row in range(0, len(data)):
            items = []
            for column in columns:
                items.append(data[row].getTableItemObject(attribute=column))
                if len(data[row].__getattribute__(column)) > columnsLength[column]:
                    columnsLength[column] = len(data[row].__getattribute__(column))
                    self.Functions.Table.Column.setWidth(tableName=tableName, column=columns.index(column), width=self.Functions.String.pixelWidth(txt=data[row].__getattribute__(column)) + 20)
            self.Functions.Table.Row.add(tableName=tableName, row=row, items=items)
            self.Functions.Label.setText(labelName='statusLabel', text=f'status: loading data ...  {int(((100 / len(data)) * row))}%', resizeWidth=True)

    def addFilterCriteria(self, filterFiledName):
        try:
            criteria = self.Functions.LineEdit.getText(lineEditName=f'{filterFiledName}LineEdit')
        except:
            criteria = self.Functions.ComboBox.getSelectedItemText(comboBoxName=f'{filterFiledName}ComboBox')
        if criteria != '':
            itemFound = False
            for i in range(0, self.Functions.ListWidget.count(listWidgetName=f'{filterFiledName}ListWidget')):
                if criteria.lower() == self.Functions.ListWidget.getItemText(listWidgetName=f'{filterFiledName}ListWidget', itemIndex=i):
                    itemFound = True
                    break
            if itemFound == False:
                self.Functions.ListWidget.addItem(listWidgetName=f'{filterFiledName}ListWidget', item=criteria)
                try:
                    self.Functions.LineEdit.clear(lineEditName=f'{filterFiledName}LineEdit')
                except:
                    self.Functions.ComboBox.setPreSelectedItem(comboBoxName=f'{filterFiledName}ComboBox', itemIndex=0)
            self.Functions.ListWidget.selectItem(listWidgetName=f'{filterFiledName}ListWidget', index=0)

    def removeFilterCriteria(self, filterFiledName):
        if self.Functions.ListWidget.count(listWidgetName=f'{filterFiledName}ListWidget') > 0:
            index = self.Functions.ListWidget.getSelectedItemIndex(listWidgetName=f'{filterFiledName}ListWidget')
            self.Functions.ListWidget.removeItem(listWidgetName=f'{filterFiledName}ListWidget', itemIndex=index)
            if self.Functions.ListWidget.count(listWidgetName=f'{filterFiledName}ListWidget') > 0:
                self.Functions.ListWidget.selectItem(listWidgetName=f'{filterFiledName}ListWidget', index=0)

    def filter(self):
        self.filteringInProgress = True
        self.deactivateButtonsWhileFiltering()
        data = self.fileData
        filterCriterias = self.collectFilterCriteria()
        Thread(target=self.Functions.Table.clear, args=('dataTable',)).start()
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
            self.Functions.Button.deactivate(buttonName=button)

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
            self.Functions.Button.activate(buttonName=button)

    def collectFilterCriteria(self):
        filterCriterias = {}
        for column in self.tableColumns:
            try:
                filterCriterias[column] = self.Functions.ListWidget.getItemsAsTextList(listWidgetName=f'{column}ListWidget')
            except:
                pass
        return filterCriterias

    def configDataTable(self, tableName):
        self.Functions.Table.Column.setCount(tableName=tableName, count=len(self.tableColumns))
        for i in range(0, len(self.tableColumns)):
            item = QTableWidgetItem()
            item.setText(self.tableColumns[i])
            item.setTextAlignment(0)
            self.Functions.Table.Column.setHeaderItem(tableName=tableName, column=i, headerItem=item)
        self.Functions.Table.Column.hide(tableName=tableName, column=0)

    def exportRecords(self):
        data = self.remmoveDuplicates(self.Functions.Table.getSelectedItems(tableName='dataTable'))
        if len(data) > 0:
            recordStrings = []
            for index in data:
                for record in self.fileData:
                    if record.recordId.lower() == self.Functions.Table.getItemText(tableName='dataTable', row=index, column=0).lower():
                        recordStrings.append(record.originalString)
            fileName = self.Functions.FileDialog.getSaveFileDialog()
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