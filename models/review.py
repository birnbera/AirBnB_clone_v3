#!/usr/bin/python3
""" holds class Review"""
import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey


class Review(BaseModel, Base):
    """Representation of Review """
    if getenv('HBNB_TYPE_STORAGE') == 'db':
        __tablename__ = 'reviews'
        text = Column(String(1024),
                      nullable=False)
        place_id = Column(String(60),
                          ForeignKey('places.id'),
                          nullable=False)
        user_id = Column(String(60),
                         ForeignKey('users.id'),
                         nullable=False)
    else:

        def __init__(self, *args, text="", place_id="", user_id="", **kwargs):
            """initializes Review"""
            self.text = text
            self.place_id = place_id
            self.user_id = user_id
            super().__init__(*args, **kwargs)
