from django.conf.urls.defaults import patterns, url
from django.views.generic import TemplateView
from contact.views import ContactFormView

urlpatterns = patterns('',
    url(r'^$', ContactFormView.as_view(), name='contact_form'),
    url(r'^submit/$', ContactFormView.as_view(), name='contact_submit'),
)
