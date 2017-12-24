#!/usr/bin/python3
"""
initialize the models package
"""

from os import getenv
import logging

logging.basicConfig(
        level=logging.DEBUG,
        filename="hbnb_activity.log", filemode='w',
        format="%(asctime)s - %(levelname)-7s - %(module)-10s - %(funcName)-8s: %(message)s")

# DBSTORAGE or IN MEMORY STORAGE
if getenv("HBNB_TYPE_STORAGE") in ["db", "sl"]:
    from models.engine.db_storage import DBStorage
    logging.info("DataBase Instance created")
    storage = DBStorage()
# FILESTORAGE
else:
    from models.engine.file_storage import FileStorage
    logging.info("FileStorage Instance created")
    storage = FileStorage()
storage.reload()
