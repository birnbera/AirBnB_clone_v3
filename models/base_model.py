#!/usr/bin/python3
"""
Contains class BaseModel
"""

import logging
from datetime import datetime
import models
from sqlalchemy import Column, String
from sqlalchemy.dialects.mysql import DATETIME
from sqlalchemy.ext.declarative import declarative_base
import uuid

log = logging.getLogger()

time_fmt = "%Y-%m-%dT%H:%M:%S.%f"

Base = declarative_base()


class BaseModel:
    """The BaseModel class from which future classes will be derived"""
    id = Column(String(60), nullable=False, primary_key=True)
    created_at = Column(DATETIME(fsp=6), nullable=False,
                        default=datetime.utcnow)
    updated_at = Column(DATETIME(fsp=6), nullable=False,
                        default=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        """Initialization of the base model"""
        self.id = kwargs.pop('id', str(uuid.uuid4()))
        self.created_at = kwargs.pop('created_at', datetime.now())
        self.updated_at = kwargs.pop('updated_at', self.created_at)
        if type(self.created_at) is str:
            self.created_at = datetime.strptime(self.created_at, time_fmt)
        if type(self.updated_at) is str:
            self.updated_at = datetime.strptime(self.updated_at, time_fmt)

        log.info("attributes defined for instance %s.%s", self.name, self.id)

        models.storage.new(self)


    def __str__(self):
        """String representation of the BaseModel class"""
        log.info("__str__ magic method called for instance: %s", self.name)
        return "[{:s}] ({:s}) {}".format(self.__class__.__name__, self.id,
                                         self.to_dict())

    def save(self):
        """updates the attribute 'updated_at' with the current datetime"""
        log.info("save method called for instance: %s", self.name)
        self.updated_at = datetime.now()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        """returns a dictionary containing all keys/values of the instance"""
        log.info("to_dict method called for instance: %s", self.name)
        new_dict = self.__dict__.copy()
        if "created_at" in new_dict:
            new_dict["created_at"] = new_dict["created_at"].isoformat()
        if "updated_at" in new_dict:
            new_dict["updated_at"] = new_dict["updated_at"].isoformat()
        new_dict["__class__"] = self.__class__.__name__
        new_dict.pop('_sa_instance_state', None)
        return new_dict

    def delete(self):
        """Delete current instance from storage by calling its delete method"""
        log.info("delete method called for instance: %s", self.name)
        models.storage.delete(self)
