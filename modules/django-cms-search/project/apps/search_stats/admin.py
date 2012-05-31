from django.contrib import admin
from search_stats.models import SearchedKeyword, ClickedResultPage


class SearchedKeywordsAdmin(admin.ModelAdmin):
    list_display = ['count', 'name', 'results', 'clicked', 'timestamp']
    list_filter = ['timestamp']
    ordering = ['-count']

admin.site.register(SearchedKeyword, SearchedKeywordsAdmin)


class ClickedResultPagesAdmin(admin.ModelAdmin):
    list_display = ['timestamp', 'page', 'keyword']
    list_filter = ['timestamp', 'page']
    ordering = ['-timestamp', 'page']

admin.site.register(ClickedResultPage, ClickedResultPagesAdmin)
