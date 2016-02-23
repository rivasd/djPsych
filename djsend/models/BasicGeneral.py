'''
Created on Feb 23, 2016

@author: User
'''
from django.db import models
from djPsych.exceptions import SettingException
from jsonfield import JSONField
# Create your models here.

class GlobalSetting(models.Model):
    """
    Experimental settings that aplly to a whole experimental run, including stimuli creation settings
    
    Use its add_to_timeline method to push other setting objects containing settings related to particular blocks
    """
    
    name = models.CharField(max_length=16, unique=True, help_text="An identifier for this set of settings, for example 'production' or 'test settings' ")
    max_consecutive_timeouts = models.IntegerField(help_text="The experiment will automatically abort if this number if the subject does not respond fast enough to this many consecutive trials")
    max_total_timeouts = models.IntegerField(help_text="The experiment will automatically abort if this many trials are allowed to timeout in total")
    fixation_cross = models.CharField(max_length = 32, help_text="The path to fixation cross image, will be appended to static/your_app_name/")
    
    # The magic: keep a field to store a JSON of any extra field a researcher might need
    extra_parameters = JSONField(null=True)
    
    def timeline(self):
        return self.timeline
    
    def pushToTimeline(self, settingObject):
        if not isinstance(settingObject, dict):
            raise SettingException("you can only add dictionaries to a timeline")
        self.timeline.append(settingObject)
        
    def toDict(self):
        dictionary = dict(self.__dict__)
        del dictionary['_state']
        return dictionary
    
    def __str__(self):
        return self.name