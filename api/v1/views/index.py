#!/usr/bin/python3
"""API endpoint"""
from flask import jsonify
from api.v1.views import app_views
from models import storage


@app_views.route('/status', strict_slashes=False)
def get_status():
    """Returns HTTP status 200"""
    return jsonify({"status": "OK"}), 200


@app_views.route('/stats', strict_slashes=False)
def get_count():
    """retrieves the number of each objects by type"""
    stats = {"amenities": "Amenity", "cities": "City", "places": "Place",
             "reviews": "Review", "states": "State", "users": "User"}
    return jsonify({name: storage.count(obj) for name, obj in stats.items()})
