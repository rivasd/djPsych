'''
Created on Feb 24, 2016

@author: Daniel Rivas
'''

from modeltranslation.translator import register, TranslationOptions
from .models import Instruction, CategorizationBlock, GenericSettingBlock, \
                    SimilarityBlock

@register(Instruction)
class InstructionTransOptions(TranslationOptions):
    fields = ('text',)

@register(CategorizationBlock)
class CategorizationBlockOptions(TranslationOptions):
    fields = ('correct_text', 'incorrect_text', 'prompt', 'timeout_message')
    
@register(GenericSettingBlock)
class GenericSettingblockOptions(TranslationOptions):
    pass

@register(SimilarityBlock)
class SimilarityBlockOptions(TranslationOptions):
    fields=('prompt', 'labels')