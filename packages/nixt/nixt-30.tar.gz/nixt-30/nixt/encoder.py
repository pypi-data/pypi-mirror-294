# This file is placed in the Public Domain.


"object encoder"


import json


from .lock   import lock
from .object import Object
from .utils  import cdir


class ObjectEncoder(json.JSONEncoder):

    "ObjectEncoder"

    def __init__(self, *args, **kwargs):
        json.JSONEncoder.__init__(self, *args, **kwargs)

    def default(self, o):
        "return stringable value."
        res = None
        if isinstance(o, dict):
            res = o.items()
        elif isinstance(o, Object):
            res = vars(o)
        elif isinstance(o, list):
            res = iter(o)
        elif isinstance(o, (type(str), type(True), type(False), type(int), type(float))):
            res = o
        if not res:
            try:
                res = json.JSONEncoder.default(self, o)
            except TypeError:
                try:
                    res = o.__dict__
                except AttributeError:
                    res = repr(o)
        return res

    def encode(self, o) -> str:
        "encode object to string."
        return json.JSONEncoder.encode(self, o)

    def iterencode(self, o, _one_shot=False):
        "loop over object to encode to string."
        return json.JSONEncoder.iterencode(self, o, _one_shot)


def dump(*args, **kw):
    "dump object to file."
    kw["cls"] = ObjectEncoder
    return json.dump(*args, **kw)


def dumps(*args, **kw):
    "dump object to string."
    kw["cls"] = ObjectEncoder
    return json.dumps(*args, **kw)


def write(obj, pth):
    "write an object to disk."
    with lock:
        cdir(pth)
        with open(pth, 'w', encoding='utf-8') as ofile:
            dump(obj, ofile, indent=4)


def __dir__():
    return (
        'dump',
        'dumps',
        'write'
    )
