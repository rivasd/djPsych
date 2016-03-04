'''
Created on Mar 3, 2016

@author: Daniel Rivas
'''

from modeltranslation.translator import register, TranslationOptions
from .models import Experiment

@register(Experiment)
class ExperimentTranslationOptions(TranslationOptions):
    fields = ('verbose_name', 'description')