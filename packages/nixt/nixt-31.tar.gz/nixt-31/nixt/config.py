# This file is placed in the Public Domain.
# pylint: disable=R0902,R0903


"configuration"


import os


from .default import Default
from .workdir import Workdir


class Config(Default):

    "Config"

    name    = Default.__module__.rsplit(".", maxsplit=2)[-2]
    wdr     = os.path.expanduser(f"~/.{name}")
    pidfile = os.path.join(wdr, f"{name}.pid")

    def __init__(self):
        Default.__init__(self)
        self.name = Config.name
        self.wdr  = Config.wdr
        self.pidfile = Config.pidfile


Workdir.wdr = Config.wdr


def __dir__():
    return (
        "Config",
    )
