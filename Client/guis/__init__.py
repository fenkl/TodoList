#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class ChooseParameters_gui(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle("Verwalter Todo-Listen")
        dir_script = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        #self.setWindowIcon(QIcon(f"{dir_script}/xGrey_windows.png"))
        self.gui_width = 450
        self.gui_height = 700
        self.setFixedSize(self.gui_width, self.gui_height)

        # in die Mitte positionieren
        screen = QDesktopWidget().screenGeometry()
        pos_width = screen.width() / 2 - self.gui_width / 2
        pos_height = screen.height() / 2 - self.gui_height / 2
        recAnzeige = QRect(QPoint(int(pos_width), int(pos_height)), QSize(self.width(), screen.height()))
        self.setGeometry(recAnzeige)

        self.createWidgets()
        self.createLayout()
        #self.createTrigger()

    def createWidgets(self):
        self.lblAuswahl = QLabel("Todo-Liste auswählen")
        self.cboAuwahl = QComboBox()

        self.frmTrenner1 = QFrame()
        self.frmTrenner1.setFrameShape(QFrame.HLine)
        self.frmTrenner1.setFrameShadow(QFrame.Sunken)
        self.frmTrenner1.setObjectName("McTrennerV")

        # TableView erstellen
        self.tableView = QTableView()
        self.model = QStandardItemModel(0, 2, self)
        self.model.setHeaderData(0, Qt.Horizontal, "Name")
        self.model.setHeaderData(1, Qt.Horizontal, "Beschreibung")
        self.tableView.setModel(self.model)

        # Spaltenbreite an Hauptfenster anpassen
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def createLayout(self):
        self.layMain = QVBoxLayout()
        self.layMain.setSpacing(1)

        self.layCalendar = QHBoxLayout()
        self.layCalendar.setSpacing(1)
        self.layCalendar.setGeometry(QRect(10, 10, 10, 10))
        self.layButtons = QHBoxLayout()
        self.layButtons.setSpacing(1)

        self.widCentral = QWidget(self)
        self.setCentralWidget(self.widCentral)
        self.widCentral.setLayout(self.layMain)

        self.layMain.addWidget(self.lblAuswahl)

        self.layMain.addWidget(self.lblAuswahl)
        self.layMain.addWidget(self.cboAuwahl)
        self.cboAuwahl.addItem("")
        self.layMain.addWidget(self.frmTrenner1)

        # TableView zum Layout hinzufügen
        self.layMain.addWidget(self.tableView)

        self.layMain.addStretch()
        self.layMain.addWidget(self.frmTrenner1)





if __name__ == "__main__":
    app = QApplication(sys.argv)
    #dir_current = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

    app.setStyleSheet("QWidget {font-size: 18px;}, QHBoxLayout {background-color:#0f3470;},"
                      " QPlainTextEdit {background-color: white;}")
    choose = ChooseParameters_gui()
    #choose.show()
    try:
        sys.exit(app.exec())
    except SystemExit or KeyboardInterrupt:
        print('Closing Window...')
