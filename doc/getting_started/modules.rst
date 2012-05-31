#################
Available modules
#################

A brief description of all modules included in Django Chuck.

Please note that this is only a minimum set of modules for the most basic tasks. More apps are available through `additional module repositories`_.

============================================================================= ==========================
Module                                                                        Description
============================================================================= ==========================
apache                                                                        Generates virtualhost for `Apache <http://httpd.apache.org>`_ and a `mod_wsgi <http://code.google.com/p/modwsgi/>`_ config
coffee-script                                                                 Installs the CoffeeScript binary into your virtualenv and adds its path to the django-compressor precompilers setting.
contact                                                                       A simple contact form app
core                                                                          Installs Django an the basic project structure
django-1.3                                                                    Installs Django 1.3 (django-sekizai, a requirement of the cms module, doesnt work with Django 1.4 yet)
django-cms                                                                    Installs `Django-Cms <http://www.django-cms>`_ and filer apps
django-cms-search                                                             `Haystack <http://haystacksearch.org/>`_ search engine for Django-Cms
django-compressor							      Compresses linked and inline JavaScript or CSS into single cached files.
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
jquery                                                                        Installs the `jQuery <http://jquery.org/>`_ javascript library
lazyemailuser                                                                 Based on `django-lazysignup <http://pypi.python.org/pypi/django-lazysignup/>`_ to collect data with an temp user and convert it to a real user with username based on email address
less-css                                                                      The dynamic stylesheet language `less-css <http://lesscss.org/>`_.
mongoengine                                                                   A Python Document-Object Mapper for working with MongoDB
mootools                                                                      Install the `Mootools <http://mootools.net/>`_ javascript library
multilang                                                                     Multiple language support
mysql                                                                         `MySQL <http://www.mysql.com>`_ database settings
nginx                                                                         Generates `NGiNX <http://www.nginx.org>`_ virtualhost config
oracle                                                                        `Oracle <http://www.oracle.com>`_ database settings
pil                                                                           The Python Image Library
postgres                                                                      `PostgreSQL <http://www.postgresql.org>`_ database settings
`south <http://south.aeracode.org/>`_                                         The defacto standard for database migrations
survey                                                                        Installs `django-crowdsourcing <http://pypi.python.org/pypi/django-crowdsourcing/1.1.31>`
tellafriend                                                                   Send link to current site in an email to tell a friend about it
twitter-bootstrap
unittest                                                                      Some wicked, cool unit testing tools
uwsgi                                                                         Generates a config and app file for your `uWSGI <http://projects.unbit.it/uwsgi/>`_ deployment
============================================================================= ==========================



###############################
Additional module repositories
###############################

Currently their is only the extra repository from Notch Interactive available on `Github <http://github.com/notch-interactive/chuck-modules>`_.
Feel free to send an email to chuck@notch-interactive.com if you want to add your Chuck module repository to this list.

To add another module repository you have to download it to a local folder and define the ``module_basedirs`` variable in your config file ``~/.django_chuck_conf.py``.

.. code-block:: bash

  module_basedirs="/some/dir/to/additionial-modules","."
