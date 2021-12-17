#!/usr/bin/python3
"""Test the api places module"""
import unittest
from api.v1.app import app
from flask import Flask
from models import storage
from models.place import Place
from models.city import City
from models.user import User
from models.state import State
import json


class TestAPIAemnities(unittest.TestCase):
    """tests the app module"""
    @classmethod
    def setUpClass(self):
        app.config['TESTING'] = True
        self.app = app.test_client()
        st= State(name="Test")
        st.save()
        self.ct = City(name="Test", state_id=st.id)
        self.ct.save()
        self.user = User(name="Test", email="test@test.test", password="test")
        self.user.save()

    def testPlacesGET(self):
        """tests the /api/v1/places route"""
        response = self.app.get(
            '/api/v1/cities/{}/places'.format(self.ct.id))
        self.assertEqual(response.status_code, 200)

    def testPlacesPOST(self):
        """tests POST for places"""
        start = storage.count('Place')
        place_args = {"name": "Test", "id": "QO", "user_id": self.user.id}
        response = self.app.post(
            '/api/v1/cities/{}/places'.format(self.ct.id),
            content_type="application/json",
            data=json.dumps(place_args),
            follow_redirects=True)
        self.assertEqual(response.status_code, 201)
        end = storage.count('Place')
        self.assertEqual(start + 1, end)

    def testSinglePlaceGET(self):
        """tests /api/v1/places/<place_id>"""
        # existing id
        ct = Place(name="Test", city_id=self.ct.id, user_id=self.user.id)
        ct.save()
        response = self.app.get('/api/v1/places/{}'.format(ct.id))
        self.assertEqual(response.status_code, 200)
        # nonexistant id
        response = self.app.get('/api/v1/places/fake')
        self.assertEqual(response.status_code, 404)

    def testSinglePlaceDELETE(self):
        """tests /api/v1/places/<place_id>"""
        pl = Place(name="Test", city_id=self.ct.id, user_id=self.user.id)
        pl.save()
        response = self.app.delete('/api/v1/places/{}'.format(pl.id))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(storage.get(Place, pl.id), None)

    def testSinglePlacePUT(self):
        """tests /api/v1/places/<place_id>"""
        # with existing id and valid json
        pl = Place(name="Test", city_id=self.ct.id, user_id=self.user.id)
        pl.save()
        place_args = {"name": "Change", "id": "Don't change",
                        "created_at": "Don't Change"}
        pl_id = pl.id
        am_created_at = pl.created_at
        response = self.app.put(
            '/api/v1/places/{}'.format(pl.id),
            content_type="application/json",
            data=json.dumps(place_args),
            follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(pl.name, "Change")
        self.assertEqual(pl_id, pl.id)
        self.assertEqual(am_created_at, pl.created_at)
        # with existing id and no json
        response = self.app.put(
            '/api/v1/places/{}'.format(pl.id))
        self.assertEqual(response.status_code, 400)
        # with nonexistant id
        response = self.app.put('/api/v1/places/fake')
        self.assertEqual(response.status_code, 404)
