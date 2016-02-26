'''
Created on Feb 23, 2016

@author: User
'''
from django.db import models
from djPsych.exceptions import SettingException
from djexperiments.models import Experiment
from jsonfield import JSONField
from .BasicBlock import BaseSettingBlock
from django.contrib.contenttypes.fields import GenericRelation
# Create your models here.

class BaseGlobalSetting(models.Model):
    """
    Experimental settings that aplly to a whole experimental run, including stimuli creation settings
    
    Use its add_to_timeline method to push other setting objects containing settings related to particular blocks
    """
    
    class Meta:
        abstract=True
    
    experiment = models.ForeignKey(Experiment)
    name = models.CharField(max_length=20, help_text="An identifier for this set of settings, for example 'production' or 'test settings' ")
    max_consecutive_timeouts = models.IntegerField(blank=True, null=True, help_text="The experiment will automatically abort if this number if the subject does not respond fast enough to this many consecutive trials")
    max_total_timeouts = models.IntegerField(blank=True, null=True, help_text="The experiment will automatically abort if this many trials are allowed to timeout in total")
    fixation_cross = models.CharField(blank=True, null=True, max_length = 32, help_text="The path to fixation cross image, will be appended to static/your_app_name/")
    
    # The magic: keep a field to store a JSON of any extra field a researcher might need
    extra_parameters = JSONField(null=True, blank=True)
        
    def toDict(self):
        dictionary = dict(self.__dict__)
        del dictionary['_state']
        return dictionary
    
    def __str__(self):
        return self.name
    
    def get_all_blocks(self):
        """
        Returns all instances of subclasses of djsend.BasicBlock.BaseSettingBlock that point to this global setting
        
        Not ordered according to their 'order' field, I leave that to a overridable function
        """
        # TODO: it would be nice to be able to do like prefetch_related() when retrieving the experiment object. So this method would not be needed. 
        # I believe this would require a complex manager function mixed with raw SQL, so I will postpone until I find someone dumb enough to accept to do it
        blocks = []
        for block_type in self.experiment.block_models.all():
            model = block_type.model_class()
            instances = model.objects.filter(part_of=self)
            for inst in instances:
                blocks.append(inst)
        return blocks
    
    def build_timeline(self, blocks=None, request=None):
        """
        Builds an array of dict instances from the given blocks (instances of a subclass of djsend.BasicBlock.BaseSettingBlock).
        Assigns that array to this object's 'timeline' attribute
        
        This array MUST be json serializable (no objects).
        The default is to simply sort the blocks by their 'position_in_timeline' attribute, then call their .toDict() method
        """
        blocks.sort(key=lambda x:x.position_in_timeline)
        timeline=[]
        for block in blocks:
            timeline.append(block.toDict())
        self.timeline = timeline
        
        
        
class GenericGlobalSetting(BaseGlobalSetting):
    pass