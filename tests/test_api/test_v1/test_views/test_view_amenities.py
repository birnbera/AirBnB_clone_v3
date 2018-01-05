#!/usr/bin/python3
"""Tests for index view of the api v1"""
import json
import unittest
from models import classes
from random import randint
from api.v1.app import app
from unittest.mock import patch
from datetime import datetime, timedelta


class TestAmenityAPI(unittest.TestCase):
    """Class to hold tests for amenities endpoint for API v1"""
    @classmethod
    def setUpClass(self):
        """Create test client for all calls to api/app"""
        app.testing = True
        self.client = app.test_client()
        self.Amenity = classes["Amenity"]

    def setUp(self):
        """Need two mock storage objects: one for the storage instance used in
        the, api directly (e.g. `storage.all`), another for storage called
        within classes themselves."""
        self.patcher1 = patch('api.v1.views.amenities.storage', autospec=True)
        self.patcher2 = patch('models.storage', autospec=True)
        self.mock_api_storage = self.patcher1.start()
        self.mock_class_storage = self.patcher2.start()

    def tearDown(self):
        """Stop mocking me"""
        self.patcher1.stop()
        self.patcher2.stop()

    def test_all_amenities(self):
        """Test route to return all amenity objects as json"""
        self.mock_api_storage.return_value = {}
        rv = self.client.get('/api/v1/amenities')
        self.assertEqual(self.mock_api_storage.all.call_count, 1)
        self.assertNotEqual(self.mock_api_storage.all.call_args, ())
        self.assertEqual(self.mock_api_storage.all.call_args[0][0], "Amenity")
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
        self.mock_api_storage.all.return_value = d
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

    def test_get_amenity(self):
        """Test route to get single amenity instance"""
        self.mock_api_storage.get.return_value = None
        amenity_id = "notarealid"
        rv = self.client.get('/api/v1/amenities/{}'.format(amenity_id))
        self.assertTrue(self.mock_api_storage.get.called)
        self.assertEqual(self.mock_api_storage.get.call_args,
                         (("Amenity", amenity_id),))
        self.assertEqual(rv.status_code, 404)
        self.assertEqual(json.loads(rv.get_data(as_text=True)),
                         {"error": "Not found"})

        a = self.Amenity()
        self.mock_class_storage.reset_mock()
        self.mock_api_storage.get.return_value = a
        amenity_id = a.id
        rv = self.client.get('/api/v1/amenities/{}'.format(amenity_id))
        self.assertEqual(rv.status_code, 200)
        self.assertTrue(self.mock_api_storage.get.called)
        self.assertEqual(self.mock_api_storage.get.call_args,
                         (("Amenity", amenity_id),))
        self.assertEqual(json.loads(rv.get_data(as_text=True)),
                         a.to_dict())

    def test_add_amenity(self):
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
        self.assertTrue(self.mock_class_storage.new.called)
        self.assertTrue(self.mock_class_storage.save.called)
        self.assertEqual(rv.status_code, 201)
        new_amty = json.loads(rv.get_data(as_text=True))
        self.assertEqual(new_amty.get("name"), data.get("name"))
        self.assertNotEqual(new_amty.get("id"), data.get("id"))
        self.assertNotEqual(new_amty.get("created_at"), data.get("created_at"))
        self.assertNotEqual(new_amty.get("updated_at"), data.get("updated_at"))

        data.update({"name": "Shleem"})
        self.mock_api_storage.all.return_value = {
            "new_amenity": self.Amenity(name="Shleem")
        }
        rv = self.client.post('/api/v1/amenities', headers=headers,
                              data=json.dumps(data))
        self.assertEqual(rv.status_code, 200)
        new_amty = json.loads(rv.get_data(as_text=True))
        self.assertEqual(new_amty.get("name"), data.get("name"))
        self.assertNotEqual(new_amty.get("id"), data.get("id"))
        self.assertNotEqual(new_amty.get("created_at"), data.get("created_at"))
        self.assertNotEqual(new_amty.get("updated_at"), data.get("updated_at"))

    def test_delete_amenity(self):
        """Test route to delete existing amenity"""
        self.mock_api_storage.get.return_value = None
        amenity_id = "notarealid"
        rv = self.client.delete('/api/v1/amenities/{}'.format(amenity_id))
        self.assertEqual(self.mock_api_storage.get.call_args,
                         (("Amenity", amenity_id),))
        self.assertEqual(rv.status_code, 404)
        self.assertEqual(json.loads(rv.get_data(as_text=True)),
                         {"error": "Not found"})

        a = self.Amenity()
        self.mock_class_storage.reset_mock()
        self.mock_api_storage.get.return_value = a
        amenity_id = a.id
        rv = self.client.delete('/api/v1/amenities/{}'.format(amenity_id))
        self.assertEqual(self.mock_api_storage.get.call_args,
                         (("Amenity", amenity_id),))
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(json.loads(rv.get_data(as_text=True)), {})
        self.assertTrue(self.mock_class_storage.delete.called)
        self.assertTrue(self.mock_api_storage.save.called)

    def test_update_amenity(self):
        """Test route to update amenity values"""
        headers = {"Content-type": "application/json"}

        self.mock_api_storage.get.return_value = None
        amenity_id = "notarealid"
        rv = self.client.put('/api/v1/amenities/{}'.format(amenity_id))
        self.assertEqual(self.mock_api_storage.get.call_args,
                         (("Amenity", amenity_id),))
        self.assertEqual(rv.status_code, 404)
        self.assertEqual(json.loads(rv.get_data(as_text=True)),
                         {"error": "Not found"})

        a = self.Amenity(name="Plumbus")
        amenity_id = a.id
        data = a.to_dict()
        data.pop('__class__', None)
        data.update({"name": "Shleem"})
        data = json.dumps(data)

        self.mock_api_storage.get.return_value = a
        rv = self.client.put('/api/v1/amenities/{}'.format(amenity_id),
                             data='{}')
        self.assertEqual(rv.status_code, 400)
        self.assertEqual(json.loads(rv.get_data(as_text=True)),
                         {'error': "Not a JSON"})

        rv = self.client.put('/api/v1/amenities/{}'.format(amenity_id),
                             headers=headers)
        self.assertEqual(rv.status_code, 400)
        self.assertEqual(json.loads(rv.get_data(as_text=True)),
                         {'error': "Not a JSON"})

        self.mock_class_storage.reset_mock()
        rv = self.client.put('/api/v1/amenities/{}'.format(amenity_id),
                             headers=headers, data=data)
        self.assertEqual(self.mock_api_storage.get.call_args,
                         (("Amenity", amenity_id),))
        self.assertTrue(self.mock_class_storage.save.called)
        self.assertEqual(a.name, "Shleem")
