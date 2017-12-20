#!/usr/bin/python3
"""API endpoint"""
from flask import abort, jsonify, request
from api.v1.views import app_views
from models import storage
from models.place import Place

@app_views.route('/cities/<city_id>/places', strict_slashes=False)
def all_places(city_id):
    """Return list of all places in respective to city"""
    all_places = storage.all("Place")
    places = [place.to_dict() for place in all_places.values() \
                if place.city_id == city_id]

    return jsonify(places) if len(places) else abort(404)

@app_views.route('/places', strict_slashes=False, methods=['POST'])
def add_place():
    """Add place to places"""
    data = request.get_json()
    if not data:
        return jsonify({'Error': "Not a JSON"}), 400
    name = data.get('name', None)
    if not name:
        return jsonify({'Error': "Missing name"}), 400

    # this place already exists. Just update place with new data
    for place in storage.all("place").values():
        if place.name == name:
            setattr(place, "name", name)
            place.save()
            return jsonify(place.to_dict()), 200

    place = place(**data)
    place.save()
    return jsonify(place.to_dict()), 201

@app_views.route('/places/<place_id>', strict_slashes=False, methods=['GET', 'PUT', 'DELETE'])
def manipulate_place(place_id):
    """GET/UPDATE/DELETE place object based off id else raise 400"""

    place = storage.get("place", place_id) # Get place
    if not place:
        abort(404)

    if request.method == 'PUT': # Update place
        data = request.get_json()
        if not data:
            return jsonify({'Error': "Not a JSON"}), 400
        # update attributes
        [setattr(place, key, value) for key, value in data.items() \
                if key not in ["id", "created_at", "updated_at"]]
        place.save()

    if request.method == 'DELETE': # Delete place
        place.delete()
        storage.save()
        return jsonify({}), 200 # DELETE method

    return jsonify(place.to_dict()), 200 # GET, PUT method
