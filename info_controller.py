from PySide2 import QtWidgets

import info


class Info(QtWidgets.QMainWindow, info.Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
