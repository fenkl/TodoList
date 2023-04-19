from database import db


class TodoList(db.Model):
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String)

    def as_dict(self):
        return {
            "id": self.id,
            "name": self.name
        }


class TodoEntry(db.Model):
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
