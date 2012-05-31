# -*- coding: utf-8 -*-

from django import forms
from django.utils.translation import ugettext_lazy as _


class TellAFriendForm(forms.Form):
    email_sender = forms.EmailField(max_length=100, label=_("E-Mail-Absender"))
    email_recipient = forms.EmailField(max_length=100, label=_(u"E-Mail-Empfänger"))
    message = forms.CharField(required=False, widget=forms.Textarea, label=_("Mitteilung"))
