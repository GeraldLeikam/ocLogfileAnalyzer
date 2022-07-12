from modules.functionsButton import ButtonFunctions
from modules.functionsTable import TableFunctions
from modules.functionsComboBox import ComboBoxFunctions
from modules.functionsString import StringFunctions
from modules.functionsLabel import LabelFunctions
from modules.functionsFile import FileFunctions
from modules.functionsLineEdit import LineEditFunctions
from modules.functionsListWidget import ListWidgetFunctions
from modules.functionsFileDialog import FileDialogFunctions


class Functions:

    def __init__(self, ui=None):
        self.ui = ui
        self.Button = ButtonFunctions(ui=ui)
        self.Table = TableFunctions(ui=ui)
        self.ComboBox = ComboBoxFunctions(ui=ui)
        self.String = StringFunctions(font=self.ui.font())
        self.Label = LabelFunctions(ui=ui)
        self.File = FileFunctions()
        self.LineEdit = LineEditFunctions(ui=ui)
        self.ListWidget = ListWidgetFunctions(ui=ui)
        self.FileDialog = FileDialogFunctions(ui=ui)

