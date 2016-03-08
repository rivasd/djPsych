'''
Created on Mar 3, 2016

@author: Daniel Rivas
'''

from modeltranslation.translator import register, TranslationOptions
from .models import Experiment
from djexperiments.models import Debrief, Lobby

@register(Experiment)
class ExperimentTranslationOptions(TranslationOptions):
    fields = ('verbose_name', 'description')
    
    
@register(Debrief)
class DebriefTranslationOptions(TranslationOptions):
    fields =('content',)
    
@register(Lobby)
class LobbyTranslationOptions(TranslationOptions):
    fields = ('content',)