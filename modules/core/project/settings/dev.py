# -*- coding: utf-8 -*-
# These settings are valid for:
# - sites: all
# - environments: dev

import os
from $PROJECT_NAME.settings.common import *

# Debug
DEBUG = True
TEMPLATE_DEBUG = DEBUG

# E-mail
EMAIL_PORT = 1025
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Cache
CACHES = {
    #!chuck_renders CACHES
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
    #!end
}

# Database
DATABASES = {
    #!chuck_renders DATABASES
    'default': {
    	'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
    	'NAME': os.path.join(SITE_ROOT, 'db','dev.sqlite3'), # Or path to database file if using sqlite3.
    	'USER': '', # Not used with sqlite3.
    	'PASSWORD': '', # Not used with sqlite3.
    	'HOST': '', # Set to empty string for localhost. Not used with sqlite3.
    	'PORT': '', # Set to empty string for default. Not used with sqlite3.
    },
    #!end
}

DEFAULT_CHARSET='utf-8'

#!chuck_renders SETTINGS
#!end
