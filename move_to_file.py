#!/usr/bin/python3
from models import storage
import json

all_objs = storage.all()

empty = {}


class MyEncoder(json.JSONEncoder):
    def default(self, o):
        return o.to_dict()


for k, v in all_objs.items():
    empty[k] = v.to_dict()


with open('file.json', 'w') as f:
    json.dump(empty, f, cls=MyEncoder)
