"""
WSGI config for djPsych project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djPsych.settings.production") # the default value will be the development settings, since it uses only sqlite

application = get_wsgi_application()
