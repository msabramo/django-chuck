from django.db import models
from  django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

class Contact(models.Model):
    """
    contact base class
    """
    firstname = models.CharField(max_length=512, blank=False, null=False, verbose_name=_("Firstname"))
    surname = models.CharField(max_length=512, blank=False, null=False, verbose_name=_("Surname"))
    email = models.EmailField(blank=False, null=True, verbose_name=_("E-Mail"))
    message = models.TextField(null=True, blank=True, verbose_name=_("Message"))
    timestamp = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __unicode__(self):
        return u"%s, %s" % (self.surname, self.firstname)

    def send(self):
        mail_text = render_to_string('contact/mail.txt', {'contact': self})
        mail_html = render_to_string('contact/mail.html', {'contact': self})
        mail_to = settings.CONTACT_MAIL_ADDRESS
        mail_subject = settings.CONTACT_MAIL_SUBJECT

        email = EmailMultiAlternatives(mail_subject[0],
                                       mail_text,
                                       self.email,
                                       mail_to,
                                       headers = {'Reply-To': self.email})
        email.attach_alternative(mail_html, "text/html")
        email.send()
