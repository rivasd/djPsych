'''
Created on Feb 24, 2016

@author: Daniel Rivas
'''
from .BasicBlock import BaseSettingBlock
from django.utils.translation import ugettext_lazy as l_
from django.db import models
from jsonfield import JSONCharField

class CategorizationBlock(BaseSettingBlock):
    
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
    
    show_response_choices = (
        ('FIRST_STIMULUS', l_('With the first stimulus')),
        ('SECOND_STIMULUS', l_('With the second stimulus')),
        ('POST_STIMULUS', l_('After both stimuli have disappeared')),                 
    )
    
    intervals = models.IntegerField(help_text=l_("How many different choices are available on the slider. For example, 5 will limit the options to 5 different places on the slider"))
    show_ticks = models.BooleanField(help_text=l_("If true, then the slider will have tick marks indicating where the response options lie on the slider."))
    show_response = models.CharField(max_length=16, choices=show_response_choices, help_text=l_("When should the response slider be shown?"))
    timing_first_stim = models.IntegerField(help_text=l_("How long to show the first stimulus for in milliseconds."))
    timing_second_stim = models.IntegerField(help_text=l_("How long to show the second stimulus for in milliseconds. -1 will show the stimulus until a response is made by the subject."))
    timing_image_gap = models.IntegerField(help_text=l_("How long to show a blank screen in between the two stimuli."))
    timing_post_trial = models.IntegerField(help_text=l_("Sets the time, in milliseconds, between the current trial and the next trial."))
    timeout = models.IntegerField(help_text=l_("How long before trial automatically times out"), default=-1)
    timeout_message = models.CharField(max_length=128, null=True, blank=True)
    
    prompt = models.CharField(max_length=32, blank=True, help_text=l_("Any content here will be displayed below the stimulus, as a reminder to the participant"))
    labels = JSONCharField(max_length=64, help_text=l_('An array of tags to label the slider. must be eclosed in square brackets. Each label must be enclosed in double quotation marks. Labels must be separated by a single comma.'))
    
    def toDict(self):
        initial = super(SimilarityBlock, self).toDict()
        initial['prompt'] = "<p class=\"prompt\"> {} </p>".format(self.prompt)
        return initial
    
class HTMLBlock(BaseSettingBlock):
    
    url = models.URLField()
    
    
    
    
    
    