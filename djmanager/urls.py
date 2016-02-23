'''
Created on Feb 22, 2016

@author: Daniel Rivas
'''

from django.conf.urls import url, include
from djexperiments.models import Experiment
from djexperiments.views import lobby, launch, summary
from djsend.views import sendSettings
from djreceive.views import save
from .views import home

urlpatterns = [
    url(r'^$', home, name="home"),
    url(r'^request$', sendSettings, name='request'),
    url(r'^save$', save, name='save')
]

inner = [
    url(r'^$', lobby, name="lobby"),
    url(r'^launch$', launch, name='launch'),
    url(r'^summary$', summary, name='summary')
]

for exp in Experiment.objects.all():
    if exp.is_active:
        regex = r'^'+exp.label+'/'
        urlpatterns.append(url(regex, include(inner, namespace=exp.label), {'exp_label': exp.label}))