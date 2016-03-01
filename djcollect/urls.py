'''
Created on Mar 1, 2016

@author: Daniel Rivas
'''
from django.conf.urls import url
from .views import collect_all

urlpatterns =[
    url(r'^all$', collect_all, name="all")
]