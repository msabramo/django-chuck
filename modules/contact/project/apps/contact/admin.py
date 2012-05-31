from django.contrib import admin
from contact.models import Contact


class ContactAdmin(admin.ModelAdmin):
    ordering = ('timestamp', 'surname', 'firstname')
    list_display = ["timestamp", "surname", "firstname", "email"]
    list_filter = ["timestamp"]
    search = ["surname", "firstname", "email", "message"]

admin.site.register(Contact, ContactAdmin)
