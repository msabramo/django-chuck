#!chuck_extends project/common.py

#!chuck_appends MIDDLEWARE_CLASSES
    'cms.middleware.multilingual.MultilingualURLMiddleware',
    'cms.middleware.page.CurrentPageMiddleware',
    'cms.middleware.user.CurrentUserMiddleware',
    'cms.middleware.toolbar.ToolbarMiddleware',
#!end

#!chuck_appends TEMPLATE_CONTEXT_PROCESSORS
    'cms.context_processors.media',
    'sekizai.context_processors.sekizai',
#!end

#!chuck_appends INSTALLED_APPS
    'cms',
    'menus',
    'cms.plugins.text',
    'easy_thumbnails',
    'filer',
    'cmsplugin_filer_file',
    'cmsplugin_filer_folder',
    'cmsplugin_filer_image',
    'cmsplugin_filer_video',

    'mptt',
    'sekizai',

    'ni_djangocms_utils',
    'ni_cmsplugins.better_link',
#!end


#!chuck_appends SETTINGS
CMS_TEMPLATES = (
    ('home.html', ugettext('Home')),
    ('subsite.html', ugettext('Subsite')),
)

CMS_SOFTROOT = False
CMS_MODERATOR = False
CMS_PERMISSION = False
CMS_REDIRECTS = True
CMS_SEO_FIELDS = True
CMS_FLAT_URLS = False
CMS_MENU_TITLE_OVERWRITE = False
CMS_HIDE_UNTRANSLATED = True
CMS_URL_OVERWRITE = False
CMS_SHOW_START_DATE = False
CMS_SHOW_END_DATE = False

THUMBNAIL_PROCESSORS = (
    'easy_thumbnails.processors.colorspace',
    'easy_thumbnails.processors.autocrop',
    #'easy_thumbnails.processors.scale_and_crop',
    'filer.thumbnail_processors.scale_and_crop_with_subject_location',
    'easy_thumbnails.processors.filters',
)
#!end

