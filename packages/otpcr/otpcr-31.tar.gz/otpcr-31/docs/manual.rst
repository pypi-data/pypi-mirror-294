.. _manual:


.. raw:: html

    <br>

.. title:: Home


**NAME**


    ``OTPCR`` - Since ``4 march 2019`` `! <source.html>`_


**SYNOPSIS**


    | ``otpcr  <cmd> [key=val] [key==val]``
    | ``otpcrc [-i] [-v]``
    | ``otpcrd`` 
    | ``otpcrs``


**DESCRIPTION**




    ``OTPCR`` holds evidence that king
    netherlands is doing a genocide, a
    written response where king
    netherlands confirmed taking note
    of “what i have written”, namely
    :ref:`proof  <evidence>` that medicine
    he uses in treatement laws like zyprexa,
    haldol, abilify and clozapine are
    poison that make impotent, is both
    physical (contracted muscles) and
    mental (make people hallucinate)
    torture and kills members of the
    victim groups.

    ``OTPCR`` contains :ref:`correspondence
    <writings>` with the International Criminal
    Court, asking for arrest of the king of the
    netherlands, for the genocide he is committing
    with his new treatement laws.

    Current status is a :ref:`"no basis to proceed"
    <writings>` judgement of the prosecutor which
    requires a :ref:`"basis to prosecute" <reconsider>`
    to have the king actually arrested.


    ``OTP-CR-117/19`` has been duly entered in the 
    Communications Register of the Office.

    Since ``4 march 2019``


**INSTALL**

    installation is done with pipx

    | ``$ pipx install otpcr``
    | ``$ pipx ensurepath``

**USAGE**

    without any argument the bot does nothing

    | ``$ otpcr``
    | ``$``

    see list of commands

    | ``$ otpcr cmd``
    | ``cfg,cmd,dne,dpl,err,exp,imp,log,mod,mre,nme,``
    | ``pwd,rem,req,res,rss,srv,syn,tdo,thr,upt``


    start a console

    | ``$ otpcrc``
    | ``>``

    use -i to init modules

    | ``$ otpcrc -i``
    | ``>``

    start daemon

    | ``$ otpcrd``
    | ``$``

    start service

    | ``$ otpcrs``
    | ``<runs until ctrl-c>``

    show request to the prosecutor

    | $ ``otpcr req``
    | Information and Evidence Unit
    | Office of the Prosecutor
    | Post Office Box 19519
    | 2500 CM The Hague
    | The Netherlands

**COMMANDS**

    here is a list of available commands

    | ``cfg`` - irc configuration
    | ``cmd`` - commands
    | ``dpl`` - sets display items
    | ``err`` - show errors
    | ``exp`` - export opml (stdout)
    | ``imp`` - import opml
    | ``log`` - log text
    | ``mre`` - display cached output
    | ``pwd`` - sasl nickserv name/pass
    | ``rem`` - removes a rss feed
    | ``res`` - restore deleted feeds
    | ``req`` - reconsider
    | ``rss`` - add a feed
    | ``syn`` - sync rss feeds
    | ``tdo`` - add todo item
    | ``thr`` - show running threads
    | ``upt`` - show uptime


**CONFIGURATION**

    irc

    | ``$ otpcr cfg server=<server>``
    | ``$ otpcr cfg channel=<channel>``
    | ``$ otpcr cfg nick=<nick>``

    sasl

    | ``$ otpcr pwd <nsvnick> <nspass>``
    | ``$ otpcr cfg password=<frompwd>``

    rss

    | ``$ otpcr rss <url>``
    | ``$ otpcr dpl <url> <item1,item2>``
    | ``$ otpcr rem <url>``
    | ``$ otpcr nme <url> <name>``

    opml

    | ``$ otpcr exp``
    | ``$ otpcr imp <filename>``

**SYSTEMD**

    put the following in ``/etc/systemd/system/otpcr.service`` and
    replace {name} with the user running pipx

    | ``[Unit]``
    | ``Description=OTPCR``
    | ``After=network-online.target``
    |
    | ``[Service]``
    | ``Type=simple``
    | ``User={name}``
    | ``Group={name}``
    | ``ExecStart=/home/{name}/.local/bin/otpcrs``
    |
    | ``[Install]``
    | ``WantedBy=multi-user.target``


    then run the following

    | ``$ sudo systemctl enable otpcr --now``

    joins #otpcr on localhost


**SOURCE**

    source is :ref:`here <source>`

**FILES**

    | ``~/.otpcr``
    | ``~/.local/bin/otpcr``
    | ``~/.local/bin/otpcrc``
    | ``~/.local/bin/otpcrd``
    | ``~/.local/bin/otpcrs``
    | ``~/.local/pipx/venvs/otpcr/*``


**AUTHOR**

    | Bart Thate ``<rssbotd@gmail.com>``


**COPYRIGHT**

    | ``OTPCR`` is Public Domain.

