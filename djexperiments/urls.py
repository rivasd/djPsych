'''
Created on Feb 22, 2016

@author: Daniel Rivas
'''
from django.conf.urls import url, include
from djexperiments.views import lobby, launch, summary, sandbox
from djreceive.views import save
from djpay.views import claim


urlpatterns =[
    url(r'^$', lobby, name='lobby'),
    url(r'^request/', include('djsend.urls', namespace='request')),
    url(r'^save$', save, name='save'),
    url(r'^launch$', launch, name='launch'),
    url(r'^summary$', summary, name='summary'),
    url(r'^claim/(?P<code>[1-9]\d*)$', claim, name='claim'),
    url(r'^collect/', include('djcollect.urls', namespace='collect')),
    url(r'^sandbox$', sandbox, name="sandbox")
]

