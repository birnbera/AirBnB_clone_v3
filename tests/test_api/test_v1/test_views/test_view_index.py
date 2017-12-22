#!/usr/bin/python3
"""Tests for index view of the api v1"""
import json
import unittest
from api.v1.app import app
from unittest.mock import patch


class TestIndexAPI(unittest.TestCase):
    """Class to hold tests for index endpoint for API v1"""
    @classmethod
    def setUpClass(self):
        """Create test client for all calls to api/app"""
        app.testing = True
        self.client = app.test_client()

    def test_get_status(self):
        """Test get_status() function returning 200 status from '/status'"""
        rv = self.client.get('/api/v1/status')
        self.assertEqual({"status": "OK"},
                         json.loads(rv.get_data(as_text=True)))
        self.assertEqual(rv.status_code, 200)
        self.assertTrue('Content-Type' in rv.headers)
        self.assertEqual(rv.headers.get('Content-Type'), 'application/json')

    @patch('models.storage.count', autospec=True)
    def test_get_count(self, mock_count):
        """Test get_count() function returning the number of each type
        of class object in storage from '/stats'"""
        def mock_returns(cls):
            d = {
                "Amenity": 47,
                "City": 36,
                "Place": 154,
                "Review": 718,
                "State": 27,
                "User": 31,
            }
            return d.get(cls, None)
        mock_count.side_effect = mock_returns
        rv = self.client.get('/api/v1/stats')
        expected = {
            "amenities": 47,
            "cities": 36,
            "places": 154,
            "reviews": 718,
            "states": 27,
            "users": 31
        }
        self.assertEqual(expected, json.loads(rv.get_data(as_text=True)))

    def test_404(self):
        """Test the result of querying a route that does not exist"""
        rv = self.client.get('/api/v1/nop')
        self.assertEqual(rv.status_code, 404)
        self.assertTrue('Content-Type' in rv.headers)
        self.assertEqual(rv.headers.get('Content-Type'), 'application/json')
        self.assertEqual({"error": "Not found"},
                         json.loads(rv.get_data(as_text=True)))
