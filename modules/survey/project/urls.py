#!chuck_extends project/urls.py

#!chuck_prepends URLS
urlpatterns += patterns('',
    url(r'^umfrage/', include('crowdsourcing.urls')),
)
#!end
