#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class ErstelleNeu(QDialog):
    def __init__(self, typ: str, parent=None):
        super(ErstelleNeu, self).__init__(parent)
        self.typ = typ
        if self.typ == "Liste":
            self.setWindowTitle("Neue Liste erstellen")
        elif self.typ == "Eintrag":
            self.setWindowTitle("Neuen Eintrag erstellen")
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        if self.typ == "Liste":
            self.name_label = QLabel("Name der Liste:")
            self.name_input = QLineEdit()

            self.create_button = QPushButton("Erstellen")
            self.create_button.clicked.connect(self.accept)
            self.cancel_button = QPushButton("Abbrechen")
            self.cancel_button.clicked.connect(self.reject)

            layout.addWidget(self.name_label)
            layout.addWidget(self.name_input)
            layout.addWidget(self.create_button)
            layout.addWidget(self.cancel_button)

        elif self.typ == "Eintrag":
            self.name_label = QLabel("Name des Eintrages:")
            self.name_input = QLineEdit()

            self.beschreibung_label = QLabel("Beschreibung:")
            self.beschreibung_input = QLineEdit()

            self.create_button = QPushButton("Erstellen")
            self.create_button.clicked.connect(self.accept)
            self.cancel_button = QPushButton("Abbrechen")
            self.cancel_button.clicked.connect(self.reject)

            layout.addWidget(self.name_label)
            layout.addWidget(self.name_input)
            layout.addWidget(self.beschreibung_label)
            layout.addWidget(self.beschreibung_input)
            layout.addWidget(self.create_button)
            layout.addWidget(self.cancel_button)


        self.setLayout(layout)


class TodoList_gui(QMainWindow):
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
        self.model = QStandardItemModel(0, 3, self)  # Spaltenanzahl auf 3 erhöhen
        self.model.setHeaderData(0, Qt.Horizontal, "Name")
        self.model.setHeaderData(1, Qt.Horizontal, "Beschreibung")
        self.tableView.setModel(self.model)
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableView.setColumnHidden(2, True)  # ID-Spalte ausblenden
        # Spaltenbreite an Hauptfenster anpassen
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)


        self.btnAddEntry = QPushButton()
        self.btnAddEntry.setText("Eintrag hinzufügen")

        self.btnDeleteEntry = QPushButton()
        self.btnDeleteEntry.setText("Eintrag löschen")

        self.btnAddList = QPushButton()
        self.btnAddList.setText("Liste hinzufügen")

        self.btnDeleteList = QPushButton()
        self.btnDeleteList.setText("Liste löschen")

        self.btnRefresh = QPushButton()
        self.btnRefresh.setText("Aktualisieren")


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
        self.layMain.setStretchFactor(self.tableView, 1)
        self.layMain.addStretch()
        self.layMain.addWidget(self.frmTrenner1)

        self.layMain.addWidget(self.btnAddEntry)
        self.layMain.addWidget(self.btnDeleteEntry)

        self.layMain.addWidget(self.frmTrenner1)
        self.layMain.addWidget(self.frmTrenner1)


        self.layMain.addWidget(self.btnAddList)
        self.layMain.addWidget(self.btnDeleteList)

        self.layMain.addWidget(self.frmTrenner1)
        self.layMain.addWidget(self.frmTrenner1)

        self.layMain.addWidget(self.btnRefresh)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    #dir_current = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

    app.setStyleSheet("QWidget {font-size: 18px;}, QHBoxLayout {background-color:#0f3470;},"
                      " QPlainTextEdit {background-color: white;}")
    choose = TodoList_gui()
    #choose.show()
    try:
        sys.exit(app.exec())
    except SystemExit or KeyboardInterrupt:
        print('Closing Window...')
