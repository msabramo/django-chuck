from haystack.views import SearchView as HaystackSearchView
from cms.models.pagemodel import Page
from cms_search.models import page_proxy_factory
from django.db.models.query_utils import Q
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
import urllib
from search_stats.models import SearchedKeyword, ClickedResultPage


def search_result_click(request, query, result):
    site = Site.objects.get_current()
    pages = Page.objects.published(site=site)
    home = pages.get_home(site=site)

    result = result.replace(home.get_slug(), "")

    if result.find('/') == 0:
        result = result[1:]

    page = pages.filter(
        Q(title_set__path='%s/%s' % (home.get_slug(), result))
    )

    if len(page) > 0:
        keyword = SearchedKeyword.objects.get(name=query)
        keyword.clicked = keyword.clicked +1
        keyword.save()

        stat = ClickedResultPage(page=page[0], keyword=keyword)
        stat.save()

    url = '/%s' % (result,)
    return HttpResponseRedirect(url)


class SearchView(HaystackSearchView):
    def get_results(self):
        r = super(SearchView, self).get_results()

        try:
            stat = SearchedKeyword.objects.filter(name= self.query)[0]
        except IndexError:
            stat = None

        if stat:
            stat.count = stat.count +1
            stat.results = len(r)
        else:
            stat = SearchedKeyword(name = self.query, results = len(r))

        stat.save()

        # results = []

        # page = page_proxy_factory("en", "Englisch")
        # results += list(r.models(page).filter(site_id=Site.objects.get_current().id))

        return r
