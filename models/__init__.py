#!/usr/bin/python3
"""
initialize the models package
"""
from os import getenv

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

from models.base_model import BaseModel
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

classes = {
    "Amenity": Amenity,
    "City": City,
    "Place": Place,
    "Review": Review,
    "State": State,
    "User": User
}

# DBSTORAGE or IN MEMORY STORAGE
if getenv("HBNB_TYPE_STORAGE") in ["db", "sl"]:
    from models.engine.db_storage import DBStorage
    storage = DBStorage()
# FILESTORAGE
else:
    from models.engine.file_storage import FileStorage
    storage = FileStorage()
storage.reload()
