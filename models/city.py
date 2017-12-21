#!/usr/bin/python3
""" holds class City"""
import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey


class City(BaseModel, Base):
    """Representation of city """
    __tablename__ = 'cities'
    name = Column(String(128),
                  nullable=False)
    state_id = Column(String(60),
                      ForeignKey('states.id'),
                      nullable=False)
    places = relationship("Place",
                          backref="cities",
                          cascade="all, delete-orphan")

    def __init__(self, *args, **kwargs):
        """initializes city"""
        self.name = kwargs.pop("name", "")
        self.state_id = kwargs.pop("state_id", "")
        super().__init__(*args, **kwargs)
