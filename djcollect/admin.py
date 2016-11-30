from django.contrib import admin
from .models import Participation, DropOut
# Register your models here.
from django.apps import apps

app = apps.get_app_config('djcollect')

@admin.register(Participation)
class ParticipationAdmin(admin.ModelAdmin):
    
    def experiment(self, obj):
        return obj.experiment.verbose_name
    
    def subject_no(self, obj):
        return obj.subject.id
    
    def paid(self, obj):
        if obj.payment is not None:
            return obj.payment.sent
        else:
            return False
    
    list_display = ('experiment', 'subject_no', 'started', 'complete', 'paid')
    
@admin.register(DropOut)
class DropOutAdmin(admin.ModelAdmin):
    
    def experiment(self, obj):
        return obj.experiment.verbose_name
    
    def subject_no(self, obj):
        return obj.subject.id
    
    list_display = ('experiment', 'subject_no', 'started', 'finished')