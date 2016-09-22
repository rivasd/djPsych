'''
Created on Feb 22, 2016

@author: Daniel Rivas
'''

from django.conf.urls import url, include
from .views import home, allExperiments


urlpatterns = [
    url(r'^$', home, name="home"),
    url(r'^profile/', include('djuser.urls', namespace='profiles')),
    url(r'^allExperiments/', allExperiments, name = "allExperiments"),
    url(r'(?P<exp_label>\w+)/', include('djexperiments.urls')),
]

