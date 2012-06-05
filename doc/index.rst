.. Django Chuck documentation master file, created by
   sphinx-quickstart on Mon May 14 11:50:54 2012.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Django Chuck's documentation!
========================================

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

***************
Getting Started
***************

.. toctree::
   :maxdepth: 2
   :numbered:

   getting_started/installation
   getting_started/basic_commands
   getting_started/project_structure
   getting_started/modules

***************
Customizations
***************

.. toctree::
   :maxdepth: 2

   customization/configuration.rst
   customization/default_modules.rst
   customization/chuck_setup.rst
   customization/writing_templates.rst
   customization/add_module.rst
   customization/writing_a_command.rst
   customization/writing_a_template_engine.rst



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

