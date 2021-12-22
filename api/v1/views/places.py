#!/usr/bin/python3
"""
Flask route that returns json status response
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.place import Place


@app_views.route('/cities/<city_id>/places', methods=['GET', 'POST'],
                 strict_slashes=False)
def places_per_city(city_id):
    """
        places route to handle http method for requested places by city
    """
    city_obj = storage.get('City', city_id)
    if city_obj is None:
        abort(404)

    if request.method == 'GET':
        all_places = storage.all('Place')
        city_places = [obj.to_dict() for obj in all_places.values()
                       if obj.city_id == city_id]
        return jsonify(city_places)

    if request.method == 'POST':
        req_json = request.get_json()
        if req_json is None:
            abort(400, 'Not a JSON')
        user_id = req_json.get("user_id")
        if user_id is None:
            abort(400, 'Missing user_id')
        user_obj = storage.get('User', user_id)
        if user_obj is None:
            abort(404)
        if req_json.get("name") is None:
            abort(400, 'Missing name')
        req_json['city_id'] = city_id
        new_object = Place(**req_json)
        storage.new(new_object)
        storage.save()
        return jsonify(new_object.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def places_with_id(place_id):
    """
        places route to handle http methods for given place
    """
    place_obj = storage.get('Place', place_id)
    if place_obj is None:
        abort(404, 'Not found')

    if request.method == 'GET':
        return jsonify(place_obj.to_dict())

    if request.method == 'DELETE':
        storage.delete(place_obj)
        storage.save()
        return jsonify({}), 200

    if request.method == 'PUT':
        req_json = request.get_json()
        if req_json is None:
            abort(400, 'Not a JSON')
        for key in req_json:
            if key not in ['id',
                           'user_id',
                           'city-id',
                           'created_at',
                           'updated_at']:
                setattr(place_obj, key, req_json[key])
        place_obj.save()
        return jsonify(place_obj.to_dict()), 200


@app_views.route('/places_search', methods=['POST'],
                 strict_slashes=False)
def places_search():
    """search filters for places"""
    filter_dict = request.get_json()
    if not filter_dict:
        abort(400, "Not a JSON")
    city_ids = filter_dict.get('cities')
    cities = []
    if 'states' in filter_dict.keys():
        for state_id in filter_dict.get('states'):
            st = storage.get('State', state_id)
            if st:
                for city in st.cities:
                        cities.append(city)
    if city_ids:
        for city_id in city_ids:
            city = storage.get('City', city_id)
            if city and city not in cities:
                cities.append(city)
    if len(cities) == 0:
        places = [place for place in storage.all('Place').values()]
    else:
        places = []
        for city in cities:
            places.append(place for place in city.places)
    am_ids = filter_dict.get('amenities')
    if not am_ids or len(am_ids) == 0:
        result = [place.to_dict() for place in places]
    else:
        result = []
        for place in places:
            for amenity in place.amenities:
                has_amenity = True
                if amenity.id not in am_ids:
                    has_amenity = False
                    break
            if has_amenity is True:
                result.append(place.to_dict())
    return jsonify(result)
