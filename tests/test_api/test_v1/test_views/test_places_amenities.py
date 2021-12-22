#!/usr/bin/python3
"""Test the api reviews module"""
import unittest
from api.v1.app import app
from flask import Flask
from models import storage
from models import amenity
from models.amenity import Amenity
from models.place import Place
from models.user import User
from models.city import City
from models.state import State
import json
from os import getenv


class TestAPIAemnities(unittest.TestCase):
    """tests the app module"""
    @classmethod
    def setUpClass(self):
        app.config['TESTING'] = True
        self.app = app.test_client()
        st = State(name="Test")
        st.save()
        ct = City(name="Test", state_id=st.id)
        ct.save()
        self.user = User(name="Test", email="test@test.test", password="test")
        self.user.save()
        self.pl = Place(name="Test", city_id=ct.id, user_id=self.user.id)
        self.pl.save()

    def testGET(self):
        """tests places_amenities GET"""
        response = self.app.get(
            '/api/v1/places/{}/amenities'.format(self.pl.id))
        self.assertEqual(response.status_code, 200)

    def testPOST(self):
        """tests POST route"""
        amenity = Amenity(name="Test")
        amenity.save()
        response = self.app.post(
            '/api/v1/places/{}/amenities/{}'.format(self.pl.id, amenity.id))
        self.assertEqual(response.status_code, 201)

    def testDELETE(self):
        """tests DELETE route"""
        amenity = Amenity(name="Test")
        amenity.save()
        if getenv("HBNB_TYPE_STORAGE") == 'db':
            self.pl.amenities.append(amenity)
        else:
            self.pl.amenity_ids.append(amenity.id)
        self.pl.save()
        self.assertTrue(amenity in self.pl.amenities)
        response = self.app.delete(
            '/api/v1/places/{}/amenities/{}'.format(self.pl.id, amenity.id))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(amenity in self.pl.amenities)
        p = storage.get(Place, self.pl.id)
        c = False
        for a in p.amenities:
            if a.id == amenity.id:
                c = True
        self.assertFalse(c)
        res = self.app.get(
            '/api/v1/places/{}/amenities'.format(self.pl.id))
        b = False
        r = res.json
        for a in r:
            if a.get('id') == amenity.id:
                b = True
        self.assertFalse(b)
