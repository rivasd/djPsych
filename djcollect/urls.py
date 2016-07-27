'''
Created on Mar 1, 2016

@author: Daniel Rivas
'''
from django.conf.urls import url
from .views import collect_all, learning_curve

urlpatterns =[
    url(r'^all$', collect_all, name="all"),
    url(r'^curve/(?P<participation>[1-9]\d*)$', learning_curve, name="plot")
]