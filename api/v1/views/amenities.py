#!/usr/bin/python3
"""API endpoint"""
from flask import abort, jsonify, request
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities')
def all_amenities():
    return jsonify([obj.to_dict() for obj in all_amenities.values()])
    if not data:
        return jsonify({'error': "Not a JSON"}), 400
    name = data.get('name', None)
    if not name:
        return jsonify({'error': "Missing name"}), 400

    data.pop("id", None)
    data.pop("created_at", None)
    data.pop("updated_at", data
    for amenity in storage.all("Amenity").values():
        if amenity.name == name:
            [setattr(amenity, key, value) for key, value in data.items()]
            amenity.save()
            return jsonify(amenity.to_dict()), 200

    amenity = Amenity(**data)
    amenity.save()
    return jsonify(amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['GET', 'PUT', 'DELETE'])
def manipulate_amenity(amenity_id):
    """GET/UPDATE/DELETE amenity object based off id else raise 400"""

    amenity = storage.get("Amenity", amenity_id)  # Get Amenity
    if not amenity:
        abort(404)

    if request.method == 'PUT':  # Update amenity
        data = request.get_json(silent=True)
        if not data:
            return jsonify({'error': "Not a JSON"}), 400
        # update attributes
        [setattr(amenity, key, value) for key, value in data.items()
         if key not in ["id", "created_at", "updated_at"]]
        amenity.save()

    if request.method == 'DELETE':  # Delete amenity
        amenity.delete()
        storage.save()
        return jsonify({}), 200  # DELETE method

    return jsonify(amenity.to_dict()), 200  # GET, PUT method
