# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.todo_entry import TodoEntry  # noqa: E501
from swagger_server.models.todo_list import TodoList  # noqa: E501
from swagger_server.test import BaseTestCase


class TestDefaultController(BaseTestCase):
    """DefaultController integration test stubs"""

    def test_todo_list_get(self):
        """Test case for todo_list_get

        Alle ToDo Listen IDs abrufen
        """
        response = self.client.open(
            '/todo-list',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_todo_list_list_id_delete(self):
        """Test case for todo_list_list_id_delete

        Eine spezifische ToDo-Liste löschen
        """
        response = self.client.open(
            '/todo-list/{list_id}'.format(list_id='list_id_example'),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_todo_list_list_id_entry_entry_id_delete(self):
        """Test case for todo_list_list_id_entry_entry_id_delete

        Ein spezifischer ToDo-Eintrag löschen
        """
        response = self.client.open(
            '/todo-list/{list_id}/entry/{entry_id}'.format(list_id='list_id_example', entry_id='entry_id_example'),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_todo_list_list_id_entry_entry_id_put(self):
        """Test case for todo_list_list_id_entry_entry_id_put

        Ein spezifischer ToDo-Eintrag aktualisieren
        """
        body = TodoEntry()
        response = self.client.open(
            '/todo-list/{list_id}/entry/{entry_id}'.format(list_id='list_id_example', entry_id='entry_id_example'),
            method='PUT',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_todo_list_list_id_entry_post(self):
        """Test case for todo_list_list_id_entry_post

        Einen Eintrag zu einer spezifischen ToDo-Liste hinzufügen
        """
        body = TodoEntry()
        response = self.client.open(
            '/todo-list/{list_id}/entry'.format(list_id='list_id_example'),
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_todo_list_list_id_get(self):
        """Test case for todo_list_list_id_get

        Eine spezifische ToDo-Liste und ihre Einträge abrufen
        """
        response = self.client.open(
            '/todo-list/{list_id}'.format(list_id='list_id_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_todo_list_post(self):
        """Test case for todo_list_post

        Eine neue ToDo-Liste erstellen
        """
        body = TodoList()
        response = self.client.open(
            '/todo-list',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
