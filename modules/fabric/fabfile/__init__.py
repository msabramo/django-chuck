from fabric.api import *
from fabric.contrib import project

"""
In order to deploy, run "fab <env> deploy"
"""

# Config. Adjust these settings according to your server
# If you need to specify a file system path, please add a trailing slash
config = {
    'live': {
        'server': 'CHANGEME@$SITE_NAME',
        'django': {
            'site_dir_name': '$SITE_NAME-live',
            'site_root': '$SERVER_PROJECT_BASEDIR/$SITE_NAME-live/',
            'project_dir_name': '$PROJECT_NAME',
            'project_root': '$SERVER_PROJECT_BASEDIR/$SITE_NAME-live/$PROJECT_NAME/',
            'settings_module': '$PROJECT_NAME.settings.live'
        },
        'virtualenv': {
            'path': '$SERVER_VIRTUALENV_BASEDIR/$SITE_NAME-live/',
            'requirements_file': '$SERVER_PROJECT_BASEDIR/$SITE_NAME-live/requirements/requirements_live.txt',
        },
        'git': {
            'server_name': 'origin',
            'branch_name': 'live',
        },
        'webserver': {
            'touch_file': '$SERVER_PROJECT_BASEDIR/$SITE_NAME-live/uwsgi/live/django_wsgi.py'
        }
    },
    'stage': {
        'server': 'CHANGEME@$SITE_NAME',
        'django': {
            'site_dir_name': '$SITE_NAME',
            'site_root': '$SERVER_PROJECT_BASEDIR/$SITE_NAME-stage/',
            'project_dir_name': '$PROJECT_NAME',
            'project_root': '$SERVER_PROJECT_BASEDIR/$SITE_NAME-stage/$PROJECT_NAME/',
            'settings_module': '$PROJECT_NAME.settings.stage'
        },
        'virtualenv': {
            'path': '$SERVER_VIRTUALENV_BASEDIR/$SITE_NAME-stage/',
            'requirements_file': '$SERVER_PROJECT_BASEDIR/$SITE_NAME-stage/requirements/requirements_live.txt',
        },
        'git': {
            'server_name': 'origin',
            'branch_name': 'stage',
        },
        'webserver': {
            'touch_file': '$SERVER_PROJECT_BASEDIR/$SITE_NAME-stage/uwsgi/stage/django_wsgi.py'
        }
    }
}

# Environments. Add as much as you defined in "config"
def stage():
    env.environment = 'stage'
    env.hosts = [config[env.environment]['server']]

def live():
    env.environment = 'live'
    env.hosts = [config[env.environment]['server']]

# Fab Tasks
def deploy():
    """
    Deploy, migrate, collect static files, restart webserver
    """
    _git_pull()
    _migrate()
    _collect_static_files()
    _restart_webserver()

# Install requirements
def install_requirements():
    """
    This is basically the same as deployment, but additionally
    installs the requirements.
    Important: Migrations are executed too!
    """
    _git_pull()
    _install_requirements()
    _syncdb()
    _migrate()
    _restart_webserver()


# Helpers

def __activate():
    return 'export LANG=de_CH.UTF-8 && source {0}bin/activate && export DJANGO_SETTINGS_MODULE={1} && export PYTHONPATH={2}'.format(
        config[env.environment]['virtualenv']['path'],
        config[env.environment]['django']['settings_module'],
        config[env.environment]['django']['site_root'],
        )

def __deactivate():
    return 'deactivate'

def _git_pull():
    with cd(config[env.environment]['django']['site_root']):
        # git reset --hard HEAD
        run('git pull {0} {1}'.format(
            config[env.environment]['git']['server_name'],
            config[env.environment]['git']['branch_name'])
        )

def _migrate():
    with cd(config[env.environment]['django']['project_root']):
        run(
            __activate() + \
            '&& django-admin.py migrate && ' + \
            __deactivate()
        )

def _syncdb():
    with cd(config[env.environment]['django']['project_root']):
        run(
            __activate() + \
            '&& django-admin.py syncdb && ' + \
            __deactivate()
        )

def _collect_static_files():
    with cd(config[env.environment]['django']['project_root']):
        run(
            __activate() + \
            '&& django-admin.py collectstatic --noinput && ' + \
            __deactivate()
        )

def _restart_webserver():
    run('touch {0}'.format(config[env.environment]['webserver']['touch_file']))

def _install_requirements():
    with cd(config[env.environment]['django']['site_root']):
        run(
            __activate() + \
            '&& pip install -r {0} && '.format(config[env.environment]['virtualenv']['requirements_file']) + \
            __deactivate()
        )
