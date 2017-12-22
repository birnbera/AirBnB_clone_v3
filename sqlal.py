#!/usr/bin/python3

from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import uuid
from datetime import datetime

Base = declarative_base()


class TestClass(Base):
    __tablename__ = "test_table"
    name = Column(String(128), nullable=False)
    id = Column(String(128), nullable=False, primary_key=True)
    timevar = Column(DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, **kwargs):
        self.name = kwargs.pop('name')
        self.id = kwargs.pop('id', str(uuid.uuid4()))
        self.timevar = kwargs.pop('timevar', datetime.utcnow())
