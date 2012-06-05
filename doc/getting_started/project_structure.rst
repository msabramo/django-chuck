##################
Project structure
##################

This section covers the file generation when running with the built-in modules. A lot of muscle went into the process of
figuring out a sensible and pragmatic default project structure that satisfies the needs of the most common use cases,
so we advise you to give the built-ins a shot, even if they don't cover your specific scenario right away. Remember,
customizing is always easy once you understand what's actually going on.

Understanding the core module
=============================

The main structure for every project you create with Django Chuck is defined by the core module. It is by definition the
entry point to every project you create. In fact, it defines (and has to define!) the very skeleton of every project
you're building with Chuck. It is also the only module that will **always** get installed with top priority. You can override
the built-in core module by providing your own via ``module_basedirs`` in your config file.

The built-in core module enforces the following structure:

The root
--------

=========================================== ==========================================================================================================
Folder                                      Description
=========================================== ==========================================================================================================
**db**                                      This is the folder, where your dev SQLite database gets created when not providing other
                                            defaults through a module. The folder and its contents are by default excluded from version control.
**<project_name>**                          This is the main project folder. Everything that is Django-related about your project should
                                            reside within this folder.
**.gitignore**                              Speaks for itself, we guess. Contains some sensible defaults.
**manage.py**                               Again, this should be clear to any Djangonaut.
**chuck_setup.py**                          This is the file that represents the Django Chuck project setup. Most important when using the
                                            the ``chuck setup_project`` command
=========================================== ==========================================================================================================

The settings
------------

By default all normal settings like *STATIC_ROOT*, *TEMPLATE_DIRS*, *MIDDLEWARE_CLASSES* and *INSTALLED_APPS* are located in
``project/settings/common.py.`` All settings that are likely to be changed after project creation like *ADMINS*, *LANGUAGE_CODE*
and *INTERNAL_IPS* can be found in ``custom.py``.
Additionally there are settings for development environment (``dev.py``), for a staging environment (``stage.py``) and
for live aka production (``live.py``).

.. note::
   If you include the ``unittest`` module you will also get a ``project/settings/test.py`` that can be used to easily setup your project in the continuous integration system `Jenkins <http://www.jenkins-ci.org>`_.

=========================================== ==========================================================================================================
Folder                                      Description
=========================================== ==========================================================================================================
**<project_name>/settings/**                The settings folder
**<project_name>/settings/__init__.py**     This one's clear, ain't it.
**<project_name>/settings/common.py**       This is the place where all the shared settings like *INSTALLED_APPS* go. Most likely to be extended in modules.
**<project_name>/settings/custom.py**       Gets imported by *common.py*. This is the place for storing settings that are
                                            likely to change, like *INTERNAL_IPS*, *ADMINS* and so on
**<project_name>/settings/dev.py**          This is the file that represents all the needs of your development environment.
                                            By default, this file gets exported as *DJANGO_SETTINGS_MODULE* in your virtualenv. This can be changed via config file.
                                            Imports * from *common.py*
**<project_name>/settings/live.py**         This is meant to represent any settings specific to your production environment.
                                            Imports * from *common.py*
**<project_name>/settings/stage.py**        This is meant to represent any settings specific to your staging or integration environment.
                                            Imports * from *common.py*
=========================================== ==========================================================================================================

The templates
-------------

=========================================== ==========================================================================================================
Folder                                      Description
=========================================== ==========================================================================================================
**templates**                               The template folder.
**templates/404.html**                      A simple default 404 page that gets displayed whenever such an error occurs.
**templates/500.html**                      A simple default 500 page that gets displayed whenever such an error occurs.
**templates/base.html**                     Should be the base for every HTML response except the error pages. Defines the very basic structural
                                            elements like the doctype, the heading and the body.
**templates/site_base.html**                Extends *base.html* and defines meta information, global style and script directives and so on.
**templates/subsite.html**                  Extends *site_base.html*, example for an actual template.
=========================================== ==========================================================================================================

The requirements
----------------
=========================================== ==========================================================================================================
Folder                                      Description
=========================================== ==========================================================================================================
**requirements/**                           The requirements folder.
**requirements/requirements.txt**           Contains the requirements for all environments.
**requirements/requirements_local.txt**     Entries should only be installed on your workstation.
**requirements/requirements_dev.txt**       This entries should get installed if you are a Django developer. This is the place where
                                            debugging and testing tools' requirements go.
**requirements/requirements_live.txt**      Takes all requirements that are used to get your hosting up and running (e.g. the production database driver).
=========================================== ==========================================================================================================