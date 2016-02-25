'''
Created on Feb 23, 2016

@author: User
'''
from django.db import models
from django.utils.translation import ugettext_lazy as l_
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from jsonfield import JSONField


class BaseSettingBlock(models.Model):
    
    class Meta:
        abstract = True
    
    global_settings_type = models.ForeignKey(ContentType)
    global_settings_id = models.PositiveIntegerField(help_text=l_("Which global settings configuration is this block-level configuration part of?"))
    part_of = GenericForeignKey('global_settings_type', 'global_settings_id')
    
    length= models.PositiveIntegerField(null=True, blank=True, help_text=l_("How many individual trials of this type should there be. You can leave blank if you don't need it"))
    for_type = models.CharField(max_length=26)
    is_practice = models.BooleanField()
    # magic field for dynamically added settings
    extra_params = JSONField()
    
class GenericSettingBlock(BaseSettingBlock):
    pass

