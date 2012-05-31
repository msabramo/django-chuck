from common import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '$PROJECT_NAME_test',                      # Or path to database file if using sqlite3.
        'USER': '$PROJECT_NAME_test',                      # Not used with sqlite3.
        'PASSWORD': 'notchtest',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

INSTALLED_APPS += ('django_jenkins', 'test_utils')

PROJECT_APPS = ('',)
JENKINS_TASKS = ( 'django_jenkins.tasks.run_pylint',
                 'django_jenkins.tasks.with_coverage',
                 'django_jenkins.tasks.django_tests',)

#!chuck_renders SETTINGS
#!end
