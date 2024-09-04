# This module is placed in the Public Domain.


"uptime"


import time


from ..command import Commands
from ..utils   import laps


STARTTIME = time.time()


def upt(event):
    "show uptime."
    event.reply(laps(time.time()-STARTTIME))


Commands.add(upt)
