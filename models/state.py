#!/usr/bin/python3
""" holds class State"""
import models
from models import BaseModel, Base
from os import getenv
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class State(BaseModel, Base):
    """Representation of state """
    __tablename__ = 'states'
    name = Column(String(128),
                  nullable=False)

    if getenv("HBNB_TYPE_STORAGE") in ["db", "sl"]:
        cities = relationship("City",
                              cascade="all, delete",
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
