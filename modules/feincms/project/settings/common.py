#!chuck_extends project/settings/common.py

#!chuck_appends INSTALLED_APPS
    'mptt',
    'feincms',
    'feincms.module.page',
    'feincms.module.medialibrary',

    'example',
#!end


#!chuck_appends SETTINGS
FEINCMS_RICHTEXT_INIT_CONTEXT = {
    'TINYMCE_JS_URL': os.path.join(STATIC_URL, 'scripts/libs/tiny_mce/tiny_mce.js'),
}
#!end

