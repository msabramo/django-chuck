from django.db import models
from cms.models import Page


class SearchedKeyword(models.Model):
    timestamp = models.DateField(auto_now=True, auto_now_add=True, verbose_name="Last searched")
    name = models.CharField(max_length=255, verbose_name="Query")
    count = models.IntegerField(default=1, verbose_name="Nr of searches")
    results = models.IntegerField(default=0, verbose_name="Last number of results")
    clicked = models.IntegerField(default=0, verbose_name="Nr of clicks")

    def __unicode__(self):
        return u'%s' % self.name

    class Meta:
        ordering = ['name']


class ClickedResultPage(models.Model):
    timestamp = models.DateField(auto_now=True, auto_now_add=True)
    keyword = models.ForeignKey(SearchedKeyword, null=True)
    page = models.ForeignKey(Page, null=True)

    def __unicode__(self):
        return u'%s' % self.page

    class Meta:
        ordering = ['page__title_set', 'timestamp']
