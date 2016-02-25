'''
Created on Feb 24, 2016

@author: Daniel Rivas
'''

from django.db import models
from django.utils.translation import ugettext_lazy as l_
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class Instruction(models.Model):
    
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    task = GenericForeignKey('content_type', 'object_id') # See: https://docs.djangoproject.com/en/1.9/ref/contrib/contenttypes/#generic-relations
    is_html = models.BooleanField(help_text=l_("check this if the content of the instruction text is valid html and wish to have it rendered as such. "))
    text = models.TextField(help_text=l_('Write your instruction page here! it can even be valid html!'))
    order = models.PositiveIntegerField(help_text=l_("if a setting has multiple instruction pages, we use this number to sort the order in which you want them presented."))
    after = models.BooleanField(help_text=l_("check if this instruction page is meant to be shown AFTER the task it is attached to."))