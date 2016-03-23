from django.contrib import admin
from django.contrib.contenttypes.admin import GenericStackedInline
from django.contrib.contenttypes.models import ContentType
from .models import *
from gfklookupwidget.widgets import GfkLookupWidget
from djmanager.utils import get_subclass_ct_pk, get_allowed_exp_for_user
# Register your models here.
# TODO: create the admin interface for the stimuli objects
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass

@admin.register(LinkedStimulus)
class LinkedStimulusAdmin(admin.ModelAdmin):
    
    def get_queryset(self, request):
        qs = super(LinkedStimulusAdmin, self).get_queryset(request)
        candidates =[link.pk for link in qs if link.get_experiment() in get_allowed_exp_for_user(request)]
        return qs.filter(pk__in=candidates)


@admin.register(MicroComponentPair)
class MCPairAdmin(admin.ModelAdmin):
    pass

class LinkedStimulusInline(GenericStackedInline):
    
    #TODO: permissions and such for the stimuli objects
    model = LinkedStimulus
    ct_field = 'setting_type'
    ct_fk_field = 'setting_id'
    extra = 1
    
    related_lookup_fields = {
        'generic' :[['stim_type', 'stim_id']]
    }
    
    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        
        if db_field.name == 'stim_type':
            
            possibilities = get_subclass_ct_pk(BaseStimuli)
            # use self.parent_model to add options to the queryset depending on the global setting model that this inline is attached to
            # it's a bit of hardcoding but at least it's all at the same place...
            if self.parent_model == SimCatGlobalSetting:
                pair_ct = ContentType.objects.get_for_model(MicroComponentPair)
                possibilities = [pair_ct.pk]
                kwargs['initial'] = pair_ct
            
            kwargs['queryset'] = ContentType.objects.filter(pk__in=possibilities)
        
        return GenericStackedInline.formfield_for_foreignkey(self, db_field, request=request, **kwargs)
    
    