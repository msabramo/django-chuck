import os
import subprocess

depends = ['django-compressor']
description = """
Module for CoffeeScript support

Installs the CoffeeScript binary into your virtualenv and adds its path to the django-compressor precompilers setting.
Requires node.js / npm in order to work.

For more information about CoffeeScript:
http://coffeescript.org/

For django-compressor usage information:
http://django_compressor.readthedocs.org
"""


def post_build():
    source = os.path.join(virtualenv_dir, 'node_modules/coffee-script/bin/coffee')
    target = os.path.join(virtualenv_dir, 'bin/coffee')
    subprocess.call(
        'cd '+virtualenv_dir+'; \
        npm install less; \
        ln -s -v '+source+' '+target+';'
        , shell=True)