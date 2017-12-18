#!/usr/bin/python3
""" holds class User"""
import models
from models.base_model import BaseModel, Base
from os import getenv
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String


class User(BaseModel, Base):
    """Representation of a user """
    if getenv('HBNB_TYPE_STORAGE') == 'db':
        __tablename__ = 'users'
        email = Column(String(128),
                       nullable=False)
        password = Column(String(128),
                          nullable=False)
        first_name = Column(String(128),
                            nullable=True)
        last_name = Column(String(128),
                           nullable=True)
        places = relationship("Place",
                              backref="user",
                              cascade="all, delete-orphan")
        reviews = relationship("Review",
                               backref="user",
                               cascade="all, delete-orphan")
    else:

        def __init__(self, *args, email="", password="",
                     first_name="", last_name="", **kwargs):
            """initializes user"""
            self.email = email
            self.password = password
            self.first_name = first_name
            self.last_name = last_name
            super().__init__(*args, **kwargs)
