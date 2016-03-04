'''
Created on Mar 2, 2016

@author: Daniel Rivas
'''
from django import forms

from .models import *
from djmanager.utils import content_type_is_subclass_of
import gfklookupwidget

class GenericSettingBlockForm(forms.ModelForm):
    
    
    class Meta:
        # looks like the admin overrides things here so whatever
        model = GenericSettingBlock
        fields= []

