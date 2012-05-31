#!chuck_extends project/settings/stage.py

#!chuck_appends DATABASES
    'default': {
        'ENGINE': 'django.db.backends.oracle', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'xe',                      # Or path to database file if using sqlite3.
        'USER': '$PROJECT_PREFIX_$PROJECT_NAME_stage',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    },
#!end
