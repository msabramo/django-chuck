
priority = 0

description = """
Django Chuck's core module

Defines the default project layout and requires only Django>=1.4.
This is the only module that gets always installed no matter what other configuration you intend to do.

However, you can easily override the core module with your own one.
If you want to have your own defaults, just copy the module folder and put it in a
directory that you expose in your configuration file, preferably before the default folder.

Example location:
/my/absolute/path/to/my_chuck_modules/core

Example configuration:
module_basedirs = ["/my/absolute/path/to/my_chuck_modules/core", "."]

Now you can adjust the contents of the core module to your needs. Read more about
overriding \ customizing modules here:
http://django-chuck.readthedocs.org
"""