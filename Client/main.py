#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import re
import requests

import json

from guis import *

if len(sys.argv) > 1:
    if sys.argv[1] == "localhost":
        base_url = "http://127.0.0.1:5000"
    else:
        print("Übergebenes Argument ist ungültig.\n\"python3 main.py localhost\" ausführen, wenn der Server auf dem "
              "localhost läuft")
        sys.exit(1)
else:
    base_url = "http://194.195.245.87:80"


def validiere_eingabe(eingabe):
    # Entfernen von Sonderzeichen
    eingabe = re.sub(r"[&?=;%#]", "", eingabe)
    # Begrenzen der Länge der Eingabe
    eingabe = eingabe[:1000]
    eingabe = eingabe.strip()
    return eingabe


def erstelleEintrag(gui):
    # Überprüfen, ob eine Liste ausgewählt ist
    if gui.cboAuwahl.currentText() == "":
        QMessageBox.about(gui, "Warnung", "Keine Todoliste ausgewählt!")
        return
    dialog = ErstelleNeu("Eintrag", gui)
    result = dialog.exec_()

    if result == QDialog.Accepted:
        eintrag_name = validiere_eingabe(dialog.name_input.text())
        eintrag_beschreibung = validiere_eingabe(dialog.beschreibung_input.text())
        todolist_id = get_selected_todolist_id(gui)
        try:
            headers = {
                "Content-Type": "application/json"
            }
            data = {
                "name": eintrag_name,
                "beschreibung": eintrag_beschreibung
            }
            json_data = json.dumps(data)
            response = requests.post(f"{base_url}/todo-list/{todolist_id}/entry", data=json_data, headers=headers)
            if response.status_code == 200:
                QMessageBox.about(gui, "Ereignis", f"{eintrag_name} angelegt!")
            else:
                QMessageBox.about(gui, "Fehler", "Fehler beim Anlegen des Eintrags")
        except requests.RequestException:
            QMessageBox.about(gui, "Fehler", "Verbindungsfehler")
        finally:
            current_index = gui.cboAuwahl.currentIndex()  # Zustand speichern
            todolisten = fuelleAuswahlBox(gui)
            gui.cboAuwahl.setCurrentIndex(current_index)  # Zustand wiederherstellen
            fuelleEintraege(gui, todolisten)


def erstelleListe(gui):
    # Dialog zum Erstellen einer neuen Liste öffnen und Ergebnis überprüfen
    dialog = ErstelleNeu("Liste", gui)
    result = dialog.exec_()

    if result == QDialog.Accepted:
        list_name = validiere_eingabe(dialog.name_input.text())
        try:
            headers = {
                "Content-Type": "application/json"
            }
            data = {
                "name": list_name
            }
            json_data = json.dumps(data)
            response = requests.post(f"{base_url}/todo-list", data=json_data, headers=headers)
            if response.status_code == 200:
                QMessageBox.about(gui, "Ereignis", f"Liste \"{list_name}\"angelegt!")
            else:
                QMessageBox.about(gui, "Fehler", "Fehler beim Anlegen der Liste")
        except requests.RequestException:
            QMessageBox.about(gui, "Fehler", "Verbindungsfehler")
        finally:
            fuelleAuswahlBox(gui)


def loescheListe(gui):
    todolist_id = get_selected_todolist_id(gui)
    if not todolist_id:
        QMessageBox.about(gui, "Fehler", "Keine Liste ausgewählt!")
        return
    try:
        requests.delete(f"{base_url}/todo-list/{todolist_id}")
    except requests.RequestException:
        QMessageBox.about(gui, "Fehler", "Verbindungsfehler")
    finally:
        aktualisiere(gui)
        QMessageBox.about(gui, "Ereignis", "Liste erfolgreich gelöscht")


def loescheEintrag(gui):
    # Überprüfen, ob ein Eintrag ausgewählt ist
    ausgewaehlter_index = gui.tableView.selectionModel().selectedIndexes()
    if not ausgewaehlter_index:
        QMessageBox.about(gui, "Fehler", "Kein Eintrag ausgewählt.")
        return

    # Ausgewählten Eintrag aus der Tabelle und auf dem Server löschen
    row = ausgewaehlter_index[0].row()
    eintrag_id = gui.model.data(gui.model.index(row, 2), Qt.UserRole + 1)
    gui.model.removeRow(row)
    todolist_id = get_selected_todolist_id(gui)

    try:
        requests.delete(f"{base_url}/todo-list/{todolist_id}/entry/{eintrag_id}")
    except requests.RequestException:
        QMessageBox.about(gui, "Fehler", "Verbindungsfehler")


def get_selected_todolist_id(gui):
    # Holt sich die aktuelle ListenID
    selected_index = gui.cboAuwahl.currentIndex()
    selected_id = gui.cboAuwahl.itemData(selected_index, Qt.UserRole)
    return selected_id


def fuelleAuswahlBox(gui) -> dict:
    # Listen vom Server abrufen und in der Auswahlbox anzeigen
    try:
        todolisten: dict = requests.get(f"{base_url}/todo-list").json()
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
    # Einträge der ausgewählten Liste vom Server abrufen und in der Tabelle anzeigen
    name_todoliste = gui.cboAuwahl.currentText()
    for todoliste in todolisten:
        if todoliste["name"] == name_todoliste:
            try:
                eintraege = requests.get(f"{base_url}/todo-list/{todoliste['id']}").json()
            except requests.RequestException:
                QMessageBox.about(gui, "Fehler", "Verbindungsfehler")
                return []
            finally:
                gui.model.clear()  # Löschen des Modells
                gui.model.setHorizontalHeaderLabels(["Name", "Beschreibung"])  # Setzen der Header
                for eintrag in eintraege:
                    item_name = QStandardItem(eintrag["name"])
                    item_beschreibung = QStandardItem(eintrag["beschreibung"])
                    item_id = QStandardItem()  # Leeren Artikel für die ID-Spalte erstellen
                    item_id.setData(eintrag["id"], Qt.UserRole + 1)  # ID als benutzerdefinierte Daten speichern
                    gui.model.appendRow([item_name, item_beschreibung, item_id])
                gui.tableView.setColumnHidden(2, True)  # ID-Spalte ausblenden
                return eintraege


def aktualisiere(gui):
    todolisten = fuelleAuswahlBox(gui)
    if gui.cboAuwahl.currentText() == "":
        gui.model.clear()  # Löschen des Modells, wenn keine Liste ausgewählt ist
    else:
        fuelleEintraege(gui, todolisten)


def main():
    app = QApplication(sys.argv)
    app.setStyleSheet("""
        QWidget {
            font-size: 18px;
            background-color: #002244;   /* Dunkleres Blau für den Hintergrund */
            color: #FFFFFF;              /* Weiße Schrift */
            }
        QCheckBox {
            border: 1px solid white;
            }
        QLabel#Title {
            color: #FFFFFF;              /* Weiße Überschrift */
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
        QTableView {
            gridline-color: #ffffff;    /* Weiße Gitterlinien */
            }
        QTableView QHeaderView::section {
            background-color: #002244;  /* Dunkelblaue Hintergrundfarbe für Überschriften */
            color: #FFFFFF;             /* Weiße Schriftfarbe für Überschriften */
            border: 1px solid #FFFFFF;  /* Weißer Rand um die Überschriften */
            }
        QPushButton {
            background-color: #FFFFFF; /* Weiße Hintergrundfarbe für Buttons */
            color: #002244;            /* Dunkelblaue Schrift auf Buttons */
            border: 2px solid #FFFFFF; /* Weißer Rand um die Buttons */
            }
        """)

    gui = TodoList_gui()
    gui.show()
    todolisten: dict = fuelleAuswahlBox(gui)
    gui.btnDeleteEntry.clicked.connect(lambda: loescheEintrag(gui))
    gui.cboAuwahl.currentIndexChanged.connect(lambda: fuelleEintraege(gui, todolisten))
    gui.btnAddList.clicked.connect(lambda: erstelleListe(gui))
    gui.btnAddEntry.clicked.connect(lambda: erstelleEintrag(gui))
    gui.btnRefresh.clicked.connect(lambda: aktualisiere(gui))
    gui.btnDeleteList.clicked.connect(lambda: loescheListe(gui))
    app.exec()


if __name__ == "__main__":
    main()
