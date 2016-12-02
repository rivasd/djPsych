from django.contrib import admin
from django.contrib.auth.models import Group, Permission
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
import os
from django.conf import settings

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
    
    def save_model(self, request, obj, form, change):
        if obj.pk is None:
            new_group = Group(name=obj.label+"_researchers")
            new_group.save()
            obj.research_group = new_group
            
            exp_content_type = ContentType.objects.get_for_model(Experiment)
            exp_perm = Permission.objects.get(content_type=exp_content_type, codename="change_experiment")
            new_group.permissions.add(exp_perm)
            
            #add the creator of the experiment in the experiment group
            request.user.groups.add(new_group)
            
            #create a new folder for this experiment
            dir_path = os.path.join(settings.MEDIA_ROOT, obj.label)
            
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
            
            template_path = os.path.join(settings.BASE_DIR, '..', 'djexperiments','static','djexperiments','template_experiment.js')
            
            with open(template_path, 'r') as content_file:
                content = content_file.read()
            
                with open(os.path.join(dir_path + os.path.sep, 'exp.js'), 'w') as temp_file:
                    temp_file.write(content)
           
        obj.save()
    
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
        


    
    