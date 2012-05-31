from django.views.generic.edit import FormView
from contact.forms import ContactForm
from django.core.urlresolvers import reverse
from django.utils.decorators import method_decorator
from honeypot.decorators import check_honeypot


class ContactFormView(FormView):
    form_class = ContactForm
    template_name = "contact/form.html"


    def get_success_url(self):
        return reverse("contact_thanks")


    @method_decorator(check_honeypot)
    def post(self, request, *args, **kwargs):
        return super(ContactFormView, self).post(self, request, *args, **kwargs)


    def form_valid(self, form):
        contact = form.save()
        contact.send()

        return super(ContactFormView, self).form_valid(form)
