'''
Created on Feb 29, 2016

@author: Daniel Rivas
'''

from django.db import models
from .runs import Run
from jsonfield import JSONField
import copy
import json

class BaseTrial(models.Model):
    """
    Abstract base class for all trial-data models. These represent a database table meant to hold the actual data collected from Subjects
    """
    
    class Meta:
        abstract = True
    
    internal_node_id = models.CharField(max_length=24)
    trial_index = models.IntegerField()
    trial_type = models.CharField(max_length=32)
    time_elapsed = models.IntegerField()
    timeout = models.BooleanField(blank=True, default=False)
    run = models.ForeignKey(Run)
    
    extra_data = JSONField(null=True, blank=True)
    
    @classmethod
    def get_actual_fields(cls):
        real_fields=[]
        for field in cls._meta.get_fields():
            if field.concrete:
                real_fields.append(field.name)
        return real_fields
    
    @classmethod
    def tweak_input(cls, data_dict):
        """
        Override this classmethod to make small corrections to the raw input dictionnary
        just before the object is created, but after the Run's pre_process_data is called
        """
        return data_dict
    
    @classmethod
    def create_from_raw_data(cls, data_dict):
        
        data_dict = cls.tweak_input(data_dict)
        extra_fields = []
        true_fields = cls.get_actual_fields()
        extra_data={}
        for key in data_dict:
            if not key in true_fields:
                # this field will not be supported by an init call, put it in extra_params
                extra_fields.append(key)
        
        # we identified the unsupported fields, now pop'em!
        for rebel_field in extra_fields:
            extra_data[rebel_field] = data_dict.pop(rebel_field)
        
        data_dict['extra_data'] = json.dumps(extra_data)
        # data_dict should be ok now
        return cls(**data_dict)
    
    def get_subject_id(self):
        return self.run.participation.subject.id
    
    def toDict(self):
        dictionary = dict(self.__dict__)
        if self.extra_data is not None:
            my_copy = copy.copy(self.extra_data) # shallow copy on purpose, you are not supposed to store nested objects in the extra_data !
            del dictionary['extra_data']
            for key, val in my_copy.iter():
                dictionary[key]=val
        dictionary['subject_id'] = self.get_subject_id()
        return dictionary
    
class CategorizationTrial(BaseTrial):
    handles = 'categorize'
    key_press = models.PositiveSmallIntegerField()
    rt = models.PositiveIntegerField()
    correct = models.BooleanField()
    category = models.CharField(max_length=24, null=True)
    
class SimilarityTrial(BaseTrial):
    handles = 'similarity'
    sim_score = models.PositiveIntegerField()
    rt = models.PositiveIntegerField()
    firstStim = models.CharField(max_length=24)
    secondStim = models.CharField(max_length=24)
    
    @classmethod
    def tweak_input(cls, data_dict):
        clean_dict = dict(data_dict)
        clean_dict['firstStim'] = data_dict['stimulus'][0]
        clean_dict['secondStim'] = data_dict['stimulus'][1]
        del clean_dict['stimulus']
        return clean_dict