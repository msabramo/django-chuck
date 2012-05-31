#!chuck_extends project/urls.py

#chuck_prepends URLS
urlpatterns += patterns('',
    url(r'^auth/', include('django_lazyemailuser.urls')),
)
#!end
