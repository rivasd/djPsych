'''
Created on Mar 3, 2016

@author: Daniel Rivas
'''
from .base import *

dev_only_apps = [
    'silk',
]

IS_PRODUCTION = False
ALLOWED_HOSTS =['www.cogcommtl.ca']
DEBUG = True
INSTALLED_APPS.extend(dev_only_apps)
MIDDLEWARE_CLASSES.extend(['silk.middleware.SilkyMiddleware'])

# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# change to live when we go live!
PAYPAL_MODE = 'live'
PAYPAL_MODE = 'sandbox'
SILKY_PYTHON_PROFILER = True
SILKY_MAX_RESPONSE_BODY_SIZE = 1

# MEDIA_ROOT for development only
MEDIA_ROOT = os.path.join(BASE_DIR, '..', 'media')