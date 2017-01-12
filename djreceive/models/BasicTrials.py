'''
Created on Feb 29, 2016

@author: Daniel Rivas
'''

from django.db import models
from .runs import Run
from jsonfield import JSONField
import copy
from django.template.defaultfilters import first


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
        
        data_dict['extra_data'] = extra_data
        # data_dict should be ok now
        return cls(**data_dict)
    
    def get_full_field_names(self):
        headers=['subject_id']
        for field in self._meta.get_fields():
            if field.concrete and not field.auto_created and not field.is_relation and not field.name == 'extra_data':
                headers.append(field.name)
        if self.extra_data is not None:
            for key in self.extra_data:
                headers.append(key)
        return set(headers)
            
    def get_subject_id(self):
        return self.run.participation.subject.id
    
    def toDict(self):
        dictionary = dict(self.__dict__)
        if self.extra_data is not None:
            my_copy = copy.copy(self.extra_data) # shallow copy on purpose, you are not supposed to store nested objects in the extra_data !
            del dictionary['extra_data']
            for key, val in my_copy.items():
                dictionary[key]=val
        del dictionary['_state']
        del dictionary['run_id']
        del dictionary['id']
        return dictionary
    
class AnimationTrial(BaseTrial):
    handles = 'animation'
    animation_sequence = JSONField(null=False, blank=True)
    responses = JSONField(null=False, blank=True)
        
class AudioCatTrial(BaseTrial):
    handles = 'audio-categorization'
    rt = models.PositiveIntegerField
    stimulus = models.CharField(max_length=128)
    key_press = models.SmallIntegerField(null = True)
    result = models.CharField(max_length=128)
    
class AudioSimilarityTrial(BaseTrial):
    handles = 'audio-similarity'
    sim_score = models.PositiveIntegerField()
    rt = models.PositiveIntegerField()
    firstStim = models.CharField(max_length=1024)
    secondStim = models.CharField(max_length=1024)
    
class ButtonResponseTrial(BaseTrial):
    handles = 'button-response'
    button_pressed = models.PositiveIntegerField()
    rt = models.PositiveIntegerField()
    
class CategorizationTrial(BaseTrial):
    handles = 'categorize'
    key_press = models.PositiveSmallIntegerField()
    rt = models.PositiveIntegerField()
    correct = models.BooleanField()
    category = models.CharField(max_length=24, null=True)
    
class CategorizeAnimationTrial(BaseTrial):
    handles = 'categorize-animation'
    key_press = models.PositiveSmallIntegerField()
    rt = models.PositiveIntegerField()
    correct = models.BooleanField()
    
class ForcedChoice(BaseTrial):
    handles = 'forcedchoice'
    rt = models.PositiveIntegerField()
    chosen = models.IntegerField()
    leftRating = models.IntegerField(null=True)
    rightRating = models.IntegerField(null=True)
    first = models.CharField(max_length=1024, null=True)
    last = models.CharField(max_length=1024, null=True)
    
class FreeSortTrial(BaseTrial):
    handles = 'free-sort'
    init_locations = JSONField(null = False, blank = True)
    moves = JSONField(null = False, blank = True)
    final_locations = JSONField(null = False, blank = True)
    rt = models.PositiveIntegerField()
    
class MultiStimMultiResponseTrial(BaseTrial):
    handles = 'multi-stim-multi-response'
    stimulus = JSONField(null = False, blank = True)
    key_press = JSONField(null = False, blank = True)
    rt = JSONField(null = False, blank = True)
    
class Rating(BaseTrial):
    handles = 'rating'
    rt = models.PositiveIntegerField()
    rating = models.IntegerField()
    stimulus = models.CharField(max_length=128)
    
class ReconstructionTrial(BaseTrial):
    handles = 'reconstruction'
    start_value = models.FloatField()
    final_value = models.FloatField()
    rt = models.PositiveIntegerField()
    
class SameDifferentTrial(BaseTrial):
    handles = 'same-different'
    stimulus = JSONField(null = False, blank = True)
    key_press = models.IntegerField()
    rt = models.PositiveIntegerField()
    correct = models.BooleanField()
    answer = models.CharField(max_length=16)   
    
class SimilarityTrial(BaseTrial):
    handles = 'similarity'
    sim_score = models.PositiveIntegerField()
    rt = models.PositiveIntegerField()
    firstStim = models.CharField(max_length=24)
    secondStim = models.CharField(max_length=24)
    
    @classmethod
    def tweak_input(cls, data_dict):
        clean_dict = dict(data_dict)
        if 'stimulus' in data_dict:
            clean_dict['firstStim'] = data_dict['stimulus'][0]
            clean_dict['secondStim'] = data_dict['stimulus'][1]
            del clean_dict['stimulus']
        return clean_dict
    
class SingleAudioTrial(BaseTrial):
    handles = 'single-audio'
    stimulus = models.CharField(max_length=128)
    key_press = models.IntegerField()
    rt = models.IntegerField()
    
class SingleStimTrial(BaseTrial):
    handles = 'single-stim'
    stimulus = models.CharField(max_length=128)
    key_press = models.IntegerField()
    rt = models.IntegerField()
        
class SurveyLikert(BaseTrial):
    handles = 'survey-likert'
    rt = models.PositiveIntegerField()
    responses = JSONField(null=False, blank=True)
    
class SurveyMultiChoice(BaseTrial):
    handles = 'survey-multi-choice'
    rt = models.PositiveIntegerField
    responses = JSONField(null=False, blank=True)
    
class SurveyTextTrial(BaseTrial):
    handles = 'survey-text'
    rt = models.PositiveIntegerField
    responses = JSONField(null=False, blank=True)

class XABTrial(BaseTrial):
    handles = 'xab'
    key_press = models.IntegerField()
    rt = models.IntegerField()
    correct = models.BooleanField()
    
    
    
    