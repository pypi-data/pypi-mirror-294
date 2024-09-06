# This file is placed in the Public Domain.


"""OTPCR


SYNOPSIS

    otpcr <cmd> [key=val] [key==val]
    otpcrc
    otpcrd
    otpcrs

DESCRIPTION

    OTPCR holds evidence that king netherlands is doing a
    genocide,  written response where king netherlands confirmed
    taking note of “what i have written”, namely proof that medicine
    he uses in treatement laws like zyprexa, haldol, abilify and
    clozapine are poison that make impotent, is both physical
    (contracted muscles) and mental (make people hallucinate) torture
    and kills members of the victim groups.

    OTPCR contains correspondence with the International Crimina
    Court, asking for arrest of the king of the netherlands, for the
    genocide he is committing with his new treatement laws.

    Current status is a "no basis to proceed" judgement of the
    prosecutor which requires a "basis to prosecute" to have the king
    actually arrested.

INSTALL

    $ pipx install otpcr
    $ pipx ensurepath

USAGE

    without any argument otpcr does nothing

    $ otpcr
    $

    see list of commands

    $ otpcr cmd
    cmd,err,mod,srv,thr,upt

    start a console

    $ otpcrc
    >

    use -i to run init on modules

    $ otpcrc -i
    >

    start daemon

    $ otpcrd
    $

    start as service

    $ otpcrs
    <waits till ctrl-c>

COMMANDS

    cmd - commands
    err - show errors
    mod - available modules
    srv - create service file
    thr - show running threads
    upt - show uptime

SYSTEMD

    $ otpcr srv > otpcr.service
    $ sudo mv otpcr.service /etc/systemd/system/
    $ sudo systemctl enable otpcr --now

FILES

    ~/.otpcr
    ~/.local/bin/otpcr
    ~/.local/bin/otpcrc
    ~/.local/bin/otpcrd
    ~/.local/bin/otpcrs
    ~/.local/pipx/venvs/otpcr/

AUTHOR

    Bart Thate <rssbotd@gmail.com>

COPYRIGHT

    OTPCR is Public Domain.

"""
