###################
Writing templates
###################

Every file in every module will get parsed and rendered through the template engine.

Template can create new files or extend block in existing files and you can use variables that get replaces by its real values.

Here is an overview about all available variables.

========================== =============
Variable                   Description
========================== =============
$EMAIL_DOMAIN              Your email domain
$PROJECT_PREFIX            The project prefix (e.g. customer)
$PROJECT_NAME              The name of the project
$SITE_NAME                 Concatination of project prefix and name
$MODULE_BASEDIR            The full path to the module directory
$PROJECT_BASEDIR           Local directory where Chuch shall create new projects
$PYTHON_VERSION            The version of the Python interpreter (e.g. 2.7)
$SERVER_PROJECT_BASEDIR    Directory where all you projects are stored on your server (used for fab file)
$SERVER_VIRTUALENV_BASEDIR Directory where all you virtualenvs are stored on your server (used for fab file)
$VIRTUALENV_BASEDIR        Local directory where Chuck shall create virtualenvs
========================== =============

A template that should be expandable needs an ``#!chuck_renders`` block. Its common practive to write block names in uppercase and they cannot contain spaces.

Let's for example create a ``requirements.txt`` file with the following content

.. code-block:: bash

  #!chuck_extends REQUIREMENTS
  #!end

The first line creates the block ``REQUIREMENTS`` which gets closed by the ``#!end`` tag. Please note that currently you cannot use nested blocks!

Now we will write another template that extends the first one.

.. code-block:: bash

  #!chuck_extends requirements.txt

  #!chuck_appends REQUIREMENTS
  Django==1.4.0
  #!end

The first line tells the template engine to read the file ``requirements.txt`` in your site directory and search for a block called ``REQUIREMENTS``. If it finds one, it appends the contents to that block. You could also use ``#!chuck_prepends`` here to prepend the content, ``#!chuck_renders`` will completly overwrite the block.

Here's an overview about all available template commands.

========================== =====================
Command                    Description
========================== =====================
#!chuck_appends            Appends to a block
#!chuck_extends            Extends the given file. Throws error if file doesnt exist
#!chuck_extends_if_exists  Extends the given file only if the file exists
#!chuck_prepends           Prepends to a block
#!chuck_renders            Creates or overwrites a block
#!end                      Closes a block
========================== =====================
