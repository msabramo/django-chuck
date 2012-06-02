import subprocess
import os

depends = ['django-compressor', 'less-css']
description = """
Adds Twitter's Bootstrap CSS library to your project.

Please note, that this module installs the source files of the Bootstrap
library and therefore needs LessCSS and Django Compressor support.

For more information, visit:
http://twitter.github.com/bootstrap/
"""

def post_build():
    bootstrap_dir = os.path.join(project_dir, 'static/bootstrap')
    if not os.path.exists(bootstrap_dir):
        os.makedirs(bootstrap_dir)
    subprocess.call(
        'cd '+site_dir+'; mkdir .src; cd .src; \
        git clone https://github.com/twitter/bootstrap.git; \
        mv -v bootstrap/less '+bootstrap_dir+'; \
        mv -v bootstrap/img '+bootstrap_dir+'; \
        mv -v bootstrap/js '+bootstrap_dir+'; \
        cd ..; rm -rf .src;',
        shell=True)