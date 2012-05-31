#!chuck_extends project/urls.py

#!chuck_prepends URLS
urlpatterns += patterns('',
    # Tell a friend
    url(r'^taf/$', 'tellafriend.views.tellafriend', name="tellafriend"),
    url(r'^taf/success/$', 'django.views.generic.simple.direct_to_template', { 'template': 'tellafriend/success.html'}, name="tellafriend_success"),
)
#!end
