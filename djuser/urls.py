'''
Created on Mar 4, 2016

@author: Daniel Rivas
'''
from django.conf.urls import url
from .views import show_profile

app_name = "users"

urlpatterns =[
    url(r'^$', show_profile, name='personal')   # matches /webexp/profile/
]                                               # '/webexp' is matched in djPsych.urls, and 'profile/' is matched in djmanager.urls which finally includes this urlpatterns