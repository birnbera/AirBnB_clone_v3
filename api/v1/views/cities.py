#!/usr/bin/python3
"""City API endpoint"""
from flask import abort, jsonify, request
from api.v1.views import app_views
from models import storage
from models.city import City

@app_views.route('/cities', strict_slashes=False)
def all_cities():
    """Return list of all cities"""
    all_cities = storage.all("City")
    return jsonify([obj.to_dict() for obj in all_cities.values()])

@app_views.route('/cities/<id>', strict_slashes=False)
def city_by_id(id):
    """Return City object based off id else raise 404"""
    city = storage.get("City", id)
    return jsonify(city.to_dict()) if city else abort(404)

@app_views.route('/cities/<id>', strict_slashes=False, methods=['DELETE'])
def delete_city(id):
    """Return City object based off id else raise 404"""
    city = storage.get("City", id)
    if city:
        storage.delete()
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)

@app_views.route('/cities', strict_slashes=False, methods=['POST'])
def create_city():
    """Create new City object from request JSON else raise 400"""
    city = request.get_json()
    if not city:
        return jsonify({"error": "Not a JSON"}), 400
    if 'name' not in city:
        return jsonify({"error": "Missing name"}), 400
    city = City(**city)
    storage.new(city)
    city.save()
    return jsonify(city.to_dict()), 201

@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['PUT'])
def update_city(city_id):
    """Update City object using data from JSON request else raise 400"""
    city = storage.get("City", city_id)
    if not city:
        abort(404)
    updates = request.get_json()
    if not updates:
        return jsonify({"error": "Not a JSON"}), 400
    updates.pop('id', None)
    updates.pop('created_at', None)
    updates.pop('updated_at', None)
    for k,v  in updates.items():
        setattr(city, k, v)
    city.save()
    return jsonify(city.to_dict()), 200
