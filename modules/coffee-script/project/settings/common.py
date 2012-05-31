#!chuck_extends project/settings/common.py

#!chuck_appends SETTINGS
COMPRESS_PRECOMPILERS += (
    'text/coffeescript', 'coffee --compile --stdio'
)
#!end