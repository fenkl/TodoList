from flask import Flask, request, jsonify, abort

import uuid
import os
from database import db
from models import TodoList, TodoEntry


BASE_DIR = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.join(BASE_DIR, 'todolist.db')}"

db.init_app(app)

with app.app_context():
    db.create_all()


@app.route('/todo-list/<list_id>', methods=['GET'])
def get_todo_list(list_id):
    todo_list = TodoList.query.get(list_id)
    if todo_list is None:
        abort(404, "Todoliste nicht gefunden")
    entries = TodoEntry.query.filter_by(list_id=list_id).all()
    return jsonify([entry.as_dict() for entry in entries])


@app.route('/todo-list/<list_id>', methods=['DELETE'])
def delete_todo_list(list_id):
    todo_list = TodoList.query.get(list_id)
    if todo_list is None:
        abort(404, "Todoliste nicht gefunden")
    entries = TodoEntry.query.filter_by(list_id=list_id).all()
    for entry in entries:
        db.session.delete(entry)
    db.session.delete(todo_list)
    db.session.commit()
    return '', 200


@app.route('/todo-list', methods=['POST'])
def create_todo_list():
    print(request.get_json())
    data = request.get_json()
    new_list = TodoList(id=str(uuid.uuid4()), name=data['name'])
    db.session.add(new_list)
    db.session.commit()
    return jsonify(new_list.as_dict()), 200


@app.route('/todo-list/<list_id>/entry', methods=['POST'])
def add_entry(list_id):
    todo_list = TodoList.query.get(list_id)
    if todo_list is None:
        abort(404, "Todoliste nicht gefunden")
    data = request.get_json()
    new_entry = TodoEntry(id=data['id'], name=data['name'], beschreibung=data['beschreibung'], list_id=list_id)
    db.session.add(new_entry)
    db.session.commit()
    return jsonify(new_entry.as_dict()), 200


@app.route('/todo-list/<list_id>/entry/<entry_id>', methods=['PUT'])
def update_entry(list_id, entry_id):
    entry = TodoEntry.query.get(entry_id)
    if entry is None or entry.list_id != list_id:
        abort(404, "Eintrag nicht gefunden")
    data = request.get_json()
    entry.name = data['name']
    entry.beschreibung = data['beschreibung']
    db.session.commit()
    return jsonify(entry.as_dict()), 200


@app.route('/todo-list/<list_id>/entry/<entry_id>', methods=['DELETE'])
def delete_entry(list_id, entry_id):
    entry = TodoEntry.query.get(entry_id)
    if entry is None or entry.list_id != list_id:
        abort(404)
    db.session.delete(entry)
    db.session.commit()
    return '', 200


if __name__ == '__main__':
    app.run(debug=True)
