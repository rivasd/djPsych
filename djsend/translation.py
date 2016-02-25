'''
Created on Feb 24, 2016

@author: Daniel Rivas
'''

from modeltranslation.translator import register, TranslationOptions
from .models import Instruction

@register(Instruction)
class InstructionTransOptions(TranslationOptions):
    fields = ('text',)
