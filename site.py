#!/usr/bin/python3

class Site:
    __objects = []

    def __init__(self, *args, **kwargs):
        """initializes state"""
        self.name = kwargs.pop("name")
        self.id = kwargs.pop("id")
        self.parent_id = kwargs.pop("parent_id")
        self.new(self)

    @property
    def cities(self):
        city_values = self.__objects
        return list(filter(lambda c: c.place_id == self.id,
                           city_values))

    def new(self, obj):
        if obj is not None:
            self.__objects += obj
