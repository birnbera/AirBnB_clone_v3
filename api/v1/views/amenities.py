#!/usr/bin/python3
"""API endpoint"""
from flask import abort, jsonify, request
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity

@app_views.route('/amenities', strict_slashes=False)
def all_amenities():
    """Return list of all amenities"""
    all_amenities = storage.all("Amenity")
    return jsonify([ obj.to_dict() for obj in all_amenities.values() ])

@app_views.route('/amenities', strict_slashes=False, methods=['POST'])
def add_amenity():
    """Add amenity to states"""
    data = request.get_json()
    if not data:
        return jsonify({'Error': "Not a JSON"}), 400
    name = data.get('name', None)
    if not name:
        return jsonify({'Error': "Missing name"}), 400

    # this amenity already exists. Just update Amenity with new data
    for amenity in storage.all("Amenity").values():
        if amenity.name == name:
            [setattr(amenity, key, value) for key, value in data.items() \
                    if key not in ["id", "created_at", "updated_at"]]
            amenity.save()
            return jsonify(amenity.to_dict()), 200

    data.pop("id", None)
    data.pop("created_at", None)
    data.pop("updated_at", None)

    amenity = Amenity(**data)
    amenity.save()
    return jsonify(amenity.to_dict()), 201

@app_views.route('/amenities/<amenity_id>', strict_slashes=False, methods=['GET', 'PUT', 'DELETE'])
def manipulate_amenity(amenity_id):
    """GET/UPDATE/DELETE amenity object based off id else raise 400"""

    amenity = storage.get("Amenity", amenity_id) # Get Amenity
    if not amenity:
        abort(404)

    if request.method == 'PUT': # Update amenity
        data = request.get_json()
        if not data:
            return jsonify({'Error': "Not a JSON"}), 400
        # update attributes
        [setattr(amenity, key, value) for key, value in data.items() \
                if key not in ["id", "created_at", "updated_at"]]
        amenity.save()

    if request.method == 'DELETE': # Delete amenity
        amenity.delete()
        storage.save()
        return jsonify({}), 200 # DELETE method

    return jsonify(amenity.to_dict()), 200 # GET, PUT method
