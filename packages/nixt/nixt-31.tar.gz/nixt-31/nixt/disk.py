# This file is placed in the Public Domain.
# pylint: disable=C,I,R


"disk"


import os


from .decoder import read
from .encoder import write
from .lock    import disklock
from .workdir import store
from .utils   import ident


def fetch(obj, pth):
    "read object from disk."
    with disklock:
        pth2 = store(pth)
        read(obj, pth2)
        return os.sep.join(pth.split(os.sep)[-3:])


def sync(obj, pth=None):
    "sync object to disk."
    with disklock:
        if pth is None:
            pth = ident(obj)
        pth2 = store(pth)
        write(obj, pth2)
        return pth


def __dir__():
    return (
        'fetch',
        'sync'
    )
