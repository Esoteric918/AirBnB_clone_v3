#!/usr/bin/python3
"""Test the app module"""
import unittest
from api.v1.app import app
from flask import Flask


class TestApp(unittest.TestCase):
    """tests the app module"""

    def testIsFlaskApp(self):
        """tests if app is a Flask instance"""
        self.assertIsInstance(app, Flask)
