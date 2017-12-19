#!/usr/bin/python3
"""API endpoint"""
from flask import abort, jsonify
from api.v1.views import app_views
from models import storage

@app_views.route('/states', strict_slashes=False)
def all_states():
    """Return list of all states"""
    all_states = storage.all("State")
    return jsonify([ obj.to_dict() for obj in all_states.values() ])

@app_views.route('/states/<id>', strict_slashes=False)
def state_by_id(id):
    """Return State object based off id else raise 404"""
    state = storage.get("State", id)
    return jsonify(state.to_dict()) if state else abort(404)


