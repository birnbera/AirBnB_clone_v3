#!/usr/bin/python3
"""Holds class State"""
import models
from os import getenv
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base


class State(BaseModel, Base):
    """Representation of state """
    __tablename__ = 'states'
    name = Column(String(128),
                  nullable=False)

    if getenv("HBNB_TYPE_STORAGE") == "db":
        cities = relationship("City",
                              cascade="all, delete-orphan",
                              backref="states")
    else:
        @property
        def cities(self):
            """fs getter attribute that returns City instances"""
            city_values = models.storage.all("City").values()
            return list(filter(lambda c: c.state_id == self.id,
                               city_values))

    def __init__(self, *args, **kwargs):
        """initializes state"""
        self.name = kwargs.pop("name", "")
        super().__init__(*args, **kwargs)
