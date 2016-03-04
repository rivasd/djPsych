'''
Created on Mar 3, 2016

@author: User
'''
from modeltranslation.translator import register, TranslationOptions
from .models import TextTrial

@register(TextTrial)
class HtmlStimTransOptions(TranslationOptions):
    fields = ('text',)