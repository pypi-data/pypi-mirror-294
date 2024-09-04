# This file is placed in the Public Domain.
# pylint: disable=R0903


"commands"


from .object import Object


class Commands:

    "Commands"

    cmds     = Object()
    modnames = Object()

    @staticmethod
    def add(func):
        "add command."
        setattr(Commands.cmds, func.__name__, func)
        if func.__module__ != "__main__":
            setattr(Commands.modnames, func.__name__, func.__module__)


def __dir__():
    return (
        'Commands',
    )
