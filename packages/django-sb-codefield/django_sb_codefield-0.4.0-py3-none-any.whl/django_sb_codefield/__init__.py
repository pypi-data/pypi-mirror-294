import django

from .version import VERSION

__version__ = ".".join([str(token) for token in VERSION])

if django.VERSION < (3, 2):
    default_app_config = "django_sb_codefield.apps.DjangoSbCodefieldConfig"
