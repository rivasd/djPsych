"""
Django settings for djPsych project.

Generated by 'django-admin startproject' using Django 1.9.2.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os
import json
from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import ugettext_lazy as l_
from django.conf.global_settings import MEDIA_URL

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Using json-based secret params to avoid any code in the secrets file
with open(os.path.join(BASE_DIR, 'settings/secrets.json'), 'r') as f:
    secrets = json.loads(f.read())

def get_secret(setting, secrets=secrets):
    """Get the secret variable or return explicit exception."""
    
    try:
        return secrets[setting]
    except KeyError:
        error_msg = "Set the {0} entry in your secrets.json file".format(setting)
        raise ImproperlyConfigured(error_msg)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = get_secret("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'modeltranslation',
    'grappelli',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'djmanager',
    'djexperiments',
    'djuser',
    'djpay',
    'djcollect',
    'djreceive',
    'djsend',
    'djstim',
    'djadmin',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.facebook',
    'django_markdown',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'djPsych.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.media',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'djuser.contextprocessors.addLoginForm',
            ],
        },
    },
]

WSGI_APPLICATION = 'djPsych.wsgi.application'





# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

TIME_ZONE = 'America/Toronto'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

# Must be set for the django-modeltranslation app otherwise it will create table rows for every django language!
LANGUAGES = [
    ('en', 'English'),
    ('fr', 'Français'),
    ('es', 'Español'),
]
MODELTRANSLATION_DEFAULT_LANGUAGE = 'en'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static")
SITE_ID = 1
# store our js dependencies as fully fledged git repos here
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'dialog_polyfill'),
    os.path.join(BASE_DIR, 'jsPsych'),
    os.path.join(BASE_DIR, 'serverPsych'),
    os.path.join(BASE_DIR, 'jsTreeGrid')
]

MEDIA_URL = '/media/'

#django-allauth settings
ACCOUNT_AUTHENTICATION_METHOD= "username_email"
LOGIN_REDIRECT_URL = "/"
# SOCIALACCOUNT_ADAPTER = 'expManager.adapters.SocialAuthAdapter'
ACCOUNT_EMAIL_VERIFICATION = 'optional'
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

ACCOUNT_EMAIL_REQUIRED = True
# email sending settings
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = get_secret("GMAIL_ACCOUNT_NAME")
EMAIL_HOST_PASSWORD = get_secret("GMAIL_ACCOUNT_PASSWORD")
DEFAULT_FROM_EMAIL = get_secret("GMAIL_ACCOUNT_NAME")


# Markdown
MARKDOWN_EDITOR_SKIN = 'simple'

# Grappelli options

GRAPPELLI_ADMIN_TITLE = l_("Web laboratory dashboard")
