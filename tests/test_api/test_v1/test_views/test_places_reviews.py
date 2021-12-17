#!/usr/bin/python3
"""Test the api reviews module"""
import unittest
from api.v1.app import app
from flask import Flask
from models import storage
from models.review import Review
from models.place import Place
from models.user import User
from models.city import City
from models.state import State
import json


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

    def testReviewsGET(self):
        """tests the /api/v1/reviews route"""
        response = self.app.get(
            '/api/v1/places/{}/reviews'.format(self.pl.id))
        self.assertEqual(response.status_code, 200)

    def testReviewsPOST(self):
        """tests POST for reviews"""
        start = storage.count('Review')
        review_args = {"name": "Test", "id": "QO", "user_id": self.user.id,
                       "text": "Review Text"}
        response = self.app.post(
            '/api/v1/places/{}/reviews'.format(self.pl.id),
            content_type="application/json",
            data=json.dumps(review_args),
            follow_redirects=True)
        self.assertEqual(response.status_code, 201)
        end = storage.count('Review')
        self.assertEqual(start + 1, end)

    def testSingleReviewGET(self):
        """tests /api/v1/reviews/<review_id>"""
        # existing id
        rv = Review(name="Test", place_id=self.pl.id, user_id=self.user.id,
                    text="Review text")
        rv.save()
        response = self.app.get('/api/v1/reviews/{}'.format(rv.id))
        self.assertEqual(response.status_code, 200)
        # nonexistant id
        response = self.app.get('/api/v1/reviews/fake')
        self.assertEqual(response.status_code, 404)

    def testSingleReviewDELETE(self):
        """tests /api/v1/reviews/<review_id>"""
        rv = Review(name="Test", place_id=self.pl.id, user_id=self.user.id,
                    text="Review text")
        rv.save()
        response = self.app.delete('/api/v1/reviews/{}'.format(rv.id))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(storage.get(Review, rv.id), None)

    def testSingleReviewPUT(self):
        """tests /api/v1/reviews/<review_id>"""
        # with existing id and valid json
        rv = Review(name="Test", place_id=self.pl.id, user_id=self.user.id,
                    text="Review text")
        rv.save()
        review_args = {"name": "Change", "id": "Don't change",
                        "created_at": "Don't Change"}
        pl_id = rv.id
        am_created_at = rv.created_at
        response = self.app.put(
            '/api/v1/reviews/{}'.format(rv.id),
            content_type="application/json",
            data=json.dumps(review_args),
            follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(rv.name, "Change")
        self.assertEqual(pl_id, rv.id)
        self.assertEqual(am_created_at, rv.created_at)
        # with existing id and no json
        response = self.app.put(
            '/api/v1/reviews/{}'.format(rv.id))
        self.assertEqual(response.status_code, 400)
        # with nonexistant id
        response = self.app.put('/api/v1/reviews/fake')
        self.assertEqual(response.status_code, 404)
