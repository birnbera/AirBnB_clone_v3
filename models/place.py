#!/usr/bin/python3
""" holds class Place"""
import models
from models import BaseModel, Base
from os import getenv
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

    if getenv("HBNB_TYPE_STORAGE") in ["db", "sl"]:
        reviews = relationship("Review", cascade="all, delete-orphan",
                               backref="places")
        amenities = relationship("Amenity",
                                 secondary='place_amenity',
                                 viewonly=False,
                                 backref="place_amenities")
    else:
        @property
        def reviews(self):
            """attribute that returns list of Review instances"""
            review_values = models.storage.all("Review").values()
            return list(filter(lambda r: r.place_id == self.id,
                               review_values))

        @property
        def amenities(self):
            """attribute that returns list of Amenity instances"""
            amenity_values = models.storage.all("Amenity").values()
            return list(filter(lambda a: a.id in self.amenity_ids,
                               amenity_values))

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
        self.amenity_ids = list(map(lambda a: a if type(a) == str else a.id,
                                    kwargs.pop("amenities", [])))
        super().__init__(*args, **kwargs)
