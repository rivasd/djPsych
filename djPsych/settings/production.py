'''
Created on Mar 3, 2016

@author: Daniel Rivas
'''

from .base import *

IS_PRODUCTION = True
DEBUG= True
ALLOWED_HOSTS =['cogcommtl.ca', 'www.cogcommtl.ca', 'localhost:8000']
DEBUG= False

prod_only_apps = [
    
]

INSTALLED_APPS.extend(prod_only_apps)

# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases
DATABASES = {
    'default': get_secret("MYSQL_CREDS")
}

# change to live when we go live!
PAYPAL_MODE = 'live'

MEDIA_ROOT = '/var/www/labo'