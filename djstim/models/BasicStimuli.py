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
    setting_type = models.ForeignKey(ContentType, related_name="stimlinks", on_delete=models.CASCADE)
    setting_id = models.PositiveIntegerField()
    setting = GenericForeignKey('setting_type', 'setting_id')
    
    # now the link to the simuli object
    stim_type = models.ForeignKey(ContentType, related_name='blocklinks', on_delete=models.CASCADE)
    stim_id = models.PositiveIntegerField()
    stimulus = GenericForeignKey('stim_type', 'stim_id')
    #TODO: maybe use grappelli's inline ordering feature instead of asking users to directly enter an index number... someone (not me!) should look into that
    index = models.PositiveSmallIntegerField(blank=True, null=True, help_text=l_("Youn can give a number to indicate the order among the pairs that point to the same block. They will be given in asceding order."))
    is_practice = models.BooleanField(default=False, help_text=l_("Check this if this stimuli should be in the practice set"))
    # TODO: There is a redundance between setting stimuli as practice and the ability to set blocks as practice blocks. What to do?
    
    
    def get_experiment(self):
        if hasattr(self.setting, 'experiment'):
            return self.setting.experiment
        else:
            return self.setting.part_of.experiment
    
    


class BaseStimuli(models.Model):
    
    class Meta: 
        abstract=True
        
    
    name = models.CharField(max_length=26, help_text=l_("A simple name for this particular stimuli pair"))
    #TODO: change the stim to be an actual fileField so that users can upload real images instead of a path.
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