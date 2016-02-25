

from django.db import models
from django.utils.translation import ugettext_lazy as l_
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class Category(models.Model):
    
    class Meta:
        verbose_name_plural = 'Categories'
        
    name = models.CharField(max_length=16)
    keycode = models.IntegerField(help_text=l_("The character keycode representing the correct response for this category. See: http://www.cambiaresearch.com/articles/15/javascript-key-codes"))
    block_type = models.ForeignKey(ContentType)
    block_id = models.PositiveIntegerField(help_text=l_("The block-level setting this category is attached to"))
    block_setting = GenericForeignKey('block_type', 'block_id')
    
    def __str__(self):
        return self.name