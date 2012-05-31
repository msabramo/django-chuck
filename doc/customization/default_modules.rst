Changing the default module set
===============================

You dont like the modules Chuck installs when creating a new project? No problem! Just specify your own module set.
For example you want to use Apache / MySQL instead of Nginx / Postgres and dont like unittests and debugging stuff.
Edit the config file ~/django_chuck_conf.py and add the following line

.. code-block:: bash

  default_modules=["core", "south", "mysql", "apache", "django-extensions"]


Overriding modules
==================

You found one module that you want to customize? Please dont do your changes in the original code. It gets overwritten when you update to a new version of Django-Chuck.

Instead you should copy the module to another directory (e.g. ~/my_chuck_modules), modify it and tell Chuck to look there first. On Linux systems Chucks core modules are stored in ``/usr/share/django-chuck``, on Mac OS X in ``/opt/local/Library/Frameworks/Python.framework/Versions/2.7/share/django-chuck`` if you installed Python via MacPorts otherwise in ``/System/Library/Frameworks/Python.framework/Versions/2.7./share/django-chuck``.

.. code-block:: bash

  cp -av /path/to/old_module ~/my_chuck_modules/old_module

Afterwards edit your config file ~/django_chuck_conf.py and add the following

.. code-block:: bash

  module_basedirs=["~/my_chuck_modules","."]

Now you can change the module to whatever you like and be sure it doesnt get erased somehow.

**Note** the core module must always be named ``core``!


Change project structure
========================

By overriding the core module you can even change the whole project structure to your own needs!

Of course you will have to adapt all additional modules you want to use, because the files to extend will point to wrong pathes.

