#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import re
import requests

import json

from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from guis import *


class ZeigeErgebnisse(QDialog):
    def __init__(self, ergebnis, strEreignis="Ergebnisanzeige"):
        QDialog.__init__(self)
        self.resize(400, 400)

        self.create_widgets()
        self.create_layout(ergebnis)
        self.setWindowTitle(strEreignis)

    def create_widgets(self):
        self.ergebnis = QTextEdit()
        self.ergebnis.setFixedSize(380, 350)
        # self.ergebnis.

    def create_layout(self, ergebnis):
        self.main_layout = QVBoxLayout()

        self.setLayout(self.main_layout)

        self.ergebnis_layout = QHBoxLayout()
        self.main_layout.addLayout(self.ergebnis_layout)
        self.ergebnis_layout.addWidget(self.ergebnis)
        self.ergebnis.setText(ergebnis)


class Abfrage:
    def __init__(self, parameters):
        self.api_baseurl = "127.0.0.1:5000"


def fuelleAuswahlBox(gui) -> dict:
    try:
        todolisten: dict = requests.get("http://127.0.0.1:5000/todo-list").json()
    except requests.RequestException:
        ergebnisse = ZeigeErgebnisse("Fehler bei Verbindung", "Verbindungsfehler")
        ergebnisse.show()
        return
    for todoliste in todolisten:
        gui.cboAuwahl.addItem(todoliste["name"])
    return todolisten


def fuelleEintraege(gui, todolisten: dict):
    name_todoliste = gui.cboAuwahl.currentText()
    for todoliste in todolisten:
        if todoliste["name"] == name_todoliste:
            try:
                eintraege = requests.get(f"http://127.0.0.1:5000/todo-list/{todoliste['id']}").json()
            except requests.RequestException:
                ergebnisse = ZeigeErgebnisse("Fehler bei Verbindung", "Verbindungsfehler")
                ergebnisse.show()
                return
            for eintrag in eintraege:
                item_name = QStandardItem(eintrag["name"])
                item_beschreibung = QStandardItem(eintrag["beschreibung"])
                gui.model.appendRow([item_name, item_beschreibung])
            return eintraege


def main():
    app = QApplication(sys.argv)
    app.setStyleSheet("""
        QWidget {
            font-size: 18px;
            }
        QCheckBox {
            border: 1px solid black;
            }
        QLabel#Title {
            color: #2b4878;
            font-size: 24px;
            font-weight: bold;
            }
        .whitebg { background-color: white; }
        QFrame {
            background: transparent;
            }
        QCalendarWidget {
            background-color: #2b4878;
            }
        """)
    # TODO: Vebrindungsfehler abfangen
    gui = ChooseParameters_gui()
    gui.show()
    todolisten: dict = fuelleAuswahlBox(gui)
    gui.cboAuwahl.currentIndexChanged.connect(lambda: fuelleEintraege(gui, todolisten))
    app.exec()


if __name__ == "__main__":
    main()
    #app = QApplication(sys.argv)
    #ergebnis = ZeigeErgebnisse("test")
    #ergebnis.show()
    #app.exec()
