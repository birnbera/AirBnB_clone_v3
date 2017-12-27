#!/usr/bin/python3
""" holds class User"""
import models
from hashlib import md5
from models import BaseModel, Base
from os import getenv
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String


class User(BaseModel, Base):
    """Representation of a user """
    __tablename__ = 'users'
    email = Column(String(128), nullable=False)
    _password = Column("password", String(128), nullable=False)
    first_name = Column(String(128), nullable=True)
    last_name = Column(String(128), nullable=True)

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
            place_values = models.storage.all("Place").values()
            return list(filter(lambda p: p.user_id == self.id,
                               place_values))

        @property
        def reviews(self):
            """Return list of reviews associated with the current user"""
            review_values = models.storage.all("Review").values()
            return list(filter(lambda r: r.user_id == self.id,
                               review_values))

    @property
    def password(self):
        """Getter for protected _password attribute."""
        return self._password

    @password.setter
    def password(self, pwd):
        """Setter for protected _password attribute. Only called by
        console or api to ensure the we do not re-hash hashed password"""
        self._password = md5(pwd.encode()).hexdigest()

    def __init__(self, *args, **kwargs):
        """initializes user"""
        self.email = kwargs.pop("email", "")

        # Order of setting password and _password is important
        # to prevent re-hashing hashed password or overwriting
        # previously set password.
        self.password = kwargs.pop("password", "")
        self._password = kwargs.pop("_password", self.password)

        self.first_name = kwargs.pop("first_name", "")
        self.last_name = kwargs.pop("last_name", "")
        super().__init__(*args, **kwargs)

    def to_dict(self, to_storage=False):
        """Return dictionary of all attributes of User. Do not
        include `password` attribute unless `to_storage=True`."""
        d = super().to_dict()
        if to_storage:
            d.update({"_password": self._password})
        return d
