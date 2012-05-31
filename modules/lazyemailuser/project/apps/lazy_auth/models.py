from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django_lazyemailuser.signals import user_registered_signal

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    language = models.CharField(max_length=2, default=settings.LANGUAGE_CODE)


def user_registered_handler(sender, **kwargs):
        user = kwargs.get('user')
        language = kwargs.get("language")

        if not language:
            language = settings.LANGUAGE_CODE

        if user:
            profile, created = UserProfile.objects.get_or_create(user=user)
            profile.language = language
            profile.save()

user_registered_signal.connect(user_registered_handler)
