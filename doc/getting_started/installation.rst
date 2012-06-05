############
Installation
############

Requirements
============

* Python 2.5 or higher
* pip
* virtualenv

Recommended
===========

* virtualenvwrapper


Installation per pip
====================

* ``pip install django-chuck``


Installation via source code
============================


* ``git clone http://www.github.com/notchinteractive/django-chuck.git``
* ``cd django-chuck``
* ``python setup.py install``

Configuration
=============

Locate the ``example_conf.py`` file on your computer:

* on Linux: ``/usr/share/django_chuck/example_conf.py``
* on Mac OS X: ``/System/Library/Frameworks/Python.framework/Versions/2.7./share/django-chuck/example_conf.py``
* on Mac OS X with a MacPorts Python version: ``/opt/local/Library/Frameworks/Python.framework/Versions/2.7/share/django-chuck/example_conf.py``

Copy the file to your home directory and name it ``django_chuck_conf.py``:

* ``~/django_chuck_conf.py``

Your config file is just a normal Python file so you need to follow the Python syntax, use Python datatypes and you
can even dynamically generate the config using functions, external modules, database settings or whatever you like.
The config get's loaded like a normal Python module.

Here's a brief description of the default settings you can configure.

======================== ===============================
setting                  description
======================== ===============================
debug                    Turn on debugging mode
default_modules          Comma-seperated list of module that should always be included when creating a new project
django_settings          Default Django settings file
module_basedirs          Comma-seperated list of directories where chuck should search for modules . will be replaced with the Django Chuck modules dir
module_aliases           A dictionary of lists containing module alias names and list of modules they install
project_basedir          Where to store your projects
python_version           Python version to use in virtualenv activate (default is version of current interpreter)
template_engine          Template engine module to use. For example if you want to use Cheetah or Mako instead of Chucks default engine.
use_virtualenvwrapper    Indicates if we should use virtualenvwrapper
version_control_system   Version control system to use (can be cvs, svn, git or hg)
virtualenv_basedir       Where to store your virtualenvs
======================== ===============================

You can add every command parameter to you config settings by using it's dest parameter.

.. code-block:: python

 ("-mbs", {
                "help": "Comma separated list of dirs where chuck should look for modules",
                "dest": "module_basedir",
                "default": None,
                "nargs": "?",
            }),

This parameter can be set by using module_basedir in the config file.


Module aliases
==============

You have some sets of modules that you want to install quite often and you don't want to type the list of modules over and over again?
No problem. Just give your module list an alias name and install that instead.

.. code-block:: python

  module_aliases = {
      "test": ["unittest", "jenkins"]
  }

Now every time you specify the alias ``test`` in either the command line call or a config parameter,
the modules ``unittest`` and ``jenkins`` will get installed.
