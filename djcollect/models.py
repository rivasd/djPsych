from django.db import models
from django.conf import settings
from djexperiments.models import Experiment
from djuser.models import Subject
from jsonfield import JSONField
from django.contrib.auth.models import User

# Create your models here.

class Participation(models.Model):
    """
    Represents a single participation of a Subject to an Experiment
      
    Meant to hold multiple Run objects, allows a participation to be completed in different attempts
    I recommend to always get a Participation instance with select_related()
    """
    
    experiment = models.ForeignKey(Experiment)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    complete = models.BooleanField()
    started = models.DateTimeField()
    # browser = models.CharField(max_length=64)
      
    #this is where the magic happens: store options in json format here so that experimental settings stay the same across sessions
    parameters = JSONField(null=True)

class Researcher(models.Model):
    """
    An extension on the Django user model that represents users who are researchers and allowed to get data.
    
    It does look like a Django permission, but first, I have no idea how to use them, and also, it's nice to store Researcher data like institution, degree, field, etc.
    """
    
    user = models.OneToOneField(User)
    institution = models.CharField(max_length=32, blank=True, null=True)
    researchs = models.ManyToManyField(Experiment, blank=True)