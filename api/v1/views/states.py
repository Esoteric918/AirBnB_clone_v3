#!/usr/bin/python3
"""states routes"""
from api.v1.views import app_views
from models import storage
from models.state import State
import json


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def getStates():
    res = []
    for state in storage.all("State").values():
        res.append(state.to_dict())
    return json.dumps(res)
