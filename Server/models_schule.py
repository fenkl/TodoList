# Autor: Francisco Fenkl
# Grundätzliche Funktion:
# Datum 1. Version: 26.04.2023

from database import db


class TodoList(db.Model):
    """
    Speicherung und Verwaltung aller To-do-Listen
    """
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String)

    def as_dict(self):
        return {
            "id": self.id,
            "name": self.name
        }


class TodoEntry(db.Model):
    """
    Speicherung und Verwaltung aller To-do-Listeneinträge mit dem Verweis auf ihre To-do-Liste
    """
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String)
    beschreibung = db.Column(db.String)
    list_id = db.Column(db.String, db.ForeignKey('todo_list.id'))

    def as_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "beschreibung": self.beschreibung,
            "list_id": self.list_id
        }
