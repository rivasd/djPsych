'''
Created on Feb 22, 2016

@author: Daniel Rivas
'''
from django.conf.urls import url, include
from djexperiments.views import lobby, launch, summary, sandbox, debrief, upload_resource, exp_filesystem
from djreceive.views import save
from djpay.views import claim

app_name = "experiments"

urlpatterns =[
    url(r'^$', lobby, name='lobby'),
    url(r'^request/', include('djsend.urls', namespace='request')),
    url(r'^save$', save, name='save'),
    url(r'^launch$', launch, name='launch'),
    url(r'^summary$', summary, name='summary'),
    url(r'^claim/(?P<code>[1-9]\d*)$', claim, name='claim'),
    url(r'^collect/', include('djcollect.urls', namespace='collect')),
    url(r'^sandbox$', sandbox, name="sandbox"),
    url(r'^debrief$', debrief, name="debrief"),
    url(r'^upload$', upload_resource, name="upload"),
    url(r'^files$', exp_filesystem, name="browse")
]

