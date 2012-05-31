#!chuck_extends project/settings/common.py

#!chuck_appends SETTINGS
HAYSTACK_SITECONF = '$PROJECT_NAME.search_sites'
HAYSTACK_SEARCH_ENGINE = 'whoosh'
HAYSTACK_WHOOSH_PATH = os.path.join(SITE_ROOT, 'whoosh')
HAYSTACK_SEARCH_RESULTS_PER_PAGE = 10
#!end

#!chuck_appends INSTALLED_APPS
    'cms_search',
    'cms_search.search_helpers',
    'haystack',
    'whoosh',
    'search',
    'search_stats',
#!end
