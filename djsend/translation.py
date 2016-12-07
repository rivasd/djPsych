'''
Created on Feb 24, 2016

@author: Daniel Rivas
'''

from modeltranslation.translator import register, TranslationOptions
from .models import Instruction, CategorizationBlock, GenericSettingBlock, \
                    SimilarityBlock, Question, ForcedChoiceBlock, RatingBlock, SurveyLikertBlock, SurveyMultiChoiceBlock, AudioCatBlock

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
    fields=('prompt', 'labels', 'timeout_message')
    
@register(Question)
class QuestionOptions(TranslationOptions):
    fields=('question_label','answer_options')
    
@register(RatingBlock)
class RatingOptions(TranslationOptions):
    fields=('prompt','choices')

@register(ForcedChoiceBlock)
class ForcedChoiceOptions(TranslationOptions):
    fields=('prompt',)

@register(SurveyLikertBlock)
class SurveyLikertOptions(TranslationOptions):
    pass

@register(SurveyMultiChoiceBlock)
class SurveyMultiChoiceOptions(TranslationOptions):
    fields=('preamble',)

@register(AudioCatBlock)
class AudioCatOptions(TranslationOptions):
    fields=('prompt','correct_feedback','incorrect_feedback', 'timeout_feedback')
    
