#!/usr/bin/python3
"""API endpoint"""
from flask import jsonify
from api.v1.views import app_views
from models import storage

@app_views.route('/states', strict_slashes=False)
def all_states():
    """Return list of all states"""
    all_states = storage.all("State")
    for state in all_states.values():


    return jsonify({"status": "OK"}), 200
