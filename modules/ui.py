from PyQt5.QtWidgets import QMainWindow
from PyQt5.Qt import QFont
from PyQt5 import QtCore
from PyQt5.uic import loadUi
from modules.functions import Functions

class Ui(QMainWindow):

    def __init__(self, uiTemplate):
        super(Ui, self).__init__() # Call the inherited classes __init__ method
        loadUi(uiTemplate, self)

        self.setFont(QFont('Ubuntu', 10))
        self.Functions = Functions(ui=self)
        self.Functions.App.connectEventFilters()
        self.initialConfig()
        self.show()

    def initialConfig(self):
        self.Functions.App.connectButtons()
        self.Functions.Qt.Label.setText(labelName='statusLabel', text=f'status: ready', resizeWidth=True)
        self.Functions.Qt.Button.deactivate(buttonName='filterButton')
        self.Functions.Qt.Button.activate(buttonName='exportButton')
        self.Functions.App.configDataTable(tableName='dataTable')

    def showWindow(self):
        Ui.show(self)

    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.KeyPress:
            if event.key() == QtCore.Qt.Key_Return or event.key() == QtCore.Qt.Key_Enter:
                if 'LineEdit' in obj.objectName():
                    if self.Functions.App.filteringInProgress == False:
                        self.Functions.App.addFilterCriteria(filterFiledName=obj.objectName().replace('LineEdit', ''))
        return super().eventFilter(obj, event)






