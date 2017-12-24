#!/usr/bin/python3
""" holds class Amenity"""
import logging
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
log = logging.getLogger()


class Amenity(BaseModel, Base):
    """Representation of Amenity """
    __tablename__ = 'amenities'
    name = Column(String(128),
                  nullable=False)

    def __init__(self, *args, **kwargs):
        """initializes Amenity"""
        self.name = kwargs.pop("name", "")

        log.info("Amenity instance created for %s", self.name)
        super().__init__(*args, **kwargs)

    log.info("%s table generated", __tablename__)
