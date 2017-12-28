#!/usr/bin/python3
"""Tests for index view of the api v1"""
import json
import unittest
from models import classes
from random import randint
from api.v1.app import app
from unittest.mock import patch
from datetime import datetime, timedelta


# Need two mock storage objects: one for the storage instance used in the,
# api directly (e.g. `storage.all`), another for storage called within
# classes themselves.
@patch('api.v1.views.amenities.storage', autospec=True)
@patch('models.storage', autospec=True)
class TestAmenityAPI(unittest.TestCase):
    """Class to hold tests for amenities endpoint for API v1"""
    @classmethod
    def setUpClass(self):
        """Create test client for all calls to api/app"""
        app.testing = True
        self.client = app.test_client()
        self.Amenity = classes["Amenity"]

    def test_all_amenities(self, mock_class_storage, mock_api_storage):
        """Test route to return all amenity objects as json"""
        mock_api_storage.return_value = {}
        rv = self.client.get('/api/v1/amenities')
        self.assertEqual(mock_api_storage.all.call_count, 1)
        self.assertNotEqual(mock_api_storage.all.call_args, ())
        self.assertEqual(mock_api_storage.all.call_args[0][0], "Amenity")
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(json.loads(rv.get_data(as_text=True)), [])

        def mock_return(cls):
            d = {}
            otype = classes.get(cls)
            for _ in range(5):
                obj = otype()
                d[cls + '.' + obj.id] = obj
            return d

        d = mock_return("Amenity")
        mock_api_storage.all.return_value = d
        a = self.Amenity()
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

    def test_add_amenity(self, mock_class_storage, mock_api_storage):
        """Test route to create new amenity"""
        headers = {"Content-type": "application/json"}

        rv = self.client.post('/api/v1/amenities', data='{}')
        self.assertEqual(rv.status_code, 400)
        self.assertEqual(json.loads(rv.get_data(as_text=True)),
                         {'error': "Not a JSON"})

        rv = self.client.post('/api/v1/amenities', headers=headers)
        self.assertEqual(rv.status_code, 400)
        self.assertEqual(json.loads(rv.get_data(as_text=True)),
                         {'error': "Not a JSON"})

        rv = self.client.post('/api/v1/amenities', headers=headers, data='{}')
        self.assertEqual(rv.status_code, 400)
        self.assertEqual(json.loads(rv.get_data(as_text=True)),
                         {'error': "Missing name"})

        time1 = datetime.fromtimestamp(randint(1, 10**9))
        time2 = time1 + timedelta(seconds=randint(1, 10**9))
        data = {
            "id": "notarealid",
            "created_at": time1.isoformat(),
            "updated_at": time2.isoformat()
        }
        rv = self.client.post('/api/v1/amenities', headers=headers,
                              data=json.dumps(data))
        self.assertEqual(rv.status_code, 400)
        self.assertEqual(json.loads(rv.get_data(as_text=True)),
                         {'error': "Missing name"})

        data.update({"name": "Plumbus"})
        rv = self.client.post('/api/v1/amenities', headers=headers,
                              data=json.dumps(data))
        self.assertTrue(mock_class_storage.new.called)
        self.assertTrue(mock_class_storage.save.called)
        self.assertEqual(rv.status_code, 201)
        new_amty = json.loads(rv.get_data(as_text=True))
        self.assertEqual(new_amty.get("name"), data.get("name"))
        self.assertNotEqual(new_amty.get("id"), data.get("id"))
        self.assertNotEqual(new_amty.get("created_at"), data.get("created_at"))
        self.assertNotEqual(new_amty.get("updated_at"), data.get("updated_at"))

        data.update({"name": "Archimedes"})
        mock_api_storage.all.return_value = {
            "new_amenity": self.Amenity(name="Archimedes")
        }
        rv = self.client.post('/api/v1/amenities', headers=headers,
                              data=json.dumps(data))
        self.assertEqual(rv.status_code, 200)
        new_amty = json.loads(rv.get_data(as_text=True))
        self.assertEqual(new_amty.get("name"), data.get("name"))
        self.assertNotEqual(new_amty.get("id"), data.get("id"))
        self.assertNotEqual(new_amty.get("created_at"), data.get("created_at"))
        self.assertNotEqual(new_amty.get("updated_at"), data.get("updated_at"))
