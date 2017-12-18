#!/usr/bin/python3
"""API endpoint"""
from flask import jsonify
from api.v1.views import app_views

@app_views.route('/status', strict_slashes=False)
def get_status():
    """Returns HTTP status 200"""
    return jsonify({"status": "OK"}), 200
