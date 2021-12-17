#!/usr/bin/python3
"""Test the api amenities module"""
import unittest
from api.v1.app import app
from flask import Flask
from models import storage
from models.amenity import Amenity
import json


class TestAPIAemnities(unittest.TestCase):
    """tests the app module"""
    @classmethod
    def setUpClass(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    def testAmenitiesGET(self):
        """tests the /api/v1/amenities route"""
        response = self.app.get('/api/v1/amenities')
        self.assertEqual(response.status_code, 200)

    def testAmenitiesPOST(self):
        """tests POST for amenities"""
        start = storage.count('Amenity')
        amenity_args = {"name": "Test", "id": "QO"}
        response = self.app.post(
            '/api/v1/amenities',
            content_type="application/json",
            data=json.dumps(amenity_args),
            follow_redirects=True)
        self.assertEqual(response.status_code, 201)
        end = storage.count('Amenity')
        self.assertEqual(start + 1, end)

    def testSingleAmenityGET(self):
        """tests /api/v1/amenities/<amenity_id>"""
        # existing id
        am = Amenity(name="Test")
        am.save()
        response = self.app.get('/api/v1/amenities/{}'.format(am.id))
        self.assertEqual(response.status_code, 200)
        # nonexistant id
        response = self.app.get('/api/v1/amenities/fake')
        self.assertEqual(response.status_code, 404)

    def testSingleAmenityDELETE(self):
        """tests /api/v1/amenities/<amenity_id>"""
        am = Amenity(name="Test")
        am.save()
        response = self.app.delete('/api/v1/amenities/{}'.format(am.id))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(storage.get(Amenity, am.id), None)

    def testSingleAmenityPUT(self):
        """tests /api/v1/amenities/<amenity_id>"""
        # with existing id and valid json
        am = Amenity(name="Test")
        am.save()
        amenity_args = {"name": "Change", "id": "Don't change",
                        "created_at": "Don't Change"}
        am_id = am.id
        am_created_at = am.created_at
        response = self.app.put(
            '/api/v1/amenities/{}'.format(am.id),
            content_type="application/json",
            data=json.dumps(amenity_args),
            follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(am.name, "Change")
        self.assertEqual(am_id, am.id)
        self.assertEqual(am_created_at, am.created_at)
        # with existing id and no json
        response = self.app.put(
            '/api/v1/amenities/{}'.format(am.id))
        self.assertEqual(response.status_code, 400)
        # with nonexistant id
        response = self.app.put('/api/v1/amenities/fake')
        self.assertEqual(response.status_code, 404)
