#!/usr/bin/python3
"""Database storage engine using SQLAlchemy with a mysql+mysqldb database
connection.
"""
import json
from os import getenv
from models import Base, classes
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session


class DBStorage:
    """Class to represent database storage object"""
    __engine = None
    __session = None
    __file_path = "file.json"

    def __init__(self):
        """ creates connection to db"""
        user = getenv('HBNB_MYSQL_USER')
        passwd = getenv('HBNB_MYSQL_PWD')
        host = getenv('HBNB_MYSQL_HOST')
        database = getenv('HBNB_MYSQL_DB')

        self.in_memory_db = getenv("HBNB_TYPE_STORAGE") == 'sl'

        if self.in_memory_db:
            self.__engine = create_engine('sqlite:///:memory:')
        elif getenv('HBNB_TYPE_STORAGE') == 'db':
            self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'
                                          .format(user,
                                                  passwd,
                                                  host,
                                                  database),
                                          pool_pre_ping=True)
        if getenv('HBNB_ENV') == 'test':
            if database == 'hbnb_dev_db':
                raise Exception("Using 'hbnb_dev_db' in 'test' mode. "
                                "This will drop all tables. "
                                "Are you sure you want to do this?")
            else:
                Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """query on current db"""
        if not self.__session:
            self.reload()
        objects = {}
        if type(cls) == str:
            cls = classes.get(cls, None)
        if cls:  # return specified object
            for obj in self.__session.query(cls):
                objects[obj.__class__.__name__ + '.' + obj.id] = obj
        else:  # return all objects
            for cls in classes.values():
                for obj in self.__session.query(cls):
                    objects[obj.__class__.__name__ + '.' + obj.id] = obj
        return objects

    def reload(self):
        """load all tables"""
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        Base.metadata.create_all(self.__engine)
        self.__session = scoped_session(session_factory)
        if self.in_memory_db:
            self.reload_from_json()
            self.__session.flush()

    def reload_from_json(self):
        """deserializes the JSON file to __objects"""
        def object_hook(o):
            if '__class__' in o:
                oclass = o['__class__']
                return classes[oclass](**o)
            else:
                return o

        try:
            with open(self.__file_path, 'r') as f:
                self.__objects = json.load(f, object_hook=object_hook)
        except:
            self.__objects.clear()
            raise

    def new(self, obj):
        """add the object to the current database session"""
        # if sl then only add if obj isnt in session
        # if db then add obj regardless into session
        if not self.get(obj.__class__.__name__, obj.id) or \
                getenv('HBNB_TYPE_STORAGE') == 'db':
            self.__session.add(obj)

    def save(self):
        """commit all changes of the current database session"""
        self.__session.commit()
        if self.in_memory_db:
            self.save_to_json()

    def save_to_json(self):
        """serializes __objects to the JSON file (path: __file_path)"""
        class MyEncoder(json.JSONEncoder):
            def default(self, o):
                try:
                    return o.to_dict()
                except AttributeError as e:
                    return o

        with open(self.__file_path, 'w') as f:
            json.dump(self.all(), f, cls=MyEncoder)

    def delete(self, obj=None):
        """delete from the current database session obj if not None"""
        if not self.__session:
            self.reload()
        if obj:
            self.__session.delete(obj)

    def close(self):
        """Dispose of current session if active"""
        self.__session.remove()

    def get(self, cls, id):
        """Retrieve object based on class name and id, else None
        if not found"""
        cls = classes.get(cls, None)
        return self.__session.query(cls).filter(cls.id == id).first() \
            if cls else None

    def count(self, cls=None):
        """Count number of objects in storage or number of type `cls`"""
        return len(self.all(cls))
