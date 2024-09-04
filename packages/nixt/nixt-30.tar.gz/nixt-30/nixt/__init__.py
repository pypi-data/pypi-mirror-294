# This file is placed in the Public Domain.


"""NIXT


SYNOPSIS

    nixt <cmd> [key=val] [key==val]
    nixtc
    nixtd
    nixts

DESCRIPTION

    NIXT does nothing, write your own commands !

INSTALL

    $ pipx install nixt
    $ pipx ensurepath

USAGE

    without any argument nixt does nothing

    $ nixt
    $

    see list of commands

    $ nixt cmd
    cmd,err,mod,srv,thr,upt

    start a console

    $ nixtc
    >

    use -i to run init on modules

    $ nixtc -i
    >

    start daemon

    $ nixtd
    $

    start as service

    $ nixts
    <waits till ctrl-c>

COMMANDS

    cmd - commands
    err - show errors
    mod - available modules
    srv - create service file
    thr - show running threads
    upt - show uptime

SYSTEMD

    $ nixt srv > nixt.service
    $ sudo mv nixt.service /etc/systemd/system/
    $ sudo systemctl enable nixt --now

FILES

    ~/.nixt
    ~/.local/bin/nixt
    ~/.local/bin/nixtc
    ~/.local/bin/nixtd
    ~/.local/bin/nixts
    ~/.local/pipx/venvs/nixt/

AUTHOR

    Bart Thate <rssbotd@gmail.com>

COPYRIGHT

    NIXT is Public Domain.

"""
