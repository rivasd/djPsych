'''
Created on Feb 24, 2016

@author: Daniel Rivas
'''

from modeltranslation.translator import register, TranslationOptions
from .models import Instruction, CategorizationBlock, GenericSettingBlock, \
                    SimilarityBlock, Question, ForcedChoiceBlock, RatingBlock, SurveyLikertBlock, SurveyMultiChoiceBlock, AudioCatBlock, SurveyTextBlock, AudioSimilarityBlock, \
                    AnimationBlock, ButtonResponseBlock, CategorizeAnimationBlock, FreeSortBlock

@register(AnimationBlock)
class AnimationBlockOptions(TranslationOptions):
    fields=('prompt',)

@register(AudioCatBlock)
class AudioCatOptions(TranslationOptions):
    fields=('prompt','correct_feedback','incorrect_feedback', 'timeout_feedback')
    
@register(AudioSimilarityBlock)
class AudioSimilarityBlockOptions(TranslationOptions):
    fields=('prompt', 'labels', 'timeout_message')
    
@register(ButtonResponseBlock)
class ButtonResponseBlockOptions(TranslationOptions):
    fields=('prompt',)
    
@register(CategorizeAnimationBlock)
class categorizeAnimationBlockOptions(TranslationOptions):
    fields=('prompt',)
    
@register(CategorizationBlock)
class CategorizationBlockOptions(TranslationOptions):
    fields = ('correct_text', 'incorrect_text', 'prompt', 'timeout_message')
    
@register(ForcedChoiceBlock)
class ForcedChoiceOptions(TranslationOptions):
    fields=('prompt',)
    
@register(FreeSortBlock)
class FreeSortBlockOptions(TranslationOptions):
    fields=('prompt',)
    
@register(GenericSettingBlock)
class GenericSettingblockOptions(TranslationOptions):
    pass

@register(Instruction)
class InstructionTransOptions(TranslationOptions):
    fields = ('text',)
    
@register(Question)
class QuestionOptions(TranslationOptions):
    fields=('question_label','answer_options')
    
@register(RatingBlock)
class RatingOptions(TranslationOptions):
    fields=('prompt','choices')

@register(SimilarityBlock)
class SimilarityBlockOptions(TranslationOptions):
    fields=('prompt', 'labels', 'timeout_message')

@register(SurveyLikertBlock)
class SurveyLikertOptions(TranslationOptions):
    pass

@register(SurveyMultiChoiceBlock)
class SurveyMultiChoiceOptions(TranslationOptions):
    fields=('preamble',)
  
@register(SurveyTextBlock)
class SurveyTextOptions(TranslationOptions):
    fields=('preamble',)
    
