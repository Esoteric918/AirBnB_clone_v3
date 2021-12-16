#!/usr/bin/python3

from flask import Flask, jsonify
from models import storage
from models.state import State
from api.v1.views import app_views

@app_views.route('/api/v1/states', methods=['GET'])
def getStates():
    res = []
    for state in storage.all(State).values():
        res.append(state.to_dict())
    return jsonify(res)
