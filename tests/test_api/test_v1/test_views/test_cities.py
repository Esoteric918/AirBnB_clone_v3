#!/usr/bin/python3
"""Test the api cities module"""
import unittest
from api.v1.app import app
from flask import Flask
from models import storage
from models.city import City
from models.state import State
import json


class TestAPIAemnities(unittest.TestCase):
    """tests the app module"""
    @classmethod
    def setUpClass(self):
        app.config['TESTING'] = True
        self.app = app.test_client()
        self.st = State(name="Test")
        self.st.save()

    def testCitiesGET(self):
        """tests the /api/v1/cities route"""
        response = self.app.get(
            '/api/v1/states/{}/cities'.format(self.st.id))
        self.assertEqual(response.status_code, 200)

    def testCitiesPOST(self):
        """tests POST for cities"""
        start = storage.count('City')
        city_args = {"name": "Test", "id": "QO"}
        response = self.app.post(
            '/api/v1/states/{}/cities'.format(self.st.id),
            content_type="application/json",
            data=json.dumps(city_args),
            follow_redirects=True)
        self.assertEqual(response.status_code, 201)
        end = storage.count('City')
        self.assertEqual(start + 1, end)

    def testSingleCityGET(self):
        """tests /api/v1/cities/<city_id>"""
        # existing id
        ct = City(name="Test", state_id=self.st.id)
        ct.save()
        response = self.app.get('/api/v1/cities/{}'.format(ct.id))
        self.assertEqual(response.status_code, 200)
        # nonexistant id
        response = self.app.get('/api/v1/cities/fake')
        self.assertEqual(response.status_code, 404)

    def testSingleCityDELETE(self):
        """tests /api/v1/cities/<city_id>"""
        ct = City(name="Test", state_id=self.st.id)
        ct.save()
        response = self.app.delete('/api/v1/cities/{}'.format(ct.id))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(storage.get(City, ct.id), None)

    def testSingleCityPUT(self):
        """tests /api/v1/cities/<city_id>"""
        # with existing id and valid json
        am = City(name="Test", state_id=self.st.id)
        am.save()
        city_args = {"name": "Change", "id": "Don't change",
                        "created_at": "Don't Change"}
        am_id = am.id
        am_created_at = am.created_at
        response = self.app.put(
            '/api/v1/cities/{}'.format(am.id),
            content_type="application/json",
            data=json.dumps(city_args),
            follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(am.name, "Change")
        self.assertEqual(am_id, am.id)
        self.assertEqual(am_created_at, am.created_at)
        # with existing id and no json
        response = self.app.put(
            '/api/v1/cities/{}'.format(am.id))
        self.assertEqual(response.status_code, 400)
        # with nonexistant id
        response = self.app.put('/api/v1/cities/fake')
        self.assertEqual(response.status_code, 404)
