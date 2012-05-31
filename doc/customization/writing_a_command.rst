Write your own command
======================

The structure of a Django Chuck command is nearly the same as a Django command. You create a new command class in ``django_chuck.commands`` that inherits from ``BaseCommand``, define your arguments, a help message and a ``handle`` function that will get called to run the command.

The parameter will get parsed by ``argparse`` so you can use all options described on `the argparse pydoc page <http://docs.python.org/library/argparse.html>`_. It's important that you set the parameters in ``__init__`` otherwise all commands would get them!

The ``handle`` function will get two parameters ``args``, the parsed command line arguments, and ``cfg``, a dictionary of all config settings. Just pass them to the constructor of the ``BaseCommand`` and you will always get either the arg value or config value if you call the property directly on your command object.

Let's say you define a new parameter ``myurl`` the user will automatically be allowed to set it either on the command line or in his config file by defining the ``dest`` value. You dont have to care where the parameter comes from you can just call ``self.myurl`` and will get the arg value, config value or None.

The ``BaseCommand`` class also gives you some helper functions.

======================= ==============
Function                Description
======================= ==============
execute_in_project(cmd) Loads virtualenv and django settings and executes the given cmd
db_cleanup              Delete django tables for complete db import
load_fixtures(file)     Load the given fixture file
======================= ==============

You want to do some cleanup after a system failure or user interruption? Just implement the method ``signal_handler`` and do what ever you want to do. By default the project- and virtualenv directory will get erased automatically if the user doesnt set ``delete_project_on_failure`` to ``False`` in the config file.

Here is a complete example:

.. code-block:: python

  import os
  from django_chuck.commands.base import BaseCommand
  from django_chuck.commands import sync_database, migrate_database

  class Command(BaseCommand):
      help = "Sync, migrate database and load fixtures"

      def __init__(self):
          super(Command, self).__init__()

          self.opts.append(("fixture_files", {
              "help": "Comma separated list of fixture files to load",
              "nargs": "?",
          }))

          self.opts.append(("my_dir", {
              "help": "My work dir to do something in there",
              "nargs": "?",
          }))


    def signal_handler(self):
        if os.path.exists(self.my_dir):
            print "Deleting directory " + self.my_dir
            shutil.rmtree(self.my_dir)


      def handle(self, args, cfg):
          super(Command, self).handle(args, cfg)

          sync_database.Command().handle(args, cfg)
          migrate_database.Command().handle(args, cfg)

          if self.fixture_files:
              for fixture_file in self.fixture_files.split(","):
                  self.db_cleanup()
                  self.load_fixtures(os.path.join(self.site_dir, "fixtures", fixture_file))
