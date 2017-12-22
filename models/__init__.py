#!/usr/bin/python3
"""
initialize the models package
"""

from os import getenv

# DBSTORAGE or IN MEMORY STORAGE
if getenv("HBNB_TYPE_STORAGE") in ["db", "sl"]:
    from models.engine.db_storage import DBStorage
    storage = DBStorage()
# FILESTORAGE
else:
    from models.engine.file_storage import FileStorage
    storage = FileStorage()
storage.reload()
