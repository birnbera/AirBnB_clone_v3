#!/usr/bin/python3
""" holds class State"""
import logging
import models
from models.base_model import BaseModel, Base
from os import getenv
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
log = logging.getLogger()


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
            log.info("fetching all cities for %s", self.name)
            city_values = models.storage.all("City").values()
            return list(filter(lambda c: c.state_id == self.id,
                               city_values))

    def __init__(self, *args, **kwargs):
        """initializes state"""
        self.name = kwargs.pop("name", "")

        log.info("State instance created for %s", self.name)
        super().__init__(*args, **kwargs)

    log.info("%s table generated", __tablename__)
