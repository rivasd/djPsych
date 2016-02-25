'''
Created on Feb 24, 2016

@author: Daniel Rivas
'''
from .BasicBlock import BaseSettingBlock
from django.utils.translation import ugettext_lazy as l_
from django.db import models

class CategorizationBlock(BaseSettingBlock):
    
    show_stim_with_feedback = models.BooleanField(default=False, help_text= l_("Should the stimulus be shown together with the feedback text?"))
    show_feedback_on_timeout = models.BooleanField(default=False, help_text=l_("Should we show the feedback even when the trial times out?"))
    timing_stim = models.IntegerField(help_text=l_("How long to show the stimulus for (milliseconds). If -1, then the stimulus is shown until a response is given."))
    timing_feedback_duration = models.IntegerField(help_text=l_("How long to show the feedback for "))
    timing_response = models.IntegerField(help_text=l_("The maximum time allowed for a response. If -1, then the experiment will wait indefinitely for a response."))
    timing_post_trial = models.IntegerField(help_text=l_("Sets the time, in milliseconds, between the current trial and the next trial."))
    
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
    prompt = models.CharField(max_length=32, blank=True, help_text=l_("Any content here will be displayed below the stimulus, as a reminder to the participant"))
    