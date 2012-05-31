import os
import django.core.handlers.wsgi

os.environ['DJANGO_SETTINGS_MODULE'] = '$PROJECT_NAME.settings.sites.default.prod.live'
application = django.core.handlers.wsgi.WSGIHandler()
