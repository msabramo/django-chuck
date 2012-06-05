chuck_setup.py
==============

The file ``chuck_setup.py`` is a normal Python file and used to describe a project. If this file is available Chuck is able to automatically setup the project using the ``setup_project`` command.

It can not only be used to describe a project (e.g. project prefix and name, settings file etc.), but also to define hooks before and every build step like syncdb or build virtualenv to customize the build process completly to your needs!

The script gets some variables and help functions injected to make your life easier. Here's an overview which variables get injected.

============== ===========
Variable       Description
============== ===========
virtualenv_dir The full path to the virtualenv
site_dir       The full path to the projects site dir
project_dir    Combination of site_dir and site_name-project_name
project_name   The name of the project
site_name      The name of the site (project_prefix)
============== ===========

And a list of help functions you can use.

======================= ==============
Function                Description
======================= ==============
execute_in_project(cmd) Loads virtualenv and django settings and executes the given command
db_cleanup              Delete django tables for complete db import. Useful for django-cms migration.
load_fixtures(file)     Load the given fixture file
======================= ==============

Last but not least a full example that will use custom syncdb and migrate parameter, add an admin user and load some fixtures after successful build.

.. code-block:: python

  project_prefix = "test"
  project_name = "project"
  django_settings = "project.settings.dev"
  extra_syncdb_options = "--all"
  extra_migrate_options = "--fake"


  def pre_git_clone():
      pass


  def post_git_clone():
      pass


  def pre_build_virtualenv():
      pass


  def post_build_virtualenv():
      pass


  def pre_sync_db():
      pass

  def post_sync_db():
      pass


  def pre_migrate_db():
      pass


  def post_migrate_db():
      db_cleanup()
      load_fixtures(os.path.join(site_dir, "fixtures", "test_data.json"))
