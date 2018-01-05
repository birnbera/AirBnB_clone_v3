#!/usr/bin/python3
"""
initialize the models package
"""
from os import getenv
import logging

logging.basicConfig(
        level=logging.DEBUG,
        filename="hbnb_activity.log", filemode='w',
        format="%(asctime)s - %(levelname)-7s - %(module)-10s - "
        "%(funcName)-8s: %(message)s")

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
    logging.info('Using sql storage instance')
    storage = DBStorage()
# FILESTORAGE
else:
    from models.engine.file_storage import FileStorage
    logging.info('Using file storage instance')
    storage = FileStorage()
storage.reload()
