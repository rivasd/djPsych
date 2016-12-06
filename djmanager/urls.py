'''
Created on Feb 22, 2016

@author: Daniel Rivas
'''

from django.conf.urls import url, include
from .views import home, allExperiments
from rest_framework import routers
from djexperiments.views import ExperimentViewSet
from djsend.views import ConfigViewSet


router = routers.DefaultRouter()
router.register(r'experiments', ExperimentViewSet, 'experiment')
router.register(r'(?P<exp_label>\w+)', ConfigViewSet, 'configs')


urlpatterns = [
    url(r'^$', home, name="home"),
    url(r'^api/', include(router.urls)),
    url(r'^profile/', include('djuser.urls', namespace='profiles')),
    url(r'^allExperiments/', allExperiments, name = "allExperiments"),
    url(r'(?P<exp_label>\w+)/', include('djexperiments.urls')),
]

