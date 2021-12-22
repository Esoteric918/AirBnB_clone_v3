#!/usr/bin/python3
"""interacts with the amenities on a place"""
from api.v1.views import app_views
from models import storage
from flask import jsonify, request, abort
from models.place import Place
from models.amenity import Amenity
from os import getenv


@app_views.route("/places/<place_id>/amenities",
                 methods=['GET'], strict_slashes=False)
def amenities_at_place(place_id):
    """Lists all amenities at a place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    res = []
    for amenity in place.amenities:
        res.append(amenity.to_dict())
    return jsonify(res)


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 methods=['POST', 'DELETE'], strict_slashes=False)
def change_amenities(place_id, amenity_id):
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if not place or not amenity:
        abort(404)
    if request.method == 'DELETE':
        if amenity not in place.amenities:
            abort(404)
        if getenv("HBNB_TYPE_STORAGE") == 'db':
            place.amenities.remove(amenity)
        else:
            place.amenity_ids.remove(amenity.id)
        place.save
        return jsonify({}), 200
    elif request.method == 'POST':
        if amenity not in place.amenities:
            if getenv("HBNB_TYPE_STORAGE") == 'db':
                place.amenities.append(amenity)
            else:
                place.amenity_ids.append(amenity.id)
            place.save()
            return jsonify(amenity.to_dict()), 201
        else:
            return jsonify(amenity.to_dict()), 200
