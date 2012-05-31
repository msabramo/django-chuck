import os, sys

sys.path.append('/home/notch/sites/$SITE_NAME-live')
sys.path.append('/home/notch/sites/$SITE_NAME-live/$PROJECT_NAME')

os.environ['DJANGO_SETTINGS_MODULE'] = '$PROJECT_NAME.settings.live'
