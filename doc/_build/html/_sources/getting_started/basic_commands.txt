##############
Basic commands
##############

Build a new project
===================

To create a project you need to specify a project prefix (e.g. customer), a project name and optionally modules to
include in your project.

Example:
The following command will build a django-cms project with unittest and jenkins support:

.. code-block:: bash

  chuck create_project <project_prefix> <project_name> django-cms,unittest,jenkins

You can also add other Python module with a version number like for using pip

.. code-block:: bash

  chuck create_project <project_prefix> <project_name> unittest,jenkins -a django-social-auth==0.6.9



Setup an existing project
=========================

At some time in your development process you have got a project in your version control system and another developer
wants to setup his or her development environment. This normally includes the following steps:

* Checkout the source
* Create virtualenv
* Install requirements
* Setup the database
* Optionally load some fixtures or other test data

After doing these steps five or tens times it gets annoying, so why don't you let Chuck do the job?

.. code-block:: bash

  chuck setup_project <url_to_repo>

For example if you use a Git repository you simply execute the following:

.. code-block:: bash

  chuck setup_project git://github.com/notch-interactive/django-chuck

.. note::
   As for now, this process is only supported for projects which got created through Django Chuck or contain a
   valid ``chuck_setup.py`` file. We plan to make this work on non-Chuck projects in the near future though.
