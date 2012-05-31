Adds Django CMS to your project.

Please note that as of yet Django CMS is not compatible with Django 1.4 and therefore
needs the django-1.3 module.

Another requirement of Django CMS is django-mptt, but because of the CMS not
being compatible with the latest django-mptt version, it is not listed as a chuck module
requirement. django-mptt will be included as a normal pip requirement (requirements/requirements.txt)
with an explicit call for the latest version that is known to be working with Django CMS.

For further information, visit;
http://docs.django-cms.org