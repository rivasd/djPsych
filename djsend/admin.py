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
from djreceive.models.BasicTrials import BaseTrial, CategorizationTrial, Rating
from django.contrib.contenttypes.admin import GenericTabularInline,\
    GenericStackedInline
from modeltranslation.admin import TranslationAdmin, TranslationGenericStackedInline
from djstim.models import Category, MicroComponentPair
from djreceive.models.CustomTrials import CogComSimilarityTrial
from djstim.admin import LinkedStimulusInline
from djsend.models.BasicBlock import SurveyMultiChoiceBlock,SurveyLikertBlock, SurveyTextBlock
from djsend.models.CustomBlock import ForcedChoiceBlock, RatingBlock, AudioCatBlock
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
        (l_("Saving & processing options"), {'fields':(('type', 'save_with'),)})
    )
    
    related_lookup_fields = {
        'generic' :[['global_settings_type', 'global_settings_id']]
    }
    
    list_display = ('name', 'get_parent_name', 'position_in_timeline', 'type', 'has_practice')
    
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
        allowed_ids = [block.pk for block in qs if block.part_of.experiment.pk in exps_ids]
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
    
    def get_form(self, request, obj=None, **kwargs):
        form = super(CategorizationBlockAdmin, self).get_form(request, obj=obj, **kwargs)
        form.base_fields['type'].initial = 'categorize'
        form.base_fields['save_with'].initial = ContentType.objects.get_for_model(CategorizationTrial)
        return form
        
        
@admin.register(SimilarityBlock)
class SimilarityBlockAdmin(GenericBlockAdmin):
    
    fieldsets = GenericBlockAdmin.fieldsets + (
        (l_("Similarity task parameters"), {'fields':(
            'intervals',
            'show_ticks',
            'show_response',
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
    
    def get_form(self, request, obj=None, **kwargs):
        form = super(SimilarityBlockAdmin, self).get_form(request, obj=obj, **kwargs)
        form.base_fields['type'].initial = 'similarity'
        form.base_fields['save_with'].initial = ContentType.objects.get_for_model(CogComSimilarityTrial)
        return form
    
    
class CategoryInline(admin.StackedInline):
    model = Category
    extra=1
    
class MCPairInline(admin.StackedInline):
    model=MicroComponentPair
    extra=1

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
        )}),
    )
    
    filter_horizontal = ['microcomponent_pairs', 'practice_pairs']
    
    inlines = [CategoryInline]
    
class QuestionAdminInline(TranslationGenericStackedInline):
    model = Question
    
@admin.register(SurveyMultiChoiceBlock)    
class SurveyMultiChoiceAdmin(GenericBlockAdmin):
    inlines = [QuestionAdminInline]
    fieldsets = GenericBlockAdmin.fieldsets + (
        (l_("Survey Multi Choice task parameters"), {'fields':(
            'preamble',
            'horizontal'
        )}),                               
    )
    
   

@admin.register(SurveyLikertBlock)    
class SurveyLikertAdmin(GenericBlockAdmin):
    inlines = [QuestionAdminInline]

@admin.register(ForcedChoiceBlock)    
class ForcedChoiceAdmin(GenericBlockAdmin):
    fieldsets = GenericBlockAdmin.fieldsets + (
        (l_("Forced Choice task parameters"), {'fields':(
            'is_html',
            'timing_stim',
            'timing_fixation',  
            'prompt', 
            'keyboard',
            'key_choices'
        )}),                               
    )

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
    )}),                               
    )
    
    def get_form(self, request, obj=None, **kwargs):
        form = super(RatingAdmin, self).get_form(request, obj=obj, **kwargs)
        form.base_fields['type'].initial = 'rating'
        form.base_fields['save_with'].initial = ContentType.objects.get_for_model(Rating)
        return form

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
        'timeout_feedback'
        
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
    
    