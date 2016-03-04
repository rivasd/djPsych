from django.contrib import admin
from .models import Experiment
from djmanager.utils import get_subclass_ct_pk
from djsend.models import BaseGlobalSetting, BaseSettingBlock
from django.contrib.contenttypes.models import ContentType
from modeltranslation.admin import TranslationAdmin

# Register your models here.

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
    
    list_display = ('__str__', 'count_finished_part', 'is_active', 'compensated')
    
    
    