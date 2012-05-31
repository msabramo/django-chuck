#!chuck_extends project/urls.py

#!chuck_appends URL_MODULES
from django.views.generic import TemplateView
from contact.views import ContactFormView
#!end

#!chuck_prepends URLS
urlpatterns += patterns('',
    url(r'^contact/$', ContactFormView.as_view(), name='contact_form'),
    url(r'^contact/submit/$', ContactFormView.as_view(), name='contact_submit'),
    url(r'^contact/thanks/$', TemplateView.as_view(template_name="contact/thanks.html"), name='contact_thanks'),
)
#!end
