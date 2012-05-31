#!chuck_extends project/urls.py

#!chuck_appends URL_MODULES
from search.forms import SearchForm
from search.views import SearchView, search_result_click
#!end


#!chuck_prepends URLS
urlpatterns += patterns('',
    url(r'^search/$', SearchView(form_class=SearchForm), name='haystack_search'),
    url(r'^search/(?P<query>.+)/result/(?P<result>.+)/$', search_result_click, name="search_result_click"),
)
#!end
