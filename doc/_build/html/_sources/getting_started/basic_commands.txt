##############
Basic commands
##############

Build a new project
===================

To create a project you need to specify a project prefix (e.g. customer), a project name and optionally modules to include in your project.
For example you the following command will build a django-cms project with a contact app:

.. code-block:: bash

  chuck create_project <project_prefix> <project_name> contact,cms

You can also add other Python module with a version number like for using pip

.. code-block:: bash

  chuck create_project <project_prefix> <project_name> cms -a Django==1.4



Setup an existing project
=========================

At some time in your development process you have got a project in your version control system and another developer wants to setup his or her development environment.
This normally includes the following steps:

* Checkout the source
* Create virtualenv
* Install requirements
* Setup the database
* Optionally load some fixtures or other test data

After doing these steps five or tens times it get's annoying so let Chuck do it for you!

.. code-block:: bash

  chuck setup_project <url>

for example if you use a Git repository you execute

.. code-block:: bash

  chuck setup_project git://github.com/notch-interactive/django-chuck

If your project wasnt created by Chuck and doesnt contain a ``chuck_setup.py`` file Chuck will ask you everything he needs to know to get everything up and running.
