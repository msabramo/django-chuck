#################
Available modules
#################

Django Chuck literally consists of modules. It is most likely that you want to write your own Chuck modules
once you understand the concept, but you got to admit that sometimes some good built-ins come in just handy. This section
is about the modules that ship with Django Chuck by default.

Hitting the docs every time you're about to install a plugin might feel circumstantial. Use ``chuck list_modules`` to get
an overview of all installed modules. Use ``chuck show_info <module_name>`` to display further information.


============================================================================= ==========================
Module                                                                        Description
============================================================================= ==========================
apache                                                                        Generates virtualhost for `Apache <http://httpd.apache.org>`_ and a `mod_wsgi <http://code.google.com/p/modwsgi/>`_ config
coffee-script                                                                 Installs the CoffeeScript binary into your virtualenv and adds its path to the django-compressor precompilers setting.
                                                                              Needs a working installation of node.js and npm.
core                                                                          The main thing!
django-1.3                                                                    Legacy support for Django 1.3.
django-cms                                                                    Installs `Django-Cms <http://www.django-cms>`_ and filer apps
django-compressor							                                  Compresses linked and inline JavaScript or CSS into single cached files.
`django-debug-toolbar <http://pypi.python.org/pypi/django-debug-toolbar/>`_   The Django debug toolbar
`django-extensions <https://github.com/django-extensions/django-extensions>`_ Common Django extensions like shell`plus
django-imagekit                                                               Automated image processing for Django models.
django-mptt                                                                   Build tree-based models
django-tastypie                                                               Creating delicious REST APIs
django-tastypie-mongoengine                                                   MongoEngine support for django-tastypie.
fabric                                                                        `Fabric <http://pypi.python.org/pypi/Fabric>`_ is a simple, Pythonic tool for remote execution and deployment.
feincms                                                                       Installs the `FeinCMS <http://www.feinheit.ch/media/labs/feincms/>`_
html5lib                                                                      Python library for working with HTML5 documents
jenkins                                                                       Plug and play integration with the `Jenkins Coninuous Integration <http://www.jenkins-ci.org>`_ server
jquery                                                                        Installs the `jQuery <http://jquery.org/>`_ javascript library.
                                                                              Needs git in order to work properly.
less-css                                                                      The dynamic stylesheet language `less-css <http://lesscss.org/>`_.
                                                                              Needs a working installation of node.js and npm.
mongoengine                                                                   A Python Document-Object Mapper for working with MongoDB
mootools                                                                      Installs the `Mootools <http://mootools.net/>`_ javascript library
mysql                                                                         `MySQL <http://www.mysql.com>`_ database settings
nginx                                                                         Generates `NGiNX <http://www.nginx.org>`_ virtualhost config
oracle                                                                        `Oracle <http://www.oracle.com>`_ database settings
pil                                                                           The Python Image Library
postgres                                                                      `PostgreSQL <http://www.postgresql.org>`_ database settings
`south <http://south.aeracode.org/>`_                                         The defacto standard for database migrations
twitter-bootstrap                                                             The current defacto standard for frontend prototyping.
                                                                              Requires git and depends on less-css module
unittest                                                                      A collection of apps that make your TDD life a lot more easier.
uwsgi                                                                         Generates a config and app file for your `uWSGI <http://projects.unbit.it/uwsgi/>`_ deployment
============================================================================= ==========================

A few words about...
====================

Testing
-------

Django itself comes with a wonderful unit testing framework but Chuck takes things even further with the unittest module,
a nice and useful collection of apps that makes the life of any TD dev a lot easier.

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
----------------------

You may want to have your web app to be quality controlled. Seriously, if you code towards a major release, you want that
happen. At this point we recommend `django-jenkins <http://pypi.python.org/pypi/django-jenkins>`_.

To get Jenkins support you need to install both the unittest and jenkins module. There is a reason for us
exposing those two modules as example alias in the ``example_conf.py``.

Additionally you will have to install the following (not Django-related) Jenkins modules to get everything up and working:

* Cobertura Plugin
* Jenkins Violations plugin

Chuck's jenkins module will create a file ``jenkins/build_script.sh`` to use to build and test your project and generate
code coverage reports.

When your server is up and running, do the following:

* Create a new job in Jenkins
* Choose *Free Style project*
* Configure your source code management and use Shell execute as
  Build step. Click on Report violations and specify the full path to the generated script and in Post-build Actions add
  ``reports/pylint.report`` as pylint xml filename pattern. Click on the checkbox publish JUnit test result report and add ``reports/TEST-*.xml``

For automatic tests choose Poll SCM in the Build Triggers section and enter ``* * * * *``

Last but not least check the Publish Cobertura Coverage Report checkbox and add ``reports/coverage.xml`` as pattern.

Now Jenkins will build your virtualenv and database, execute the unit tests, checks source code quality using pylint and
generates code coverage reports every time you checkin some new code.


Deployment
----------

We assume you want to deploy your Django project using the WSGI interface. Normally this can be a tedious and
error-prone job so let Chuck do it for you!

Chuck has got a module uwsgi to create a config xml named ``uwsgi.xml`` created and an app file called ``django_wsgi.py``.
Now all you have to do to deploy it on a `uWSGI <http://projects.unbit.it/uwsgi/>`_ server is

.. code-block:: bash

  uwsgi -x uwsgi/live/uwsgi.xml

Assumed you used either the apache or nginx module to create your project you will find a corresponding directory in the
projects hosting subdirectory to easily add your project as a virtual host to your webserver.

If your project is running on a remote server it's very likely that you want to update it after some time. If installed
with the fabric module, Chuck created a fab file for you to connect via ssh, checkout the latest source branch
(we use stage for testing and live for production environment), play in database updates, update static files and
reload the webserver.

Have a look at ``fabfile/__init__.py`` and at least change the user- and hostname for the ssh connection, but surely we also couldnt guess your remote directory structure so adjust them as well.
Afterwards deployment is as easy as hitting a button. For example this will update your production environment:

.. code-block:: bash

  fab live deploy

