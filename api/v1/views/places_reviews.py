#!/usr/bin/python3
'''City Routes'''
from api.v1.views import app_views
from models import storage
from models.review import Review
from flask import jsonify, request, abort
from models.place import Place


@app_views.route('/places/<place_id>/reviews',
                 methods=['GET'], strict_slashes=False)
def placeReview(place_id):
    """ gets all the places"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    res = []
    for review in place.reviews:
        res.append(review.to_dict())
    return jsonify(res)


@app_views.route('/reviews/<review_id>',
                 methods=['GET'], strict_slashes=False)
def getReview(review_id):
    revP = storage.get(Review, review_id)
    if revP is None:
        abort(404)
    else:
        return jsonify(revP.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
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


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def makeReview(place_id):
    """make a review for place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    rev_dict = request.get_json()
    if not rev_dict:
        abort(400, "Not a JSON")
    user_id = rev_dict.get("user_id")
    if user_id is None:
        abort(400, "Missing user_id")
    elif storage.get('User', user_id) is None:
        abort(404)
    elif "text" not in rev_dict.keys():
        abort(400, "Missing text")
    else:
        review = Review(**rev_dict)
        review.place_id = place.id
        storage.new(review)
        storage.save()
        return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def updateReview(review_id):
    """update a place"""
    obj = storage.get(Review, review_id)
    if obj is None:
        abort(404)
    res = request.get_json()
    if res is None:
        abort(400, "Not a JSON")
    else:
        for key in res:
            if key not in ['id',
                           'user_id',
                           'place_id',
                           'created_at',
                           'updated_at']:
                setattr(obj, key, res[key])
        obj.save()
        newOb = obj.to_dict()
        return jsonify(newOb), 200
