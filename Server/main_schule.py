# Autor: Francisco Fenkl
# Grundätzliche Funktion: REST-API für die Verwaltung mehrerer Todo-Listen
# Datum 1. Version: 26.04.2023

# TODO: OpenApi Spezifikation anpassen

import uuid
import os
from database import db
from models_schule import TodoList, TodoEntry

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
def get_list_ids():
    """
    Der User kann sich alle To-do-List-Ids holen
    :return:
    """
    todo_lists = TodoList.query.all()
    result = [item.as_dict() for item in todo_lists]
    return jsonify(result)


@app.route("/todo-list/<list_id>", methods=["GET"])
def get_todo_list(list_id):
    """
    Der User kann sich eine To-do-Liste mit ihren Einträgen ansehen
    :param list_id
    :return: Einträge der To-do-Liste mit allen Details, bei Fehler 404
    """
    todo_list = TodoList.query.get(list_id)
    if todo_list is None:
        abort(404, "Todoliste nicht gefunden")
    entries = TodoEntry.query.filter_by(list_id=list_id).all()
    return jsonify([entry.as_dict() for entry in entries])


@app.route("/todo-list/<list_id>", methods=["DELETE"])
def delete_todo_list(list_id):
    """
    Der User kann To-do-Listen anhand der entsprechenden list-id löschen
    :param list_id
    :return: 200, bei Fehler 404
    """
    todo_list = TodoList.query.get(list_id)
    if todo_list is None:
        abort(404, "Todoliste nicht gefunden")
    entries = TodoEntry.query.filter_by(list_id=list_id).all()
    for entry in entries:
        db.session.delete(entry)
    db.session.delete(todo_list)
    db.session.commit()
    return "", 200


@app.route("/todo-list", methods=["POST"])
def create_todo_list():
    """
    Der User kann eine To-do-Liste anlegen
    :return:
    """
    data = request.get_json()
    new_list = TodoList(id=str(uuid.uuid4()), name=data["name"])
    db.session.add(new_list)
    db.session.commit()
    return jsonify(new_list.as_dict()), 200


@app.route("/todo-list/<list_id>/entry", methods=["POST"])
def add_entry(list_id):
    """
    Der User kann mit Angabe der entsprechenden list_id einen Eintrag zu einer To-do-Liste hinzufügen
    :param list_id
    :return: Neuen Eintrag mit Details, bei Fehler 404
    """
    todo_list = TodoList.query.get(list_id)
    if todo_list is None:
        abort(404, "Todoliste nicht gefunden")
    data = request.get_json()
    try:
        new_entry = TodoEntry(id=str(uuid.uuid4()), name=data['name'], beschreibung=data['beschreibung'], list_id=list_id)
    except Exception as e:
        abort(404, f"Fehler bei Anlegen: {e}")
        return
    db.session.add(new_entry)
    db.session.commit()
    return jsonify(new_entry.as_dict()), 200


@app.route("/todo-list/<list_id>/entry/<entry_id>", methods=["PUT"])
def update_entry(list_id, entry_id):
    entry = TodoEntry.query.get(entry_id)
    if entry is None or entry.list_id != list_id:
        abort(404, "Eintrag nicht gefunden")
    data = request.get_json()
    entry.name = data["name"]
    entry.beschreibung = data["beschreibung"]
    db.session.commit()
    return jsonify(entry.as_dict()), 200


@app.route("/todo-list/<list_id>/entry/<entry_id>", methods=["DELETE"])
def delete_entry(list_id, entry_id):
    entry = TodoEntry.query.get(entry_id)
    if entry is None or entry.list_id != list_id:
        abort(404)
    db.session.delete(entry)
    db.session.commit()
    return "", 200


if __name__ == "__main__":
    app.run(debug=True)
