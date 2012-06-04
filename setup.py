import os
import sys
from distutils.command.build_py import build_py as _build_py
from distutils.core import setup
from distutils.dir_util import copy_tree, remove_tree


class build_py(_build_py):
    CLASSIFIERS = [
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: WSGI',
        'Topic :: Software Development',
        'Topic :: Software Development :: Build Tools',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
    ]

    setup(name="django-chuck",
          version="0.1",
          author="Notch Interactive GmbH",
          author_email="chuck@notch-interactive.com",
          url="http://github.com/notch-interactive/django-chuck",
          description="Your powerful project punch button",
          long_description="""Django Chuck is a modular, open source, command-based project build system, that gives you the power to create new projects as fast as pushing a button.""

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
Mercurial.""",

          packages=["django_chuck", "django_chuck.commands", "django_chuck.base", "django_chuck.template", "django_chuck.template.notch_interactive"],
          scripts=["chuck"],
          data_files=[(os.path.join("share", "django_chuck"), ['example_conf.py'])],
    )

    module_dest_dir = os.path.join(sys.prefix, "share", "django_chuck", "modules")

    if os.path.exists(module_dest_dir):
        remove_tree(module_dest_dir)

    copy_tree("modules", module_dest_dir, verbose=1, preserve_symlinks=1)
