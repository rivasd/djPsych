

from django.db import models
from django.utils.translation import ugettext_lazy as l_
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from .CustomGeneral import SimCatGlobalSetting

class Category(models.Model):
    
    class Meta:
        verbose_name_plural = 'Categories'
        
    name = models.CharField(max_length=16)
    keycode = models.IntegerField(help_text=l_("The character keycode representing the correct response for this category. See: http://www.cambiaresearch.com/articles/15/javascript-key-codes"))
    setting = models.ForeignKey(SimCatGlobalSetting)
    
    def __str__(self):
        return self.name
    
class MicroComponentPair(models.Model):
    index = models.PositiveIntegerField()
    setting = models.ForeignKey(SimCatGlobalSetting)
    first = models.CharField(max_length=16)
    second = models.CharField(max_length=16)
    
    def __str__(self):
        return self.setting.name + "-" + str(self.index)