#!/usr/bin/python3
'''Places Routes'''
from api.v1.views import app_views
from models import storage
from models.city import City
from flask import jsonify, request, abort
from models.place import Place


@app_views.route('cities/<city_id>/places',
                 methods=['GET'], strict_slashes=False)
def getALLplaces(city_id):
    """ gets all the places"""
    if city_id is None:
        abort(404)

    res = []
    for place in storage.all("Place").values():
        res.append(place.to_dict())
    return jsonify(res)


@app_views.route('places/<place_id>',
                 methods=['GET'], strict_slashes=False)
def getPlaces(place_id):
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    else:
        return jsonify(place.to_dict())

@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def deleteplaces(place_id):
    """Deletes a place"""
    place_dict = storage.get("Place", place_id)
    if place_dict is None:
        abort(404)
    else:
        storage.delete(place_dict)
        storage.save()
        return jsonify({}), 200

@app_views.route('cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def createPlaces(city_id):
    """create a place"""
    c_dict = storage.get(City, city_id)
    pl_dict = request.get_json()
    if not c_dict:
        abort(404)
    if not pl_dict:
        abort(400, "Not a JSON")

    user = pl_dict.get('user_id')
    if user is None:
        abort(400, "Missing user_id")
    s = []
    for i in storage.all("User").values():
        s.append(s.id)
    if "name" not in pl_dict.keys():
        abort(400, "Missing name")

    pl_dict = Place(**pl_dict)
    storage.new(pl_dict)
    storage.save()
    return jsonify(pl_dict.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def updatePlaces(place_id):
    """update a place"""
    obj = storage.get(Place, place_id)
    if obj is None:
        abort(404)
    res = request.get_json()
    if res is None:
        abort(400, "Not a JSON")
    else:
        for k, v in res.item():
            if k in ['id',
                     'created_at',
                     'updated_at',
                     'user_id',
                     'city_id']:
                pass
            else:
                setattr(obj, k, v)
        storage.save()
        newOb = obj.to_dict()
        return jsonify(newOb), 200
