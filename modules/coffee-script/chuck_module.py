import os
import subprocess

depends = ['django-compressor']

def post_build():
    source = os.path.join(virtualenv_dir, 'node_modules/coffee-script/bin/coffee')
    target = os.path.join(virtualenv_dir, 'bin/coffee')
    subprocess.call(
        'cd '+virtualenv_dir+'; \
        npm install less; \
        ln -s -v '+source+' '+target+';'
        , shell=True)