'''
Created on Mar 2, 2016

@author: Daniel Rivas
'''
from django.conf.urls import url
from .views import sendSettings, serve_snippet

urlpatterns = [
    url(r'^$', sendSettings, name='fullconfig'),
    url(r'^snippet/(?P<template>\w+[.]html)$', serve_snippet, name="snippet")
]