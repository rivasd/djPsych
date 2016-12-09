'''
Created on Feb 23, 2016

@author: User
'''
from django.db import models
from django.utils.translation import ugettext_lazy as l_
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from jsonfield import JSONField
from .Instructions import Instruction
import json
from gfklookupwidget.fields import GfkLookupField
from pip.cmdoptions import verbose
from .BaseStimuli import BaseStimuli, Question


class BaseSettingBlock(models.Model):
    
    class Meta:
        abstract = True
        index_together = ['global_settings_type', 'global_settings_id'] # indexed because block settings will be frequently fetched by these fields, and rarely created.
        
        
    
    global_settings_type = models.ForeignKey(ContentType, help_text=l_("What kind of global configuration is this object part of?"))
    global_settings_id = models.PositiveIntegerField(help_text=l_("Which configuration object among your configs of the above type is this block attached to?"))
    part_of = GenericForeignKey('global_settings_type', 'global_settings_id')
    
    name = models.CharField(max_length=24, help_text=l_("A short name to describe this block"))
    position_in_timeline = models.PositiveSmallIntegerField(null=True, blank=True, help_text=l_("This number is used by the global setting this object is part of to build its timeline. It represents the ordinal position in which this block should come."))
    reprise = models.PositiveSmallIntegerField(null=True, blank=True, help_text=l_("If set, indicates that this block is a reprise of the n'th block, where n is the value of the field"))
    length= models.PositiveIntegerField(null=True, blank=True, help_text=l_("How many individual trials of this type should there be. You can leave blank if you don't need it"))
    type = models.CharField(max_length=26, help_text=l_("This will be passed as the 'type' parameter to jsPsych. It tells it which plugin to use to render these trials."))
    save_with = models.ForeignKey(ContentType, related_name='created_%(class)ss', help_text=l_("Choose the data model that will be used to save all trials that have their 'type' parameter equal to what you wrote above.\
     If You have different block-setting objects (like this one) that have the same 'type' but different 'save_with', then there is no guarantee which data-model will be used. This is because I think there is no real reason why two different 'categorization' blocks should be saved with different data-models: even if they have wildly different stimuli or timing settings, they should return the same kind of data."))
    has_practice = models.BooleanField(help_text=l_("Check if you want to mark this block to need a practice block before, useful to guide client-side JS code."), default=False)
    instructions = GenericRelation(Instruction)
    # magic field for dynamically added settings. Be careful the keys of this JSON object do not clash with the name of a field on the model, or they will get replaced
    extra_params = JSONField(null=True, blank=True)
    
    def toDict(self):
        if self.reprise is not None:
            return {'reprise': self.reprise}
        dictionary = dict(self.__dict__)
        del dictionary['_state']
        del dictionary['global_settings_id']
        del dictionary['global_settings_type_id']
        del dictionary['id']
        # add the params from the extra_params field. be careful for overrides!
        if self.extra_params is not None:
            for key, value in self.extra_params.items():
                dictionary[key] = value
        
        dictionary['instructions'] = self.sort_instructions()
        return dictionary
    
    
    
    def sort_instructions(self):
        instructions = {}
        instructions_before=[]
        instructions_after=[]
        for inst in self.instructions.all():
            if not inst.after:
                instructions_before.append(inst)
            else:
                instructions_after.append(inst)
        instructions_before.sort(key=lambda x:x.order)
        instructions_after.sort(key=lambda x:x.order)
        
        if instructions_after:
            instructions['after']={'type': 'instructions', 'pages': []}
            for instruction in instructions_after:
                instructions['after']['pages'].append(instruction.toDict()['text'])
                
        if instructions_before:
            instructions['before']={'type': 'instructions', 'pages': []}
            for instruction in instructions_before:
                instructions['before']['pages'].append(instruction.toDict()['text'])
        
        return instructions
    
    def get_parent_name(self):
        
        if self.part_of is not None and hasattr(self.part_of, 'name'):
            return self.part_of.name
        else:
            return l_("No name for the containing global config")
            
    get_parent_name.short_description= l_("Part of")
    
class GenericSettingBlock(BaseSettingBlock):
    
    class Meta:
        verbose_name= l_("Experimental block basic configuration")
    
    def __str__(self):
        # Translators: 
        return l_('Exp. block "')+self.name+'"'
    pass

class SurveyMultiChoiceBlock(BaseSettingBlock):
    
    preamble = models.TextField(help_text = l_("A short paragraphe that will display at the top of your questions page"))
    horizontal = models.BooleanField(help_text=l_("Do you want the answer choices to be displayed horizontally? If so, put true, else put false."), default=False)
    
    questions = GenericRelation(Question)
    
    def toDict(self):
        initial = super(SurveyMultiChoiceBlock,self).toDict()
        
        questions_list = []
        option_labels_list = []
        question_requirement_list = []
        
        for question in self.questions.all():
            questions_list.append(question.question_label)
            option_labels_list.append(question.answer_options.split(','))
            question_requirement_list.append(question.required)
               
        initial['questions'] = questions_list
        initial['options'] = option_labels_list
        initial['required'] = question_requirement_list
        initial['preamble'] = self.preamble
        
        return initial


class SurveyLikertBlock(BaseSettingBlock):
    
    questions = GenericRelation(Question)
    
    def toDict(self):
        
        initial = super(SurveyLikertBlock,self).toDict()
        
        questions_list = []
        option_labels_list = []
        question_requirement_list = []
        
        for question in self.questions.all():
            questions_list.append(question.question_label)
            option_labels_list.append(question.answer_options.split(','))
            question_requirement_list.append(question.required)           
            
        initial['questions'] = questions_list
        initial['labels'] = option_labels_list
        initial['required'] = question_requirement_list
        
        return initial
    
class SurveyTextBlock(BaseSettingBlock):
    
    questions = GenericRelation(Question)
    preamble = models.TextField(blank = True, null = True, help_text = l_("A short paragraphe that will display at the top of your questions page"))
    
    def toDict(self):
        
        initial = super(SurveyTextBlock,self).toDict()
        
        questions_list = []
        option_labels_list = []
        question_requirement_list = []
        
        for question in self.questions.all():
            questions_list.append(question.question_label)
            option_labels_list.append(question.answer_options.split(','))
            question_requirement_list.append(question.required)           
            
        initial['questions'] = questions_list
        initial['labels'] = option_labels_list
        initial['required'] = question_requirement_list
        initial['preamble'] = self.preamble
        
        return initial
        
        
        
        
        
        
        
    
    

