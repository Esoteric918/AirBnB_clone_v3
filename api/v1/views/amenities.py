#!/usr/bin/python3
"""amenities routes"""
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from flask import jsonify, request, abort


@app_views.route('/amenities', methods=['GET', 'POST'],
                 strict_slashes=False)
def all_amenities():
    if request.method == 'GET':
        res = []
        for amenity in storage.all(Amenity).values():
            res.append(amenity.to_dict())
        return jsonify(res)
    elif request.method == 'POST':
        amenity_dict = request.get_json()
        if not amenity_dict:
            abort(400, "Not a JSON")
        if 'name' not in amenity_dict.keys():
            abort(400, "Missing name")
        amenity = Amenity(**amenity_dict)
        storage.new(amenity)
        storage.save()
        return jsonify(amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['GET', 'DELETE'],
                 strict_slashes=False)
def single_amenity(amenity_id):
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    if request.method == 'GET':
        return jsonify(amenity.to_dict())
    elif request.method == 'DELETE':
        storage.delete(amenity)
        storage.save()
        return jsonify({}), 200
    elif request.method == 'PUT':
        update_dict = request.get_json()
        if not update_dict:
            abort(400, "Not a JSON")
        for key in update_dict:
            if key not in ['created_at', 'id', 'updated_at']:
                setattr(amenity, key, update_dict[key])
        amenity.save()
        return jsonify(amenity.to_dict()), 200
