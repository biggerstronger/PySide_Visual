# -- coding: utf-8 --

import sys
import sqlite3
from PySide2 import QtWidgets, QtCore

from hello_controller import Hello


def run_ui():
    app = QtWidgets.QApplication(sys.argv)
    window = Hello()
    window.show()
    sys.exit(app.exec_())


def main():
    c = sqlite3.connect("db.db")
    curs = c.cursor()
    curs.execute("""CREATE TABLE IF NOT EXISTS zakup
                                      (id INTEGER NOT NULL UNIQUE,
                                      name integer,
                                      amount integer,
                                      price integer,
                                      norm integer,
                                      PRIMARY KEY ('id' AUTOINCREMENT)
                                      );
                                  """)
    run_ui()


if __name__ == "__main__":
    main()
