'''
Created on Feb 24, 2016

@author: Daniel Rivas
'''
from .BasicBlock import BaseSettingBlock
from django.utils.translation import ugettext_lazy as l_
from django.db import models
from jsonfield import JSONCharField

class CategorizationBlock(BaseSettingBlock):
    type = 'categorize'
    
    correct_text = models.CharField(max_length=64, help_text=l_("Text to show after a subject makes a correct categorization"))
    incorrect_text = models.CharField(max_length=64, help_text=l_("Text to show after a subject makes an incorrect categorization"))
    prompt = models.CharField(max_length=64, help_text=l_("Text to show beneath the stimuli for all trials, as a reminder of what to do."))
    timeout_message = models.CharField(max_length=64, help_text=l_("Text to display when a subject does not respond fast enough and the trial times out"))
    
    show_stim_with_feedback = models.BooleanField(default=False, help_text= l_("Should the stimulus be shown together with the feedback text?"))
    show_feedback_on_timeout = models.BooleanField(default=False, help_text=l_("Should we show the feedback even when the trial times out?"))
    timing_stim = models.IntegerField(null=True, help_text=l_("How long to show the stimulus for (milliseconds). If -1, then the stimulus is shown until a response is given."))
    timing_feedback_duration = models.IntegerField(null=True, help_text=l_("How long to show the feedback for "))
    timing_response = models.IntegerField(null=True, help_text=l_("The maximum time allowed for a response. If -1, then the experiment will wait indefinitely for a response."))
    timing_post_trial = models.IntegerField(null=True, help_text=l_("Sets the time, in milliseconds, between the current trial and the next trial."))
    
    def toDict(self):
        initial = super(CategorizationBlock, self).toDict()
        initial['correct_text'] = "<p class=\"feedback success\">{} </p>".format(self.correct_text)
        initial['incorrect_text'] = "<p class=\"feedback error\">{} </p>".format(self.incorrect_text)
        initial['prompt'] = "<p class=\"prompt\">{} </p>".format(self.prompt)
        initial['timeout_message'] = "<p class=\"feedback error\">{} </p>".format(self.timeout_message)
        return initial
        
class SimilarityBlock(BaseSettingBlock):
    type = 'similarity'
    
    show_response_choices = (
        ('FIRST_STIMULUS', l_('With the first stimulus')),
        ('SECOND_STIMULUS', l_('With the second stimulus')),
        ('POST_STIMULUS', l_('After both stimuli have disappeared')),                 
    )
    
    intervals = models.IntegerField(help_text=l_("How many different choices are available on the slider. For example, 5 will limit the options to 5 different places on the slider"))
    show_ticks = models.BooleanField(help_text=l_("If true, then the slider will have tick marks indicating where the response options lie on the slider."))
    show_response = models.CharField(max_length=16, choices=show_response_choices, help_text=l_("When should the response slider be shown?"))
    timing_fixation_cross = models.IntegerField(default = 1500, help_text=l_("How long to show the fixation cross for in milliseconds."))
    timing_first_stim = models.IntegerField(help_text=l_("How long to show the first stimulus for in milliseconds."))
    timing_second_stim = models.IntegerField(help_text=l_("How long to show the second stimulus for in milliseconds. -1 will show the stimulus until a response is made by the subject."))
    timing_image_gap = models.IntegerField(help_text=l_("How long to show a blank screen in between the two stimuli."))
    timing_post_trial = models.IntegerField(help_text=l_("Sets the time, in milliseconds, between the current trial and the next trial."))
    is_audio = models.BooleanField(default = False, help_text=l_("If you use audio stimuli, check this box."))

    timeout = models.IntegerField(help_text=l_("time limit for the participant before the trial automatically advances"), default=-1)
    timeout_message = models.CharField(max_length=128, blank=True, null=True, help_text=l_('message to display if the participant takes too long to respond'))

    
    prompt = models.CharField(max_length=32, blank=True, help_text=l_("Any content here will be displayed below the stimulus, as a reminder to the participant"))
    labels = JSONCharField(max_length=64, help_text=l_('An array of tags to label the slider. must be eclosed in square brackets. Each label must be enclosed in double quotation marks. Labels must be separated by a single comma.'))
    
    def toDict(self):
        initial = super(SimilarityBlock, self).toDict()
        initial['prompt'] = "<p class=\"prompt\"> {} </p>".format(self.prompt)
        initial['timeout_message'] = "<p class=\"feedback error\">{} </p>".format(self.timeout_message)
        return initial
    
class AudioSimilarityBlock(BaseSettingBlock):
    type = 'audio-similarity'
    
    
    intervals = models.IntegerField(help_text=l_("How many different choices are available on the slider. For example, 5 will limit the options to 5 different places on the slider"))
    show_ticks = models.BooleanField(help_text=l_("If true, then the slider will have tick marks indicating where the response options lie on the slider."))
    timing_first_stim = models.IntegerField(help_text=l_("How long to play the first sound for in milliseconds."))
    timing_second_stim = models.IntegerField(help_text=l_("How long to play the second sound for in milliseconds. -1 will show the stimulus until a response is made by the subject."))
    timing_gap = models.IntegerField(help_text=l_("How long is the gap between the two sounds"), blank = True, null = True)

    timeout = models.IntegerField(help_text=l_("time limit for the participant before the trial automatically advances"), default=-1)
    timeout_message = models.CharField(max_length=128, blank=True, null=True, help_text=l_('message to display if the participant takes too long to respond'))

    
    prompt = models.CharField(max_length=32, blank=True, help_text=l_("Any content here will be displayed below the stimulus, as a reminder to the participant"))
    labels = JSONCharField(max_length=64, help_text=l_('An array of tags to label the slider. must be eclosed in square brackets. Each label must be enclosed in double quotation marks. Labels must be separated by a single comma.'))
    
    def toDict(self):
        initial = super(AudioSimilarityBlock, self).toDict()
        initial['prompt'] = "<p class=\"prompt\"> {} </p>".format(self.prompt)
        initial['timeout_message'] = "<p class=\"feedback error\">{} </p>".format(self.timeout_message)
        return initial
    
class HTMLBlock(BaseSettingBlock):
    type = 'html'
    
    url = models.URLField()
    
    
class RatingBlock(BaseSettingBlock):
    type = 'rating'
    
    
    is_html = models.BooleanField(help_text=l_("True if the stimulus is html instead of being a image url"))
    
    prompt = models.CharField(max_length=256, blank=True, help_text=l_("Any content here will be displayed below the stimulus, as a reminder to the participant"))
    
    response = models.CharField(max_length = 16, default = 'slider', choices = (('boxes','boxes'),('slider','slider')), help_text=l_("Choice between displaying a slider or choices in boxes for response"))
    
    labels = models.CharField(max_length = 1024,blank=True, help_text=l_("Sets the labels that you can slide on with the slider. You have separate them with a coma and no spaces."))
    intervals = models.CharField(max_length = 16, blank=True, help_text=l_("The first and last value associated with the labels on the slider. You have to separate the two with a coma and no spaces"))
    show_ticks = models.BooleanField(blank=True, help_text=l_("True if you want to show ticks on the slider"))
    
    choices = models.CharField(blank=True, max_length = 1024, help_text=l_("Sets the options that you can choose for the rating boxes. You have separate them with a coma and non spaces."))
    timeout = models.IntegerField(help_text=l_("time limit for the participant before the trial automatically advances"), default=-1)
    timeout_message = models.CharField(max_length=128, blank=True, help_text=l_("Any content here will be displayed as a feedback given to the participants when they time out."))
    timeout_message_timing = models.IntegerField(help_text=l_("How long to show the timeout prompt for."), default=1000)


    def toDict(self):
        initial = super(RatingBlock,self).toDict()
        initial['labels'] = self.labels.split(',')
        initial['intervals'] = self.intervals.split(',')
        initial['choices'] = self.choices.split(',')
        initial['prompt'] = self.prompt
        return initial
        
    
class ForcedChoiceBlock(BaseSettingBlock):
    type = 'forcedchoice' 
    
    is_html = models.BooleanField(help_text=l_("True if the stimulus is html instead of being a image url"))
    timing_stim = models.IntegerField(help_text=l_("How long to show the stimuli for in milliseconds."))
    timing_fixation = models.IntegerField(help_text=l_("How long to show the fixation cross for in milliseconds."))  
    prompt = models.CharField(max_length=256, blank=True, help_text=l_("Any content here will be displayed below the stimulus, as a reminder to the participant"))
    keyboard = models.BooleanField(help_text=l_("True if the response is made by pressing keys instead of clicking on the pictures"))
    key_choices = models.CharField(blank=True, max_length = 1024, help_text=l_("Choose the keys (letters) you have to press for each stimulus. You have separate them with a coma. ex: k,l"))
    timeout = models.IntegerField(help_text=l_("time limit for the participant before the trial automatically advances"), default=-1)
    timeout_message = models.CharField(max_length=128, blank=True, help_text=l_("Any content here will be displayed as a feedback given to the participants when they time out."))
    timeout_message_timing = models.IntegerField(help_text=l_("How long to show the timeout prompt for."), default=1000)
    
    def toDict(self):
        initial = super(ForcedChoiceBlock,self).toDict()
        initial['key_choices'] = self.key_choices.split(',')
        initial['prompt'] = self.prompt
        return initial
    
class AudioCatBlock(BaseSettingBlock):
    type = 'audio-categorization'
    choices = models.CharField(blank=True, max_length = 1024, help_text=l_("Choose the keys associated for all categories. You have separate them with a coma and non spaces."))
    timing_response = models.IntegerField(help_text=l_("time limit for the participant before the trial automatically advances"), default=-1)
    prompt = models.CharField(max_length=256, blank=True, help_text=l_("Any content here will be displayed below the stimulus, as a reminder to the participant"))
    timing_feedback = models.IntegerField(help_text=l_("How long to show the feedback message for in milliseconds.")) 
    correct_feedback = models.CharField(max_length=64, blank=True, help_text=l_("Any content here will be displayed as a feedback given to the participants when he hits the correct category"))
    incorrect_feedback = models.CharField(max_length=64, blank=True, help_text=l_("Any content here will be displayed as a feedback given to the participants when he doesn't hit the correct category"))
    timeout_feedback = models.CharField(max_length=64, blank=True, help_text=l_("Any content here will be displayed as a feedback given to the participants when he takes too long to answer the question if there is a timeout"))
    show_icon = models.BooleanField(default = False, help_text=l_('Check this box to have a speaker icon presented in the same time as the sound.'))
    forced_listening = models.BooleanField(default = False, help_text=l_('Check this box if you want to force the subject to listen to the whole sound before answering'))
    
    def toDict(self):
        initial = super(AudioCatBlock,self).toDict()
        initial['choices'] = self.choices.split(',')
        initial['prompt'] = "<p class=\"prompt\"> {} </p>".format(self.prompt)
        initial['correct_feedback'] = self.correct_feedback
        initial['incorrect_feedback'] = self.incorrect_feedback
        initial['timeout_feedback'] = self.timeout_feedback
        return initial
    
class AudioABXBlock(BaseSettingBlock):
    type = 'audio-abx'
    choices = choices = models.CharField(blank=True, max_length = 1024, help_text=l_("Choose the keys associated for all categories. You have separate them with a coma and non spaces."))
    timeout = models.IntegerField(help_text=l_("time limit for the participant before the trial automatically advances"), default=-1)
    timeout_feedback = models.CharField(max_length=64, blank=True, help_text=l_("Any content here will be displayed as a feedback given to the participants when he takes too long to answer the question if there is a timeout"))
    timing_feedback = models.IntegerField(help_text=l_("How long to show the feedback message for in milliseconds."))
    timing_gap = models.IntegerField(help_text=l_("How long to leave blank between the sounds."))
    prompt = models.CharField(max_length=256, blank=True, help_text=l_("Any content here will be displayed below the stimulus, as a reminder to the participant"))
    key_first = models.CharField(max_length=3, blank=True, help_text=l_("The key that the person have to press if the first sound is the same as the last"))
    key_second = models.CharField(max_length=3, blank=True, help_text=l_("The key that the person have to press if it is the second sound that is the same as the last"))
    
    def toDict(self):
        initial = super(AudioABXBlock,self).toDict()
        initial['choices'] = self.choices.split(',')
        initial['prompt'] = "<p class=\"prompt\"> {} </p>".format(self.prompt)
        initial['timeout_feedback'] = self.timeout_feedback
        return initial
    
class ABXBlock(BaseSettingBlock):
    type = 'abx'
    choices = choices = models.CharField(blank=True, max_length = 1024, help_text=l_("Choose the keys associated for all categories. You have separate them with a coma and non spaces."))
    timeout = models.IntegerField(help_text=l_("time limit for the participant before the trial automatically advances"), default=-1)
    timeout_feedback = models.CharField(max_length=64, blank=True, help_text=l_("Any content here will be displayed as a feedback given to the participants when he takes too long to answer the question if there is a timeout"))
    timing_feedback = models.IntegerField(help_text=l_("How long to show the feedback message for in milliseconds."))
    timing_gap = models.IntegerField(help_text=l_("How long to leave blank between the stimuli."))
    timing_stims = models.IntegerField(help_text=l_("How long to show the stimuli for."))
    prompt_position = models.IntegerField(choices= ((1, 'With the first image and until the end of the trial'), (2, 'After the three images and until the end of the trial')),help_text=l_('When do you want the prompt to appear'))
    prompt = models.CharField(max_length=256, blank=True, help_text=l_("Any content here will be displayed below the stimulus, as a reminder to the participant"))
    key_first = models.CharField(max_length=3, blank=True, help_text=l_("The key that the person have to press if the first image is the same as the last"))
    key_second = models.CharField(max_length=3, blank=True, help_text=l_("The key that the person have to press if it is the second image that is the same as the last"))
    
    def toDict(self):
        initial = super(ABXBlock,self).toDict()
        initial['choices'] = self.choices.split(',')
        initial['prompt'] = "<p class=\"prompt\"> {} </p>".format(self.prompt)
        initial['timeout_feedback'] = self.timeout_feedback
        return initial
        
        
    