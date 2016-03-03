'''
Created on Mar 3, 2016

@author: Daniel Rivas
'''

from .base import *

DEBUG= False
ALLOWED_HOSTS =['www.cogcommtl.ca']

prod_only_apps = [
    
]

INSTALLED_APPS.extend(prod_only_apps)

# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases


DATABASES = {
    'default': get_secret("MYSQL_CREDS")
}