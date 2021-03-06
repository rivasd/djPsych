from django.contrib import admin
from django.utils.translation import ugettext_lazy as l_
# Register your models here.
from django_markdown.models import MarkdownField
from django_markdown.widgets import AdminMarkdownWidget
from django.apps import apps
from .models import *
from .adminForms import GenericSettingBlockForm
from django.contrib.contenttypes.models import ContentType
import inspect
from djmanager.utils import get_allowed_exp_for_user, get_subclass_ct_pk
from djreceive.models.BasicTrials import BaseTrial, CategorizationTrial, Rating, AudioSimilarityTrial
from django.contrib.contenttypes.admin import GenericTabularInline,\
    GenericStackedInline
from modeltranslation.admin import TranslationAdmin, TranslationGenericStackedInline
from djstim.models import Category, MicroComponentPair
from djreceive.models.CustomTrials import CogComSimilarityTrial
from djstim.admin import LinkedStimulusInline
from djsend.models.BasicBlock import SurveyMultiChoiceBlock,SurveyLikertBlock, SurveyTextBlock, AnimationBlock, ButtonResponseBlock, CategorizeAnimationBlock, \
    FreeSortBlock, MultiStimMultiResponseBlock, ReconstructionBlock, SameDifferentBlock, SingleAudioBlock, SingleStimBlock, XABBlock
from djsend.models.CustomBlock import ForcedChoiceBlock, RatingBlock, AudioCatBlock, AudioSimilarityBlock, AudioABXBlock, ABXBlock, RelationCategorizationBlock
from djsend.models.BaseStimuli import Question


class InstructionInline(TranslationGenericStackedInline):
    model = Instruction
    extra = 1
    classes = ('grp-collapse grp-open',)


@admin.register(GenericSettingBlock)
class GenericBlockAdmin(TranslationAdmin):
    
    class Media:
        js = (
            'modeltranslation/js/force_jquery.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.24/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }
    
    
    formfield_overrides = {MarkdownField: {'widget': AdminMarkdownWidget}}
    fieldsets=(
        (l_("Experimental structure options"), {'fields': (('global_settings_type', 'global_settings_id'), 'position_in_timeline', 'reprise')}),
        (l_("General parameters"), {'fields':('name', 'length', 'has_practice', 'extra_params')}),
        (l_("Saving & processing options"), {'fields':(('save_with',),)})
    )
    
    related_lookup_fields = {
        'generic' :[['global_settings_type', 'global_settings_id']]
    }
    
    def get_exp(self, obj):
        return obj.part_of.experiment.verbose_name
    
    
    list_display = ('name', 'get_parent_name', 'get_exp','position_in_timeline', 'has_practice')
    
    inlines = [ InstructionInline,]
    
    def get_form(self, request, obj=None, **kwargs):
        normal_form=  super(GenericBlockAdmin, self).get_form(request, obj=obj, **kwargs)
        normal_form.base_fields['global_settings_type'].queryset = ContentType.objects.filter(pk__in=get_subclass_ct_pk(BaseGlobalSetting))
        normal_form.base_fields['save_with'].queryset = ContentType.objects.filter(pk__in=get_subclass_ct_pk(BaseTrial))
        return normal_form

    def get_queryset(self, request):
        qs = super(GenericBlockAdmin, self).get_queryset(request)
        exps = get_allowed_exp_for_user(request)
        exps_ids = [exp.pk for exp in exps]
        allowed_ids = []
        # we need to deal with potentially invalid part_of generic relations, since they are not updated on related object deletion
        for block in qs:
            if block.part_of and block.part_of.experiment.pk in exps_ids:
                allowed_ids.append(block.pk)
        
        return qs.filter(pk__in=allowed_ids)


@admin.register(GenericGlobalSetting)
class GenericGlobalSettingAdmin(admin.ModelAdmin):
    
    fieldsets=(
        (l_("Identification settings"), {'fields':(('name', 'experiment'))}),
        (l_("Basic parameters"), {'fields': ('max_consecutive_timeouts', 'max_total_timeouts', 'fixation_cross')}),
        (l_("Additional parameters"), {'fields':("extra_parameters",)})
    )
    
    list_display = ('name', 'experiment')
    
    def get_queryset(self, request):
        qs = super(GenericGlobalSettingAdmin, self).get_queryset(request)
        return qs.filter(experiment__in=get_allowed_exp_for_user(request))
    
    inlines = [ LinkedStimulusInline, ]
    
    
# ModelAdmins for the more targeted config models

@admin.register(ABXBlock)    
class ABXBlock(GenericBlockAdmin):
    fieldsets = GenericBlockAdmin.fieldsets + (
        (l_("ABX task parameters"), {'fields':(
            'choices',
            'prompt',
            'prompt_position',
            'timeout',
            'timing_stims',
            'timing_feedback',
            'timeout_feedback',
            'timing_fixation_cross',
            'timing_gap',
            'key_first',
            'key_second'       
        )}),                               
    )  

@admin.register(AnimationBlock)    
class AnimationBlockAdmin(GenericBlockAdmin):
    fieldsets = GenericBlockAdmin.fieldsets + (
        (l_("Animation task parameters"), {'fields':(
            'choices',
            'prompt',
            'frame_time',
            'frame_isi',
            'sequence_reps'
            
        )}),                               
    )

@admin.register(AudioABXBlock)    
class AudioABXBlock(GenericBlockAdmin):
    fieldsets = GenericBlockAdmin.fieldsets + (
        (l_("Audio ABX task parameters"), {'fields':(
            'choices',
            'prompt',
            'timeout',
            'timeout_feedback',
            'timing_gap',
            'key_first',
            'key_second'       
        )}),                               
    )     

@admin.register(AudioCatBlock)    
class AudioCatAdmin(GenericBlockAdmin):
    fieldsets = GenericBlockAdmin.fieldsets + (
        (l_("Audio Categorization task parameters"), {'fields':(
            'choices',
            'prompt',
            'correct_feedback',
            'incorrect_feedback',
            'timing_feedback',
            'timing_response',
            'timeout_feedback',
            'show_icon',
            'forced_listening'
            
        )}),                               
    )

    
@admin.register(AudioSimilarityBlock)
class AudioSimilarityBlockAdmin(GenericBlockAdmin):
    
    fieldsets = GenericBlockAdmin.fieldsets + (
        (l_("Audio Similarity task parameters"), {'fields':(
            'intervals',
            'show_ticks',
            'timing_first_stim',
            'timing_second_stim',
            'timeout',
            'timeout_message',
            'prompt',
            'timing_gap'
        )}),                               
    )
    

    
@admin.register(ButtonResponseBlock)
class ButtonResponseBlockAdmin(GenericBlockAdmin):
    
    fieldsets = GenericBlockAdmin.fieldsets + (
        (l_("Button Reponse task parameters"), {'fields':(
            'is_html',
            'choices',
            'timing_stim',
            'timing_response',
            'response_ends_trial',
            'prompt'
        )}),                               
    )

@admin.register(CategorizationBlock)
class CategorizationBlockAdmin(GenericBlockAdmin):
    
    fieldsets = GenericBlockAdmin.fieldsets + (
        (l_("Categorization task parameters"), {'fields': (
            'correct_text',
            'incorrect_text',
            'prompt',
            'timeout_message',
            'show_stim_with_feedback',
            'show_feedback_on_timeout',
            'timing_stim',
            'timing_feedback_duration',
            'timing_response',
            'timing_post_trial'
        )}),
    )
    
    related_lookup_fields = {
        'generic' :[['global_settings_type', 'global_settings_id']]
    }
    

    
@admin.register(CategorizeAnimationBlock)  
class CategorizeAnimationBlockAdmin(GenericBlockAdmin):
    fieldsets = GenericBlockAdmin.fieldsets + (
        (l_("Categorize animation task parameters"), {'fields':(
            'choices',
            'correct_text',
            'incorrect_text',
            'frame_time',
            'sequence_reps',
            'allow_response_before_complete',
            'prompt',
            'timing_feedback_duration'
        )}),                               
    )
      
class CategoryInline(admin.StackedInline):
    model = Category
    extra=1

@admin.register(ForcedChoiceBlock)    
class ForcedChoiceAdmin(GenericBlockAdmin):
    fieldsets = GenericBlockAdmin.fieldsets + (
        (l_("Forced Choice task parameters"), {'fields':(
            'is_html',
            'timing_stim',
            'timing_fixation',  
            'prompt', 
            'keyboard',
            'key_choices',
            'timeout',
            'timeout_message',
            'timeout_message_timing'
        )}),                               
    )
    
@admin.register(FreeSortBlock)    
class FreeSortBlockAdmin(GenericBlockAdmin):
    fieldsets = GenericBlockAdmin.fieldsets + (
        (l_("Free Sort task parameters"), {'fields':(
            'stim_height',
            'stim_width',
            'sort_area_height',
            'sort_area_width',
            'prompt',
            'prompt_location'
        )}),                               
    )
    
class MCPairInline(admin.StackedInline):
    model=MicroComponentPair
    extra=1
    
@admin.register(MultiStimMultiResponseBlock)    
class MultiStimMultiResponseBlockAdmin(GenericBlockAdmin):
    fieldsets = GenericBlockAdmin.fieldsets + (
        (l_("Multi Stim Multi Response task parameters"), {'fields':(
            'is_html',
            'prompt',
            'choices',
            'timing_stim',
            'timing_response',
            'response_ends_trial'           
        )}),                               
    )
    
class QuestionAdminInline(TranslationGenericStackedInline):
    model = Question

@admin.register(RatingBlock)    
class RatingAdmin(GenericBlockAdmin):
    fieldsets = GenericBlockAdmin.fieldsets + (
        (l_("Rating task parameters"), {'fields':(
            'is_html',
            'prompt',
            'response',
            'labels',
            'intervals',
            'show_ticks',
            'choices',
            'timeout',
            'timeout_message',
            'timeout_message_timing'
        )}),                            
    )
    

    
@admin.register(ReconstructionBlock)
class ReconstructionBlockAdmin(GenericBlockAdmin):
    fieldsets = GenericBlockAdmin.fieldsets + (
        (l_("Reconstruction task parameters"), {'fields':(
            'starting_value',
            'step_size',
            'key_increase',
            'key_decrease'
        )}),                            
    )
    
@admin.register(RelationCategorizationBlock)    
class RelationCategorizationBlockAdmin(GenericBlockAdmin):
    fieldsets = GenericBlockAdmin.fieldsets + (
        (l_("Relation Categorization task parameters"), {'fields':(
            'prompt',
            'timeout',
            'timing_stims',
            'timing_feedback',
            'timeout_feedback',
            'timing_fixation_cross',
            'timing_after',
            'same_key',
            'different_key',
            'correct',
            'incorrect',
            'is_there_feedback',
            'response_wait'       
        )}),                               
    ) 
    
@admin.register(SameDifferentBlock)
class SameDifferentBlockAdmin(GenericBlockAdmin):
    fieldsets = GenericBlockAdmin.fieldsets + (
        (l_("Same Different task parameters"), {'fields':(
            'is_html',
            'same_key',
            'different_key',
            'timing_first_stim',
            'timing_gap',
            'timing_second_stim',
            'prompt'
        )}),                            
    )


@admin.register(SimCatGlobalSetting)
class SimCatSettingAdmin(GenericGlobalSettingAdmin):
    
    fieldsets = GenericGlobalSettingAdmin.fieldsets + (
        (l_("Categorical Perception Exp Settings"), {'fields':(
            'sample_table_height',
            'sample_table_width',
            'levels',
            'density',
            'size',
            'number_of_pauses',
            'length',
            'practices',
            'microcomponent_pairs',
            'practice_pairs',
            'difficulty'
        )}),
    )
    
    filter_horizontal = ['microcomponent_pairs', 'practice_pairs']
    
    inlines = [CategoryInline]

@admin.register(SimilarityBlock)
class SimilarityBlockAdmin(GenericBlockAdmin):
    
    fieldsets = GenericBlockAdmin.fieldsets + (
        (l_("Similarity task parameters"), {'fields':(
            'intervals',
            'show_ticks',
            'show_response',
            'timing_fixation_cross',
            'timing_first_stim',
            'timing_second_stim',
            'timing_image_gap',
            'timing_post_trial',
            'timeout',
            'timeout_message',
            'prompt',
            'is_audio'
        )}),                               
    )
    

    
@admin.register(SingleAudioBlock)
class SingleAudioBlockAdmin(GenericBlockAdmin):
    
    fieldsets = GenericBlockAdmin.fieldsets + (
        (l_("Single Audio task parameters"), {'fields':(
            'prompt',
            'choices',
            'timing_response',
            'response_ends_trial'
        )}),                               
    )
    
@admin.register(SingleStimBlock)
class SingleStimBlockAdmin(GenericBlockAdmin):
    
    fieldsets = GenericBlockAdmin.fieldsets + (
        (l_("Single Stim task parameters"), {'fields':(
            'is_html',
            'prompt',
            'choices',
            'timing_stim',
            'timing_response',
            'response_ends_trial'
        )}),                               
    )
    
@admin.register(SurveyLikertBlock)    
class SurveyLikertAdmin(GenericBlockAdmin):
    fieldsets = GenericBlockAdmin.fieldsets + (
        (l_("Survey Likert parameters"), {'fields':(
            'preamble',
        )}),                               
    )
    inlines = [QuestionAdminInline]
    
@admin.register(SurveyMultiChoiceBlock)    
class SurveyMultiChoiceAdmin(GenericBlockAdmin):
    inlines = [QuestionAdminInline]
    fieldsets = GenericBlockAdmin.fieldsets + (
        (l_("Survey Multi Choice task parameters"), {'fields':(
            'preamble',
            'horizontal'
        )}),                               
    )


@admin.register(SurveyTextBlock)    
class SurveyTextAdmin(GenericBlockAdmin):
    inlines = [QuestionAdminInline]
    fieldsets = GenericBlockAdmin.fieldsets + (
        (l_("Survey Text task parameters"), {'fields':(
            'preamble',
        )}),                               
    )
    
@admin.register(XABBlock)
class XABBlockAdmin(GenericBlockAdmin):
    fieldsets = GenericBlockAdmin.fieldsets + (
        (l_("XAB task parameters"), {'fields':(
            'is_html',
            'left_key',
            'right_key',
            'timing_x',
            'timing_xab_gap',
            'timing_ab',
            'timing_response',
            'prompt'
        )}),                            
    )

    
    