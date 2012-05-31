##################
Project structure
##################

What's all that stuff?!
=======================

Django Chuck generates a whole lot stuff for you if you use the default core moduleset like uwsgi config files and a fab file for a smooth deployment process, requirement files to automatically install Python modules using pip, a chuck_setup.py file for easy project setup and a settings file plus shell script for plug and play Jenkins integration. This section will give you a brief overview about what jewels are included and how you can use them.


Requirements
============

All project requirements are stored in the files under the requirements subdirectory.

* requirements.txt contains the requirements for all environments
* requirements_local.txt entries should only be installed on your workstation
* requirements_dev.txt stuff should be installed if you are a Django developer. It includes debugging and testing tools.
* requirements_live.txt takes all modules that are used to get your hosting up and running (e.g. the production database driver)


Settings structure
==================

By default all normal settings like STATIC_ROOT, TEMPLATE_DIRS, MIDDLEWARE_CLASSES and INSTALLED_APPS are located in ``project/settings/common.py.`` All settings that are likely to be changed by you like ADMINS, LANGUAGE_CODE and INTERNAL_IPS can be found in ``custom.py``.

Additionally there are settings for development environment (``dev.py``), for a staging environment (``stage.py``) and for live aka production (``live.py``).

If you included the unittest module you will also get a ``project/settings/test.py`` that can be used to easily setup your project in the continuous integration system `Jenkins <http://www.jenkins-ci.org>`_.


Testing
========

Django itself comes with a wonderful unit testing framework that Django Chuck extends with some sweet additional modules.

================================================================ ================
Module                                                           Description
================================================================ ================
`django-test-utils <http://django-test-utils.readthedocs.org>`_  Let you run a test server that will automatically generate view tests while browsing the site
`django-any <https://github.com/kmmbvnr/django-any>`_            Allows you to easily generate some random test data
`pylint <http://www.logilab.org/project/pylint>`_                Checks your code quality for best practices and awful smells
`django-jenkins <http://pypi.python.org/pypi/django-jenkins>`_   Plug and play continuous integration with Django and Jenkins
`coverage <http://nedbatchelder.com/code/coverage/>`_            Calculatze the code coverage of your unit tests
`mock <http://pypi.python.org/pypi/mock/>`_                      A mocking library
================================================================ ================


Continuous integration
======================

To get Jenkins support you need to install both unittest and jenkins module!

Additionally you will have to install the following Jenkins modules to get everything up and working:

* Cobertura Plugin
* Jenkins Violations plugin

Chucks jenkins module will create a file ``jenkins/build_script.sh`` to use to build and test your project and generate code coverage reports.

Create a new job in Jenkins, choose Free Style project, configure your source code management and use Shell execute as Build step. Click on Report violations and specify the full path to the generated script and in Post-build Actions add ``reports/pylint.report`` as pylint xml filename pattern. Click on the checkbox publish JUnit test result report and add ``reports/TEST-*.xml``

For automatic tests choose Poll SCM in the Build Triggers section and enter ``* * * * *``

Last but not least check the Publish Cobertura Coverage Report checkbox and add ``reports/coverage.xml`` as pattern.

Now Jenkins will build your virtualenv and database, execute the unit tests, checks source code quality using pylint and generates code coverage reports every time you checkin some new code.


Deployment
==========

Of course of want to deploy your Django project using the WSGI interface. Normally this can be an tedious and error-prone job so let Chuck do it for you!
Chuck has got a module uwsgi to create a config xml named ``uwsgi.xml`` created and an app file called ``django_wsgi.py``.
Now all you have to do to deploy it on a `uWSGI <http://projects.unbit.it/uwsgi/>`_ server is

.. code-block:: bash

  uwsgi -x uwsgi/live/uwsgi.xml

Assumed you used either apache or nginx module to create your project you will find a corresponding directory in the hosting subdirectory to easily add your project as a virtual host to your webserver.

If your project is running on a remote server it's very likely that you want to update it after some time. Chuck created a fab file for you to connect via ssh, checkout the latest source branch (we use stage for testing and live for production environment), play in database updates, update static files and reload the webserver.

Have a look at ``fabfile/__init__.py`` and at least change the user- and hostname for the ssh connection, but surely we also couldnt guess your remote directory structure so adjust them as well.
Afterwards deployment is as easy as hitting a button. For example this will update your production environment:

.. code-block:: bash

  fab live deploy
