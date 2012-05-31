#!chuck_extends project/urls.py

#!chuck_appends URLS
urlpatterns += patterns('',
    url(r'', include('feincms.urls')),
)
#!end
