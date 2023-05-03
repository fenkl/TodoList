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


def erstelleListe(gui):
    dialog = ErstelleTodoListe(gui)
    result = dialog.exec_()

    if result == QDialog.Accepted:
        list_name = dialog.name_input.text()
        try:
            headers = {
                "Content-Type": "application/json"
            }
            data = {
                "name": list_name
            }
            json_data = json.dumps(data)
            response = requests.post("http://127.0.0.1:5000/todo-list", data=json_data, headers=headers)
            if response.status_code == 200:
                QMessageBox.about(gui, "Ereignis", "Liste angelegt!")
            else:
                QMessageBox.about(gui, "Fehler", "Fehler beim Anlegen der Liste")
        except requests.RequestException:
            QMessageBox.about(gui, "Fehler", "Verbindungsfehler")
        finally:
            fuelleAuswahlBox(gui)


def loescheEintrag(gui):
    ausgewaehlter_index = gui.tableView.selectionModel().selectedIndexes()
    if not ausgewaehlter_index:
        QMessageBox.about(gui, "Fehler", "Kein Eintrag ausgewählt.")
        return
    row = ausgewaehlter_index[0].row()
    eintrag_id = gui.model.data(gui.model.index(row, 2), Qt.UserRole + 1)
    gui.model.removeRow(row)
    todolist_id = get_selected_todolist_id(gui)

    try:
        requests.delete(f"http://127.0.0.1:5000/todo-list/{todolist_id}/entry/{eintrag_id}")
    except requests.RequestException:
        QMessageBox.about(gui, "Fehler", "Verbindungsfehler")


def get_selected_todolist_id(gui):
    selected_index = gui.cboAuwahl.currentIndex()
    selected_id = gui.cboAuwahl.itemData(selected_index, Qt.UserRole)
    return selected_id

def fuelleAuswahlBox(gui) -> dict:
    try:
        todolisten: dict = requests.get("http://127.0.0.1:5000/todo-list").json()
    except requests.RequestException:
        QMessageBox.about(gui, "Fehler", "Verbindungsfehler")
        return {}
    gui.cboAuwahl.clear()
    gui.cboAuwahl.addItem("")
    for todoliste in todolisten:
        index = gui.cboAuwahl.count()
        gui.cboAuwahl.addItem(todoliste["name"])
        gui.cboAuwahl.setItemData(index, todoliste["id"],
                                  Qt.UserRole)  # ToDoList-IDs als Combobox-Daten speichern
    return todolisten


def fuelleEintraege(gui, todolisten: dict) -> list:
    name_todoliste = gui.cboAuwahl.currentText()
    for todoliste in todolisten:
        if todoliste["name"] == name_todoliste:
            try:
                eintraege = requests.get(f"http://127.0.0.1:5000/todo-list/{todoliste['id']}").json()
            except requests.RequestException:
                QMessageBox.about(gui, "Fehler", "Verbindungsfehler")
                return []
            for eintrag in eintraege:
                item_name = QStandardItem(eintrag["name"])
                item_beschreibung = QStandardItem(eintrag["beschreibung"])
                item_id = QStandardItem()  # Leeren Artikel für die ID-Spalte erstellen
                item_id.setData(eintrag["id"], Qt.UserRole + 1)  # ID als benutzerdefinierte Daten speichern
                gui.model.appendRow([item_name, item_beschreibung, item_id])
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
    gui.btnDeleteEntry.clicked.connect(lambda: loescheEintrag(gui))
    gui.cboAuwahl.currentIndexChanged.connect(lambda: fuelleEintraege(gui, todolisten))
    gui.btnAddList.clicked.connect(lambda: erstelleListe(gui))
    app.exec()


if __name__ == "__main__":
    main()
    #app = QApplication(sys.argv)
    #ergebnis = ZeigeErgebnisse("test")
    #ergebnis.show()
    #app.exec()
