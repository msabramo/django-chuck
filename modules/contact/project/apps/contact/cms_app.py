from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool


class ContactApp(CMSApp):
    name = 'Contact'
    urls = ['contact.urls']

apphook_pool.register(ContactApp)
