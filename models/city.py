#!/usr/bin/python3
""" holds class City"""
import models
from models import BaseModel, Base
from os import getenv
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

    if getenv("HBNB_TYPE_STORAGE") in ["db", "sl"]:
        places = relationship("Place",
                              backref="cities",
                              cascade="all, delete-orphan")

    else:
        @property
        def places(self):
            """Return all places associated with the current city"""
            place_values = models.storage.all("Place").values()
            return list(filter(lambda p: p.city_id == self.id,
                               place_values))

    def __init__(self, *args, **kwargs):
        """initializes city"""
        self.name = kwargs.pop("name", "")
        self.state_id = kwargs.pop("state_id", "")
        super().__init__(*args, **kwargs)
