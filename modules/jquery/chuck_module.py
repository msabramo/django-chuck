import subprocess
import os


def post_build():
    jquery_dir = os.path.join(project_dir, 'static/scripts/libs/jquery')
    if not os.path.exists(jquery_dir):
            os.makedirs(jquery_dir)
    subprocess.call(
        'cd '+site_dir+'; mkdir .src; cd .src; \
        git clone git://github.com/jquery/jquery.git; \
        cd jquery; \
        make; \
        mv -v dist/* '+jquery_dir+'; \
        cd '+site_dir+'; rm -rf .src;',
        shell=True)