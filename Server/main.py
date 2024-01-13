# Autor: Francisco Fenkl
# Grundätzliche Funktion: REST-API für die Verwaltung mehrerer Todo-Listen
# Datum 1. Version: 26.04.2023
# angepasst für Merles Todoliste am 13.01.2024


import os
from database import db
from models import TodoEntry

from flask import Flask, request, jsonify, abort


# Ordner, in dem das Programm liegt
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

# Anbindung an Datenbank (im gleichen Ordner wie das Pythonskript)
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.join(BASE_DIR, 'todolist.db')}"

db.init_app(app)

with app.app_context():
    # Falls die Tabellen (aus database.py) in der Datenbank noch nicht vorhanden sind, werden sie hier erstellt
    db.create_all()


@app.route("/todo-list", methods=["GET"])
def get_todo_list():
    """
    Der User kann sich eine To-do-Liste mit ihren Einträgen ansehen
    :param list_id
    :return: Einträge der To-do-Liste mit allen Details, bei Fehler 404
    """
    entries = TodoEntry.query.all()
    return jsonify([entry.as_dict() for entry in entries])


@app.route("/todo-list/entry", methods=["POST"])
def add_entry():
    """
    Der User kann mit Angabe der entsprechenden list_id einen Eintrag zu einer To-do-Liste hinzufügen
    :param list_id
    :return: Neuen Eintrag mit Details, bei Fehler 404
    """

    data = request.get_json()
    try:
        new_entry = TodoEntry(text=data['text'])
    except Exception as e:
        abort(404, f"Fehler bei Anlegen: {e}")
        return
    db.session.add(new_entry)
    db.session.commit()
    return jsonify(new_entry.as_dict()), 200


@app.route("/todo-list/entry/<entry_id>", methods=["PUT"])
def update_entry(entry_id):
    entry = TodoEntry.query.get(entry_id)
    if entry is None:
        abort(404, "Eintrag nicht gefunden")
    data = request.get_json()
    entry.name = data["name"]
    entry.beschreibung = data["beschreibung"]
    db.session.commit()
    return jsonify(entry.as_dict()), 200


@app.route("/todo-list/entry/<entry_id>", methods=["DELETE"])
def delete_entry(entry_id):
    entry = TodoEntry.query.get(entry_id)
    if entry is None:
        abort(404)
    db.session.delete(entry)
    db.session.commit()
    return "", 200


if __name__ == "__main__":
    app.run(debug=True)
