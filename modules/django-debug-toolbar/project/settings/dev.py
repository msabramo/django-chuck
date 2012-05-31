#!chuck_extends project/settings/dev.py

#!chuck_appends SETTINGS
INSTALLED_APPS += ('debug_toolbar',)

# Django debug toolbar
# You have to enable the debug toolbar in a custom settings file because we don't want to enable it for every developer
DEBUG_TOOLBAR_PANELS = (
     'debug_toolbar.panels.version.VersionDebugPanel',
     'debug_toolbar.panels.timer.TimerDebugPanel',
     'debug_toolbar.panels.settings_vars.SettingsVarsDebugPanel',
     'debug_toolbar.panels.headers.HeaderDebugPanel',
     'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
     'debug_toolbar.panels.template.TemplateDebugPanel',
#     'debug_toolbar.panels.sql.SQLDebugPanel',
     'debug_toolbar.panels.signals.SignalDebugPanel',
     'debug_toolbar.panels.logger.LoggingPanel',
)

DEBUG_TOOLBAR_CONFIG = {
     'INTERCEPT_REDIRECTS': False,
     #'SHOW_TOOLBAR_CALLBACK': custom_show_toolbar,
     'HIDE_DJANGO_SQL': True,
     #'TAG': 'div',
}
#!end
