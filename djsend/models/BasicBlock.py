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
    position_in_timeline = models.PositiveSmallIntegerField(default=0, help_text=l_("This number is used by the global setting this object is part of to build its timeline. It represents the ordinal position in which this block should come."))
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
                if instruction.show_clickable_nav:
                    instructions['after']["show_clickable_nav"] = True
                if instruction.key_forward:
                    instructions['before']["key_forward"] = instruction.key_forward    
                instructions['after']['pages'].append(instruction.toDict()['text'])
                
        if instructions_before:
            instructions['before']={'type': 'instructions', 'pages': []}
            for instruction in instructions_before:
                
                if instruction.show_clickable_nav:
                    instructions['before']["show_clickable_nav"] = True
                if instruction.key_forward:
                    instructions['before']["key_forward"] = instruction.key_forward
                
                
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

class AnimationBlock(BaseSettingBlock):
    
    frame_time = models.IntegerField(default = 250, help_text=l_("How long to display each image (in milliseconds)"))
    frame_isi = models.IntegerField(default = 0, help_text=l_("If greater than 0, then a gap will be shown between each image in the sequence. This parameter specifies the length of the gap."))
    sequence_reps = models.IntegerField(default = 1, help_text=l_("How many times to show the entire sequence. There will be no gap (other than the gap specified by frame_isi) between repetitions"))
    choices = models.CharField(blank=True, max_length = 1024, help_text=l_(" keys that the subject is allowed to press in order to respond to the stimulus. You have separate them with a coma. ex: k,l"))
    prompt = models.CharField(max_length=256, blank=True, help_text=l_("Any content here will be displayed below the stimulus, as a reminder to the participant"))
    
    def toDict(self):
        initial = super(AnimationBlock,self).toDict()
        initial['choices'] = self.choices.split(',')
        initial['prompt'] = "<p class=\"prompt\"> {} </p>".format(self.prompt)
        return initial
    
class ButtonResponseBlock(BaseSettingBlock):
    is_html = models.BooleanField(default = False, help_text=l_("If stimulus is an HTML-formatted string, this parameter needs to be set to true."))
    choices = models.CharField(blank=True, max_length = 1024, help_text=l_(" keys that the subject is allowed to press in order to respond to the stimulus. You have separate them with a coma. ex: k,l"))
    prompt = models.CharField(max_length=256, blank=True, help_text=l_("Any content here will be displayed below the stimulus, as a reminder to the participant"))
    timing_stim = models.IntegerField(help_text=l_("How long to show the stimulus for in milliseconds. If the value is -1, then the stimulus will be shown until the subject makes a response."), default =-1)
    timing_response = models.IntegerField(help_text=l_("time limit for the participant before the trial automatically advances"), default=-1)
    response_ends_trial = models.BooleanField(help_text=l_("If true, then the trial will end whenever the subject makes a response (assuming they make their response before the cutoff specified by the  timing_response parameter). If false, then the trial will continue until the value for  timing_response is reached."), default=True)
    
    def toDict(self):
        initial = super(ButtonResponseBlock,self).toDict()
        initial['choices'] = self.choices.split(',')
        initial['prompt'] = "<p class=\"prompt\"> {} </p>".format(self.prompt)
        return initial
    
class CategorizeAnimationBlock(BaseSettingBlock):
    choices = models.CharField(blank=True, max_length = 1024, help_text=l_(" keys that the subject is allowed to press in order to respond to the stimulus. You have separate them with a coma. ex: k,l"))
    correct_text = models.CharField(max_length= 64, help_text=l_("String to show when the correct answer is given."), default = "Correct.")
    incorrect_text = models.CharField(max_length= 64, help_text=l_("String to show when the wrong answer is given."), default = "Wrong.")
    frame_time = models.IntegerField(default = 250, help_text=l_("How long to display each image (in milliseconds)."))
    sequence_reps = models.IntegerField(default = 1, help_text=l_("How many times to show the entire sequence."))
    allow_response_before_complete = models.BooleanField(default = False, help_text=l_("If true, the subject can respond before the animation sequence finishes."))
    prompt = models.CharField(max_length=256, blank=True, help_text=l_("Any content here will be displayed below the stimulus, as a reminder to the participant"))
    timing_feedback_duration = models.IntegerField(default = 2000, help_text=l_("How long to show the feedback (milliseconds)."))
    
    def toDict(self):
        initial = super(ButtonResponseBlock,self).toDict()
        initial['choices'] = self.choices.split(',')
        initial['prompt'] = "<p class=\"prompt\"> {} </p>".format(self.prompt)
        return initial
    
class FreeSortBlock(BaseSettingBlock):
    stim_height = models.PositiveIntegerField(default = 100, help_text=l_("The height of the images in pixels."))
    stim_width = models.PositiveIntegerField(default = 100, help_text=l_("The width of the images in pixels."))
    sort_area_height = models.PositiveIntegerField(default = 800, help_text=l_("The height of the container that subjects can move the stimuli in. Stimuli will be constrained to this area."))
    sort_area_width = models.PositiveIntegerField(default = 800, help_text=l_("The width of the container that subjects can move the stimuli in. Stimuli will be constrained to this area."))
    prompt = models.CharField(max_length=256, blank=True, help_text=l_("The intention is that it can be used to provide a reminder about the action the subject is supposed to take (e.g. which key to press)."))
    prompt_location = models.CharField(default = 'above', max_length=24, help_text=l_("Indicates whether to show the prompt 'above' or 'below' the sorting area."))
    
    def toDict(self):
        initial = super(FreeSortBlock,self).toDict()
        initial['prompt'] = "<p class=\"prompt\"> {} </p>".format(self.prompt)
        return initial
    
class MultiStimMultiResponseBlock(BaseSettingBlock):
    is_html = models.BooleanField(default = False, help_text=l_("If stimulus is an HTML-formatted string, this parameter needs to be set to true."))
    choices = models.CharField(blank=True, max_length = 1024, help_text=l_(" keys that the subject is allowed to press in order to respond to the stimulus. You have separate each choice with a coma and the choices for different responses with a semi-colon. ex: k,l;f,g;g,h"))
    prompt = models.CharField(max_length=256, blank=True, help_text=l_("The intention is that it can be used to provide a reminder about the action the subject is supposed to take (e.g. which key to press)."))
    timing_stim = models.CharField(blank=True, max_length = 1024, help_text=l_(" length of time to display the corresponding stimulus for in milliseconds. Separe them with a coma and no space."))
    timing_response = models.IntegerField(help_text=l_("How long to wait for the subject to make all responses before ending the trial in milliseconds. If the subject fails to make a response in a response group before this timer is reached, the the subject's response for that response group will be recorded as -1 for the trial and the trial will end. If the value of this parameter is -1, then the trial will wait for a response indefinitely."), default=-1)
    response_ends_trial = models.BooleanField(help_text=l_("If true, then the trial will end whenever the subject makes a response (assuming they make their response before the cutoff specified by the  timing_response parameter). If false, then the trial will continue until the value for timing_response is reached."), default=True)
    
    
    def toDict(self):
        initial = super(MultiStimMultiResponseBlock,self).toDict()
        initial['choices'] = [x.split(',') for x in self.choices.split(';')]
        initial['timing_stim'] = self.timing_stim.split(',')
        initial['prompt'] = "<p class=\"prompt\"> {} </p>".format(self.prompt)
        return initial

class ReconstructionBlock(BaseSettingBlock):
    starting_value = models.FloatField(default = 0.5, help_text=l_("The starting value of the stimulus parameter."))
    step_size = models.FloatField(default = 0.05, help_text=l_("The change in the stimulus parameter caused by pressing one of the modification keys."))
    key_increase = models.CharField(max_length=2, default='h', help_text=l_("The key to press for increasing the parameter value."))
    key_decrease = models.CharField(max_length=2, default='g', help_text=l_("The key to press for decreasing the parameter value."))
    
class SameDifferentBlock(BaseSettingBlock):
    is_html = models.BooleanField(default = False, help_text=l_("If stimulus is an HTML-formatted string, this parameter needs to be set to true."))
    same_key = models.CharField(max_length = 2, default = 'q', help_text=l_("The key that subjects should press to indicate that the two stimuli are the same."))
    different_key = models.CharField(max_length = 2, default = 'p', help_text=l_("The key that subjects should press to indicate that the two stimuli are different."))
    timing_first_stim = models.IntegerField(default = 1000, help_text=l_("How long to show the first stimulus for in milliseconds. If the value of this parameter is -1 then the stimulus will be shown until the subject presses any key."))
    timing_gap = models.IntegerField(default = 500, help_text= l_("How long to show a blank screen in between the two stimuli."))
    timing_second_stim = models.IntegerField(default = 1000, help_text= l_("How long to show the second stimulus for in milliseconds. If the value of this parameter is -1 then the stimulus will be shown until the subject responds."))
    prompt = models.CharField(max_length=256, blank=True, help_text=l_("The intention is that it can be used to provide a reminder about the action the subject is supposed to take (e.g. which key to press)."))
    
    def toDict(self):
        initial = super(SameDifferentBlock,self).toDict()
        initial['prompt'] = "<p class=\"prompt\"> {} </p>".format(self.prompt)
        return initial
    
class SingleAudioBlock(BaseSettingBlock):
    choices = models.CharField(blank=True, max_length = 1024, help_text=l_(" keys that the subject is allowed to press in order to respond to the stimulus. You have separate them with a coma. ex: k,l"))
    prompt = models.CharField(max_length=256, blank=True, help_text=l_("The intention is that it can be used to provide a reminder about the action the subject is supposed to take (e.g. which key to press)."))
    timing_response = models.IntegerField(help_text=l_("time limit for the participant before the trial automatically advances"), default=-1)
    response_ends_trial = models.BooleanField(help_text=l_("If true, then the trial will end whenever the subject makes a response (assuming they make their response before the cutoff specified by the  timing_response parameter). If false, then the trial will continue until the value for  timing_response is reached."), default=True)
    
    def toDict(self):
        initial = super(SingleAudioBlock,self).toDict()
        initial['choices'] = self.choices.split(',')
        initial['prompt'] = "<p class=\"prompt\"> {} </p>".format(self.prompt)
        return initial
    
class SingleStimBlock(BaseSettingBlock):
    is_html = models.BooleanField(default = False, help_text=l_("If stimulus is an HTML-formatted string, this parameter needs to be set to true."))
    choices = models.CharField(blank=True, max_length = 1024, help_text=l_(" keys that the subject is allowed to press in order to respond to the stimulus. You have separate them with a coma. ex: k,l"))
    prompt = models.CharField(max_length=256, blank=True, help_text=l_("The intention is that it can be used to provide a reminder about the action the subject is supposed to take (e.g. which key to press)."))
    timing_stim = models.IntegerField(default = -1, help_text=l_("How long to show the stimulus for in milliseconds. If the value is -1, then the stimulus will be shown until the subject makes a response."))
    timing_response = models.IntegerField(help_text=l_("time limit for the participant before the trial automatically advances"), default=-1)
    response_ends_trial = models.BooleanField(help_text=l_("If true, then the trial will end whenever the subject makes a response (assuming they make their response before the cutoff specified by the  timing_response parameter). If false, then the trial will continue until the value for  timing_response is reached."), default=True)
    
    def toDict(self):
        initial = super(SingleStimBlock,self).toDict()
        initial['choices'] = self.choices.split(',')
        initial['prompt'] = "<p class=\"prompt\"> {} </p>".format(self.prompt)
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
            if question.answer_options is not None:
                option_labels_list.append(question.answer_options.split(','))
            question_requirement_list.append(question.required)           
            
        initial['questions'] = questions_list
        initial['labels'] = option_labels_list
        initial['required'] = question_requirement_list
        initial['preamble'] = self.preamble
        
        return initial
    
class XABBlock(BaseSettingBlock):
    
    is_html = models.BooleanField(default = False, help_text=l_("If stimulus is an HTML-formatted string, this parameter needs to be set to true."))
    left_key = models.CharField(max_length = 2, default = 'q', help_text=l_("Which key the subject should press to indicate that the target is on the left side."))
    right_key = models.CharField(max_length = 2, default = 'p', help_text=l_("Which key the subject should press to indicate that the target is on the right side."))
    prompt = models.CharField(max_length=256, blank=True, help_text=l_("The intention is that it can be used to provide a reminder about the action the subject is supposed to take (e.g. which key to press)."))
    timing_x = models.IntegerField(default = 1000, help_text=l_("How long to show the X stimulus for in milliseconds."))
    timing_xab_gap = models.IntegerField(default = 1000, help_text=l_("How long to show a blank screen in between X and AB in milliseconds."))
    timing_ab = models.IntegerField(default = -1, help_text=l_("How long to show A and B in milliseconds. If the value of this parameter is -1, then the stimuli will remain on the screen until a response is given."))
    timing_response = models.IntegerField(default = -1, help_text=l_("The maximum duration to wait for a response, measured from the onset of the AB portion of the trial. If -1, then the trial will wait indefinitely for a response."))
        
    def toDict(self):
        initial = super(XABBlock,self).toDict()
        initial['prompt'] = "<p class=\"prompt\"> {} </p>".format(self.prompt)
        return initial    
        
        
        
        
    
    

