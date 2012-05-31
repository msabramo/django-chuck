# -*- coding: utf-8 -*-
import logging
from django.db.models.query_utils import Q
from classytags.arguments import IntegerArgument, Argument
from classytags.core import Options
from classytags.helpers import InclusionTag
from django import template
from django.conf import settings
from django.contrib.sites.models import Site
from django.core.cache import cache
from django.core.urlresolvers import reverse
from django.utils.translation import activate, get_language, ugettext
from cms.models.pagemodel import Page
from cms.utils.moderator import get_page_queryset
from cms.utils.page_resolver import get_page_from_request
from menus.menu_pool import menu_pool
import urllib

register = template.Library()

class ShowBreadcrumb(InclusionTag):
    """
    Shows the breadcrumb from the node that has the same url as the given url

    - start level: after which level should the breadcrumb start? 0=home
    - template: template used to render the breadcrumb
    """
    name = 'show_breadcrumb'
    template = 'menu/dummy.html'

    options = Options(
        Argument('path', default='', required=True),
        Argument('template', default='search/breadcrumb.html', required=False),
    )

    def get_context(self, context, path, template):
        try:
            # If there's an exception (500), default context_processors may not be called.
            request = context['request']
        except KeyError:
            return {'template': 'cms/content.html'}

        pages_root = urllib.unquote(reverse("pages-root"))
        # Stripp off anchors
        old_path = path
        path = path.split('#')[0]
        # Strip off the non-cms part of the URL
        path = path[len(pages_root):-1]
        i = path.find('/')
        path = path[i+1:]
        logging.debug('path: %s' % path)

        site = Site.objects.get_current()

        pages = Page.objects.published(site=site)
        home = pages.get_home(site=site)

        page = pages.filter(
            Q(title_set__path='%s/%s' % (home.get_slug(), path))
        )

        logging.debug(page)
        path = old_path

        try:
            ancestors = page[0].get_cached_ancestors()
        except:
            ancestors = []

        ancestors.reverse()

        # import pudb; pudb.set_trace()

        # for ancestor in ancestors:
        #     path = path.split('#')[0]
        #     path = path[len(pages_root):-1]
        #     i = path.find('/')
        #     path = path[i+1:]

        context.update({'ancestors':ancestors,
                        'template': template})
        return context

register.tag(ShowBreadcrumb)
