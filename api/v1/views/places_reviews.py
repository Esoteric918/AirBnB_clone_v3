#!/usr/bin/python3
'''City Routes'''
from api.v1.views import app_views
from models import storage
from models import review
from models.review import Review
from flask import jsonify, request, abort
from models.place import Place


@app_views.route('places/<place_id>/reviews',
                 methods=['GET'], strict_slashes=False)
def placeReview(place_id):
    """ gets all the places"""
    if place_id is None:
        abort(404)

    res = []
    for place in storage.all("Place").values():
        res.append(place.to_dict())
    return jsonify(res)


@app_views.route('reviews/<review_id>',
                 methods=['GET'], strict_slashes=False)
def getReview(review_id):
    revP = storage.get(Review, review_id)
    if revP is None:
        abort(404)
    else:
        return jsonify(revP.to_dict())

@app_views.route('reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def deleteReview(review_id):
    """Deletes a place"""
    rev_dict = storage.get(Review, review_id)
    if rev_dict is None:
        abort(404)
    else:
        storage.delete(rev_dict)
        storage.save()
        return jsonify({}), 200

@app_views.route('places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def makePlace(place_id):
    place = storage.get(Place, place_id)
    rev_dict = request.get_json()
    if not place:
        abort(404)
    elif not rev_dict:
        abort(400, "Not a JSON")
    elif "name" not in rev_dict.keys():
        abort(400, "Missing name")
    else:
        city = Place(**rev_dict)
        storage.new(rev_dict)
        storage.save()
        return jsonify(place.to_dict()), 201


@app_views.route('reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def updatePlaces(review_id):
    """update a place"""
    obj = storage.get(Review, review_id)
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
                     'place_id']:
                    pass
            else:
                setattr(obj, k, v)
        storage.save()
        newOb = obj.to_dict()
        return jsonify(newOb), 200
