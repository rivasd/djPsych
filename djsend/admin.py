from django.contrib import admin
from django.utils.translation import ugettext_lazy as l_
# Register your models here.
from django_markdown.admin  import MarkdownModelAdmin
from django_markdown.models import MarkdownField
from django_markdown.widgets import AdminMarkdownWidget
from django.apps import apps
from .models import *
from .adminForms import GenericSettingBlockForm
from django.contrib.contenttypes.models import ContentType
import inspect
app = apps.get_app_config('djsend')

@admin.register(GenericSettingBlock)
class GenericBlockAdmin(admin.ModelAdmin):
    
    form= GenericSettingBlockForm
    
    formfield_overrides = {MarkdownField: {'widget': AdminMarkdownWidget}}
    fieldsets=(
        (l_("Experimental structure options"), {'fields': (('global_settings_type', 'global_settings_id'), 'position_in_timeline', 'reprise')}),
        (l_("General parameters"), {'fields':('length', 'is_practice', 'extra_params')}),
        (l_("Saving & processing options"), {'fields':(('type', 'save_with'),)})
    )
    
    def get_form(self, request, obj=None, **kwargs):
        normal_form=  super(GenericBlockAdmin, self).get_form(request, obj=obj, **kwargs)
        global_cts=[]
        for ct in ContentType.objects.all():
            if inspect.isclass(ct.model_class()) and issubclass(ct.model_class(), BaseGlobalSetting):
                global_cts.append(ct.pk)
        
        normal_form.base_fields['global_settings_type'].queryset = ContentType.objects.filter(pk__in=global_cts)
        return normal_form


class GenericGlobalSettingAdmin(admin.ModelAdmin):
    
    
    
    
    fieldsets=(
        (l_("Identification settings"), {'fields':(('name', 'experiment'),)}),
        (l_("Basic parameters"), {'fields': ('max_consecutive_timeouts', 'max_total_timeouts', 'fixation_cross')}),
        (l_("Additional parameters"), {'fields':("extra_parameters",)})
    )
    
