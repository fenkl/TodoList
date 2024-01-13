# Autor: Francisco Fenkl
# Grundätzliche Funktion:
# Datum 1. Version: 26.04.2023
# angepasst für Merles Todoliste am 13.01.2024

from database import db


class todoliste(db.Model):
    """
    Speicherung und Verwaltung aller To-do-Listeneinträge mit dem Verweis auf ihre To-do-Liste
    """
    id = db.Column(db.String, primary_key=True)
    task = db.Column(db.String)

    def as_dict(self):
        return {
            "id": self.id,
            "text": self.task
        }
