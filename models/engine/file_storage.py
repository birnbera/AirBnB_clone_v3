#!/usr/bin/python3
"""
Contains the FileStorage class
"""
import json
from models import classes


class FileStorage:
    """serializes instances to a JSON file & deserializes back to instances"""
    # string - path to the JSON file
    __file_path = "file.json"
    # dictionary - empty but will store all objects by <class name>.id
    __objects = {}

    def all(self, cls=None):
        """returns the dictionary __objects"""
        if not cls:
            return self.__objects
        elif type(cls) == str:
            return {k: v for k, v in self.__objects.items()
                    if v.__class__.__name__ == cls}
        else:
            return {k: v for k, v in self.__objects.items()
                    if v.__class__ == cls}

    def new(self, obj):
        """sets in __objects the obj with key <obj class name>.id"""
        if obj is not None:
            key = obj.__class__.__name__ + "." + obj.id
            self.__objects[key] = obj

    def save(self):
        """serializes __objects to the JSON file (path: __file_path)"""
        class MyEncoder(json.JSONEncoder):
            def default(self, o):
                try:
                    return o.to_dict(to_storage=True)
                except AttributeError as e:
                    return o

        with open(self.__file_path, 'w') as f:
            json.dump(self.__objects, f, cls=MyEncoder)

    def reload(self):
        """deserializes the JSON file to __objects"""
        def object_hook(o):
            if '__class__' in o:
                oclass = o['__class__']
                return classes[oclass](**o)
            else:
                return o

        try:
            with open(self.__file_path, 'r') as f:
                self.__objects = json.load(f, object_hook=object_hook)
        except FileNotFoundError:
            self.__objects.clear()

    def delete(self, obj=None):
        """delete obj from __objects if it’s inside"""
        if obj is not None:
            del self.__objects[obj.__class__.__name__ + '.' + obj.id]
            self.save()

    def close(self):
        """Deserialize JSON file to objects"""
        self.__objects.clear()
        self.reload()

    def get(self, cls, id):
        """Returns obj based on cls and id else None"""
        return self.__objects.get(cls + '.' + id, None) \
            if type(cls) == str and type(id) == str else None

    def count(self, cls=None):
        """Count number of objects in storage or specific number
        of cls objects"""
        return len(self.all(cls))
