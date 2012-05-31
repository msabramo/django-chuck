from django import forms
from haystack.forms import SearchForm

class SonovaSearchForm(SearchForm):
    q = forms.CharField(max_length=255, label="Search for")

#    def __init__(self, *args, **kwargs):
#        super(ModelSearchForm, self).__init__(*args, **kwargs)
