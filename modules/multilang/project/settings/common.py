#!chuck_extends project/settings/common.py

#!chuck_appends MIDDLEWARE_CLASSES
    'cms.middleware.multilingual.MultilingualURLMiddleware',
#!end

#!chuck_appends SETTINGS
LANGUAGES = (
    ('de', ugettext('Deutsch')),
    ('fr', ugettext('Französisch')),
    ('it', ugettext('Italienisch')),
)

CMS_FRONTEND_LANGUAGES = ("de", "fr", "it")

MODELTRANSLATION_DEFAULT_LANGUAGE = "de"
MODELTRANSLATION_TRANSLATION_REGISTRY = "$PROJECT_NAME.translation"

# TRANSURLVANIA
MULTILANG_LANGUAGE_DOMAINS = {
    'de': ('$SITE_NAME', 'German Site', '$SITE_NAME'),
    'fr': ('$SITE_NAME', 'French Site', '$SITE_NAME'),
    'it': ('$SITE_NAME', 'Italian Site', '$SITE_NAME'),
}

MULTILANG_DEFAULT_FROM_EMAIL = {
    'de': '',
    'fr': '',
    'it': '',
}
#!end

#!chuck_appends INSTALLED_APPS
    'modeltranslation',
    'transurlvania',
#!end
