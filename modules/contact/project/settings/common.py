#!chuck_extends project/settings/common.py

#!chuck_appends SETTINGS
HONEYPOT_FIELD_NAME="address_addon"
CONTACT_MAIL_SUBJECT = ""
CONTACT_MAIL_ADDRESS = []
#!end

#!chuck_appends INSTALLED_APPS
    'honeypot',
    'contact',
#!end

