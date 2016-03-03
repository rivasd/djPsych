'''
Created on Mar 3, 2016

@author: Daniel Rivas
'''
from .base import *

dev_only_apps = [
    'debug_toolbar'
]

DEBUG = True
INSTALLED_APPS.extend(dev_only_apps)

# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
