'''
Created on Feb 24, 2016

@author: dan_1_000
'''

from django.db import models
from django.utils.translation import ugettext_lazy as l_
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
import json


class LinkedStimulus(models.Model):
    """
    Model used to implemented Generic many to many relations between a setting object and a stimuli object
    
    Since djPsych is heavily centered around the django admin, we need to be able to add stimuli objects to stuff as Inlines
    Both librairies adressing generic m2m relationships that I found are poor and, critically, offer no admin integration.
    """
    # First the link to the setting object
    setting_type = models.ForeignKey(ContentType)
    setting_id = models.PositiveIntegerField()
    setting = GenericForeignKey('setting_type', 'setting_id')
    
    # now the link to the simuli object
    stim_type = models.ForeignKey(ContentType)
    stim_id = models.PositiveIntegerField()
    stimulus = GenericForeignKey('stim_type', 'stim_id')
    
    
    


class BaseStimuli(models.Model):
    
    class Meta: 
        abstract=True
        
    
    name = models.CharField(max_length=26, help_text=l_("A simple name for this particular stimuli pair"))
    index = models.PositiveSmallIntegerField(blank=True, null=True, help_text=l_("Youn can give a number to indicate the order among the pairs that point to the same block. They will be given in asceding order."))
    stimulus = models.CharField(max_length=256, help_text=l_("The path to your stimuli file inside the static files folder we provided. Or it can be a short HTML string"))
    
    def to_Dict(self):
        dct = {}
        dct['name'] = self.name
        dct['stimulus'] = self.stimulus
        return json.dumps(dct)
    
class GenericStimuliPair(BaseStimuli):
    second_stim = models.CharField(max_length=256, help_text = l_("The path to your stimuli file inside the static files folder we provided. Or it can be a short HTML string"))
    
    def to_Dict(self):
        dct={}
        dct['name'] = self.name
        dct['stimuli'] = [self.stimulus, self.second_stim]
        return json.dumps(dct)
    pass

class GenericSingleStimuli(BaseStimuli):
    pass