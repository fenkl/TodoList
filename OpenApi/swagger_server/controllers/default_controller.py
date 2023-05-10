import connexion
import six

from swagger_server.models.todo_entry import TodoEntry  # noqa: E501
from swagger_server.models.todo_list import TodoList  # noqa: E501
from swagger_server import util


def todo_list_get():  # noqa: E501
    """Alle ToDo Listen IDs abrufen

     # noqa: E501


    :rtype: List[TodoList]
    """
    return 'do some magic!'


def todo_list_list_id_delete(list_id):  # noqa: E501
    """Eine spezifische ToDo-Liste löschen

     # noqa: E501

    :param list_id: 
    :type list_id: str

    :rtype: None
    """
    return 'do some magic!'


def todo_list_list_id_entry_entry_id_delete(list_id, entry_id):  # noqa: E501
    """Ein spezifischer ToDo-Eintrag löschen

     # noqa: E501

    :param list_id: 
    :type list_id: str
    :param entry_id: 
    :type entry_id: str

    :rtype: None
    """
    return 'do some magic!'


def todo_list_list_id_entry_entry_id_put(body, list_id, entry_id):  # noqa: E501
    """Ein spezifischer ToDo-Eintrag aktualisieren

     # noqa: E501

    :param body: 
    :type body: dict | bytes
    :param list_id: 
    :type list_id: str
    :param entry_id: 
    :type entry_id: str

    :rtype: TodoEntry
    """
    if connexion.request.is_json:
        body = TodoEntry.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def todo_list_list_id_entry_post(body, list_id):  # noqa: E501
    """Einen Eintrag zu einer spezifischen ToDo-Liste hinzufügen

     # noqa: E501

    :param body: 
    :type body: dict | bytes
    :param list_id: 
    :type list_id: str

    :rtype: TodoEntry
    """
    if connexion.request.is_json:
        body = TodoEntry.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def todo_list_list_id_get(list_id):  # noqa: E501
    """Eine spezifische ToDo-Liste und ihre Einträge abrufen

     # noqa: E501

    :param list_id: 
    :type list_id: str

    :rtype: List[TodoEntry]
    """
    return 'do some magic!'


def todo_list_post(body):  # noqa: E501
    """Eine neue ToDo-Liste erstellen

     # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: TodoList
    """
    if connexion.request.is_json:
        body = TodoList.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
