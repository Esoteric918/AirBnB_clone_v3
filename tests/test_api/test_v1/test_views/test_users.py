#!/usr/bin/python3
"""Test the api users module"""
import unittest
from api.v1.app import app
from flask import Flask
from models import storage
from models.user import User
import json


class TestAPIAemnities(unittest.TestCase):
    """tests the app module"""
    @classmethod
    def setUpClass(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    def testUsersGET(self):
        """tests the /api/v1/users route"""
        response = self.app.get('/api/v1/users')
        self.assertEqual(response.status_code, 200)

    def testUsersPOST(self):
        """tests POST for users"""
        start = storage.count('User')
        user_args = {"name": "Test", "id": "QO",
                     "email": "test@test.test", "password": "test"}
        response = self.app.post(
            '/api/v1/users',
            content_type="application/json",
            data=json.dumps(user_args),
            follow_redirects=True)
        self.assertEqual(response.status_code, 201)
        end = storage.count('User')
        self.assertEqual(start + 1, end)

    def testSingleUserGET(self):
        """tests /api/v1/users/<user_id>"""
        # existing id
        st = User(name="Test", email="test@test.test", password="test")
        st.save()
        response = self.app.get('/api/v1/users/{}'.format(st.id))
        self.assertEqual(response.status_code, 200)
        # nonexistant id
        response = self.app.get('/api/v1/users/fake')
        self.assertEqual(response.status_code, 404)

    def testSingleUserDELETE(self):
        """tests /api/v1/users/<user_id>"""
        st = User(name="Test", email="test@test.test", password="test")
        st.save()
        response = self.app.delete('/api/v1/users/{}'.format(st.id))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(storage.get(User, st.id), None)

    def testSingleUserPUT(self):
        """tests /api/v1/users/<user_id>"""
        # with existing id and valid json
        am = User(name="Test", email="test@test.test", password="test")
        am.save()
        user_args = {"name": "Change", "id": "Don't change",
                     "created_at": "Don't Change",
                     "email": "test@test.test", "password": "test"}
        am_id = am.id
        am_created_at = am.created_at
        response = self.app.put(
            '/api/v1/users/{}'.format(am.id),
            content_type="application/json",
            data=json.dumps(user_args),
            follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(am.name, "Change")
        self.assertEqual(am_id, am.id)
        self.assertEqual(am_created_at, am.created_at)
        # with existing id and no json
        response = self.app.put(
            '/api/v1/users/{}'.format(am.id))
        self.assertEqual(response.status_code, 400)
        # with nonexistant id
        response = self.app.put(
            '/api/v1/users/fake')
        self.assertEqual(response.status_code, 404)
