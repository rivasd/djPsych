'''
Created on Feb 28, 2016

@author: dan_1_000
'''
from django.db import models
from djcollect.models import Participation
from django.contrib.contenttypes.models import ContentType
# Create your models here.

class Run(models.Model):
    """
    Represents a single run of an experiment for a given subject. This is because one subject may split his Participation to
    an Experiment over multiple Runs
    """
    participation = models.ForeignKey(Participation)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    browser = models.CharField(max_length=16, null=True)
    browser_version = models.CharField(max_length=8, null=True)
    used_trials = models.ManyToManyField(ContentType)
    
    
    def pre_process_data(self, data_object, request):
        """
        Override this method to make any adjustments to the raw data that is about to be turned to a Trial object attached to this Run
        """
        
        return data_object
    
    def get_trials(self):
        trials = []
        for trial_ct in self.used_trials.all():
            for trial in trial_ct.model_class().objects.filter(run=self).order_by("trial_index"):
                trials.append(trial)
        return trials
            