#!/usr/bin/python3
""" holds class Amenity"""
from models import BaseModel, Base
from sqlalchemy import Column, String


class Amenity(BaseModel, Base):
    """Representation of Amenity """
    __tablename__ = 'amenities'
    name = Column(String(128),
                  nullable=False)

    def __init__(self, *args, **kwargs):
        """initializes Amenity"""
        self.name = kwargs.pop("name", "")
        super().__init__(*args, **kwargs)
