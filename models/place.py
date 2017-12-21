#!/usr/bin/python3
""" holds class Place"""
import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, Integer, Float, Table, ForeignKey
from sqlalchemy.orm import relationship

place_amenity = Table('place_amenity', Base.metadata,
                      Column('place_id',
                             String(60),
                             ForeignKey('places.id'),
                             primary_key=True,
                             nullable=False),
                      Column('amenity_id',
                             String(60),
                             ForeignKey('amenities.id'),
                             primary_key=True,
                             nullable=False))


class Place(BaseModel, Base):
    """Representation of Place """
    __tablename__ = 'places'
    city_id = Column(String(60),
                     ForeignKey("cities.id"),
                     nullable=False)
    user_id = Column(String(60),
                     ForeignKey('users.id'),
                     nullable=False)
    name = Column(String(128),
                  nullable=False)
    description = Column(String(1024),
                         nullable=True)
    number_rooms = Column(Integer,
                          default=0,
                          nullable=False)
    number_bathrooms = Column(Integer,
                              default=0,
                              nullable=False)
    max_guest = Column(Integer,
                       default=0,
                       nullable=False)
    price_by_night = Column(Integer,
                            default=0,
                            nullable=False)
    latitude = Column(Float, default=0.0)
    longitude = Column(Float, default=0.0)
    reviews = relationship("Review", cascade="all, delete", # add this
                           backref="places")
    amenities = relationship("Amenity",
                             secondary='place_amenity', # add quotes to place_amenity
                             viewonly=False,
                             backref="place_amenities")


    def __init__(self, *args, **kwargs):
        """initializes Place"""
        self.city_id = kwargs.pop("city_id", "")
        self.user_id = kwargs.pop("user_id", "")
        self.name = kwargs.pop("name", "")
        self.description = kwargs.pop("description", "")
        self.number_rooms = kwargs.pop("number_rooms", 0)
        self.number_bathrooms = kwargs.pop("number_bathrooms", 0)
        self.max_guest = kwargs.pop("max_guest", 0)
        self.price_by_night = kwargs.pop("price_by_night", 0)
        self.latitude = kwargs.pop("latitude", 0.0)
        self.longitude = kwargs.pop("longitude", 0.0)
        self.amenity_ids = kwargs.pop("amenity_ids", [])
        super().__init__(*args, **kwargs)

        @property
        def reviews(self):
            """attribute that returns list of Review instances"""
            values_review = models.storage.all("Review").values()
            list_review = []
            for review in values_review:
                if review.place_id == self.id:
                    list_review.append(review)
            return list_review

        @property
        def amenities(self):
            """attribute that returns list of Amenity instances"""
            values_amenity = models.storage.all("Amenity").values()
            list_amenity = []
            for amenity in values_amenity:
                if amenity.place_id == self.id:
                    list_amenity.append(amenity)
            return list_amenity
