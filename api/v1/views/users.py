#!/usr/bin/python3
"""users routes"""
from api.v1.views import app_views
from models import storage
from models.user import User
from flask import jsonify, request, abort


@app_views.route('/users', methods=['GET', 'POST'],
                 strict_slashes=False)
def all_users():
    if request.method == 'GET':
        res = []
        for user in storage.all(User):
            res.append(user.to_dict())
        return jsonify(res)
    elif request.method =='POST':
        user_dict = request.get_json()
        if not user_dict:
            abort(400, "Not a JSON")
        if 'name' not in user_dict.keys():
            abort(400, "Missing name")
        user = User(**user_dict)
        storage.new(user)
        storage.save()
        return jsonify(user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['GET', 'DELETE'],
                 strict_slashes=False)
def single_user(user_id):
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    if request.method == 'GET':
        return jsonify(user.to_dict())
    elif request.method == 'DELETE':
        storage.delete(user)
        storage.save()
        return jsonify({}), 200
    elif request.method == 'PUT':
        update_dict = request.get_json()
        if not update_dict:
            abort(400, "Not a JSON")
        for key in update_dict:
            if key not in ['created_at', 'id', 'updated_at']:
                setattr(user, key, update_dict[key])
        user.save()
        return jsonify(user.to_dict()), 200
