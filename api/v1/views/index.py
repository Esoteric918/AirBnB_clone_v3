#!/usr/bin/python3

from api.v1.views import app_views
from flask import Flask, jsonify
from models import storage


@app_views.route('/status', strick_slashes=False)
def status():
    return jsonify(status="OK")

@app_views.route('/api/v1/stats')
def stats():
    return jsonify(amenities=storage.count("Amenity"),
                   cities=storage.count("City"),
                   places=storage.count("Place"),
                   reviews=storage.count("Review"),
                   states=storage.count("State"),
                   user=storage.count("User"))
