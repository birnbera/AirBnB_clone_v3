#!/usr/bin/python3
"""City API endpoint"""
from flask import abort, jsonify
from api.v1.views import app_views
from models import storage

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
