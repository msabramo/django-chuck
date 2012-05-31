#!chuck_extends project/settings/common.py

#!chuck_appends SETTINGS
COMPRESS_PRECOMPILERS += (
    'text/less', 'lessc {infile} {outfile}'
)
#!end