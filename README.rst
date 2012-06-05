::
    _____  __                            ______ __                __
    |     \|__|.---.-.-----.-----.-----. |      |  |--.--.--.----.|  |--.
    |  --  |  ||  _  |     |  _  |  _  | |   ---|     |  |  |  __||    <
    |_____/|  ||___._|__|__|___  |_____| |______|__|__|_____|____||__|__|
          |___|            |_____|

=================================================
Django Chuck - Your powerful project punch button
=================================================

About
-----

Django Chuck is a modular, open source, command-based project build system
developed by Notch Interactive GmbH, that gives you the power to create
new projects as fast as pushing on a button.

In the Django Chuck world, everything is organized within so-called modules, which
incrementally get compiled into a project. There is really nothing that you can't
configure or adjust and guess what, writing and adjusting your modules is totally easy.
On top of that, Django Chuck comes with an already impressive amount of built-in
modules and a bullet proof project structure.

But Chuck cannot be just used to create a project. It can also checkout the
source for you and setup everything until the dev server is up and running and
you're ready to do your development work. Just leave all the annoying stuff
to Chuck and if there is some task Chuck can't do for you at the moment you
can add your own command to let Chuck configure your continuous integration
system, setup your hosting or do whatever you might imagine!

.. warning::
   Please note, that currently Django Chuck does NOT work on Windows machines. Please note
   further, that even though there are bindings to almost all important VC systems, only
   Git has been thoroughly tested.


Installation
------------

* You need Python 2.5 or higher, pip and virtualenv. Virtualenvwrapper is
  also supported.

* Copy the example.conf to your home dir (~/.django_chuck_conf.py), edit it
  and at least have a look at the following files::

    modules/core/project/settings/custom.py
    modules/core/fabfile/__init__.py


How to use it
-------------

List all available modules::

    chuck list_modules

Show information about a module::

    chuck show_info <module_name>

Create a new project with django-tastypie, html5lib and jquery support::

    chuck create_project test project django-tastypie,html5lib,jquery

Setup an existing project with virtualenv and db::

     chuck setup_project <[cvs|svn|git|hg]-url>

Rebuild your database and load some fixtures::

    chuck rebuild_database test project /path/to/fixture/file.json

For more commands ands information see::

    chuck -h
    chuck <command> -h
