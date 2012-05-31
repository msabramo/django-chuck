#!chuck_extends project/settings/common.py

#!chuck_prepends AUTHENTICATION_BACKENDS
    'django_lazyemailuser.backends.EmailOrUsernameModelBackend',
#!end

#!chuck_appends AUTHENTICATION_BACKENDS
    'django_lazyemailuser.backends.LazySignupBackend',
#!end

#!chuck_appends SETTINGS
AUTH_PROFILE_MODULE = "lazy_auth.UserProfile"
#!end

#!chuck_appends INSTALLED_APPS
    'lazy_auth',
    'django_lazyemailuser',
#!end
