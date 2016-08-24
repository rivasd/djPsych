"""djPsych URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from djmanager.views import index
from django.conf import settings
from djexperiments.experiments.simcat import texture_generator
import allauth.urls


urlpatterns = [
    url(r'^grappelli/', include('grappelli.urls')), # grappelli URLS
    url(r'^admin/', admin.site.urls),
    url(r'^webexp/', include('djmanager.urls', namespace='webexp')),
    url(r'^markdown/', include( 'django_markdown.urls')),
    url(r'^accounts/', include(allauth.urls)),
    url(r'^textures$', texture_generator, name="texturegenerator"),
    url(r'^$', index, name='index'),
]

if settings.IS_PRODUCTION is False:
    additional = [url(r'^silk/', include('silk.urls', namespace='silk'))]
    urlpatterns.extend(additional)

