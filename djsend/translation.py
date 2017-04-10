'''
Created on Feb 24, 2016

@author: Daniel Rivas
'''

from modeltranslation.translator import register, TranslationOptions
from .models import Instruction, CategorizationBlock, GenericSettingBlock, \
                    SimilarityBlock, Question, ForcedChoiceBlock, RatingBlock, SurveyLikertBlock, SurveyMultiChoiceBlock, AudioCatBlock, SurveyTextBlock, AudioSimilarityBlock, \
                    AnimationBlock, ButtonResponseBlock, CategorizeAnimationBlock, FreeSortBlock, MultiStimMultiResponseBlock, ReconstructionBlock, SameDifferentBlock, SingleAudioBlock, \
                    SingleStimBlock, XABBlock, AudioABXBlock, ABXBlock
@register(ABXBlock)
class ABXOptions(TranslationOptions):
    fields=('prompt', 'timeout_feedback')

@register(AnimationBlock)
class AnimationBlockOptions(TranslationOptions):
    fields=('prompt',)
    
@register(AudioABXBlock)
class AudioABXOptions(TranslationOptions):
    fields=('prompt', 'timeout_feedback')

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
    fields=('prompt','timeout_message')
    
@register(FreeSortBlock)
class FreeSortBlockOptions(TranslationOptions):
    fields=('prompt',)
    
@register(GenericSettingBlock)
class GenericSettingblockOptions(TranslationOptions):
    pass

@register(Instruction)
class InstructionTransOptions(TranslationOptions):
    fields = ('text',)
    
@register(MultiStimMultiResponseBlock)
class MultiStimMultiResponseBlockOptions(TranslationOptions):
    fields = ('prompt',)
    
@register(Question)
class QuestionOptions(TranslationOptions):
    fields=('question_label','answer_options')
    
@register(RatingBlock)
class RatingOptions(TranslationOptions):
    fields=('prompt','choices', 'timeout_message')
    
@register(ReconstructionBlock)
class ReconstructionBlockOptions(TranslationOptions):
    pass

@register(SameDifferentBlock)
class SameDifferentBlockOptions(TranslationOptions):
    fields=('prompt',)

@register(SimilarityBlock)
class SimilarityBlockOptions(TranslationOptions):
    fields=('prompt', 'labels', 'timeout_message')
    
@register(SingleAudioBlock)
class SingleAudioBlockOptions(TranslationOptions):
    fields=('prompt',)
    
@register(SingleStimBlock)
class SingleStimBlockOptions(TranslationOptions):
    fields=('prompt',)

@register(SurveyLikertBlock)
class SurveyLikertOptions(TranslationOptions):
    fields=('preamble',)
    pass

@register(SurveyMultiChoiceBlock)
class SurveyMultiChoiceOptions(TranslationOptions):
    fields=('preamble',)
  
@register(SurveyTextBlock)
class SurveyTextOptions(TranslationOptions):
    fields=('preamble',)
    
@register(XABBlock)
class XABBlockOptions(TranslationOptions):
    fields=('prompt',)
    
