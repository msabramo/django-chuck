import os
import subprocess

depends = ['django-compressor']
name = "less-css"

def post_build():
    source = os.path.join(virtualenv_dir, 'node_modules/less/bin/lessc')
    target = os.path.join(virtualenv_dir, 'bin/lessc')
    subprocess.call(
        'cd '+virtualenv_dir+'; \
        npm install less; \
        ln -s -v '+source+' '+target+';'
        , shell=True)