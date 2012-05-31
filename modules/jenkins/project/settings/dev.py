#!chuck_extends project/settings/dev.py

#!chuck_appends SETTINGS
INSTALLED_APPS += ('django_jenkins',)
#PROJECT_APPS = ('',)
JENKINS_TASKS = ( 'django_jenkins.tasks.run_pylint',
                 'django_jenkins.tasks.with_coverage',
                 'django_jenkins.tasks.django_tests',)
#!end
