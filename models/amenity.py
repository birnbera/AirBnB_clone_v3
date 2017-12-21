#!/usr/bin/python3
"""Holds class Amenity"""
import sqlalchemy
from sqlalchemy import Column, String
from models.base_model import BaseModel, Base


class Amenity(BaseModel, Base):
    """Representation of Amenity """
    __tablename__ = 'amenities'
    name = Column(String(128),
                  nullable=False)

    def __init__(self, *args, **kwargs):
        """initializes Amenity"""
        self.name = kwargs.pop("name", "")
        super().__init__(*args, **kwargs)
