#!/usr/bin/python3
"""Tests for index view of the api v1"""
import json
import unittest
from api.v1.app import app
from unittest.mock import patch
from models.amenity import Amenity
from models.engine.db_storage import name2class


class TestAmenityAPI(unittest.TestCase):
    """Class to hold tests for amenities endpoint for API v1"""
    @classmethod
    def setUpClass(self):
        """Create test client for all calls to api/app"""
        app.testing = True
        self.client = app.test_client()

    @patch('models.storage.all', autospec=True)
    def test_all_amenities(self, mock_storage):
        """Test route to return all amenity objects as json"""
        mock_storage.return_value = {}
        rv = self.client.get('/api/v1/amenities')
        self.assertEqual(mock_storage.call_count, 1)
        self.assertNotEqual(mock_storage.call_args, ())
        self.assertEqual(mock_storage.call_args[0][0], "Amenity")
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(json.loads(rv.get_data(as_text=True)), [])
        def mock_return(cls):
            d = {}
            otype = name2class.get(cls)
            for _ in range(5):
                obj = otype()
                d[cls + '.' + obj.id] = obj
            return d
        d = mock_return("Amenity")
        mock_storage.return_value = d
        a = Amenity()
        rv = self.client.get('/api/v1/amenities')
        returned_amenities = json.loads(rv.get_data(as_text=True))
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(len(returned_amenities), 5)
        self.assertEqual(sorted(returned_amenities[0].keys()),
                         sorted(a.to_dict().keys()))
        self.assertEqual(sorted(map(lambda a: a.get('id'),
                                    returned_amenities)),
                         sorted(map(lambda v: v.id,
                                    d.values())))
