#!/usr/bin/python3
""" holds class Review"""
from models import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy import ForeignKey


class Review(BaseModel, Base):
    """Representation of Review """
    __tablename__ = 'reviews'
    text = Column(String(1024),
                  nullable=False)
    place_id = Column(String(60),
                      ForeignKey('places.id'),
                      nullable=False)
    user_id = Column(String(60),
                     ForeignKey('users.id'),
                     nullable=False)

    def __init__(self, *args, **kwargs):
        """initializes Review"""
        self.text = kwargs.pop("text", "")
        self.place_id = kwargs.pop("place_id", "")
        self.user_id = kwargs.pop("user_id", "")
        super().__init__(*args, **kwargs)
