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
        self.setWindowTitle("Requester ZimbraApi")
        dir_script = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        self.setWindowIcon(QIcon(f"{dir_script}/xGrey_windows.png"))
        self.gui_width = 350
        self.gui_height = 450
        self.setFixedSize(self.gui_width, self.gui_height)

        # in die Mitte positionieren
        screen = QDesktopWidget().screenGeometry()
        pos_width = screen.width() / 2 - self.gui_width / 2
        pos_height = screen.height() / 2 - self.gui_height / 2
        recAnzeige = QRect(QPoint(pos_width, pos_height), QSize(self.width(), screen.height()))
        self.setGeometry(recAnzeige)

        self.createWidgets()
        self.createLayout()
        self.createTrigger()

    def createWidgets(self):
        self.lblTitle = QLabel("Abfrage")
        self.lblTitle.setObjectName("Title")
        self.lblTitle.setStyleSheet("color: #34568c;")

        self.lblMethode = QLabel("Methode")
        self.cboMethode = QComboBox()
        self.cboMethode.addItems(["GET", "POST"])
        self.frmTrenner1 = QFrame()
        self.frmTrenner1.setFrameShape(QFrame.HLine)
        self.frmTrenner1.setFrameShadow(QFrame.Sunken)
        self.frmTrenner1.setObjectName("McTrennerV")

        self.lblUser = QLabel("User: ")
        self.txtUser = QLineEdit()
        self.txtUser.setObjectName("Username")
        self.txtUser.setText("")

        self.lblDatum = QLabel("Datum")
        self.calDatum = QCalendarWidget()
        self.calDatum.setStyleSheet("background-color: #34568c;")

        self.lblZeit = QLabel("Zeit: Start-Ende(HH:MM-HH:MM)")
        self.txtZeit = QLineEdit()

        self.lblTerminname = QLabel("Betreff")
        self.txtTerminname = QLineEdit()

        self.lblBeschreibung = QLabel("Beschreibung")
        self.txtBeschreibung = QPlainTextEdit()
        self.txtBeschreibung.setPlaceholderText("hier eingeben...")

        self.chkForce = QCheckBox("Force")

        self.btnLos = QPushButton("Los")

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

        self.layMain.addWidget(self.lblTitle)

        self.layMain.addWidget(self.lblMethode)
        self.layMain.addWidget(self.cboMethode)
        self.layMain.addWidget(self.frmTrenner1)

        self.layMain.addWidget(self.lblUser)
        self.layMain.addWidget(self.txtUser)
        self.layMain.addWidget(self.lblDatum)
        self.layMain.addLayout(self.layCalendar)
        self.layCalendar.addWidget(self.calDatum)
        self.layMain.addStretch()
        self.layMain.addWidget(self.frmTrenner1)

        self.layMain.addWidget(self.lblZeit)
        self.lblZeit.setVisible(False)
        self.layMain.addWidget(self.txtZeit)
        self.txtZeit.setVisible(False)

        self.layMain.addWidget(self.frmTrenner1)

        self.layMain.addWidget(self.lblTerminname)
        self.lblTerminname.setVisible(False)
        self.layMain.addWidget(self.txtTerminname)
        self.txtTerminname.setVisible(False)

        self.layMain.addWidget(self.frmTrenner1)

        self.layMain.addWidget(self.lblBeschreibung)
        self.lblBeschreibung.setVisible(False)
        self.layMain.addWidget(self.txtBeschreibung)
        self.txtBeschreibung.setVisible(False)

        self.layMain.addWidget(self.frmTrenner1)

        self.layMain.addWidget(self.chkForce)
        self.chkForce.setVisible(False)

        self.layMain.addWidget(self.frmTrenner1)

        self.layMain.addLayout(self.layButtons)

        self.layButtons.addWidget(self.btnLos)

    def createTrigger(self):
        self.cboMethode.currentIndexChanged.connect(self.indexchange)

    def indexchange(self):
        if self.cboMethode.currentText() == "POST":
            self.gui_width = 350
            self.gui_height = 700
            self.setFixedSize(self.gui_width, self.gui_height)
            self.lblZeit.setVisible(True)
            self.txtZeit.setVisible(True)
            self.lblTerminname.setVisible(True)
            self.txtTerminname.setVisible(True)
            self.chkForce.setVisible(True)
            self.lblBeschreibung.setVisible(True)
            self.txtBeschreibung.setVisible(True)
        else:
            self.gui_width = 350
            self.gui_height = 450
            self.setFixedSize(self.gui_width, self.gui_height)
            self.lblZeit.setVisible(False)
            self.txtZeit.setVisible(False)
            self.lblTerminname.setVisible(False)
            self.txtTerminname.setVisible(False)
            self.chkForce.setVisible(False)
            self.lblBeschreibung.setVisible(False)
            self.txtBeschreibung.setVisible(False)


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
