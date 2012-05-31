from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
#!chuck_renders URL_MODULES #!end

admin.autodiscover()

#!chuck_renders URLS
urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
)

# static media
if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )
#!end
