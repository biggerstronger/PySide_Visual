from PySide2 import QtCore, QtWidgets, QtGui
from PySide2.QtGui import QIcon
from PySide2.QtCore import QSize
import hello
import maincontrol


class Hello(QtWidgets.QMainWindow, hello.Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.main = maincontrol.Main()
        self.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
        self.icon = QIcon("hello.jpg")
        self.pushButton.setIcon(self.icon)
        self.pushButton.setIconSize(QSize(268, 383))
        self.show()
        self.pushButton.clicked.connect(self.startapp)

    def startapp(self):
        self.close()
        self.main.show()
