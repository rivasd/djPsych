'''
Created on Feb 24, 2016

@author: dan_1_000
'''

from django.db import models
from django.utils.translation import ugettext_lazy as l_
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
import json

class BaseStimuli(models.Model):
    
    class Meta: 
        abstract=True
        
    block_type = models.ForeignKey(ContentType)
    block_id = models.PositiveIntegerField()
    block_setting = GenericForeignKey('block_type', 'block_id')
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