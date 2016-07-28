from django.contrib import admin
from .models import Experiment
from djmanager.utils import get_subclass_ct_pk, get_allowed_exp_for_user
from djsend.models import BaseGlobalSetting, BaseSettingBlock
from django.contrib.contenttypes.models import ContentType
from modeltranslation.admin import TranslationAdmin,\
    TranslationGenericStackedInline, TranslationTabularInline,\
    TranslationStackedInline
from djexperiments.models import Debrief, Lobby
from django_markdown.models import MarkdownField
from django_markdown.widgets import AdminMarkdownWidget

# Register your models here.

class DebriefTabularInline(TranslationStackedInline):
    
    model = Debrief
    fields = ['experiment', 'content']
    
    def get_queryset(self, request):
        qs = super(DebriefTabularInline, self).get_queryset(request)
        exps = get_allowed_exp_for_user(request)
        return qs.filter(experiment__in=exps)
    
    def get_form(self, request, obj=None, **kwargs):
        form = super(DebriefTabularInline, self).get_form(request, obj=obj, **kwargs)
        form.base_fields['experiment'].queryset = get_allowed_exp_for_user(request)


class LobbyTabularInline(TranslationStackedInline):
    model = Lobby
    fields = ['experiment', 'content']
    
    def get_queryset(self, request):
        qs = super(LobbyTabularInline, self).get_queryset(request)
        exps = get_allowed_exp_for_user(request)
        return qs.filter(experiment__in=exps)
    
    def get_form(self, request, obj=None, **kwargs):
        form = super(LobbyTabularInline, self).get_form(request, obj=obj, **kwargs)
        form.base_fields['experiment'].queryset = get_allowed_exp_for_user(request)


@admin.register(Experiment)
class ExperimentAdmin(TranslationAdmin):
    
    def get_queryset(self, request):
        qs = super(ExperimentAdmin, self).get_queryset(request)
        exp_groups = request.user.groups.filter(name__endswith="researchers")
        return qs.filter(research_group__in=exp_groups)
    
    def get_form(self, request, obj=None, **kwargs):
        form = super(ExperimentAdmin, self).get_form(request, obj=obj, **kwargs)
        
        glob_settings_pks = get_subclass_ct_pk(BaseGlobalSetting)
        block_settings_pks = get_subclass_ct_pk(BaseSettingBlock)
                
        form.base_fields['settings_model'].queryset = ContentType.objects.filter(pk__in=glob_settings_pks)
        form.base_fields['block_models'].queryset = ContentType.objects.filter(pk__in=block_settings_pks)
        
        return form
    
    filter_horizontal=['block_models']
    
    list_display = ('__str__', 'count_finished_part', 'is_active', 'compensated', 'amount_spent')
    
    inlines = [DebriefTabularInline, LobbyTabularInline]


@admin.register(Debrief)
class DebriefAdmin(TranslationAdmin):
    
    fields = ['experiment', 'content']
    
    def get_queryset(self, request):
        qs = super(DebriefAdmin, self).get_queryset(request)
        exps = get_allowed_exp_for_user(request)
        return qs.filter(experiment__in=exps)
    
    def get_form(self, request, obj=None, **kwargs):
        form = super(DebriefAdmin, self).get_form(request, obj=obj, **kwargs)
        form.base_fields['experiment'].queryset = get_allowed_exp_for_user(request)
        


    
    