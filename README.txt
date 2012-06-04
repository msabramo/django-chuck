 _____  __                            ______ __                __
|     \|__|.---.-.-----.-----.-----. |      |  |--.--.--.----.|  |--.
|  --  |  ||  _  |     |  _  |  _  | |   ---|     |  |  |  __||    <
|_____/|  ||___._|__|__|___  |_____| |______|__|__|_____|____||__|__|
      |___|            |_____|

-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=--=-
Django Chuck - Your powerful project punch button
-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=--=-

////[ About

Django Chuck is a modular, open source, command-based project build system
developed by Notch Interactive GmbH, that gives you the power to create
new projects as fast as pushing on a button.

It creates a virtualenv and a Django project for you, installs all required
Python packages, creates the database and a fab file for automatic
deployment and thanks to the module system you can easily add functionality
like CMS, Facebook, Twitter, multilang and search engine support to a new
or existing project.

But Chuck cannot be just used to create a project it can also checkout the
source for you and setup everything until the Django server is running and
you're ready to do your development work. Just leave all the annoying stuff
to Chuck and if there is some task Chuck can't do for you at the moment you
can add your own command to let Chuck configure your continuous integration
system, setup your hosting or do whatever you might imagine!

Currently supported version control systems are: CVS, Subversion, GIT and
Mercurial.


////[ Installation

- You need Python 2.5 or higher, pip and virtualenv. Virtualenvwrapper is
also supported.

- Copy the example.conf to your home dir (~/.django_chuck.conf), edit it
and at least have a look at the following files:

--> modules/core/project/settings/custom.py
--> modules/core/fabfile/__init__.py


////[ How to use it

# Create a new project with cms, search and twitter support
cd dir-of-django-chuck
chuck create_project test project contact,cms

# Setup an existing project with virtualenv and db
chuck setup_project <[cvs|svn|git|hg]-url>

# Rebuild your database and load some fixtures
chuck rebuild_database test project /path/to/fixture/file.json

# For more commands ands information see
chuck -h
chuck <command> -h
