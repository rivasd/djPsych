'''
Created on Feb 22, 2016

@author: Daniel Rivas
'''
from django.conf.urls import url
from djexperiments.views import lobby, launch, summary
from djcollect.views import sendSettings
from djreceive.views import save


urlpatterns =[
    url(r'^$', lobby, name='lobby'),
    url(r'^request$', sendSettings, name='request'),
    url(r'^save$', save, name='save'),
    url(r'^launch$', launch, name='launch'),
    url(r'^summary$', summary, name='summary'),
]

