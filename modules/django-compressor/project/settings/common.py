#!chuck_extends project/settings/common.py

#!chuck_appends INSTALLED_APPS
'compressor',
#!end

#!chuck_appends STATICFILES_FINDERS
'compressor.finders.CompressorFinder',
#!end

#!chuck_appends SETTINGS
COMPRESS_PRECOMPILERS = ()
#!end