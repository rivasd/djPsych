'''
Created on Feb 28, 2016

@author: dan_1_000
'''
from django.db import models
from djcollect.models import Participation
# Create your models here.

class Run(models.Model):
    """
    Represents a single run of an experiment for a given subject. This is because one subject may split his Participation to
    an Experiment over multiple Runs
    """
    participation = models.ForeignKey(Participation)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    browser = models.CharField(max_length=16, editable=False, null=True)
    browser_version = models.CharField(max_length=8, editable=False, null=True)
    
    def pre_process_data(self, data_object, request):
        """
        Override this method to make any adjustments to the raw data that is about to be turned to a Trial object attached to this Run
        """
        
        return data_object