from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QLineEdit

from PyQt5.Qt import QFont
from PyQt5 import QtCore
from PyQt5.uic import loadUi
from modules.functions import Functions
from modules.functionsApp import AppFunctions
from modules.items import TabelColumnHeaderItem
from threading import Thread


class Ui(QMainWindow):

    def __init__(self, uiTemplate):
        super(Ui, self).__init__(parent=None) # Call the inherited classes __init__ method
        loadUi(uiTemplate, self)

        self.setFont(QFont('Ubuntu', 10))
        self.Functions = Functions(ui=self)
        self.AppFunctions = AppFunctions(functions=self.Functions)
        self.configButtonConnections()
        self.configUiElementsEvents()
        self.initialConfig()
        self.show()

    def initialConfig(self):
        self.Functions.Label.setText(labelName='statusLabel', text=f'status: ready', resizeWidth=True)
        self.Functions.Button.deactivate(buttonName='filterButton')
        self.Functions.Button.deactivate(buttonName='exportButton')
        self.AppFunctions.configDataTable(tableName='dataTable')

    def showWindow(self):
        Ui.show(self)

    def configButtonConnections(self):
        self.Functions.Button.addClickedConnection(buttonName='openFileButton', connectFunction=lambda x: Thread(target=self.AppFunctions.openFileButtonFunction).start())
        self.Functions.Button.addClickedConnection(buttonName='reqIdAddButton', connectFunction=lambda x: self.AppFunctions.addFilterCriteria('reqId'))
        self.Functions.Button.addClickedConnection(buttonName='levelAddButton', connectFunction=lambda x: self.AppFunctions.addFilterCriteria('level'))
        self.Functions.Button.addClickedConnection(buttonName='userAddButton', connectFunction=lambda x: self.AppFunctions.addFilterCriteria('user'))
        self.Functions.Button.addClickedConnection(buttonName='appAddButton', connectFunction=lambda x: self.AppFunctions.addFilterCriteria('app'))
        self.Functions.Button.addClickedConnection(buttonName='methodAddButton', connectFunction=lambda x: self.AppFunctions.addFilterCriteria('method'))
        self.Functions.Button.addClickedConnection(buttonName='reqIdRemoveButton', connectFunction=lambda x: self.AppFunctions.removeFilterCriteria('reqId'))
        self.Functions.Button.addClickedConnection(buttonName='levelRemoveButton', connectFunction=lambda x: self.AppFunctions.removeFilterCriteria('level'))
        self.Functions.Button.addClickedConnection(buttonName='userRemoveButton', connectFunction=lambda x: self.AppFunctions.removeFilterCriteria('user'))
        self.Functions.Button.addClickedConnection(buttonName='appRemoveButton', connectFunction=lambda x: self.AppFunctions.removeFilterCriteria('app'))
        self.Functions.Button.addClickedConnection(buttonName='methodRemoveButton', connectFunction=lambda x: self.AppFunctions.removeFilterCriteria('method'))
        self.Functions.Button.addClickedConnection(buttonName='filterButton', connectFunction=lambda x: Thread(target=self.AppFunctions.filter).start())
        self.Functions.Button.addClickedConnection(buttonName='exportButton', connectFunction=lambda x: Thread(target=self.AppFunctions.exportRecords).start())

    def configUiElementsEvents(self):
        self.findChild(QLineEdit, 'reqIdLineEdit').installEventFilter(self)
        self.findChild(QLineEdit, 'userLineEdit').installEventFilter(self)
        self.findChild(QLineEdit, 'appLineEdit').installEventFilter(self)

    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.KeyPress:
            if event.key() == QtCore.Qt.Key_Return or event.key() == QtCore.Qt.Key_Enter:
                if 'LineEdit' in obj.objectName() or 'ComboBox' in obj.objectName:
                    if self.AppFunctions.filteringInProgress == False:
                        self.AppFunctions.addFilterCriteria(filterFiledName=obj.objectName().replace('LineEdit', '').replace('ComboBox', ''))
        return super().eventFilter(obj, event)






