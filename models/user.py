#!/usr/bin/python3
""" holds class User"""
import models
from models.base_model import BaseModel, Base
from os import getenv
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String


class User(BaseModel, Base):
    """Representation of a user """
    __tablename__ = 'users'
    email = Column(String(128),
                   nullable=False)
    password = Column(String(128),
                      nullable=False)
    first_name = Column(String(128),
                        nullable=True)
    last_name = Column(String(128),
                       nullable=True)

    if getenv("HBNB_TYPE_STORAGE") in ["db", "sl"]:
        places = relationship("Place",
                              backref="user",
                              cascade="all, delete-orphan")
        reviews = relationship("Review",
                               backref="user",
                               cascade="all, delete-orphan")
    else:
        @property
        def places(self):
            """Return list of places associated with the current user"""
            place_values

        @property
        def reviews(self):
            """Return list of reviews associated with the current user"""
            review_values = models.storage.all("Review").values()
            return list(filter(lambda r: r.user_id == self.id,
                               review_values))

    def __init__(self, *args, **kwargs):
        """initializes user"""
        self.email = kwargs.pop("email", "")
        self.password = kwargs.pop("password", "")
        self.first_name = kwargs.pop("first_name", "")
        self.last_name = kwargs.pop("last_name", "")
        super().__init__(*args, **kwargs)
