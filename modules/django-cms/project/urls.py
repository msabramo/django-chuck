#!chuck_extends project/urls.py

#!chuck_appends URLS
urlpatterns += patterns('',
    url(r'^', include('filer.server.urls')),
    url(r'^', include('cms.urls')),
)
#!end
