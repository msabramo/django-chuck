Add your own modules
====================

Modules in Django-Chuck are like patches. You describe what the module should change incrementally in which files.
It's best practice to name the change file like the original file an place it in the same directory structure, but if you like you can also create one large file and put all your changes in it. That should be useful if you want to send your new module to chuck@notch-interactive.com so we can possibly include it in our module repository.

Before creating your own module you should configure Chuck to use your own module directory by adding it to the ``module_basedirs`` settings and create a new directory in it holding the files of your new module (e.g. coffeemaker).

Afterwards you normally need a requirements.txt and some settings so let us create those directories

.. code-block:: bash

  mkdir coffeemaker/requirements
  mkdir -p coffeemaker/project/settings

The ``project`` directory will get renamed to whatever the user specifies as project name.

Now we create the file requirements.txt to add our requirements (coffeemaschine) to the projects requirements file. Therefore we define that we want to extends ``requirements/requirements.txt`` and append a line to the ``REQUIREMENTS`` block.

.. code-block:: bash

  #!chuck_extends requirements/requirements.txt

  #!chuck_appends REQUREMENTS
  coffeemaschine
  #!end

Have a look at the core modules ``requirements/requirements.txt`` file and you will see the defined ``REQUIREMENTS`` block there

.. code-block:: bash

  #!chuck_renders REQUIREMENTS
  Django==1.3.1
  #!end

Remember ``#!chuck_appends`` will append to that block while ``#!chuck_prepends`` will prepend and ``#!chuck_renders`` will completly overwrite the block.

Next we need to add some settings (INSTALLED_APPS, and the COFFEEMAKER_HEAT variable).
Here's the patch file ``coffeemaker/project/settings/common.py``

.. code-block:: bash

  #!chuck_extends project/settings/common.py

  #!chuck_appends INSTALLED_APPS
  'coffeemaker',
  #!end

  #!chuck_appends SETTINGS
  COFFEEMAKER_HEAT=60
  #!end

You see the code blocks are normally named after the Django variable or list they extend or after the file they append.
For more examples dont be shy and have a look at the default modules. They dont bite ;)


Module dependencies
===================

Your module needs another module to be installed? No problem. Just create a file called ``chuck_module.py`` to the root directory of your module with the following content:

.. code-block:: python

  depends = ["some_module"]

Now ``some_module`` gets installed before your module is processed.



Module post-build-actions
=========================

Your module needs to do something after the whole project has been build? Just create a function called ``post_build`` in ``chuck_module.py`` and let it do whatever you like.
Here's a small example to delete a setting file if it exists.

.. code-block:: python

  def post_build():
      dev_setting = os.path.join(project_dir, "settings", "dev.py")

      if os.access(dev_setting, os.R_OK):
          print "Removing " + dev_setting
          os.unlink(dev_setting)

The file ``chuck_module.py`` gets the same variables and functions injected as :doc:`chuck_setup` with one exception it additionally get a list called ``installed_modules`` which of course is a list of all successfully installed modules.

.. code-block:: python

  def post_build():
      if "cms" in installed_modules:
          # do some fancy stuff

