import os
import sqlite3
import time

from PySide2 import QtWidgets, QtGui, QtHelp, QtCore
from PySide2.QtCore import QPersistentModelIndex, Qt
from PySide2.QtWidgets import QWidget

import errordialog
import hello_controller
import mainwindow

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))


class Help(QtWidgets.QTextBrowser):
    def __init__(self, helpEngine, parent=None):
        super().__init__(parent)
        self.helpEngine = helpEngine

    def loadResource(self, _type, name):
        if name.scheme() == "qthelp":
            return self.helpEngine.fileData(name)
        else:
            return super().loadResource(_type, name)


class Main(QtWidgets.QMainWindow, mainwindow.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.createHelpWindow()
        self.helpAction = QtWidgets.QAction(self.tr("Справка"), self)
        self.helpAction.setShortcut(QtGui.QKeySequence.HelpContents)
        self.helpAction.triggered.connect(self.helpWindow.show)
        self.helpMenu = QtWidgets.QMenu(self.tr("&Помощь"), self)
        self.helpMenu.addAction(self.helpAction)
        self.menuBar().addMenu(self.helpMenu)
        self.setupUi(self)
        self.pushButton_6.clicked.connect(self.add_db)
        self.pushButton_3.clicked.connect(self.delete)
        self.tableWidget.setRowCount(0)
        self.tableWidget_2.setRowCount(0)
        self.pushButton_2.clicked.connect(self.save_all)
        self.pushButton_5.clicked.connect(self.save_zakup)
        self.show_all()
        self.show_zakup()

    def createHelpWindow(self):
        self.helpEngine = QtHelp.QHelpEngine(
            os.path.join(CURRENT_DIR, "documentation", "qgraphicshelpexample.qhc")
        )
        self.helpEngine.setupData()

        tWidget = QtWidgets.QListWidget()
        textViewer = Help(self.helpEngine)
        tWidget.addItem("Склад")
        tWidget.addItem("Закупки")
        tWidget.addItem("Добавление")

        def spravka():
            if tWidget.currentItem().text() == 'Склад':
                textViewer.setSource("documentation/skl.html")
            elif tWidget.currentItem().text() == 'Закупки':
                textViewer.setSource("documentation/zak.html")
            elif tWidget.currentItem().text() == 'Добавление':
                textViewer.setSource("documentation/add.html")

        self.connect(tWidget, QtCore.SIGNAL("itemDoubleClicked (QListWidgetItem *)"), spravka)

        self.helpEngine.setUsesFilterEngine(True)
        self.helpEngine.indexWidget().linkActivated.connect(textViewer.setSource)

        horizSplitter = QtWidgets.QSplitter(QtCore.Qt.Horizontal)
        horizSplitter.insertWidget(0, tWidget)
        horizSplitter.insertWidget(1, textViewer)
        horizSplitter.hide()

        self.helpWindow = QtWidgets.QDockWidget(self.tr("Help"), self)
        self.helpWindow.setWidget(horizSplitter)
        self.helpWindow.hide()
        self.addDockWidget(QtCore.Qt.BottomDockWidgetArea, self.helpWindow)

    def save_all(self):
        with open('print_all.txt', 'w', newline='') as file:
            file.write('Наименование' + '   ' + 'Количество' + '   ' + 'Цена' + '   ' + 'Норма' + '\n')
            for i in range(self.tableWidget.rowCount()):
                file.write(self.tableWidget.item(i, 0).text() + ' ' * 14 + self.tableWidget.item(i,
                                                                                                 1).text() + ' ' * 10 + self.tableWidget.item(
                    i, 2).text() + ' ' * 4 + self.tableWidget.item(i, 3).text() + '\n')

        os.startfile('print_all.txt', 'print')

    def save_zakup(self):
        with open('print_zakup.txt', 'w', newline='') as file:
            file.write('Наименование' + '   ' + 'Количество' + '   ' + 'Цена' + '   ' + 'Норма' + '\n')
            for i in range(self.tableWidget_2.rowCount()):
                file.write(self.tableWidget_2.item(i, 0).text() + ' ' * 14 + self.tableWidget_2.item(i,
                                                                                                     1).text() + ' ' * 10 + self.tableWidget_2.item(
                    i, 2).text() + ' ' * 4 + self.tableWidget_2.item(i, 3).text() + '\n')
            file.write('\n' + 'Итого:     ' + self.label_6.text())
        os.startfile('print_zakup.txt', 'print')

    def delete(self):
        if self.tableWidget.selectionModel().hasSelection():
            indexes = [QPersistentModelIndex(index) for index in self.tableWidget.selectionModel().selectedRows()]
            for index in sorted(indexes):
                print('Deleting row %d...' % index.row())
                try:
                    c = sqlite3.connect("db.db")
                    curs = c.cursor()
                    curs.execute("""DELETE FROM zakup WHERE name = ?""", (self.tableWidget.currentItem().text(),))
                    c.commit()
                    c.close()
                    self.tableWidget.removeRow(index.row())
                except:
                    self.tableWidget.removeRow(index.row())
        else:
            print('No row selected!')
        self.tableWidget_2.setRowCount(0)
        self.show_zakup()

    def show_all(self):
        c = sqlite3.connect("db.db")
        curs = c.cursor()
        curs.execute("""SELECT * FROM zakup""")
        rows = curs.fetchall()
        for i in range(len(rows)):
            self.tableWidget.insertRow(i)
            self.tableWidget.setItem(i, 0, QtWidgets.QTableWidgetItem(str(rows[i][1])))
            self.tableWidget.setItem(i, 1, QtWidgets.QTableWidgetItem(str(rows[i][2])))
            self.tableWidget.setItem(i, 2, QtWidgets.QTableWidgetItem(str(rows[i][3])))
            self.tableWidget.setItem(i, 3, QtWidgets.QTableWidgetItem(str(rows[i][4])))
            self.tableWidget.item(i, 0).setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            self.tableWidget.item(i, 1).setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            self.tableWidget.item(i, 2).setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            self.tableWidget.item(i, 3).setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
        c.close()

    def show_zakup(self):
        summa = 0
        c = sqlite3.connect("db.db")
        curs = c.cursor()
        curs.execute("""SELECT * FROM zakup WHERE (amount < norm)""")
        rows = curs.fetchall()
        for i in range(len(rows)):
            self.tableWidget_2.insertRow(i)
            self.tableWidget_2.setItem(i, 0, QtWidgets.QTableWidgetItem(str(rows[i][1])))
            self.tableWidget_2.setItem(i, 1, QtWidgets.QTableWidgetItem(str(rows[i][2])))
            self.tableWidget_2.setItem(i, 2, QtWidgets.QTableWidgetItem(str(rows[i][3])))
            self.tableWidget_2.setItem(i, 3, QtWidgets.QTableWidgetItem(str(rows[i][4])))
            self.tableWidget.item(i, 0).setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            self.tableWidget.item(i, 1).setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            self.tableWidget.item(i, 2).setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            self.tableWidget.item(i, 3).setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            summa += (rows[i][4] - rows[i][2]) * rows[i][3]
        c.close()
        self.label_6.setText(str(summa) + '$')

    def add_db(self):
        try:
            int(self.lineEdit_5.text())
            float(self.lineEdit_6.text())
            int(self.lineEdit_7.text())
            c = sqlite3.connect("db.db")
            curs = c.cursor()
            curs.execute("""INSERT INTO zakup(name, amount, price, norm) VALUES(?,?,?,?)""",
                         (self.lineEdit_4.text(), self.lineEdit_5.text(), self.lineEdit_6.text(), self.lineEdit_7.text()))
            c.commit()
            c.close()
            self.tableWidget.setRowCount(0)
            self.tableWidget_2.setRowCount(0)
            self.show_all()
            self.show_zakup()
            self.tabWidget.setCurrentIndex(0)
            self.lineEdit_4.clear()
            self.lineEdit_5.clear()
            self.lineEdit_6.clear()
            self.lineEdit_7.clear()
        except ValueError:
            self.error = ErrorController()
            self.error.error_msg()
            self.error.show()


class ErrorController(QtWidgets.QMainWindow, errordialog.Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButtonOK.clicked.connect(self.close)

    def error_msg(self):
        self.labelError.setText('Количество, цена и наименование должны быть числами!')
